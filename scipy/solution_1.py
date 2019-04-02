g = 9.82
L = 0.5
m = 0.1

def pendulum_model(t, y):
    """
    The right-hand side of the pendulum ODE
    """
    phi_1, phi_2, p_1, p_4 = y[0], y[1], y[2], y[3]
    
    dphi_1 = 6.0/(m*L**2) * (2 * p_1 - 3 * np.cos(phi_1-phi_2) * p_4)/(16 - 9 * np.cos(phi_1-phi_2)**2)
    dphi_2 = 6.0/(m*L**2) * (8 * p_4 - 3 * np.cos(phi_1-phi_2) * p_1)/(16 - 9 * np.cos(phi_1-phi_2)**2)
    dp_1 = -0.5 * m * L**2 * ( dphi_1 * dphi_2 * np.sin(phi_1-phi_2) + 3 * (g/L) * np.sin(phi_1))
    dp_4 = -0.5 * m * L**2 * (-dphi_1 * dphi_2 * np.sin(phi_1-phi_2) + (g/L) * np.sin(phi_2))
    
    return [dphi_1, dphi_2, dp_1, dp_4]

# initial values  
y0 = [np.pi/3, -np.pi/4, 0, 0.065]
t_start, t_end = 0, 20  

solution = solve_ivp(pendulum_model, (t_start, t_end), y0, t_eval=np.linspace(t_start, t_end, 40000))

x1s = + L * np.sin(solution.y[0])
y1s = - L * np.cos(solution.y[0])

x2s = x1s + L * np.sin(solution.y[1])
y2s = y1s - L * np.cos(solution.y[1])

plt.plot(x1s, y1s, '.', alpha=0.02, color='xkcd:sky blue')
plt.plot(x2s, y2s, '.', alpha=0.1, color='xkcd:dark magenta')
plt.axis('off')
None
