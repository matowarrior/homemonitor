from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from ruuvitag_sensor.ruuvi import RuuviTagSensor
import argparse

database = "mydb"
parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
parser.add_argument('macaddr')
parser.add_argument('location')
args =  parser.parse_args(['@args.txt'])
macs = args.macaddr.split(",")
locations= args.location.split(",")
timeout_in_sec = 15

client = InfluxDBClient(url="http://localhost:8086", token="my-token", org="my-org")
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()


#Get broadcast data
datas = RuuviTagSensor.get_data_for_sensors(macs, timeout_in_sec)
sensor1 = None
sensor2 = None
sensor3 = None
print("Raw data")
print(datas[macs[0]])
print(datas[macs[1]])
print(datas[macs[2]])
try:
    sensor1 = datas[macs[0]]
except Exception:
    pass
try:
    sensor2 = datas[macs[1]]
except Exception:
    pass
try:
    sensor3 = datas[macs[2]]
except Exception:
    pass
i = -1
for sensor in [sensor1, sensor2, sensor3]:
    i+=1
    write_api.write(database, "my-org", {"measurement": "ruuvitag",
                                            "tags": {"location": locations[i],"mac": macs[i]},
                                            "fields": {"humidity": sensor["humidity"], "temperature": sensor["temperature"],
                                                       "pressure": sensor["pressure"], "battery": sensor["battery"]}})
