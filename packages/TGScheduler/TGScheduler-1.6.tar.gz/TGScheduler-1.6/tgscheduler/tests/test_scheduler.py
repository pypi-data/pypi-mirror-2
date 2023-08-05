from nose.tools import raises

from tgscheduler import start_scheduler, stop_scheduler, add_single_task,\
                                    add_interval_task, add_monthly_task, add_weekday_task, \
                                    add_cron_like_task

def functest(*args, **kws):
    pass

def test_scheduler():
    sched = start_scheduler()
    assert hasattr(sched, "running") == True 
    assert sched.running == True  
    
    task = add_single_task(functest, taskname="singletest")
    assert task.action == functest
    assert task.name == "singletest"
    
    task = add_weekday_task(functest, [2], (0, 0), taskname="weekdaytest")
    assert task.action == functest
    assert task.name == "weekdaytest"
    
    task = add_monthly_task(functest, (2, 10), (1, 0), taskname="monthlytest")
    assert task.action == functest
    assert task.name == "monthlytest"
    
    task = add_interval_task(functest, 60*10, taskname="intervaltest")
    assert task.action == functest
    assert task.name == "intervaltest"
    
def test_cron_like_business_hours():
    task = add_cron_like_task(functest, "*/30 8-12,14-18 * * MON-FRI", taskname="crontest_business_hours")
    assert task.action == functest
    assert task.name == "crontest_business_hours"
    assert task.minutes == [0, 30], \
        "Invalid minutes: %s" % t.minutes
    assert task.hours == [8, 9, 10, 11, 12, 14, 15, 16, 17, 18], \
        "Invalid hours: %s" % t.hours
    assert task.doms == range(1, 32), \
        "Invalid doms: %s" % t.doms
    assert task.months == range(1, 13), \
        "Invalid months: %s" % t.months
    assert task.dows == range(0, 5), \
        "Invalid dows: %s" % t.dows

def test_cron_like_complex():
    task = add_cron_like_task(functest, "5-10,25-30,57 8-12,14-18 2,25-28 Jan-mar,10-12 SuN-wEd", taskname="crontest_complex")
    assert task.action == functest
    assert task.name == "crontest_complex"
    assert task.minutes == [5, 6, 7, 8, 9, 10, 25, 26, 27, 28, 29, 30, 57], \
        "Invalid minutes: %s" % t.minutes
    assert task.hours == [8, 9, 10, 11, 12, 14, 15, 16, 17, 18], \
        "Invalid hours: %s" % t.hours
    assert task.doms == [2, 25, 26, 27, 28], \
        "Invalid doms: %s" % t.doms
    assert task.months == [1, 2, 3, 10, 11, 12], \
        "Invalid months: %s" % t.months
    assert task.dows == [0, 1, 2, 6], \
        "Invalid dows: %s" % t.dows

@raises(ValueError)
def test_cron_like_failure():
    """ This test should fail with ValueError as we feed the scheduler with
    an incorrect value: `Jan-12` (mixing names and integers is not supported)
    """
    task = add_cron_like_task(functest, "* * * Jan-12 *", taskname="crontest3")
    assert False, "This shouldn't have worked"

def test_stop_scheduler():
    stop_scheduler()

