import pytest


from qpy.job import Job


ARRIVAL_TIME = 5
COMPLETION_TIME = 8
INITIAL_SERVER = 2
JOB_ID = 1
NEW_SERVER = 3
PRIORITY = 0
NEGATIVE_VALUE = -1

@pytest.fixture
def job_test_object():
    return Job(id=JOB_ID, arrival_time=ARRIVAL_TIME, current_server=INITIAL_SERVER, priority=PRIORITY)


"""
Particionamento do espaço de entrada para função serve() da classe Job utilizando Each Choice Coverage:
    service_started_time: 0 | < 0 | > 0
"""

"""service_started_time > 0 (Válido)"""
def test_serve_when_job_waited_in_queue_should_append_queue_time(job_test_object):
    job_test_object.serve(service_started_time=COMPLETION_TIME)

    assert job_test_object.queue_times_per_server[INITIAL_SERVER] == COMPLETION_TIME - ARRIVAL_TIME

"""service_started_time = 0 (Válido)"""
def test_serve_when_job_doesnt_wait_should_remain_with_queue_time_zero(job_test_object):
    job_test_object.serve(service_started_time=ARRIVAL_TIME)

    assert job_test_object.queue_times_per_server[INITIAL_SERVER] == 0

"""service_started_time < 0 (Inválido)"""
def test_serve_when_job_is_executed_before_arrival_should_raise_exception(job_test_object):
    with pytest.raises(ValueError):
        job_test_object.serve(service_started_time=NEGATIVE_VALUE)


"""
Particionamento do espaço de entrada para função reroute() da classe Job utilizando Each Choice Coverage:
    completion_time: < 0 | >= 0
    new_server: < 0 | >= 0 | None
"""

"""completion_time >= 0 | new_server = None (Válido)"""
def test_reroute_when_new_server_isnt_provided_should_compute_total_time(job_test_object):
    job_test_object.reroute(completion_time=COMPLETION_TIME)

    assert job_test_object.total_time_per_server[INITIAL_SERVER] == COMPLETION_TIME - ARRIVAL_TIME
    assert job_test_object.current_server == INITIAL_SERVER

"""completion_time >= 0 | new_server >= 0 (Válido)"""
def test_reroute_when_new_server_is_provided_should_switch_servers(job_test_object):
    job_test_object.reroute(completion_time=COMPLETION_TIME, new_server=NEW_SERVER)

    assert job_test_object.total_time_per_server[INITIAL_SERVER] == COMPLETION_TIME - ARRIVAL_TIME
    assert job_test_object.current_server == NEW_SERVER

"""completion_time < 0 | new_server >= 0 (Inválido)"""
def test_reroute_when_completion_time_is_invalid_should_raise_exception(job_test_object):
    with pytest.raises(ValueError):
        job_test_object.reroute(completion_time=NEGATIVE_VALUE, new_server=NEW_SERVER)

"""completion_time >= 0 | new_server < 0 (Inválido)"""
def test_reroute_when_new_server_is_invalid_should_raise_exception(job_test_object):
    with pytest.raises(ValueError):
        job_test_object.reroute(completion_time=COMPLETION_TIME, new_server=NEGATIVE_VALUE)