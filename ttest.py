from scipy import optimize
def f(x,a):
    return (x**3 - a)


sol = optimize.root_scalar(f, bracket=[2, 3], method='brentq', args=(1))
print(sol.root)