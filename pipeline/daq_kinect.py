import json

from core import PDU
from lib.log import setup_logging

class DAQKinect(PDU):
    QUEUE = 'daq-kinect'
    EXPERIMENT_FILE = '/home/diana/ami/amilab-basis/test/daq-kinect-sample.txt'

    def process_message(self, message):
        if message.get('start', False) is True:
            # Read messages from recorded experiment and forward them to Router.
            with open(self.EXPERIMENT_FILE) as f:
                messages = f.readlines()
                for message in messages:
                    message = json.loads(message)
                    self.send_to('measurements', message)

if __name__ == "__main__":
    setup_logging()
    module = DAQKinect()
    module.run()
