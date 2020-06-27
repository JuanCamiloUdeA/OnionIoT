from OmegaExpansion import AdcExp # Omega library to work with the ADS1015
adc = AdcExp.AdcExp()
volts=adc.read_voltage(0) # Function to read the current voltage value 
'''
adc.rea_voltage(a)
a=0
A0 Channel
a=1
A1 Channel
a=2
A2 Channel
a=3
A3 Channel 
'''
print(volts)