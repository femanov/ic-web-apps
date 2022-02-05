#!/usr/bin/env python3

from acc_db.db import AccConfig
from srv_config import SrvConfig

db = AccConfig()

# software servers:
print('CXv4 software servers db-based config generator')

db.execute('select id from namesys where soft order by name')
srvs = db.cur.fetchall()

print('printing by cls --------')
for srv in srvs:
    s = SrvConfig(srv[0], db)

print('------------------------')



