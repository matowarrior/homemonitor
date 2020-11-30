from influxdb import InfluxDBClient
from ruuvitag_sensor.ruuvi import RuuviTagSensor
import time
import argparse

parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
parser.add_argument('macaddr')
parser.add_argument('location')
parser.add_argument('cred')
args =  parser.parse_args(['@args.txt'])

macs = args.macaddr.split(",")
locations= args.location.split(",")
creds = args.cred.split(",")

#Get broadcast data
timeout_in_sec = 15
datas = RuuviTagSensor.get_data_for_sensors(macs, timeout_in_sec)
sensor1 = None
sensor2 = None
sensor3 = None
#print("Raw data")
#print(datas[macs[0]])
#print(datas[macs[1]])
#print(datas[macs[2]])
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
timestamp = time.time_ns()
json_body = []
i = -1
for sensor in [sensor1, sensor2, sensor3]:
    i+=1
    if sensor is None:
        continue
    json_body.append(
    {
        "measurement": "ruuvitag",
        "tags": {
            "mac": sensor["mac"],
            "location":locations[i]
        },
        "time": timestamp,
        "fields": {
            "humidity": sensor["humidity"], "temperature": sensor["temperature"],
            "pressure": sensor["pressure"], "battery": sensor["battery"]
        }
    }
    )

client = InfluxDBClient('localhost', 8086, creds[0], creds[1], 'mydb')
client.write_points(json_body)
