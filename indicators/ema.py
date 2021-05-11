import numpy as np 


# https://stackoverflow.com/a/42915307
def np_ema(current_price, prev_ema, window):
    k = 2 / ( window + 1 )
    return current_price * k + prev_ema * (1 - k)
