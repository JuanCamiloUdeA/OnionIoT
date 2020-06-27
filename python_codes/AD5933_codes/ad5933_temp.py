from OmegaExpansion import onionI2C
import time 
 
# Initializing the variables  
i2c = onionI2C.OnionI2C()
SLAVE_ADDRESS=0x0D
CTRL_REG=0x80
CTRL_REG2=0x81
DELAY=0.010

# Setting up and reseting the device
i2c.writeByte(SLAVE_ADDRESS,CTRL_REG,0x0)
time.sleep(DELAY)

i2c.writeByte(SLAVE_ADDRESS,CTRL_REG2,0x10)
time.sleep(DELAY)

# Code to read the temperature from AD5933

i2c.writeByte(SLAVE_ADDRESS,CTRL_REG,0x90)
time.sleep(DELAY)
data = i2c.readBytes(0x0D,0x92,2)
data2= i2c.readBytes(0x0D,0x93,2)
temp1=(data[0])
temp1=temp1<<8;
temp1=temp1 & 0xFFFF
temp1 |= data2[0]
temp1 &= 0x3FFF;
temp1=int(temp1)
if (temp1 & 0x2000 == 1):
	temp1 -= 0x4000
temp1 /= 32.00;
temp1=round(temp1,2) 
temp2=(((temp1*9)/(5))+(32))
print "Temperature in Celsius : %.2f %%" %temp1
print "Temperature in Fahrenheit : %.2f %%" %temp2