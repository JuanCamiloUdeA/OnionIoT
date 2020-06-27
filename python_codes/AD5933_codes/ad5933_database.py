from OmegaExpansion import onionI2C
import time 
import datetime
import math
import MySQLdb


conn= MySQLdb.connect(
        host='127.0.0.1',
        user='root',
        passwd='purdue',
        db ='flexilab',
        )
cur = conn.cursor()
 
# Initializing the variables  
i2c = onionI2C.OnionI2C()
''' Arrow to switch between the temperature and the impedance mesaurement 
a=1 Impedance
a=2 Temperature 
a=3 Exit
'''
z=1
# Defining the registers and the initial values 

SLAVE_ADDRESS=0x0D
CTRL_REG=0x80
CTRL_REG2=0x81

ADDR_PTR=0xB0

START_FREQ_R1=0x82
START_FREQ_R2=0x83
START_FREQ_R3 =0x84

FREG_INCRE_R1=0x85
FREG_INCRE_R2=0x86
FREG_INCRE_R3=0x87

NUM_INCRE_R1=0x88
NUM_INCRE_R2=0x89

NUM_SCYCLES_R1=0x8A
NUM_SCYCLES_R2=0x8B

RE_DATA_R1=0x94
RE_DATA_R2=0x95

IMG_DATA_R1=0x96
IMG_DATA_R2=0x97


STATUS_REG=0x8F
DELAY=0.010
DELAY2=0.001

#Defining constants 
MCLK=(16.776)*(10**6);
start_freq=(2)*(10**3);
incre_freq=(1)*(10**3);
incre_num=35;

# Function to compute the 2's complement 
def convb(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    if(val<0):
    	val+1
    return val

def temp():
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


# Function number 1
def getFrequency(freq,MCLK,n):
	if(n==1):
		val=((freq/(MCLK/4.0))*(2**27))
		val=int(val)
		val=val >>0x10
		val=val & 0xFF
	elif(n==2):
		val=((freq/(MCLK/4.0))*(2**27))
		val=int(val)
		val=val >>0x08
		val=val & 0xFF
	elif(n==3):
		val=((freq/(MCLK/4.0))*(2**27))
		val=int(val)
		val=val & 0xFF
		
	return val 
	
	

# Function number 2
def programReg():
	# Set Range 1, PGA gain 1
	i2c.writeByte(SLAVE_ADDRESS,CTRL_REG,0x01)
	time.sleep(DELAY2)
	# Set settling cycles
	i2c.writeByte(SLAVE_ADDRESS,NUM_SCYCLES_R1,0x07)
	time.sleep(DELAY2)
	i2c.writeByte(SLAVE_ADDRESS,NUM_SCYCLES_R2, 0xFF)
	time.sleep(DELAY2)
	#Start frequency of 1kHz
	a1=getFrequency(start_freq,MCLK,1)
	a2=getFrequency(start_freq,MCLK,2)
	a3=getFrequency(start_freq,MCLK,3)
	#Start frequency of 1kHz
	i2c.writeByte(SLAVE_ADDRESS,START_FREQ_R1,a1)
	time.sleep(DELAY2)
	i2c.writeByte(SLAVE_ADDRESS,START_FREQ_R2,a2)
	time.sleep(DELAY2)
	i2c.writeByte(SLAVE_ADDRESS,START_FREQ_R3,a3)
	b1=getFrequency(incre_freq,MCLK,1)
	b2=getFrequency(incre_freq,MCLK,2)
	b3=getFrequency(incre_freq,MCLK,3)
	#Increment by 1 Khz
	i2c.writeByte(SLAVE_ADDRESS,FREG_INCRE_R1,b1)
	time.sleep(DELAY2)
	i2c.writeByte(SLAVE_ADDRESS,FREG_INCRE_R2,b2)
	time.sleep(DELAY2)
	i2c.writeByte(SLAVE_ADDRESS,FREG_INCRE_R3,b3)
	time.sleep(DELAY2)
	#Points in Frequency sweep(100), max 511
	c1=incre_num & 0x001F00
	c1=c1>>0x08
	c2=incre_num & 0x0000FF
	#Points in Frequency sweep(100), max 511
	i2c.writeByte(SLAVE_ADDRESS,NUM_INCRE_R1,c1)
	time.sleep(DELAY2)
	i2c.writeByte(SLAVE_ADDRESS,NUM_INCRE_R2,c2)

def initial():
	# Setting up and reseting the device
	i2c.writeByte(SLAVE_ADDRESS,CTRL_REG,0x0)
	time.sleep(DELAY)
	i2c.writeByte(SLAVE_ADDRESS,CTRL_REG2,0x10)
	time.sleep(DELAY)
	conn= MySQLdb.connect(
        host='127.0.0.1',
        user='root',
        passwd='flexilab',
        db ='flexilab',
        )
	cur = conn.cursor()
	programReg()
	

initial()
time.sleep(1)

def runsweep():
	re=0;
	img=0;
	freq=0;
	mag=0;
	phase=0;
	gain=0;
	Impedance=0;
	GF=0;
	FFW=0;
	wt=0;
	BF=0;
	totmag = 0;
	count = 0;
	avgmag=0;
	totimp = 0;	
	avgimp=0;
	i= 0;
	Resistance=0;
	Reactance=0;
	# Getting the values in order to begin to sweep
	data=i2c.readBytes(SLAVE_ADDRESS,CTRL_REG,1)
	data=data[0]
	data=((data & 0x07)|(0xB0))
	i2c.writeByte(SLAVE_ADDRESS,CTRL_REG,data)
	time.sleep(DELAY)
	data2=i2c.readBytes(SLAVE_ADDRESS,CTRL_REG,1)
	data2=data2[0]
	data2=((data2 & 0x07)|(0x10))
	i2c.writeByte(SLAVE_ADDRESS,CTRL_REG,data2)
	time.sleep(DELAY)
	data3=i2c.readBytes(SLAVE_ADDRESS,CTRL_REG,1)
	data3=data3[0]
	data3=((data3 & 0x07)|(0x20))
	i2c.writeByte(SLAVE_ADDRESS,CTRL_REG,data3)
	time.sleep(DELAY)
	# Standby 10110000 Mask D8-10 avoid tampering with gains 
	
	# Initialize sweep

	# Start Sweep
	
	status=i2c.readBytes(SLAVE_ADDRESS,STATUS_REG,1)
	status=status[0]
	status=status & 0x07
	time.sleep(0.100)
	while (status<4):
		status=i2c.readBytes(SLAVE_ADDRESS,STATUS_REG,1)
		status=status[0]
		status=status & 0x07
		time.sleep(0.100)
		status2=i2c.readBytes(SLAVE_ADDRESS,STATUS_REG,1)
		arrow=status2[0]
		arrow=arrow & 2
		if (arrow==2):
			time.sleep(0.050)
			R1=i2c.readBytes(SLAVE_ADDRESS,RE_DATA_R1,1)
			time.sleep(0.050)
			R1=R1[0]
			R2=i2c.readBytes(SLAVE_ADDRESS,RE_DATA_R2,1)
			R2=R2[0]
			R1=R1<<8
			re1=(R1)|(R2)
			if(re1<32767):
				re=re1
			else:
				re=convb(re1,16)
			time.sleep(0.050)
			R1=i2c.readBytes(SLAVE_ADDRESS,IMG_DATA_R1,1)
			time.sleep(0.050)
			R2=i2c.readBytes(SLAVE_ADDRESS,IMG_DATA_R2,1)
			R1=(R1[0]<<8)
			R2=R2[0]
			img1=(R1)|(R2)
			if(img1<32767):
				img=img1
			else:
				img=convb(img1,16)
			freq=(i*incre_freq)+(start_freq)
			re2=re*re
			img2=img*img
			mag=re2+img2
			mag=(mag**0.5)
			totmag=totmag + mag 
			count=count+1
			
			# Calibrations
			# First one
			#GF=(((116.582)*(10**-11))+((202.841)*(10**-18)*(freq-start_freq)))
			# 10 KiloOhmns 10 to 50 kHz
			GF=(((5.15114)*(10**-9))+((7.83149)*(10**-16)*(freq-start_freq)))
			# 20 KiloOhmns with 10 KiloOhms to reference 
			
			
			Impedance=(1)/(GF*mag);
			
			totimp=totimp+Impedance;
			
			img=img*1.00
			re=re*1.00
			phase=math.atan(img/re)
			phase=math.degrees(phase)
			phase=round(phase,2)
			
			img=int(img)
			re=int(re)
			
			Resistance=(1)/(GF*re)
			Reactance=(1)/(GF*img)
			freqs=freq/1000
			Impedances=Impedance/1000
			print "Frequency in kHz : %.2f %%" %freqs
			print "Magnitude : %.2f %%" %mag
			print "Impedance in Ohmns : %.2f %%" %Impedances
			print "Phase in degrees : %.2f %%" %phase
			currentDT = datetime.datetime.now()
			sqli="INSERT INTO `data_ad5933` (`Frequency`,`Magnitude`,`Impedance`,`Phase`,`Resistance`,`Reactance`,`time`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
			args=(freqs,mag,Impedances,phase,Resistance,Reactance,currentDT)
			cur.execute(sqli,args)
			time.sleep(DELAY)
			
			status3=i2c.readBytes(SLAVE_ADDRESS,STATUS_REG,1)
			time.sleep(DELAY2)
			status3=status3[0]
			status3=(status3 & 0x07)
			if (status3<4):
				status4=i2c.readBytes(SLAVE_ADDRESS,CTRL_REG,1)
				status4=status4[0]
				status4=status4 & 0x07
				status4=status4 |0x30
				i2c.writeByte(SLAVE_ADDRESS,CTRL_REG,status4)
				time.sleep(0.200)
				i=i+1
			avgmag=totmag/count
			avgimp=totimp/count
			
	
	status5=i2c.readBytes(SLAVE_ADDRESS,CTRL_REG,1)
	status5=status5[0]
	status5=status5 & 0x07
	status5=status5 | 0xA0
	avgmag=round(avgmag,2)
	avgimp=avgimp/1000
	avgimp=round(avgimp,2)
	print "Average of Magnitude: %.2f %%" %avgmag
	print "Average of Impedance : %.2f %%" %avgimp
	time.sleep(DELAY)
	i2c.writeByte(SLAVE_ADDRESS,CTRL_REG,status5)
	time.sleep(DELAY2)
	
	
	


while(z==1):
	a=input('What do you want to see \n1.Impedance \n2.Temperatue \n3.Exit\n')
	if(a==1):
		initial()
		time.sleep(0.100)
		runsweep()
	elif(a==2):
		initial()
		time.sleep(0.100)
		temp()
	elif(a==3):
		z=2
		cur.close()