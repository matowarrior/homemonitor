# homemonitor
Monitor RuuviTag sensors on a Raspberry Pi, write broadcasted data to InfluxDB and graph it with Grafana. Raspberry Pi OS all the packages described below have been installed in December 2020. Easiest way to get InfluxDB and Grafafa is to use the [IOTstack](https://github.com/SensorsIot/IOTstack) project.

### Raspberry Pi
This project is running on a 8GB Raspberry Pi 4 with the standard Raspberry Pi OS. More information on setting up the [Raspberry Pi](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up).

### RuuviTag
Install the RuuviTag and InfluxDB python packages and the required bluetooth tool.
```sh
pip3 install --user ruuvitag-sensor
sudo apt-get install bluez-hcidump && echo +++ install successful +++
pip3 install influxdb-client[ciso]
```
Testing can be done with the included command line utility.
```sh
python3 /home/pi/.local/lib/python3.7/site-packages/ruuvitag_sensor --help
```
More information from [RuuviTag](https://github.com/ttu/ruuvitag-sensor) github page.

### IOTStack
IOTstack has great documentation on how to [get started](https://sensorsiot.github.io/IOTstack/Getting-Started/) and the different containers. Install IOTStack and when asked install docker and reboot.
```sh
curl -fsSL https://raw.githubusercontent.com/SensorsIot/IOTstack/master/install.sh | bash
```
Use the ./menu.sh script from IOTstack folder to install the containers. In this case select InfluxDB, Grafana and portainer-ce. Once the installation is complete start the containers with the command
```sh
docker-compose up -d
```
Running InfluxDB in a container means we need to launch the CLI to create our database from portainer ce. First time using portainer ce select connection method "Manage the local Docker environment". Use a browser to connect to your Raspberry Pi on port 9000.
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
More information on getting started with [InfluxDB](https://docs.influxdata.com/influxdb/v1.8/introduction/get-started/)

### Running ruuviinfluxdb.py
Start data collecting so we have something to graph in the next step. args.text holds the RuuviTag sensors MAC addresses and locations. Code waits for 15 seconds to receive broadcast data and is set to run once every minute with crontab. Edit crontab
```sh
crontab -e
```
Add the following line
```sh
*/1 * * * * python3 /home/pi/ruuviinfluxdb.py
```

### Grafana
Use a browser to connect to your Raspberry Pi on port 3000. From the main page add a Datasource.
* Datasource select InfluxDB
* URL: http://yourIP:8086/
* Fill influxdb details: mydb
  
To graph data create a dashboard and a new panel to query the data you want.
##### Temperatue query example.
![Temperature query](https://github.com/matowarrior/homemonitor/blob/main/screenshots/Query.png)
More information on how to use [Grafana](https://grafana.com/docs/grafana/latest/datasources/influxdb/) with InfluxDB.

