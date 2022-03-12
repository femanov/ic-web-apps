#!/usr/bin/env python3

from acc_db.db import AccConfig
from srv_config import SrvConfig
from srv_mirror import SrvMirrorConfig

db = AccConfig()

# software servers:
print('CXv4 software servers db-based config generator')

db.execute('select id from namesys where soft order by name')
srv_ids = db.cur.fetchall()

# creating servers
srvs = {sid[0]: SrvConfig(sid[0], db) for sid in srv_ids}

# generating servers configs
for sid in srvs:
    srvs[sid].save2file()


db.execute('select id,source_id from srvmirror')
mir_ids = db.cur.fetchall()

srv_mirrors = {}
for mid in mir_ids:
    m_id, source_id = mid
    if source_id in srvs:
        srv_mirrors[m_id] = SrvMirrorConfig(m_id, db, src_srv=srvs[source_id])
    else:
        srv_mirrors[m_id] = SrvMirrorConfig(m_id, db, src_id=source_id)





