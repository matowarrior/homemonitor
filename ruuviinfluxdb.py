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

sensors = {}
for sensor in range(len(macs)):
    sensors[macs[sensor]] = locations[sensor] 
print(sensors)

#Get broadcast data
datas = RuuviTagSensor.get_data_for_sensors(macs, timeout_in_sec)
print("Raw data")
for sensor in range(len(macs)):
    print(datas[macs[sensor]])

for k,v in sensors.items():
    try:
        write_api.write(database, "my-org", {"measurement": "ruuvitag",
                                            "tags": {"location": v,"mac": k},
                                            "fields": {"humidity": datas[k]["humidity"], "temperature": datas[k]["temperature"],
                                                       "pressure": datas[k]["pressure"], "battery": datas[k]["battery"]}})
    except:
        print(f"failed {v}")
