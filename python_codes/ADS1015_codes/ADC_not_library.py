from OmegaExpansion import onionI2C
# Libraries for handling I2C ports 

i2c = onionI2C.OnionI2C()
# Initializinf the I2C port

# This vector has two address of the ADS1015. Those are mandatory for getting the voltage values
data = [0x84,0x83]
i2c.writeBytes(0x48, 0x01, data)
# Command to read the voltage value with two bytes 
data = i2c.readBytes(0x48, 0x00, 2)
# Converting the MSB
ads=data[0]*256
# Adding the LSB
raw_adc = ads + data[1]

# Those equations were gotten by a Calibration proccess. 
# ADC vs Voltage
if ((raw_adc>60000) and (raw_adc<65480)):
	a=raw_adc*0.0001;
	if(raw_adc<61000):
		a=0
		if (a==0):
			v=0
		else:
			v=(a-7.01)
			v=abs(v)
	
elif (raw_adc>1300 and raw_adc<10000):
	a=0.0001*raw_adc
	v=a+0.7135

elif(raw_adc>10000 and raw_adc <21500):
	a=0.0001*raw_adc
	v=a+0.6505;
	
elif (raw_adc>100 and raw_adc<1301):
	a=raw_adc*0.0001
	v=a+0.6403

elif (raw_adc>10500 and raw_adc<58999):
	a=raw_adc*0.0000006
	v=a+0.6284;
		
if(v>1.6):
	v=v+0.42
if(v>3.15):
	v=3.28

v=round(v,2);
print(v)
