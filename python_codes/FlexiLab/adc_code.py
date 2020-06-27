import onionGpio
import time
import datetime
import MySQLdb
from OmegaExpansion import onionI2C
# Database

conn= MySQLdb.connect(
        host='127.0.0.1',
        user='root',
        passwd='flexilab',
        db ='flexilab',
        )
cur = conn.cursor()

#Defining LED 
ledon=onionGpio.OnionGpio(19);
status=ledon.setInputDirection();
value=ledon.getValue()
value=int(value);
i2c = onionI2C.OnionI2C()
z=1

while(z==1):
	value=ledon.getValue()
	value=int(value);
	if(value==1):
	# Get I2C bus
		data = [0x84,0x83]
		i2c.writeBytes(0x48, 0x01, data)

#Time in miliseconds
#timestart=time.clock()*1000;

		#for x in range(0,50):
	
		data = i2c.readBytes(0x48, 0x00, 2)
		ads=data[0]*256
		raw_adc = ads + data[1]
	#time.sleep(0.03)
	
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

# Range from 2V to 3.3V
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
	#print(v)
	#time2=time.clock()*1000
	#t=(time2-timestart)
	#t=round(t,2)
	#print(t);
		currentDT = datetime.datetime.now()
		sqli="INSERT INTO `data` (`voltage`,`time`) VALUES (%s,%s)"
		args=(v,currentDT)
		cur.execute(sqli,args)
		time.sleep(0.350);
	

	elif(value==0):
		z=2;
		cur.close()
