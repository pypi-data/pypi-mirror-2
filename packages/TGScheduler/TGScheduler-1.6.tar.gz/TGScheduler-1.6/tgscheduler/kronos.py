"""Module that provides a cron-like task scheduler.

This task scheduler is designed to be used from inside your own program.
You can schedule Python functions to be called at specific intervals or
days. It uses the standard 'sched' module for the actual task scheduling,
but provides much more:

* repeated tasks (at intervals, or on specific days)
* error handling (exceptions in tasks don't kill the scheduler)
* optional to run scheduler in its own thread or separate process
* optional to run a task in its own thread or separate process

If the threading module is available, you can use the various Threaded
variants of the scheduler and associated tasks. If threading is not
available, you could still use the forked variants. If fork is also
not available, all processing is done in a single process, sequentially.

There are three Scheduler classes:

    Scheduler    ThreadedScheduler    ForkedScheduler

You usually add new tasks to a scheduler using the add_interval_task or
add_daytime_task methods, with the appropriate processmethod argument
to select sequential, threaded or forked processing. NOTE: it is impossible
to add new tasks to a ForkedScheduler, after the scheduler has been started!
For more control you can use one of the following Task classes
and use schedule_task or schedule_task_abs:

    IntervalTask    ThreadedIntervalTask    ForkedIntervalTask
    SingleTask      ThreadedSingleTask      ForkedSingleTask 
    WeekdayTask     ThreadedWeekdayTask     ForkedWeekdayTask
    MonthdayTask    ThreadedMonthdayTask    ForkedMonthdayTask

Kronos is the Greek God of Time.

Kronos scheduler (c) Irmen de Jong.
This version has been extracted from the Turbogears source repository
and slightly changed to be completely stand-alone again. Also some fixes
have been made to make it work on Python 2.6 (sched module changes).
The version in Turbogears is based on the original stand-alone Kronos.
This is open-source software, released under the MIT Software License:
http://www.opensource.org/licenses/mit-license.php

"""

__version__ = "2.0"

__all__ = [
    "DayTaskRescheduler",
    "ForkedIntervalTask",
    "ForkedMonthdayTask",
    "ForkedScheduler",
    "ForkedSingleTask",
    "ForkedTaskMixin",
    "ForkedWeekdayTask",
    "ForkedCronLikeTask",
    "IntervalTask",
    "MonthdayTask",
    "CronLikeTask",
    "Scheduler",
    "SingleTask",
    "Task",
    "ThreadedIntervalTask",
    "ThreadedMonthdayTask",
    "ThreadedScheduler",
    "ThreadedSingleTask",
    "ThreadedTaskMixin",
    "ThreadedWeekdayTask",
    "ThreadedCronLikeTask",
    "WeekdayTask",
    "add_interval_task",
    "add_monthday_task",
    "add_single_task",
    "add_weekday_task",
    "add_cron_like_task",
    "cancel",
    "method",
]

import os
import sys
import sched
import time
import traceback
import weakref

import logging
log = logging.getLogger(__name__)

import datetime
from dateutil.rrule import rrule, SECONDLY

# bounds for each field of the cron-like syntax
MINUTE_BOUNDS = (0, 59)
HOUR_BOUNDS = (0, 23)
DOM_BOUNDS = (1, 31)
MONTH_BOUNDS = (1, 12)
DOW_BOUNDS = (0, 7)

# some fields of the cron-like syntax can be specified as names
MONTH_MAPPING = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}
DOW_MAPPING = {'sun': 0, 'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5,
        'sat': 6}


class method:
    sequential = "sequential"
    forked = "forked"
    threaded = "threaded"

class Scheduler:
    """The Scheduler itself."""

    def __init__(self):
        self.running = True
        self.sched = sched.scheduler(time.time, self.__delayfunc)
        self.tasks = dict()

    def __delayfunc(self, delay):
        """ 
        This delay function is basically a time.sleep() that is
        divided up, so that we can check the self.running flag while delaying.
        there is an additional check in here to ensure that the top item of
        the queue hasn't changed 
        """
        if delay < 10:
            time.sleep(delay)
        else:
            toptime = self._getqueuetoptime()
            endtime = time.time() + delay
            period = 5
            stoptime = endtime - period
            while self.running and stoptime > time.time():
                self._acquire_lock()
                try:
                    if not self._getqueuetoptime() == toptime:
                        break
                finally:
                    self._release_lock()

                time.sleep(period)
            if not self.running or self._getqueuetoptime() != toptime:
                return
            now = time.time()
            if endtime > now:
                time.sleep(endtime - now)

    def _acquire_lock(self):
        pass

    def _release_lock(self):
        pass

    def add_interval_task(self, action, taskname, initialdelay, interval,
            processmethod, args, kw):
        """Add a new Interval Task to the schedule.
        
        A very short initialdelay or one of zero cannot be honored, you will 
        see a slight delay before the task is first executed. This is because
        the scheduler needs to pick it up in its loop.

        """
        if initialdelay < 0 or interval < 1:
            raise ValueError("Delay or interval must be >0")
        # Select the correct IntervalTask class. Not all types may be available!
        if processmethod == method.sequential:
            TaskClass = IntervalTask
        elif processmethod == method.threaded:
            TaskClass = ThreadedIntervalTask
        elif processmethod == method.forked:
            TaskClass = ForkedIntervalTask
        else:
            raise ValueError("Invalid processmethod")
        if not args:
            args = []
        if not kw:
            kw = {}
        if self.running:
            self._acquire_lock()
            try:
                if self.tasks.has_key(taskname):
                    raise ValueError("A task with the name %s already exists" % taskname)
            finally:
                self._release_lock()
        else:
            if self.tasks.has_key(taskname):
                raise ValueError("A task with the name %s already exists" % taskname)
        task = TaskClass(taskname, interval, action, args, kw)
        self.schedule_task(task, initialdelay)
        return task

    def add_single_task(self, action, taskname, initialdelay, processmethod,
            args, kw):
        """ Add a new task to the scheduler that will only be executed once. """
        if initialdelay < 0:
            raise ValueError("Delay must be >0")
        # Select the correct SingleTask class. Not all types may be available!
        if processmethod == method.sequential:
            TaskClass = SingleTask
        elif processmethod == method.threaded:
            TaskClass = ThreadedSingleTask
        elif processmethod == method.forked:
            TaskClass = ForkedSingleTask
        else:
            raise ValueError("Invalid processmethod")
        if not args:
            args = []
        if not kw:
            kw = {}
        if self.running:
            self._acquire_lock()
            try:
                if self.tasks.has_key(taskname):
                    raise ValueError("A task with the name %s already exists" % taskname)
            finally:
                self._release_lock()
        else:
            if self.tasks.has_key(taskname):
                raise ValueError("A task with the name %s already exists" % taskname)
        task = TaskClass(taskname, action, args, kw)
        self.schedule_task(task, initialdelay)
        return task

    def add_daytime_task(self, action, taskname, weekdays, monthdays, timeonday,
            processmethod, args, kw):
        """ Add a new Day Task (Weekday or Monthday) to the schedule. """
        if weekdays and monthdays:
            raise ValueError("You can only specify weekdays or monthdays, "
                "not both")
        if not args:
            args = []
        if not kw:
            kw = {}
        if weekdays:
            # Select the correct WeekdayTask class.
            # Not all types may be available!
            if processmethod == method.sequential:
                TaskClass = WeekdayTask
            elif processmethod == method.threaded:
                TaskClass = ThreadedWeekdayTask
            elif processmethod == method.forked:
                TaskClass = ForkedWeekdayTask
            else:
                raise ValueError("Invalid processmethod")
            if self.running:
                self._acquire_lock()
                try:
                    if self.tasks.has_key(taskname):
                        raise ValueError("A task with the name %s already exists" % taskname)
                finally:
                    self._release_lock()
            else:
                if self.tasks.has_key(taskname):
                    raise ValueError("A task with the name %s already exists" % taskname)
            task = TaskClass(taskname, weekdays, timeonday, action, args, kw)
        if monthdays:
            # Select the correct MonthdayTask class.
            # Not all types may be available!
            if processmethod == method.sequential:
                TaskClass = MonthdayTask
            elif processmethod == method.threaded:
                TaskClass = ThreadedMonthdayTask
            elif processmethod == method.forked:
                TaskClass = ForkedMonthdayTask
            else:
                raise ValueError("Invalid processmethod")
            if self.running:
                self._acquire_lock()
                try:
                    if self.tasks.has_key(taskname):
                        raise ValueError("A task with the name %s already exists" % taskname)
                finally:
                    self._release_lock()
            else:
                if self.tasks.has_key(taskname):
                    raise ValueError("A task with the name %s already exists" % taskname)
            task = TaskClass(taskname, monthdays, timeonday, action, args, kw)
        firsttime = task.get_schedule_time(True)
        self.schedule_task_abs(task, firsttime)
        return task

    def add_cron_like_task(self, action, taskname, cron_str,
            processmethod, args, kw):
        """ Add a new Cron-like Task to the schedule. """
        if not args:
            args = []
        if not kw:
            kw = {}
        if processmethod == method.sequential:
            TaskClass = CronLikeTask
        elif processmethod == method.threaded:
            TaskClass = ThreadedCronLikeTask
        elif processmethod == method.forked:
            TaskClass = ForkedCronLikeTask
        else:
            raise ValueError("Invalid processmethod")
        if self.running:
            self._acquire_lock()
            try:
                if self.tasks.has_key(taskname):
                    raise ValueError("A task with the name %s already exists" % taskname)
            finally:
                self._release_lock()
        else:
            if self.tasks.has_key(taskname):
                raise ValueError("A task with the name %s already exists" % taskname)
        task = TaskClass(taskname, action, cron_str, args, kw)
        firsttime = task.get_schedule_time()
        self.schedule_task_abs(task, firsttime)
        return task

    def schedule_task(self, task, delay):
        """
        Add a new task to the scheduler with the given delay (seconds).
        Low-level method for internal use.
        """
        if self.running:
            # lock the sched queue, if needed
            self._acquire_lock()
            try:
                task.event = self.sched.enter(delay, 0, task,
                            (weakref.ref(self),) )
                if task.name:
                    self.tasks[task.name] = task
                else:
                    log.debug("task %s doesn't have a name" % task)
            finally:
                self._release_lock()
        else:
            task.event = self.sched.enter(delay, 0, task,
                        (weakref.ref(self),) )
            if task.name:
                self.tasks[task.name] = task
            else:
                log.debug("task %s doesn't have a name" % task)

    def schedule_task_abs(self, task, abstime):
        """
        Add a new task to the scheduler for the given absolute time value.
        Low-level method for internal use.
        """
        if self.running:
            # lock the sched queue, if needed
            self._acquire_lock()
            try:
                task.event = self.sched.enterabs(abstime, 0, task,
                                    (weakref.ref(self),) )
                if task.name:
                    self.tasks[task.name] = task
                else:
                    log.debug("task %s doesn't have a name" % task)
            finally:
                self._release_lock()
        else:
            task.event = self.sched.enterabs(abstime, 0, task,
                                (weakref.ref(self),) )
            if task.name:
                self.tasks[task.name] = task
            else:
                log.debug("task %s doesn't have a name" % task)

    def start(self):
        """ Start the scheduler. """
        self._run()

    def stop(self):
        """ Remove all pending tasks and stop the Scheduler. """
        self.running = False
        self._clearschedqueue()

    def cancel(self, task):
        """Cancel given scheduled task."""
        if self.running:
            self._acquire_lock()
            try:
                self.sched.cancel(task.event)
                if task.name and self.tasks.has_key(task.name):
                    del self.tasks[task.name]
            finally:
                self._release_lock()
        else:
            self.sched.cancel(task.event)
            if task.name and self.tasks.has_key(task.name):
                del self.tasks[task.name]

    if sys.version_info >= (2,6):
        # code for sched module of python 2.6+
        def _getqueuetoptime(self):
            if len(self.sched._queue):
                return self.sched._queue[0].time
        def _clearschedqueue(self):
            self.sched._queue[:] = []
    else:
        # code for sched module of python 2.5 and older
        def _getqueuetoptime(self):
            if len(self.sched.queue) and len(self.sched.queue[0]):
                return self.sched.queue[0][0]
        def _clearschedqueue(self):
            self.sched.queue[:] = []

    def _run(self):
        """ Low-level run method to do the actual scheduling loop. """
        while self.running:
            try:
                self.sched.run()
            except Exception, err:
                log.error("ERROR DURING SCHEDULER EXECUTION", exc_info=1)
                log.error("-" * 20)
            # queue is empty; sleep a short while before checking again
            if self.running:
                time.sleep(5)


class Task:
    """ Abstract base class of all scheduler tasks """

    def __init__(self, name, action, args, kw):
        """This is an abstract class!"""
        self.name = name
        self.action = action
        self.args = args
        self.kw = kw

    def __call__(self, schedulerref):
        """Execute the task action in the scheduler's thread."""
        try:
            self.execute()
        except Exception, err:
            self.handle_exception(err)
        self.reschedule(schedulerref())

    def reschedule(self, scheduler):
        """ This method should be defined in one of the sub classes! """
        raise NotImplementedError("You're using the abstract base class 'Task',"
            " use a concrete class instead")

    def execute(self):
        """Execute the actual task."""
        self.action(*self.args, **self.kw)

    def handle_exception(self, exc):
        """ Handle any exception that occured during task execution. """
        log.error("ERROR DURING TASK EXECUTION", exc_info=1)
        log.error("-" * 20)


class SingleTask(Task):
    """ A task that only runs once. """

    def reschedule(self, scheduler):
        pass


class IntervalTask(Task):
    """ A repeated task that occurs at certain intervals (in seconds) ."""

    def __init__(self, name, interval, action, args=None, kw=None):
        Task.__init__(self, name, action, args, kw)
        self.interval = interval

    def reschedule(self, scheduler):
        """Reschedule this task according to its interval (in seconds)."""
        if scheduler.running:
            scheduler.schedule_task(self, self.interval)


class DayTaskRescheduler:
    """A mixin class that contains the reschedule logic for the DayTasks."""

    def __init__(self, timeonday):
        self.timeonday = timeonday

    def get_schedule_time(self, today):
        """Calculate the time value at which this task is to be scheduled."""
        now = list(time.localtime())
        if today:
            # schedule for today. let's see if that is still possible
            if (now[3], now[4]) >= self.timeonday:
                # too bad, it will be tomorrow
                now[2] += 1
        else:
            # tomorrow
            now[2] += 1
        # set new time on day (hour,minute)
        now[3], now[4] = self.timeonday
        # seconds
        now[5] = 0
        return time.mktime(now)

    def reschedule(self, scheduler):
        """Reschedule this task according to the daytime for the task.
        
        The task is scheduled for tomorrow, for the given daytime.

        """
        # (The execute method in the concrete Task classes will check
        # if the current day is a day on which the task must run).
        if scheduler.running:
            abstime = self.get_schedule_time(False)
            scheduler.schedule_task_abs(self, abstime)


class WeekdayTask(DayTaskRescheduler, Task):
    """A task that is called at specific days in a week (1-7), at a fixed time
    on the day.
    
    """

    def __init__(self, name, weekdays, timeonday, action, args=None, kw=None):
        if type(timeonday) not in (list, tuple) or len(timeonday) != 2:
            raise TypeError("timeonday must be a 2-tuple (hour,minute)")
        if type(weekdays) not in (list, tuple):
            raise TypeError("weekdays must be a sequence of weekday numbers "
                "1-7 (1 is Monday)")
        DayTaskRescheduler.__init__(self, timeonday)
        Task.__init__(self, name, action, args, kw)
        self.days = weekdays

    def execute(self):
        # This is called every day, at the correct time. We only need to
        # check if we should run this task today (this day of the week).
        weekday = time.localtime().tm_wday + 1
        if weekday in self.days:
            self.action(*self.args, **self.kw)


class MonthdayTask(DayTaskRescheduler, Task):
    """A task that is called at specific days in a month (1-31), at a fixed 
    time on the day.
    
    """

    def __init__(self, name, monthdays, timeonday, action, args=None, kw=None):
        if type(timeonday) not in (list, tuple) or len(timeonday) != 2:
            raise TypeError("timeonday must be a 2-tuple (hour,minute)")
        if type(monthdays) not in (list, tuple):
            raise TypeError("monthdays must be a sequence of monthdays numbers "
                "1-31")
        DayTaskRescheduler.__init__(self, timeonday)
        Task.__init__(self, name, action, args, kw)
        self.days = monthdays

    def execute(self):
        # This is called every day, at the correct time. We only need to
        # check if we should run this task today (this day of the month).
        if time.localtime().tm_mday in self.days:
            self.action(*self.args, **self.kw)


class CronLikeTask(Task):
    """A class that is scheduled with a cron-like syntax.
    """
    def __init__(self, name, action, cron_str, args=None, kw=None):
        Task.__init__(self, name, action, args, kw)

        self.cron_str = cron_str
        try:
            min_str, hour_str, dom_str, month_str, dow_str = cron_str.split()
        except:
            raise ValueError("Invalid value: %s" % cron_str)

        self.minutes = self.__process_str(min_str, MINUTE_BOUNDS)
        self.hours = self.__process_str(hour_str, HOUR_BOUNDS)
        self.doms = self.__process_str(dom_str, DOM_BOUNDS)
        self.months = self.__process_str(month_str, MONTH_BOUNDS, mapping=MONTH_MAPPING)

        # dows are somewhat special:
        #   * Cron accepts both 0 and 7 for Sunday
        #     => we deal with that using the "% 7" operator and a temporary set
        #   * Python starts with Monday = 0 while Cron starts with Sunday = 0
        #     => we deal with that by substracting 1
        #   * (SUN - 1) % 7 = (0 - 1) % 7 = 6
        #     => we need to sort the list
        self.dows = list(set([ (dow - 1) % 7 \
                for dow in self.__process_str(dow_str,
                        DOW_BOUNDS, mapping=DOW_MAPPING) ]))
        self.dows.sort()

    def __process_str(self, time_str, bounds, mapping=None):
        """Transforms a field of the cron-like string into a list

        Note: specifying a range as a mix of integers and names
              (months and dows) is NOT supported

        @param time_str: a field in the cron-like string
        @type time_str: string

        @param bounds: the acceptable limits for this field
        @type bounds: 2-tuple of integers

        @param mapping: the mapping between names and integer values
        @type mapping: dict
        """
        freq = 1
        if '/' in time_str:
            try:
                time_str, freq = time_str.split('/')
                freq = int(freq)
            except:
                raise ValueError("Invalid value: '%s'" % time_str)

        if time_str == '*':
            result = range(bounds[0], bounds[1] + 1)
            return result[::freq]

        result = list()

        for item in time_str.split(','):
            if not '-' in item:
                # ex: time_str = "1,4,23"
                try:
                    time = int(item)
                except:
                    if mapping and mapping.has_key(item.lower()):
                        time = mapping[item.lower()]
                    else:
                        raise ValueError("Invalid value: '%s'" % time_str)

                if time < bounds[0] or time > bounds [1]:
                    raise ValueError("Invalid value: '%s'" % time_str)

                result.append(time)
            else:
                # ex: time_str = "1-4,7-9"
                try:
                    interval_low, interval_high = item.split('-')
                except:
                    # an interval can only have one dash
                    raise ValueError("Invalid value: '%s'" % time_str)

                try:
                    # intervals are specified as integers
                    time_low = int(interval_low)
                    time_high = int(interval_high)
                except:
                    if mapping and mapping.has_key(interval_low.lower()) \
                            and mapping.has_key(interval_high.lower()):
                        # in some cases names can be used (months or dows)
                        time_low = mapping[interval_low.lower()]
                        time_high = mapping[interval_high.lower()]
                    else:
                        raise ValueError("Invalid value: '%s'" % time_str)

                if time_low < bounds[0] or time_high > bounds [1]:
                    raise ValueError("Invalid value: '%s'" % time_str)

                result.extend(range(time_low, time_high + 1))

        # filter results by frequency
        return result[::freq]

    def get_schedule_time(self):
        """Determine the next execution time of the task.
        """
        now = datetime.datetime.now()

        # rrule will return `now` as the next execution time if `now` fills the
        # criteria. This has the nasty effect of relaunching the same task over
        # and over during one second.
        # That only happens when `now.second == 0` (which is always the case
        # after the first execution as cron doesn't handle anything below the
        # minute), so let's add one second to `now`, just to be sure
        now = now + datetime.timedelta(seconds=1)

        next = list(rrule(SECONDLY, count=1, bysecond=0, byminute=self.minutes,
                byhour=self.hours, bymonthday=self.doms, bymonth=self.months,
                byweekday=self.dows, dtstart=now)[0].timetuple())

        return time.mktime(next)

    def reschedule(self, scheduler):
        """Reschedule this task according to its cron-like string.
        """
        if scheduler.running:
            abstime = self.get_schedule_time()
            scheduler.schedule_task_abs(self, abstime)


try:
    import threading

    class ThreadedScheduler(Scheduler):
        """A Scheduler that runs in its own thread."""

        def __init__(self):
            Scheduler.__init__(self)
            # we require a lock around the task queue
            self.thread = None
            self._lock = threading.Lock()

        def start(self):
            """Splice off a thread in which the scheduler will run."""
            self.thread = threading.Thread(target=self._run)
            self.thread.setDaemon(True)
            self.thread.start()
            
        def stop(self):
            """Stop the scheduler and wait for the thread to finish."""
            Scheduler.stop(self)
            try:
                self.thread.join()
            except AttributeError:
                pass

        def _acquire_lock(self):
            """Lock the thread's task queue."""
            self._lock.acquire()
            
        def _release_lock(self):
            """Release the lock on th ethread's task queue."""
            self._lock.release()


    class ThreadedTaskMixin:
        """A mixin class to make a Task execute in a separate thread."""

        def __call__(self, schedulerref):
            """Execute the task action in its own thread."""
            threading.Thread(target=self.threadedcall).start()
            self.reschedule(schedulerref())

        def threadedcall(self):
            """ 
            This method is run within its own thread, so we have to
            do the execute() call and exception handling here.
            """
            try:
                self.execute()
            except Exception, err:
                self.handle_exception(err)

    class ThreadedIntervalTask(ThreadedTaskMixin, IntervalTask):
        """Interval Task that executes in its own thread."""
        pass

    class ThreadedSingleTask(ThreadedTaskMixin, SingleTask):
        """Single Task that executes in its own thread.""" 
        pass

    class ThreadedWeekdayTask(ThreadedTaskMixin, WeekdayTask):
        """Weekday Task that executes in its own thread."""
        pass

    class ThreadedMonthdayTask(ThreadedTaskMixin, MonthdayTask):
        """Monthday Task that executes in its own thread."""
        pass

    class ThreadedCronLikeTask(ThreadedTaskMixin, CronLikeTask):
        """Cron-like Task that executes in its own thread."""
        pass

except ImportError:
    # threading is not available
    pass


if hasattr(os, "fork"):
    import signal

    class ForkedScheduler(Scheduler):
        """A Scheduler that runs in its own forked process."""

        def __del__(self):
            if hasattr(self, "childpid"):
                os.kill(self.childpid, signal.SIGKILL)

        def start(self):
            """Fork off a new process in which the scheduler will run."""
            pid = os.fork()
            if pid == 0:
                # we are the child
                signal.signal(signal.SIGUSR1, self.signalhandler)
                self._run()
                os._exit(0)
            else:
                # we are the parent
                self.childpid = pid
                # can no longer insert in the scheduler queue
                del self.sched

        def stop(self):
            """Stop the scheduler and wait for the process to finish."""
            os.kill(self.childpid, signal.SIGUSR1)
            os.waitpid(self.childpid, 0)

        def signalhandler(self, sig, stack):
            Scheduler.stop(self)


    class ForkedTaskMixin:
        """A mixin class to make a Task execute in a separate process."""

        def __call__(self, schedulerref):
            """Execute the task action in its own process."""
            pid = os.fork()
            if pid == 0:
                # we are the child
                try:
                    self.execute()
                except Exception, err:
                    self.handle_exception(err)
                os._exit(0)
            else:
                # we are the parent
                self.reschedule(schedulerref())


    class ForkedIntervalTask(ForkedTaskMixin, IntervalTask):
        """Interval Task that executes in its own process."""
        pass

    class ForkedSingleTask(ForkedTaskMixin, SingleTask):
        """Single Task that executes in its own process."""
        pass

    class ForkedWeekdayTask(ForkedTaskMixin, WeekdayTask):
        """Weekday Task that executes in its own process."""
        pass

    class ForkedMonthdayTask(ForkedTaskMixin, MonthdayTask):
        """Monthday Task that executes in its own process."""
        pass

    class ForkedCronLikeTask(ForkedTaskMixin, CronLikeTask):
        """Cron-like Task that executes in its own process."""
        pass

if __name__ == "__main__":
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    log.addHandler(ch)

    def testaction(arg):
        log.warn(">>>TASK %s sleeping 3 seconds", arg)
        time.sleep(3)
        log.warn("<<<END_TASK %s", arg)

    s = ThreadedScheduler()
    s.add_interval_task( testaction, "test action 1", 0, 4, method.threaded, ["task 1"], None )
    s.start()

    log.info("Scheduler started, waiting 15 sec....")
    time.sleep(15)

    log.info("STOP SCHEDULER")
    s.stop()

    log.info("EXITING")


