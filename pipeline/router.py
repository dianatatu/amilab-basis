import time

from core import PDU
from lib.log import setup_logging

class Router(PDU):
    QUEUE = 'measurements'

    def process_message(self, message):
        self.logger.info("Received %r message." % message['type'])

        # Route messages towards mongo-writer.
        # created_at should be normally set as close to the data generation
        # as possible and should be the timestamp that the measurement
        # was physically generated. Since this is not always possible, the
        # default is the time of entry in the pipeline.
        message['created_at'] = message.get('created_at', int(time.time()))
        self.send_to('mongo-writer', message)

        # Send to Dashboard module only if it's a Kinect RGB image.
        if (message['sensor_type'] == 'kinect' and
            message['type'] in ['image_rgb', 'skeleton']):
                self.send_to('dashboard', message)

if __name__ == "__main__":
    setup_logging()
    module = Router()
    module.run()
