import sympy as sym
from sympy import GF

def make_poly(coeffs):
    """Create a polynomial in x."""
    x = sym.Symbol('x')
    N = len(coeffs)
    coeffs = list(reversed(coeffs))
    y = 0
    for i in range(N):
        y += (x**i)*coeffs[i]
    y = sym.poly(y)
    return y