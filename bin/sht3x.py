from Adafruit_SHT31 import *

sensorIn = SHT31(address = 0x44)
sensorOut = SHT31(address = 0x45)

degreesIn = sensorIn.read_temperature()
humidityIn = sensorIn.read_humidity()

degreesOut = sensorOut.read_temperature()
humidityOut = sensorOut.read_humidity()

print('Temp OUT             = {0:0.1f} deg C'.format(degreesOut))
print('Humidity OUT        = {0:0.1f} %'.format(humidityOut))

print('Temp IN             = {0:0.1f} deg C'.format(degreesIn))
print('Humidity IN        = {0:0.1f} %'.format(humidityIn))
