import math
def mcnemar(X, Y):
    n = len(X)
    b = c = 0
    for i in range(n):
        if X[i] == 1 and Y[i] == 0:
            b += 1
        elif X[i] == 0 and Y[i] == 1: 
            c += 1
            
    diff = abs(b - c)
    total = b + c
    chi_square = 0
    
    if total == 0:
        chi_square = 0.0
    else:
        if total < 25:
            adjusted_diff = max(0.0, diff - 0.5)
            chi_square = (adjusted_diff ** 2) / total
        else:
            chi_square = (diff ** 2) / total
        
    p_value = 1 - math.erf(1 - math.sqrt(chi_square**2/2))
    return chi_square