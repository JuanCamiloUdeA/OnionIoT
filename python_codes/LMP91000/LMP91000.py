from OmegaExpansion import AdcExp
from OmegaExpansion import onionI2C
import time 

#i2c initialization 
i2c = onionI2C.OnionI2C()


LMP91000_STATUS_REG=(0x00)    
LMP91000_LOCK_REG=(0x01)    
LMP91000_TIACN_REG=(0x10)    
LMP91000_REFCN_REG=(0x11)    
LMP91000_MODECN_REG=(0x12)    

# LOCK register bitfield definition
LMP91000_WRITE_LOCK=(0x01) 
LMP91000_WRITE_UNLOCK=(0x00)

# STATUS register bitfield definition
LMP91000_READY=(0x01)
LMP91000_NOT_READY=(0x00)

#TIACN register bitfield definition
LMP91000_TIA_GAIN_EXT=(0x00) 
LMP91000_TIA_GAIN_2P75K=(0x04)
LMP91000_TIA_GAIN_3P5K=(0x08)
LMP91000_TIA_GAIN_7K=(0x0C)
LMP91000_TIA_GAIN_14K=(0x10) 
LMP91000_TIA_GAIN_35K=(0x14)
LMP91000_TIA_GAIN_120K=(0x18)
LMP91000_TIA_GAIN_350K=(0x1C)
LMP91000_RLOAD_10OHM=(0x00)        
LMP91000_RLOAD_33OHM=(0x01)
LMP91000_RLOAD_50OHM=(0x02)
LMP91000_RLOAD_100OHM=(0x03) 

#REFCN register bitfield definition
LMP91000_REF_SOURCE_INT=(0x00) 
LMP91000_REF_SOURCE_EXT=(0x80) 
LMP91000_INT_Z_20PCT=(0x00)
LMP91000_INT_Z_50PCT=(0x20)
LMP91000_INT_Z_67PCT=(0x40)
LMP91000_INT_Z_BYPASS=(0x60)
LMP91000_BIAS_SIGN_NEG=(0x00)
LMP91000_BIAS_SIGN_POS=(0x10)
LMP91000_BIAS_0PCT=(0x00)
LMP91000_BIAS_1PCT=(0x01) 
LMP91000_BIAS_2PCT=(0x02) 
LMP91000_BIAS_4PCT=(0x03) 
LMP91000_BIAS_6PCT=(0x04) 
LMP91000_BIAS_8PCT=(0x05) 
LMP91000_BIAS_10PCT=(0x06) 
LMP91000_BIAS_12PCT=(0x07) 
LMP91000_BIAS_14PCT=(0x08) 
LMP91000_BIAS_16PCT=(0x09) 
LMP91000_BIAS_18PCT=(0x0A) 
LMP91000_BIAS_20PCT=(0x0B) 
LMP91000_BIAS_22PCT=(0x0C) 
LMP91000_BIAS_24PCT=(0x0D) 

#MODECN register bitfield definition
LMP91000_FET_SHORT_DISABLED=(0x00)
LMP91000_FET_SHORT_ENABLED=(0x80)
LMP91000_OP_MODE_DEEP_SLEEP=(0x00) 
LMP91000_OP_MODE_GALVANIC=(0x01)
LMP91000_OP_MODE_STANDBY=(0x02)
LMP91000_OP_MODE_AMPEROMETRIC=(0x03)
LMP91000_OP_MODE_TIA_OFF=(0x06)
LMP91000_OP_MODE_TIA_ON=(0x07)

''' Functions inputs
'''
# First configure 
a=(LMP91000_TIA_GAIN_3P5K | LMP91000_RLOAD_100OHM)
b=(LMP91000_REF_SOURCE_INT | LMP91000_INT_Z_50PCT | 0x00 | LMP91000_BIAS_0PCT)
c=(LMP91000_FET_SHORT_DISABLED | LMP91000_OP_MODE_AMPEROMETRIC)

# Second 
b1=(LMP91000_REF_SOURCE_INT | LMP91000_INT_Z_50PCT | 0x00 | 6)
b2=(LMP91000_REF_SOURCE_INT | LMP91000_INT_Z_50PCT | 0x00 | 5)
b3=(LMP91000_REF_SOURCE_INT | LMP91000_INT_Z_50PCT | 0x00 | 4)
b4=(LMP91000_REF_SOURCE_INT | LMP91000_INT_Z_50PCT | 0x00 | 3)
b5=(LMP91000_REF_SOURCE_INT | LMP91000_INT_Z_50PCT | 0x00 | 2)
b6=(LMP91000_REF_SOURCE_INT | LMP91000_INT_Z_50PCT | 0x00 | 0)

# Third
b00=(LMP91000_REF_SOURCE_INT | LMP91000_INT_Z_50PCT | 0x10 | 0)
b11=(LMP91000_REF_SOURCE_INT | LMP91000_INT_Z_50PCT | 0x10 | 2)
b22=(LMP91000_REF_SOURCE_INT | LMP91000_INT_Z_50PCT | 0x10 | 3)
b33=(LMP91000_REF_SOURCE_INT | LMP91000_INT_Z_50PCT | 0x10 | 4)
b44=(LMP91000_REF_SOURCE_INT | LMP91000_INT_Z_50PCT | 0x10 | 5)
b55=(LMP91000_REF_SOURCE_INT | LMP91000_INT_Z_50PCT | 0x10 | 6)
b66=(LMP91000_REF_SOURCE_INT | LMP91000_INT_Z_50PCT | 0x10 | 7)
b77=(LMP91000_REF_SOURCE_INT | LMP91000_INT_Z_50PCT | 0x10 | 8)
b88=(LMP91000_REF_SOURCE_INT | LMP91000_INT_Z_50PCT | 0x10 | 9)
b99=(LMP91000_REF_SOURCE_INT | LMP91000_INT_Z_50PCT | 0x10 | 10)
b100=(LMP91000_REF_SOURCE_INT | LMP91000_INT_Z_50PCT | 0x10 | 11)

ScanRate=10

ScanNumber=0
NumberOfScans=1


''' Functions
'''
# Voltage to ADC 
def adcval(x):
	adc = AdcExp.AdcExp()
	volts=adc.read_voltage(x)
	volts=round(volts,2)
	raw_adc=(4095*volts)/(3.3)
	if raw_adc>4095:
		raw_adc=4095
	raw_adc=int(raw_adc)
	return raw_adc

def configure(a,b,c):
	data=i2c.readBytes(0x48,LMP91000_STATUS_REG,1)
	status=data[0]
	time.sleep(0.010)
	if(status==0x01):
		#unlock
		i2c.writeByte(0x48,LMP91000_LOCK_REG,LMP91000_WRITE_UNLOCK)
		time.sleep(0.010)
		#Commands 
		i2c.writeByte(0x48,LMP91000_TIACN_REG,a)
		time.sleep(0.010)
		i2c.writeByte(0x48,LMP91000_REFCN_REG,b)
		time.sleep(0.010)
		i2c.writeByte(0x48,LMP91000_MODECN_REG,c)
		time.sleep(0.010)
		#Lock
		i2c.writeByte(0x48,LMP91000_LOCK_REG,LMP91000_WRITE_LOCK)
		time.sleep(0.010)
		
while(ScanNumber<NumberOfScans):
	print('Initializing......')
	configure(a,b,c)
	time.sleep(10)
	print('Start..')
	# First loop
	for i in range(6,-1,-1):
		if(i != 1):
			if(i==6):
				configure(a,b1,c)
			elif(i==5):
				configure(a,b2,c)
			elif(i==4):
				configure(a,b3,c)
			elif(i==3):
				configure(a,b4,c)
			elif(i==2):
				configure(a,b5,c)
			elif(i==0):
				configure(a,b6,c)
			time.sleep(ScanRate)
			print(adcval(0))

	# Second loop
	for i in range(1,12,1):
		if(i != 1):
			if(i==2):
				configure(a,b11,c)
			elif(i==3):
				configure(a,b22,c)
			elif(i==4):
				configure(a,b33,c)
			elif(i==5):
				configure(a,b44,c)
			elif(i==6):
				configure(a,b55,c)
			elif(i==7):
				configure(a,b66,c)
			elif(i==8):
				configure(a,b77,c)
			elif(i==9):
				configure(a,b88,c)
			elif(i==10):
				configure(a,b99,c)
			elif(i==11):	
				configure(a,b100,c)
			time.sleep(ScanRate)
			print(adcval(0))

	# Third loop
	for i in range(10,-1,-1):
		if(i != 1):
			if(i==10):
				configure(a,b99,c)
			elif(i==9):
				configure(a,b88,c)
			elif(i==8):
				configure(a,b77,c)
			elif(i==7):
				configure(a,b66,c)
			elif(i==6):
				configure(a,b55,c)
			elif(i==5):
				configure(a,b44,c)
			elif(i==4):
				configure(a,b33,c)
			elif(i==3):
				configure(a,b22,c)
			elif(i==2):
				configure(a,b11,c)
			elif(i==0):
				configure(a,b00,c)
			time.sleep(ScanRate)
			print(adcval(0))

	# Last loop
	for i in range(2,7,1):
		if(i==2):
			configure(a,b5,c)
		elif(i==3):
			configure(a,b4,c)
		elif(i==4):
			configure(a,b3,c)
		elif(i==5):
			configure(a,b2,c)
		elif(i==6):
			configure(a,b1,c)
		time.sleep(ScanRate)
		print(adcval(0))

	ScanNumber=ScanNumber+1
	print('ScanNumber')
	print(ScanNumber)
	print('Complete')