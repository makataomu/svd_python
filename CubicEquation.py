# square root - babylonian method
def manual_sqrt(x, tolerance=1e-10):
    if x < 0:
        raise ValueError("Cannot compute square root of a negative number.")
    guess = x / 2.0
    while abs(guess * guess - x) > tolerance:
        guess = (guess + x / guess) / 2.0
    return guess

# acos - taylor series approximation
def manual_acos(x, tolerance=1e-10):
    if x < -1 or x > 1:
        raise ValueError("Invalid input for acos. Must be between -1 and 1.")
    
    term = x
    acos_val = 0
    n = 0
    while abs(term) > tolerance:
        coef = (1.0 if n == 0 else (-1) ** n) / (2 * n + 1)
        acos_val += coef * (x ** (2 * n + 1))
        n += 1
    
    return (3.14159265358979 / 2.0) - acos_val

# cos - Taylor series approximation
def manual_cos(x, tolerance=1e-10):
    x = x % (2 * 3.14159265358979)  # angle: 0 - 2π
    term = 1
    cos_val = 0
    n = 0
    while abs(term) > tolerance:
        term = ((-1) ** n) * (x ** (2 * n)) / factorial(2 * n)
        cos_val += term
        n += 1
    return cos_val

def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

def cube_root(x):
    if x >= 0:
        return x ** (1 / 3)
    else:
        return -(-x) ** (1 / 3)


def CubicEquation(a, b, c, d):
    if a == 0:
        return "Error: a must be non-zero."
    
    # depressed cubic form: t^3 + pt + q = 0
    p = (3 * a * c - b ** 2) / (3 * a ** 2)
    q = (2 * b ** 3 - 9 * a * b * c + 27 * a ** 2 * d) / (27 * a ** 3)
    
    # discriminant
    delta = (q ** 2) / 4 + (p ** 3) / 27
    
    if delta > 0:  # 1 real 2 img 
        S = cube_root(-q / 2 + manual_sqrt(delta))
        T = cube_root(-q / 2 - manual_sqrt(delta))
        x1 = S + T - b / (3 * a)
        
        # img roots
        real_part = -0.5 * (S + T) - b / (3 * a)
        imaginary_part = manual_sqrt(3) / 2 * (S - T)
        x2 = f"{round(real_part, 6)} + {round(imaginary_part, 6)}i"
        x3 = f"{round(real_part, 6)} - {round(imaginary_part, 6)}i"
        
        return round(x1, 6), x2, x3
    
    elif delta == 0:  # 2-3 real
        if q == 0:
            x1 = -b / (3 * a) 
            return round(x1, 6), round(x1, 6), round(x1, 6)
        else:
            S = cube_root(-q / 2)
            x1 = 2 * S - b / (3 * a)
            x2 = -S - b / (3 * a)
            return round(x1, 6), round(x2, 6), round(x2, 6)
    
    else:  # 3 real
        theta = manual_acos(-q / 2 / manual_sqrt(-(p ** 3) / 27))
        x1 = 2 * manual_sqrt(-p / 3) * manual_cos(theta / 3) - b / (3 * a)
        x2 = 2 * manual_sqrt(-p / 3) * manual_cos((theta + 2 * 3.14159265358979) / 3) - b / (3 * a)
        x3 = 2 * manual_sqrt(-p / 3) * manual_cos((theta + 4 * 3.14159265358979) / 3) - b / (3 * a)
        return round(x1, 6), round(x2, 6), round(x3, 6)

a = float(input("a: "))
b = float(input("b: "))
c = float(input("c: "))
d = float(input("d: "))

print(CubicEquation(a, b, c, d))