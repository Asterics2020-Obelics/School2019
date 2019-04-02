def poisson(k, lamb):
    """poisson pdf, parameter lamb is the fit parameter"""
    return (lamb**k/special.factorial(k)) * np.exp(-lamb)


def negLogLikelihood(params, data):
    """ the negative log-Likelohood-Function"""
    lnl = - np.sum(np.log(poisson(data, params[0])))
    return lnl


# minimize the negative log-Likelihood
result = optimize.minimize(negLogLikelihood,  x0=[1], args=(data,))

print(result)

# plot poisson-deviation with fitted parameter
x_plot = np.linspace(0, 12, 1500)

plt.hist(data.ravel(), bins=np.arange(12) - 0.5, density=True,)
plt.plot(x_plot, poisson(x_plot, result.x), 'r-', lw=2)
