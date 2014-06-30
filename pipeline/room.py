from collections import deque
import time

from core import PDU
from lib.log import setup_logging


class Room(PDU):
    QUEUE = 'room'

    def process_message(self, message):
        """
        Message sample:
        {
            'interval': ... ,
            'timezone_history': ... ,
            'bodystates': ... ,
            'starttime': ... ,
            'endtime': ... ,
            'metrics': {
                'skin_temp': ... ,
                'gsr': ... ,
                'calories': ... ,
                'steps': ... ,
                'air_temp': {
                    'min': ... ,
                    'max': ... ,
                    'sum': ... ,
                    'summary': ... ,
                    'values': ... ,
                    'stdev': ... ,
                    'avg': ...
                }
                'heartrate' : {
                    'min': ... ,
                    'max': ... ,
                    'sum': ... ,
                    'summary': ... ,
                    'values': ... ,
                    'stdev': ... ,
                    'avg': ...
                }
            }
        }
        """
        event = None
        self.logger.info("Received %r message." % message['type'])
	
        if message['type'] != 'basis':
            return

	hr = message.get('metrics', {}).get('heartrate', {}).get('values')
        if not hr:
            return
 
        if not event:
            return

        # Send heart rate event to email sender
        message = {
            'type': 'HR_ASC' # or 'HR_DESC'
        }
        self.send_to('email-sender', message)


if __name__ == "__main__":
    setup_logging()
    module = Router()
    module.run()
