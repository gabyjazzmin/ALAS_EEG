# Using Hexiwear with Python
# Script to get the device data and append it to a file
# Usage
# python GetData.py <device>
# e.g. python GetData.py "00:29:40:08:00:01"
import pexpect
import time
import sys
import os
import json
import csv
import pandas as pd
from pandas.core.frame import DataFrame

# ---------------------------------------------------------------------
# function to transform hex string like "0a cd" into signed integer
# ---------------------------------------------------------------------
def hexStrToInt(hexstr):
    val = int(hexstr[0:2],16) + (int(hexstr[3:5],16)<<8)
    if ((val&0x8000)==0x8000): # treat signed 16bits
        val = -((val^0xffff)+1)
    return val
# ---------------------------------------------------------------------

parsed_to_json = []

DEVICE = "00:1F:50:04:00:0C" # hexiwear ALAS-Tecnologico de Monterrey

if len(sys.argv) == 2:
  DEVICE = str(sys.argv[1])

# Run gatttool interactively.
child = pexpect.spawn("gatttool -I")

# Connect to the device.
print("Connecting to:"),
print(DEVICE)

NOF_REMAINING_RETRY = 3

while True:
  try:
    child.sendline("connect {0}".format(DEVICE))
    child.expect("Connection successful", timeout=5)
  except pexpect.TIMEOUT:
    NOF_REMAINING_RETRY = NOF_REMAINING_RETRY-1
    if (NOF_REMAINING_RETRY>0):
      print ("timeout, retry...") 
      continue
    else:
      print ("timeout, giving up.")
      break
  else:
    print("Connected!")
    break

if NOF_REMAINING_RETRY>0:
  try:
    while(True):
      time.sleep(1) 
      unixTime = int(time.time())
      unixTime += 60*60 # GMT+1
      unixTime += 60*60 # added daylight saving time of one hour
  
#[{‘tiempo’: 0, ‘speed: 12’}, {‘tiempo’: 1, ’speed’: 67}] 
#parsed_to_json = [] 

  # open file
  #file = open("data.csv", "a")
  #if (os.path.getsize("data.csv")==0):
  #  file.write("Device\ttime\tAppMode\tBattery\tAmbient\tTemperature\tHumidity\tPressure\tHeartRate\tSteps\tCalorie\tAccX\tAccY\tAccZ\tGyroX\tGyroY\tGyroZ\tMagX\tMagY\tMagZ\n")
      file = open("./HexiWear/dataHexi.csv", "a")
      if (os.path.getsize("./HexiWear/dataHexi.csv",)==0):
        file.write("Time,Temperature,HeartRate\n")
      
  #file.write(DEVICE)
      #file.write('Time:')
      file.write(str(unixTime)) # Unix timestamp in seconds 
      file.write(",")

  # App mode
  #child.sendline("char-read-hnd 0x6d")
  #child.expect("Characteristic value/descriptor: ", timeout=5)
  #child.expect("\r\n", timeout=5)
  #print("AppMode:  "),
  #print(child.before),
  #print(str(int(child.before[0:2],16)))

  #file.write(str(int(child.before[0:2],16)))
  #file.write("\t")
  
  # Battery
  #child.sendline("char-read-hnd 0x28")
  #child.expect("Characteristic value/descriptor: ", timeout=5)
  #child.expect("\r\n", timeout=5)
  #print("Battery:  "),
  #print(child.before),
  #print(str(int(child.before[0:2],16)))

  #file.write(str(int(child.before[0:2],16)))
  #file.write("\t")
  
  # Ambient Light (0x2011)
  #child.sendline("char-read-hnd 0x3f")
  #child.expect("Characteristic value/descriptor: ", timeout=5)
  #child.expect("\r\n", timeout=5)
  #print("Ambient:  "),
  #print(child.before),
  #print(str(int(child.before[0:2],16)))

  #file.write(str(int(child.before[0:2],16)))
  #file.write("\t")

      #Temperature (0x2012)
      child.sendline("char-read-hnd 0x43")
      child.expect("Characteristic value/descriptor: ", timeout=5)
      child.expect("\r\n", timeout=5)
      print("Temperature:  "),
      print(child.before),
      print(float(hexStrToInt(child.before[0:5]))/100)
      #file.write('Temperature:')
      file.write(str(float(hexStrToInt(child.before[0:5]))/100))
      file.write(",")
 
  # Humidity (0x2013)
  #child.sendline("char-read-hnd 0x47")
  #child.expect("Characteristic value/descriptor: ", timeout=5)
  #child.expect("\r\n", timeout=5)
  #print("Humidity:  "),
  #print(child.before),
  #print(float(hexStrToInt(child.before[0:5]))/100)

  #file.write(str(float(hexStrToInt(child.before[0:5]))/100))
  #file.write("\t")

  # Pressure (0x2014)
  #child.sendline("char-read-hnd 0x4b")
  #child.expect("Characteristic value/descriptor: ", timeout=5)
  #child.expect("\r\n", timeout=5)
  #print("Pressure:  "),
  #print(child.before),
  #print(float(hexStrToInt(child.before[0:5]))/100)

  #file.write(str(float(hexStrToInt(child.before[0:5]))/100))
  #file.write("\t")

      #HeartRate (0x2021)
      child.sendline("char-read-hnd 0x52")
      child.expect("Characteristic value/descriptor: ", timeout=5)
      child.expect("\r\n", timeout=5)
      print('HeartRate:'),
      print(child.before),
      print(str(int(child.before[0:2],16)))
      #file.write('HeartRate:')
      file.write(str(int(child.before[0:2],16)))
      file.write(",")

      

  # Steps (0x2022)
  #child.sendline("char-read-hnd 0x56")
  #child.expect("Characteristic value/descriptor: ", timeout=5)
  #child.expect("\r\n", timeout=5)
  #print("Steps:  "),
  #print(child.before),
  #print(hexStrToInt(child.before[0:5]))

  #file.write(str(hexStrToInt(child.before[0:5])))
  #file.write("\t")

  # Calorie (0x2023)
  #child.sendline("char-read-hnd 0x5a")
  #child.expect("Characteristic value/descriptor: ", timeout=5)
  #child.expect("\r\n", timeout=5)
  #print("Calorie:  "),
  #print(child.before),
  #print(hexStrToInt(child.before[0:5]))

  #file.write(str(hexStrToInt(child.before[0:5])))
  #file.write("\t")

  # Accelerometer
      #child.sendline("char-read-hnd 0x30")
      #child.expect("Characteristic value/descriptor: ", timeout=5)
      #child.expect("\r\n", timeout=5)
      #print("Accel:  "),
      #print(child.before),
      #print(float(hexStrToInt(child.before[0:5]))/100),
      #print(float(hexStrToInt(child.before[6:11]))/100),
      #print(float(hexStrToInt(child.before[12:17]))/100)
      
      #file.write(str(float(hexStrToInt(child.before[0:5]))/100))
      #file.write(",")
      #file.write(str(float(hexStrToInt(child.before[6:11]))/100))
      #file.write(",")
      #file.write(str(float(hexStrToInt(child.before[12:17]))/100))
      #file.write(",")
  
  # Gyro
  #child.sendline("char-read-hnd 0x34")
  #child.expect("Characteristic value/descriptor: ", timeout=5)
  #child.expect("\r\n", timeout=10)
  #print("Gyro:   "),
  #print(child.before),
  #print(float(hexStrToInt(child.before[0:5]))/100),
  #print(float(hexStrToInt(child.before[6:11]))/100),
  #print(float(hexStrToInt(child.before[12:17]))/100)
  #file.write(str(float(hexStrToInt(child.before[0:5]))/100))
  #file.write("\t")
  #file.write(str(float(hexStrToInt(child.before[6:11]))/100))
  #file.write("\t")
  #file.write(str(float(hexStrToInt(child.before[12:17]))/100))
  #file.write("\t")
  
  # Magnetometer
  #child.sendline("char-read-hnd 0x38")
  #child.expect("Characteristic value/descriptor: ", timeout=5)
  #child.expect("\r\n", timeout=10)
  #print("Magneto:"),
  #print(child.before),
  #print(hexStrToInt(child.before[0:5])),
  #print(hexStrToInt(child.before[6:11])),
  #print(hexStrToInt(child.before[12:17]))

  #file.write(str(float(hexStrToInt(child.before[0:5]))/100))
  #file.write("\t")
  #file.write(str(float(hexStrToInt(child.before[6:11]))/100))
  #file.write("\t")
  #file.write(str(float(hexStrToInt(child.before[12:17]))/100))
  #file.write("\t")

      file.write("\n")
      file.close()

      
      #data = [{'Time': str(unixTime) , 'Temp': str(float(hexStrToInt(child.before[0:5]))/100), 'HeartRate':str(int(child.before[0:2],16))}]

      #with open("respuestaHexi.json", "w") as jsonfile:
       # datos = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '))
        #jsonfile.write(datos)
      #else:
          #data.insert(len(data), {'Time': str(unixTime) , 'Temp': str(float(hexStrToInt(child.before[0:5]))/100), 'HeartRate':str(int(child.before[0:2],16))})
          #with open("respuestaHexi.json", "w") as jsonfile:
            #datos = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '))
            #jsonfile.write(datos)

      print("Datos de hexiwear registrados!")
      #parsed_to_json.append({ 'Time': str(unixTime) , 'Temp': str(float(hexStrToInt(child.before[0:5]))/100), 'HeartRate':str(int(child.before[0:2],16))}) 
      
      #sys.exit(0)
    #else:
     # print("FAILED!")
      #sys.exit(-1)
  except KeyboardInterrupt: #Terminamos programa+Generamos JSON
    '''
    data = pd.read_csv('dataHexi.csv')
    df = DataFrame(data)
    df = df.to_dict()
    #leector de csv
    with open("hexi.json", 'a') as jsonfile:
      datos = json.dumps(df,indent=4, sort_keys=True, separators=(',', ': '))
      jsonfile.write(datos)
    '''

    #file = open("dataHexi.json", "a")
    #file.write('\n ]')
    #file.close()
    sys.exit(0)

'''

target=open("dataHexi.json", "w")
    for line in file:
      target.write(line[:-1]).rstrip(',')
    if(i == 1):
        data = [{'Time': 1, 'Pred': int(cants.argmax() + 1),
                 'Prob1': (cants[0]/cants.sum())*100,
                 'Prob2': (cants[1]/cants.sum())*100,
                 'Prob3': (cants[2]/cants.sum())*100}]

        with open("respuesta3.json", 'w') as jsonfile:
            datos = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '))
            jsonfile.write(datos)
    else:
        data.insert(len(data), {'Time': i, 'Pred':  int(cants.argmax() + 1),
                                'Prob1': (cants[0]/cants.sum())*100,
                                'Prob2': (cants[1]/cants.sum())*100,
                                'Prob3': (cants[2]/cants.sum())*100})
        with open('respuesta3.json', 'w') as jsonfile :
            datos = json.dumps(data, indent = 4, sort_keys = True, separators = (',', ': '))
            jsonfile.write(datos)
            '''
