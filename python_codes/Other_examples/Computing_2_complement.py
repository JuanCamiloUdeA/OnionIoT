# Code to compute the 2's complement of int value val 
def convb(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    if(val<0):
    	val+1
    return val