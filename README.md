# homemonitor
Monitor RuuviTag sensors on a raspberry pi and write broadbasted data to InfluxDB. Raspberry Pi OS all the packages described below have been installed in November 2020.

### Raspberry Pi
This project is running on a 8GB Raspberry Pi 4 with the standard Raspberry Pi OS. More information on setting up the [Raspberry Pi](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up).

### RuuviTag
More information from [RuuviTag](https://github.com/ttu/ruuvitag-sensor) github page.
```sh
pip3 install --user ruuvitag-sensor
sudo apt-get install bluez-hcidump && echo +++ install successful +++
python3 /home/pi/.local/lib/python3.7/site-packages/ruuvitag_sensor --help
```
### InfluxDB
Installing from repo got version 1.6.4
```sh
sudo apt install influxdb
sudo apt install influxdb-client
pip3 install influxdb
```

### Grafana
```sh
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
sudo apt install -y grafana
sudo /bin/systemctl enable grafana-server
sudo /bin/systemctl start grafana-server
```
More information on how to use [Grafana](https://grafana.com/docs/grafana/latest/datasources/influxdb/) with InfluxDB.
