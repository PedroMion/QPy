from qpy import QueueDiscipline


def get_queue_discipline(queueProperties):
    match queueProperties.queueDiscipline:
        case 'fcfs':
            return QueueDiscipline.fcfs()
        case 'lcfs':
            return QueueDiscipline.lcfs()
        case 'srt':
            return QueueDiscipline.srt(bool(queueProperties.params['withPreemption']))
        case 'rr':
            return QueueDiscipline.round_robin(float(queueProperties.params['preemptionTime']))
        case 'priority':
            return QueueDiscipline.priority_queue(bool(queueProperties.params['withPreemption']))
        case _:
            raise ValueError('Queue discipline not allowed: ' + queueProperties.queueDiscipline)