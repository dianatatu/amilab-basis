import json
import logging

from bottle import Bottle, run, static_file

from core import settings
from decorators import query_param
from lib.dashboard_cache import DashboardCache
from lib.log import setup_logging
from lib.session_store import SessionStore

logger = logging.getLogger(__name__)

app = Bottle()
dashboard_cache = DashboardCache()
session_store = SessionStore()

POSITIONS_LIMIT = 100

if getattr(settings, 'SERVE_DASHBOARD_VIA_API', False):
    @app.route('/static/<filepath:path>')
    def static_serve(filepath):
        return static_file(filepath, root=getattr(settings, 'STATIC_FILES_DIR', '.'))

@app.route('/latest_kinect_rgb/:sensor_id', method='GET')
def get_latest_kinect_rgb(sensor_id = 'daq-01'):
    try:
        result = dashboard_cache.get(sensor_id=sensor_id,
                                     sensor_type='kinect',
                                     measurement_type='image_rgb')
        return json.loads(result)
    except:
        logger.exception("Failed to get latest kinect RGB from Redis")
        return {}

@app.route('/latest_kinect_skeleton/:sensor_id', method='GET')
def get_latest_kinect_skeleton(sensor_id = 'daq-01'):
    try:
        result = dashboard_cache.get(sensor_id=sensor_id,
                                     sensor_type='kinect',
                                     measurement_type='skeleton')
        return json.loads(result)
    except:
        logger.exception("Failed to get latest kinect skeleton from Redis")
        return {}


@app.route('/latest_subject_positions/:sensor_id', method='GET')
def get_latest_subject_positions(sensor_id = 'daq-01'):
    try:
        result = dashboard_cache.lrange(sensor_id=sensor_id,
                                        sensor_type='kinect',
                                        measurement_type='subject_position',
                                        start=0,
                                        stop=POSITIONS_LIMIT)
        dashboard_cache.ltrim(sensor_id=sensor_id,
                              sensor_type='kinect',
                              measurement_type='subject_position',
                              start=0,
                              stop=POSITIONS_LIMIT)
        return {'data': result}

    except:
        logger.exception("Failed to get list of latest subject positions from "
                         "Redis")
        return {}


if __name__ == '__main__':
    setup_logging()
    params = {
        'host': '0.0.0.0',
        'port': 8000
    }
    #if getattr(settings, 'BOTTLE_BACKEND'):
    #    params['server'] = getattr(settings, 'BOTTLE_BACKEND')
    run(app, **params)
