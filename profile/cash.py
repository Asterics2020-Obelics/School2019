"""How to make cash with Python, fast!

The binned Poisson likelihood in astronomy is sometimes called the Cash fit
statistic, because it was described in detail in a paper by Cash 1979
(http://adsabs.harvard.edu/abs/1979ApJ...228..939C).

For observed counts ``n`` and expected counts ``mu`` it is given by:

    C = 2 (mu - n log(mu))

and if there are bins with zero predicted counts one has to ignore them via:

    C = 0 if mu <= 0

Below you will find a common application example: a 1-dimensional counts
histogram and a Cash statistic fit of a Gaussian model.
"""
import numpy as np


def model(x, amplitude, mean, stddev):
    """Evaluate Gaussian model."""
    return amplitude * np.exp(-0.5 * (x - mean) ** 2 / stddev ** 2)


def cash(n, mu):
    """Cash statistic for observed counts `n` and expected counts `mu`."""
    term = n * np.log(mu)
    stat = 2 * (mu - term)
    mask = n > 0
    stat = np.where(mask, stat, 0)
    return stat.sum()


def benchmark():
    # Set parameters
    number_of_bins = int(1e6)
    number_of_evaluations = 100
    amplitude = 10
    mean = 0
    stddev = 10

    # Set up a test case
    x = np.linspace(start=-10, stop=+10, num=number_of_bins)
    dx = x[1] - x[0]
    np.random.seed(0)
    n = np.random.poisson(model(x, amplitude, mean, stddev))

    # Evaluate likelihood ten times.
    # Usually you would do it many times, using for example
    # scipy.optimize.minimize to find the best-fit parameters.
    for _ in range(number_of_evaluations):
        y = model(x, amplitude, mean, stddev)
        mu = dx * y
        stat = cash(n, mu)

    # Check on output for test case. This result shouldn't change as you try out
    # different implementations - apart from differences caused by floating point
    # rounding differences.
    np.testing.assert_allclose(stat, 1.481885e08, rtol=1e-3)


if __name__ == "__main__":
    benchmark()
