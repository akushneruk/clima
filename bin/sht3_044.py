from Adafruit_SHT31 import *

sensorIn = SHT31(address = 0x44)
sensorOut = SHT31(address = 0x45)

degreesIn = sensor.read_temperature()
humidityIn = sensor.read_humidity()

degreesOut = sensorOut.read_temperature()
humidityOut = sensorOut.read_humidity()

print('Temp IN             = {0:0.3f} deg C'.format(degreesOut))
print('Humidity OUT        = {0:0.2f} %'.format(humidityOut))

print('Temp IN             = {0:0.3f} deg C'.format(degreesIn))
print('Humidity OUT        = {0:0.2f} %'.format(humidityIn))