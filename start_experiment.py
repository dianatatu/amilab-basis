import kestrel
import json

c = kestrel.Client(['localhost:22133'])

message = json.dumps({'start': True})
c.add('daq-kinect', message)
#c.add('daq-basis', message)
