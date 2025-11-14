from qpy.distribution import Distribution


DELTA_PERCENTAGE = 0.05 # 5% margin of error
NUMBER_OF_EXECUTIONS = 100000
CONSTANT_VALUE = 2
LAMBDA_VALUE_EXPONENTIAL = 2
LOWER_BOUND_UNIFORM = 0
UPPER_BOUND_UNIFORM = 4
MU_NORMAL = 10
SIGMA_NORMAL = 2


def value_within_range(expected: float, actual: float, delta: float):
    margin = delta * expected

    return (actual >= expected - margin) and (actual <= expected + margin)

def test_constant_distribution_samples():
    distribution = Distribution.constant(value = CONSTANT_VALUE)

    sample_sum = 0

    for _ in range(NUMBER_OF_EXECUTIONS):
        sample_sum += distribution.sample()
    
    assert sample_sum // NUMBER_OF_EXECUTIONS == CONSTANT_VALUE

def test_exponential_distribution_samples():
    distribution = Distribution.exponential(lambda_value=LAMBDA_VALUE_EXPONENTIAL)

    sample_sum = 0

    for _ in range(NUMBER_OF_EXECUTIONS):
        sample_sum += distribution.sample()
    
    assert value_within_range(LAMBDA_VALUE_EXPONENTIAL, sample_sum / NUMBER_OF_EXECUTIONS, DELTA_PERCENTAGE)

def test_uniform_distribution_samples():
    distribution = Distribution.uniform(LOWER_BOUND_UNIFORM, UPPER_BOUND_UNIFORM)

    sum_lower_half = 0
    sum_upper_half = 0

    for _ in range(NUMBER_OF_EXECUTIONS):
        sample = distribution.sample()

        if sample < UPPER_BOUND_UNIFORM // 2:
            sum_lower_half += 1
        else:
            sum_upper_half += 1
    
    assert value_within_range(sum_upper_half, sum_lower_half, DELTA_PERCENTAGE)

def test_normal_distribution_samples():
    distribution = Distribution.normal(MU_NORMAL, SIGMA_NORMAL)

    sample_sum = 0

    for _ in range(NUMBER_OF_EXECUTIONS):
        sample_sum += distribution.sample()
    
    assert value_within_range(MU_NORMAL, sample_sum / NUMBER_OF_EXECUTIONS, DELTA_PERCENTAGE)