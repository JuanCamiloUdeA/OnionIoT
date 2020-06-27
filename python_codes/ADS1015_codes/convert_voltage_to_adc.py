from OmegaExpansion import AdcExp # Library to handle ADS105 Onion Omega 
'''
Function to convert volts to ADC 
X=0  A0 channel
x=1  A1 channel
x=2 A2 channel
x=3 A3 channel
'''

def adcval(x):
	adc = AdcExp.AdcExp()
	# Getting the current value in volts
	volts=adc.read_voltage(x)
	volts=round(volts,2)
	# Equations ADC vs Volts 
	raw_adc=(4095*volts)/(3.3)
	if raw_adc>4095:
		raw_adc=4095
	raw_adc=int(raw_adc)
	return raw_adc # Return the ADC value
	

print(adcval(0))