import math

def int_round(n):
    dec = n - math.floor(n)
    if dec < 0.5:
        return math.floor(n)
    else:
        return math.ceil(n)

def round_limit(n, sig_figs=2, special_1_rule=True):
    if abs(n) >= 10.0:
        return (f'{int_round(n)}')
    elif (abs(n) >= 1) and (abs(n) < 2):
        if special_1_rule:
            sig_figs = sig_figs + 1
    # round with sig figs
    order = math.floor(math.log10(abs(n)))
    nD = sig_figs - order - 1
    n_rounded = '%.*f' % (nD, n)
    return n_rounded
