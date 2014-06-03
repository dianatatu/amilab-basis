import kestrel
import json

c = kestrel.Client(['localhost:22133'])

json_data = open('/home/diana/ami/amilab-basis/test/measurements_sample.json')
message = json.load(json_data)
from nose.tools import set_trace; set_trace()
c.add('measurements', json.dumps(message))
