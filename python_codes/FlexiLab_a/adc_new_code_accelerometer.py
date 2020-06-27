# This file contains the steps in order to install ADC library on the Onion-Omega and the code to get a data and storage into a defined database 
# opkg install python python-adc-exp
import onionGpio
import time
import datetime
import MySQLdb
from OmegaExpansion import AdcExp
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
value=int(value)
adc = AdcExp.AdcExp()
z=1

while(z==1):
	value=ledon.getValue()
	value=int(value);
	if(value==1):
		volts=adc.read_voltage(1) # Using the A0 port of the ADC extension 
		currentDT = datetime.datetime.now()
		sqli="INSERT INTO `data_a` (`voltage`,`time`) VALUES (%s,%s)"
		args=(volts,currentDT)
		cur.execute(sqli,args)
		time.sleep(0.300);
		
	elif(value==0):
		z=2;
		cur.close()