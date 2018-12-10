def sample_size(population_size):
    """Calculates the sample size.

    Calculates the sample size required to draw from a population size `population_size`
    with a confidence level of 99% and a margin of error of 1%.

    Args:
      population_size (int): The population size to draw from.
    """
    margin_of_error = 0.01
    fraction_picking = 0.50
    z_score = 2.58 # Corresponds to confidence level 99%
    numerator = (z_score**2 * fraction_picking * (1 - fraction_picking)) / (margin_of_error**2)
    denominator = 1 + (z_score**2 * fraction_picking * (1 - fraction_picking)) / (margin_of_error**2 * population_size)
    return numerator / denominator
