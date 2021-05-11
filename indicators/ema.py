# https://stackoverflow.com/a/42915307
def numpy_ewma(data, window):
    returnArray = np.empty((data.shape[0]))
    returnArray.fill(np.nan)
    e = data[0]
    alpha = 2 / float(window + 1)
    for s in range(data.shape[0]):
        e =  ((data[s]-e) *alpha ) + e
        returnArray[s] = e
    return returnArray
