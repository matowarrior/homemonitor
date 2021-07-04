# homemonitor
Monitor RuuviTag sensors on a Raspberry Pi, write broadcasted data to InfluxDB and graph it with Grafana. For Zigbee devices I use deconz. Raspberry Pi OS all the packages described below have been installed in March 2021. Easiest way to get InfluxDB and Grafafa is to use the [IOTstack](https://github.com/SensorsIot/IOTstack) project.

### Raspberry Pi
This project is running on a 8GB Raspberry Pi 4 with the standard Raspberry Pi OS. More information on setting up the [Raspberry Pi](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up).

### RuuviTag
Install the RuuviTag and InfluxDB python packages and the required bluetooth tool.
```sh
pip3 install --user ruuvitag-sensor
sudo apt-get install bluez-hcidump && echo +++ install successful +++
pip3 install influxdb-client[ciso]
```
ruuvitag-sensor 1.1.0 has requirement rx<3, but you'll have rx 3.1.1 which is incompatible. This can be ignored
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
Deconz needs to told the device so check it in advance with dmesg.
```sh
dmesg | grep tty
```
Use the
```sh
./menu.sh
```
 script from IOTstack folder to install the containers. In this case select InfluxDB, Grafana, portainer-ce and deconz. Once the installation is complete start the containers with the command
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
In the home folder clone this project.
```sh
git clone https://github.com/matowarrior/homemonitor.git
```
Start data collecting so we have something to graph in the next step. args.text holds the RuuviTag sensors MAC addresses and locations. Code waits for 15 seconds to receive broadcast data and is set to run once every minute with crontab. Edit crontab
```sh
crontab -e
```
Add the following line
```sh
*/1 * * * * cd /home/pi/homemonitor/ && python3 ruuviinfluxdb.py
```

### Grafana
Use a browser to connect to your Raspberry Pi on port 3000. Default credentials are admin,admin.From the main page add a Datasource.
* Datasource select InfluxDB
* URL: http://yourIP:8086/
* Fill influxdb details: mydb
  
To graph data create a dashboard and a new panel to query the data you want.
My [Grafana configuration](Grafana.md) is shown on its own page. More information on how to use [Grafana](https://grafana.com/docs/grafana/latest/datasources/influxdb/) with InfluxDB.

### Deconz & Zigbee
```sh
sudo usermod -a -G dialout pi
```
Phoscon UI http://your.local.ip.address:8090/
### Misc
From the IOTstack menu:
* Set swappines to 0
* install log to ram
```sh
sudo nano /etc/log2ram.conf
```
I have set the sizes to 140M and 200M. sudo nano /etc/logrotate.conf
rotate log files daily
daily
keep 2 days worth of backlogs
rotate 2
### DuckDNS
https://www.duckdns.org/
nano ~/IOTstack/duck/duck.sh
```sh
* */1 * * * sudo ~/IOTstack/duck/duck.sh >/dev/null 2>&1
```
### VPN
https://pivpn.io/
* curl -L https://install.pivpn.io | bash
* pivpn -a

### Dropbox
./menu.sh
Install Dropbox
sudo bash ./scripts/backup.sh 2 pi

### Syncthing
Local network backup with [Syncthing](https://syncthing.net/). Follow the installation guide. Run syncthing to generate config files.
```sh
syncthing
```
After syncthing has started press Ctrl + C to shut it down.

Update the address in the gui section with the Pi address to allow LAN GUI access.
```sh
nano ~/.config/syncthing/config.xml
```
Setup syncthing as a service
```sh
sudo nano /lib/systemd/system/syncthing.service
```
Copy contents from [Syncthing github](https://github.com/syncthing/syncthing/blob/main/etc/linux-systemd/system/syncthing%40.service)
Change the user to pi.
Enable service
```sh
sudo systemctl enable syncthing
```
File sharing configuration can now be done in the GUI.