# clima system monitoring for meet
### on Rasperberry Pi model 3



## Setup ENV

1.  
```bash
    sudo apt-get update && apt-get upgrade -y
```
2. Create new sudo  user and enable ssh service.
3. Enable i2c bus.

4. Setup serial for rpi. 
[Like this]                        :http://www.electronicwings.com/raspberry-pi/raspberry-pi-uart-communication-using-python-and-c

5.
```bash
    sudo apt-get install python3-pip
    sudo python3 -m pip install --upgrade pip setuptools wheel
```

6. 
```bash
    sudo pip3 install Adafruit_DHT
    sudo pip3 install Adafruit_SHT31
    sudo pip3 install Adafruit_GPIO
```
7. 