import subprocess as sp
import re
import time

while True:
    accuracy = 3
    pshellcomm = ['powershell']
    pshellcomm.append('add-type -assemblyname system.device; ' \
                      '$loc = new-object system.device.location.geocoordinatewatcher;' \
                      '$loc.start(); ' \
                      'while(($loc.status -ne "Ready") -and ($loc.permission -ne "Denied")) ' \
                      '{start-sleep -milliseconds 100}; ' \
                      '$acc = %d; ' \
                      'while($loc.position.location.horizontalaccuracy -gt $acc) ' \
                      '{start-sleep -milliseconds 100; $acc = [math]::Round($acc*1.5)}; ' \
                      '$loc.position.location.latitude; ' \
                      '$loc.position.location.longitude; ' \
                      '$loc.position.location.horizontalaccuracy; ' \
                      '$loc.stop()' % (accuracy))

    p = sp.Popen(pshellcomm, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.STDOUT, text=True)
    (out, err) = p.communicate()
    out = out.split('\n')

    lat = float(out[0])
    long = float(out[1])
    print(lat, long)
    collect_data = {'longitude': long, 'latitude': lat}
    time.sleep(10)