# CLIMA SYSTEM MONITORING for meat
#### on Rasperberry Pi model 3, nextion and python3

### Setup ENV

1. Fix locale and configure device (enable: ssh, i2c and serial)

2. Install Grafana
  1. Intall use [this](http://docs.grafana.org/installation/debian)
  2. Run Grafan using via systemd
    ```bash
        sudo systemctl daemon-reload
        sudo systemctl start grafana-server
        sudo systemctl status grafana-server
        sudo systemctl enable grafana-server.service
    ```
  3. Reboot and check

3. Install influxDB
    [InfluxDB](https://canox.net/2018/01/installation-von-grafana-influxdb-telegraf-auf-einem-raspberry-pi/)
    ```bash
        curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
        echo "deb https://repos.influxdata.com/debian stretch stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
        sudo apt update
        sudo apt install influxdb 
        sudo systemctl enable influxdb
        sudo systemctl start influxdb 
        influx
        CREATE USER admin WITH PASSWORD 'YOUR_PASSWORD' WITH ALL PRIVILEGES
        CREATE DATABASE clima
    ```
4.  Install pip and all needed dependency
    ```bash
        sudo apt-get install python3-pip
        sudo python3 -m pip install --upgrade pip setuptools wheel
        sudo pip3 install Adafruit_SHT31
        sudo pip3 install Adafruit_GPIO
        sudo pip3 install automationhat
        sudo pip3 install influxdb
        sudo pip3 install flask
        sudo pip3 install schedule
    ```
5. Install git and  clone repo
    ```bash
        sudo apt-get install git -y
        git clone https://github.com/akushneruk/clima.git
    ```
6. Install supervisor and import configs from ./supervisor_confgs. Check if status up and runnig !

# INFO
Relays:
GPIO 26 -- Lamp
GPIO 6 -- Ventilation
GPIO 13 -- Humidity