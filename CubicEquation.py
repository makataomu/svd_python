def manual_sqrt(x, tolerance=1e-10):
    if x < 0:
        raise ValueError("Cannot compute square root of a negative number.")
    if x == 0:
        return 0.0
    if x == 1:
        return 1.0

    guess = x if x > 1 else 1.0
    while True:
        next_guess = (guess + x / guess) / 2.0
        if abs(next_guess - guess) < tolerance:  
            break
        guess = next_guess
        
    return guess


pi = 3.14159
two_pi = 2 * pi


def manual_cos(x, tolerance=1e-10):
    x = x % two_pi  # angle: 0 - 2π
    term = 1
    cos_val = term
    n = 1
    while abs(term) > tolerance:
        term = (-term * x * x) / ((2 * n - 1) * (2 * n))  # use the previous term
        cos_val += term
        n += 1
    return cos_val

def manual_acos(x, tolerance=1e-10):
    if x < -1 or x > 1:
        raise ValueError("Invalid input for acos. Must be between -1 and 1.")
    
    # acos(x) = pi/2 - asin(x)
    if x < 0:
        return pi / 2 + manual_acos(-x)
    
    term = x
    acos_val = 0
    n = 0
    while abs(term) > tolerance:
        coef = (1.0 if n == 0 else (-1) ** n) / (2 * n + 1)
        acos_val += coef * (x ** (2 * n + 1))
        n += 1

    return pi / 2 - acos_val

# newton's method
def cube_root(x, tolerance=1e-10):
    if x == 0:
        return 0
    guess = x / 3.0
    while abs(guess**3 - x) > tolerance:
        guess = (2.0 * guess + x / (guess ** 2)) / 3.0
    return guess

def find_rational_roots(a, b, c, d):
    def divisors(n):
        result = set()
        for i in range(1, int(abs(n)) + 1):
            if n % i == 0:
                result.add(i)
                result.add(-i)
        return result

    # potential roots
    p_divisors = divisors(d)
    q_divisors = divisors(a)

    for p in p_divisors:
        for q in q_divisors:
            root = p / q
            if abs(a * root**3 + b * root**2 + c * root + d) < 1e-10: 
                return root
    return None

# reducing cubic to quadratic
def synthetic_division(a, b, c, root):
    new_b = a * root + b
    new_c = new_b * root + c
    return a, new_b, new_c

def solve_quadratic(a, b, c):
    discriminant = b**2 - 4 * a * c
    if discriminant > 0:
        sqrt_discriminant = manual_sqrt(discriminant)
        x1 = (-b + sqrt_discriminant) / (2 * a)
        x2 = (-b - sqrt_discriminant) / (2 * a)
        return round(x1, 6), round(x2, 6)
    elif discriminant == 0:
        x = -b / (2 * a)
        return round(x, 6), round(x, 6)
    else:
        real_part = round(-b / (2 * a), 6)
        imaginary_part = round(manual_sqrt(-discriminant) / (2 * a), 6)
        return f"{real_part} + {imaginary_part}i", f"{real_part} - {imaginary_part}i"

def CubicEquation(a, b, c, d):
    if a == 0:
        return "Error: a must be non-zero."

    rational_root = find_rational_roots(a, b, c, d)
    
    if rational_root is not None:
        new_a, new_b, new_c = synthetic_division(a, b, c, rational_root)
        x2, x3 = solve_quadratic(new_a, new_b, new_c)
        return round(rational_root, 6), x2, x3
    else:
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
            real_part = round(-0.5 * (S + T) - b / (3 * a), 6)
            imaginary_part = round(manual_sqrt(3) / 2 * (S - T), 6)
            x2 = f"{real_part} + {imaginary_part}i"
            x3 = f"{real_part} - {imaginary_part}i"
            
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
            x2 = 2 * manual_sqrt(-p / 3) * manual_cos((theta + 2 * pi) / 3) - b / (3 * a)
            x3 = 2 * manual_sqrt(-p / 3) * manual_cos((theta + 4 * pi) / 3) - b / (3 * a)
            return round(x1, 6), round(x2, 6), round(x3, 6)

# a = float(input("a: "))
# b = float(input("b: "))
# c = float(input("c: "))
# d = float(input("d: "))

# print(CubicEquation(a, b, c, d))