def sample_size(train_size):
    z_score = 2.58 # Corresponds to confidence level 99%
    margin_of_error = 0.01
    fraction_picking = 0.50
    numerator = (z_score**2 * fraction_picking * (1 - fraction_picking)) / (margin_of_error**2)
    denominator = 1 + (z_score**2 * fraction_picking * (1 - fraction_picking)) / (margin_of_error**2 * train_size)
    return numerator / denominator
