from splunk_http_event_collector import http_event_collector 
import json
import bme680
import time

print("""read-all.py - Displays temperature, pressure, humidity, and gas.

Press Ctrl+C to exit!

""")

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except IOError:
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

# These calibration data can safely be commented
# out, if desired.

print('Calibration data:')
for name in dir(sensor.calibration_data):

    if not name.startswith('_'):
        value = getattr(sensor.calibration_data, name)

        if isinstance(value, int):
            print('{}: {}'.format(name, value))

# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

print('\n\nInitial reading:')
for name in dir(sensor.data):
    value = getattr(sensor.data, name)

    if not name.startswith('_'):
        print('{}: {}'.format(name, value))

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)




# Create event collector object, default SSL and HTTP Event Collector Port
http_event_collector_key = "c0a9a81c-8c39-4c47-bc5f-7cc4366826c8"
http_event_collector_host = "splunk-dev.dv-aws.uk"

testevent = http_event_collector(http_event_collector_key, http_event_collector_host)
testevent.popNullFields = False


# Start event payload and add the metadata information



payload = {}
payload.update({"index":"pi_test_metrics"})
payload.update({"sourcetype":"bme680_test"})
payload.update({"source":"wonderfulDayForPie"})
payload.update({"host":"Testing-Sensor"})

payload0 = {}
payload0.update({"index":"pi_test_metrics"})
payload0.update({"sourcetype":"bme680_test"})
payload0.update({"source":"wonderfulDayForPie"})
payload0.update({"host":"Testing-Sensor"})

payload1 = {}
payload1.update({"index":"pi_test_metrics"})
payload1.update({"sourcetype":"bme680_test"})
payload1.update({"source":"wonderfulDayForPie"})
payload1.update({"host":"Testing-Sensor"})

payload2 = {}
payload2.update({"index":"pi_test_metrics"})
payload2.update({"sourcetype":"bme680_test"})
payload2.update({"source":"wonderfulDayForPie"})
payload2.update({"host":"Testing-Sensor"})

payload3 = {}
payload3.update({"index":"pi_test_metrics"})
payload3.update({"sourcetype":"bme680_test"})
payload3.update({"source":"wonderfulDayForPie"})
payload3.update({"host":"Testing-Sensor"})


event={"sensor":"bme680", "room":"spare_room", "metric_name":"placeholder"}
event0={"sensor":"bme680", "room":"spare_room", "metric_name":"temperature"}
event1={"sensor":"bme680", "room":"spare_room", "metric_name":"pressure"}
event2={"sensor":"bme680", "room":"spare_room", "metric_name":"humidity"}
event3={"sensor":"bme680", "room":"spare_room", "metric_name":"gas_resistence"}


# Up to 10 heater profiles can be configured, each
# with their own temperature and duration.
# sensor.set_gas_heater_profile(200, 150, nb_profile=1)
# sensor.select_gas_heater_profile(1)

print('\n\nPolling:')
try:
    while True:
        epoch_time=time.time()
        if sensor.get_sensor_data():
            output = '{0:.2f} C,{1:.2f} hPa,{2:.2f} %RH'.format(
                sensor.data.temperature,
                sensor.data.pressure,
                sensor.data.humidity)

            event.update({"_value":sensor.data.temperature, "metric_name":"temperature"})
            payload.update({"time":epoch_time, "fields":event})
            testevent.batchEvent(payload)
            
            event.update({"_value":sensor.data.pressure, "metric_name":"pressure"})
            payload.update({"time":epoch_time, "fields":event})
            testevent.batchEvent(payload)
            
            event.update({"_value":sensor.data.humidity, "metric_name":"humidity"})
            payload.update({"time":epoch_time, "fields":event})
            testevent.batchEvent(payload)
            

            if sensor.data.heat_stable:
#                print('{0},{1} Ohms'.format(
#                    output,
#                    sensor.data.gas_resistance))
#                event3.update({"_value":sensor.data.gas_resistance})
                resistance=sensor.data.gas_resistance
                event.update({"_value":sensor.data.gas_resistance, "metric_name":"gas_resistance"})
                payload.update({"time":epoch_time, "fields":event})
                testevent.batchEvent(payload)
#                print(sensor.data.gas_resistance)

#            else:
#                print(output)

# #        print(event)
#         payload0.update({"time":epoch_time, "fields":event0})
# #        print(payload0)
#         testevent.sendEvent(payload0)
# #        del payload0["time"]
        
#         payload1.update({"time":epoch_time, "fields":event1})
# #        print(payload1)
#         testevent.sendEvent(payload1)
# #        del payload1["time"]
        
#         payload2.update({"time":epoch_time, "fields":event2})
# #        print(payload2)
#         testevent.sendEvent(payload2)
# #        del payload2["time"]
        
#         payload3.update({"time":epoch_time, "fields":event3})
# #        print(payload3)
#         testevent.sendEvent(payload3)
# #        del payload3["time"]

        testevent.flushBatch()        
        time.sleep(5)

except KeyboardInterrupt:
    pass
