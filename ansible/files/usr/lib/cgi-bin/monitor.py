#!/usr/bin/env python

import sqlite3
import os
import time
import glob

# global variables
dbname='/var/www/templog.db'

# store the temperature in the database
def log_temperature(temp,w1id):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    curs.execute("INSERT INTO temps values(datetime('now','localtime'), (?),(?))", (temp,w1id))

    # commit the changes
    conn.commit()

    conn.close()

# display the contents of the database
def display_data():

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    for row in curs.execute("SELECT * FROM temps"):
        print str(row[0])+"	"+str(row[1])

    conn.close()

# get temerature
# returns None on error, or the temperature as a float
def get_temp(devicefile):

    try:
        fileobj = open(devicefile,'r')
        lines = fileobj.readlines()
        fileobj.close()
    except:
        return None

    # get the status from the end of line 1 
    status = lines[0][-4:-1]

    # is the status is ok, get the temperature from line 2
    if status=="YES":
        #print status
        tempstr= lines[1][-6:-1]
        tempvalue=float(tempstr)/1000
        #print tempvalue
        return tempvalue
    else:
        #print "There was an error."
        return None



# main function
# This is where the program starts 
def main():

    # enable kernel modules
    os.system('sudo modprobe w1-gpio')
    os.system('sudo modprobe w1-therm')

    # search for a device file that starts with 28
    devicelist = glob.glob('/sys/bus/w1/devices/28*')
    
    if devicelist=='':
        #print ("No device to probe.")
        return None
    else:
        # append /w1slave to the device file
        for i in devicelist:
            w1devicefile = i + '/w1_slave'
            #print ("this is "+w1devicefile[-24:-9])
            temperature = get_temp(w1devicefile)
            if temperature != None:
                log_temperature(temperature,w1devicefile[-24:-9])
            else:
                temperature = get_temp(w1devicefile)
                log_temperature(temperature,w1devicefile[-24:-9])
            
if __name__=="__main__":
    main()




