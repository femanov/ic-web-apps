#!/usr/bin/env python3

from acc_db.db import *

dtypes = {
    'int8':   'b',
    'int16':  'h',
    'int32':  'i',
    'int':    'i',
    'int64':  'q',
    'float':  's',
    'double': 'd',
    'text':   't',
    'utext':  'u',
    '':       'd',
}

ext_srv = 'cxhw:1'


db = acc_db()

# software servers located at ichw1-2,
# 0 - server for automatic control software
# 1 - extension devices - all soft devtypes with not soft server will be here
# 2 - balakin's data processing software

# in a DB level 'soft' is int field of devtype, if it's > 0 - it is a software devtype

# select servers from DB
db.execute('select id, name from namesys where soft=1')
srvs = db.cur.fetchall()
db.conn.commit()

for srv in srvs:
    print(srv)
    db.execute('select distinct dts from (select dev_devtype.dev_id, array_agg(devtype.id order by devtype.id) as dts'
        ' from dev_devtype, devtype, dev, namesys where dev_devtype.devtype_id=devtype.id and devtype.soft>0'
        ' and dev_devtype.dev_id=dev.id and dev.namesys_id=namesys.id and namesys.soft>0 and namesys.id=%s'
        ' group by dev_devtype.dev_id) as t1', (srv[0],))
    dts = db.cur.fetchall()
    if srv[1] == ext_srv:
        db.execute(
            'select distinct dts from (select dev_devtype.dev_id, array_agg(devtype.id order by devtype.id) as dts'
            ' from dev_devtype, devtype, dev, namesys where dev_devtype.devtype_id=devtype.id and devtype.soft>0'
            ' and dev_devtype.dev_id=dev.id and dev.namesys_id=namesys.id and namesys.soft=0'
            ' group by dev_devtype.dev_id) as t1')
        exts = db.cur.fetchall()
        dts = dts + exts
    dts = [x[0] for x in dts]
    db.conn.commit()
    print(dts)

    conf_file = open('devlist-' + srv[1].replace(':', '-') + '.lst', 'w')

    dt_names = []
    for x in dts:
        db.execute('select name from devtype WHERE id=ANY(%s)', (x,))
        names = db.cur.fetchall()
        db.conn.commit()
        dt_name = '_'.join([y[0] for y in names])
        dt_names.append(dt_name)

        # may be better use select distinct
        db.execute('select chan.id,chan.name,chan.dtype,chan.dsize,chan.units'
                   ' from devtype_chans,chan'
                   ' where devtype_chans.devtype_id=any(%s) and devtype_chans.chan_id=chan.id', (x,))
        chans = db.cur.fetchall()
        db.conn.commit()

        chan_data = []
        chan_names = []
        for y in range(len(chans)):
            c = chans[y]
            chan_data.append('w1%s%d' % (dtypes[c[2]], c[3]))
            chan_names.append('%s %d' % (c[1], y))

        dt_str = 'devtype ' + dt_name + ' ' + ','.join(chan_data) + ' {\n' + '\n'.join(chan_names) + '\n}\n\n'
        conf_file.write(dt_str)

    db.execute('select dev.id,dev.name,array_agg(devtype.id order by devtype.id)'
               ' from dev_devtype,devtype,dev,namesys where dev.id=dev_devtype.dev_id and dev_devtype.devtype_id=devtype.id'
               ' and devtype.soft>0 and dev.namesys_id=namesys.id and namesys.id=%s'
               ' group by dev.id order by dev.ord', (srv[0],))
    devs = db.cur.fetchall()

    if srv[1] == ext_srv:
        db.execute('select dev.id,dev.name,array_agg(devtype.id order by devtype.id)'
                   ' from dev_devtype,devtype,dev,namesys where dev.id=dev_devtype.dev_id and dev_devtype.devtype_id=devtype.id'
                   ' and devtype.soft>0 and dev.namesys_id=namesys.id and namesys.soft=0'
                   ' group by dev.id order by dev.ord')
        devs = devs + db.cur.fetchall()


    db.conn.commit()

    for x in devs:
        ind = dts.index(x[2])
        # need to check for points in dev name
        if '.' in x[1]:
            dev_name = x[1].replace('.', '_')
            conf_file.write('dev %s %s/noop ~ -\n' % (dev_name, dt_names[ind]))
            conf_file.write('cpoint %s %s\n' % (x[1], dev_name))
        else:
            conf_file.write('dev %s %s/noop ~ -\n' % (x[1], dt_names[ind]))

    conf_file.close()

# update files to server