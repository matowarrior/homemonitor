# homemonitor
Monitor RuuviTag sensors on a Raspberry Pi, write broadcasted data to InfluxDB and graph it with Grafana. Raspberry Pi OS all the packages described below have been installed in November 2020.

### Raspberry Pi
This project is running on a 8GB Raspberry Pi 4 with the standard Raspberry Pi OS. More information on setting up the [Raspberry Pi](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up).

### RuuviTag
Install the RuuviTag python package and the required bluetooth tool.
```sh
pip3 install --user ruuvitag-sensor
sudo apt-get install bluez-hcidump && echo +++ install successful +++
```
Testing can be done with the included command line utility.
```sh
python3 /home/pi/.local/lib/python3.7/site-packages/ruuvitag_sensor --help
```
More information from [RuuviTag](https://github.com/ttu/ruuvitag-sensor) github page.

### InfluxDB
Installing from repo got version 1.6.4
```sh
sudo apt install influxdb
sudo apt install influxdb-client
pip3 install influxdb
service influxdb start
```
Start InfluxDB CLI
```sh
influx
```
Create database called mydb and exit.
```sh
create database mydb
exit
```
This is the only configuration needed for InfluxDB.
More information on getting started with [InfluxDB](https://docs.influxdata.com/influxdb/v1.6/introduction/getting-started/)

### Running ruuviinfluxdb.py
Start data collecting so we have something to graph in the next step. args.text holds the RuuviTag sensors MAC addresses and locations as well as the InfluxDB credentials. Code waits for 15 seconds to receive broadcast data and is set to run once every minute with crontab. Edit crontab
```sh
crontab -e
```
Add the following line
```sh
*/1 * * * * python3 /home/pi/ruuviinfluxdb.py
```

### Grafana
Installing Grafana
```sh
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
sudo apt install -y grafana
sudo /bin/systemctl enable grafana-server
sudo /bin/systemctl start grafana-server
```
To access the data add InfluxDB as a data source (Side menu -> Configuration -> Data Sources). With Influx version 1.6.4, choose type InfluxQL. To graph data create a dashboard and a new panel to query the data you want.
##### Temperatue query example.
![Temperature query](https://github.com/matowarrior/homemonitor/blob/main/screenshots/Query.png)
More information on how to use [Grafana](https://grafana.com/docs/grafana/latest/datasources/influxdb/) with InfluxDB.

