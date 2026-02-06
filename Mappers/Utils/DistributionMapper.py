from qpy import Distribution


def get_distribution(distributionProperties):
    match distributionProperties.distribution:
        case 'exponential':
            return Distribution.exponential(mean_time_between_events=distributionProperties.params['meanTime'])
        case 'constant':
            return Distribution.constant(value=distributionProperties.params['constantValue'])
        case 'uniform':
            return Distribution.uniform(lower_bound=distributionProperties.params['lowerBound'], upper_bound=distributionProperties.params['upperBound'])
        case 'normal':
            return Distribution.normal(mu=distributionProperties.params['mu'], sigma=distributionProperties.params['sigma'])
        case _:
            raise ValueError('Distribution not allowed: ' + distributionProperties.distribution)