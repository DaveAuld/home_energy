import threading
import time
import glob

def getCurrentTemp(sensorPath):
  #Return Variable
  SensorValue = ""

  #open the sensor file and read the contents then close the sensor file
  rawsensor = open(sensorPath + "/w1_slave")
  data = rawsensor.read()
  rawsensor.close() 

  #Check the first line ends in YES, this is CRC OK
  firstLine = str.split(data, "\n")[0]
  if (firstLine.endswith("YES")): 
    secondLine = str.split(data, "\n")[1]
    SensorValue = float(secondLine.split('t=')[1]) / 1000
  else:
    SensorValue = ":ERROR:"

  #Print the output
  return (str(SensorValue))

#Define a Temperature Sensor Object
class TemperatureSensor:
  def __init__(self,SensorIDPath):
    #Store the device path    
    self.SensorIDPath = SensorIDPath

    #Take the path and extract the ID
    self.SensorID = SensorIDPath.split("/")
    self.SensorID = self.SensorID[5]

  def snapshotValue(self):
    return getCurrentTemp(self.SensorIDPath)

  def snapshotRecord(self):
    return "123.123"

#Define a Temperature Sensor Reading Object
class TemperatureSensorReading():
  def __init__(self, SensorID, Timestamp, Value):
    self.SensorID = SensorID
    self.Timestamp = Timestamp
    self.Value = Value

#Set the devices folder location
DEVICESDIR = "/sys/bus/w1/devices/"

#Create a list of temperature devices found on the bus, these begin 28-
TemperatureSensorPathList = glob.glob(DEVICESDIR + "28-*")

#Iterate all the devices and add them to the sensor list
TemperatureSensorList = [];
for sensor in TemperatureSensorPathList:
  newSensor = TemperatureSensor(sensor)
  TemperatureSensorList.append(newSensor)  


print "Reading Temperature from " + str(len(TemperatureSensorList)) + " sensor(s)."

while 1==1:
  for sensor in TemperatureSensorList:
    print sensor.snapshotValue()
    print sensor.snapshotRecord()
    time.sleep(1)
