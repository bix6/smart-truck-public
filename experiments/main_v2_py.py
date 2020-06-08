import datetime
import requests

# Set a default in case the file is missing / corrupt.
truckId = -1

# Try to read the file & set the id of the truck from the file in /boot.
try:
    # This path will change to /boot/truckId on the Pi
    #f = open('/boot/truckId','r')
    f = open('truckId','r')
    tid = f.readline()
    f.close()

    # only set the ID if it's numeric
    if tid.isdigit():
        truckId = tid
except Exception as e:
    print('Warning! No Truck ID set!', e)
    pass


# Just for testing, switch to our own URL later.
url = 'http://httpbin.org/post'

units = 12.4012
unit_type = 'gallons'

lat = 37.414917
lng = -122.099426

payload = {
    'timestamp': datetime.datetime.utcnow().isoformat(),
    'units': units,
    'unit_type': unit_type,
    'latitude': lat,
    'longitude': lng,
    'truckId': truckId
}

r = requests.post(url, json=payload)

if r.status_code == requests.codes.ok:
    print(r.text)
else:
    print(r.raise_for_status())