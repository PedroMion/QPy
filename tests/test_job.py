import pytest


from qpy.job import Job


ARRIVAL_TIME = 5
COMPLETION_TIME = 8
INITIAL_SERVER = 2
JOB_ID = 1
NEW_SERVER = 3
PRIORITY = 0

@pytest.fixture
def job_test_object():
    return Job(id=JOB_ID, arrival_time=ARRIVAL_TIME, current_server=INITIAL_SERVER, priority=PRIORITY)


def test_serve_when_job_waited_should_append_queue_time(job_test_object):
    job_test_object.serve(service_started_time=COMPLETION_TIME)

    assert job_test_object.queue_times_per_server[INITIAL_SERVER] == COMPLETION_TIME - ARRIVAL_TIME

def test_serve_when_job_dont_wait_should_remain_with_queue_time_zero(job_test_object):
    job_test_object.serve(service_started_time=ARRIVAL_TIME)

    assert job_test_object.queue_times_per_server[INITIAL_SERVER] == 0

def test_reroute_when_new_server_isnt_provided_should_compute_total_time(job_test_object):
    job_test_object.reroute(completion_time=COMPLETION_TIME)

    assert job_test_object.total_time_per_server[INITIAL_SERVER] == COMPLETION_TIME - ARRIVAL_TIME
    assert job_test_object.current_server == INITIAL_SERVER

def test_reroute_when_new_server_is_provided_should_switch_servers(job_test_object):
    job_test_object.reroute(completion_time=COMPLETION_TIME, new_server=NEW_SERVER)

    assert job_test_object.total_time_per_server[INITIAL_SERVER] == COMPLETION_TIME - ARRIVAL_TIME
    assert job_test_object.current_server == NEW_SERVER

def test_switch_servers_and_compute_state_should_alter_state(job_test_object):
    job_test_object.reroute(completion_time=COMPLETION_TIME, new_server=NEW_SERVER)

    assert job_test_object.current_server == NEW_SERVER
    assert job_test_object.arrival_time_at_current_server == COMPLETION_TIME
    assert COMPLETION_TIME in job_test_object.arrival_times_per_server[NEW_SERVER]
    assert job_test_object.total_visits_per_server[NEW_SERVER] == 1