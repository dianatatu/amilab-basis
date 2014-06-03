KESTREL_SERVERS=['localhost:22133']
MONGO_SERVER='localhost:27017'
REDIS_SERVER='localhost'
REDIS_PORT=6379
REDIS_DASHBOARD_DB=0
REDIS_SESSION_DB=1
REDIS_PROCESSED_SESSION_DB=2

try:
    from settings_local import *
except:
    pass
