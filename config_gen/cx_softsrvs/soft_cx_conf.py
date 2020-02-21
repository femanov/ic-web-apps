#!/usr/bin/env python3

from acc_db.db import AccConfig
import os

print('CXv4 software servers db-based config generator')

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

db = AccConfig()

# software servers:
# extension devices - placed to default soft-server (first which has def_soft)
# others - as related in database

db.execute('select id,name from namesys where soft and def_soft limit 1')
ext_srv = db.cur.fetchall()[0]

print('extension devises server:', ext_srv)

# select servers from DB
#os.mkdir("./types")

db.execute('select id, name, info from namesys where soft order by name')
srvs = db.cur.fetchall()

for srv in srvs:
    print(srv)
    dirName = "./types/" + srv[1]
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory ", dirName, " Created ")
    else:
        print("Directory ", dirName, " already exists")

    db.execute('select distinct array_agg(devtype.id order by devtype.id) '
               ' from dev_devtype, devtype, dev, namesys where dev_devtype.devtype_id=devtype.id and devtype.soft'
               ' and dev_devtype.dev_id=dev.id and dev.namesys_id=namesys.id and namesys.soft and namesys.id=%s'
               ' group by dev_devtype.dev_id', (srv[0],))
    dts = db.cur.fetchall()
    if srv[0] == ext_srv[0]:
        db.execute(
            'select distinct array_agg(devtype.id order by devtype.id)'
            ' from dev_devtype, devtype, dev, namesys where dev_devtype.devtype_id=devtype.id and devtype.soft'
            ' and dev_devtype.dev_id=dev.id and dev.namesys_id=namesys.id and not namesys.soft'
            ' group by dev_devtype.dev_id')
        exts = db.cur.fetchall()
        dts = dts + exts

    dts = [x[0] for x in dts]
    print(dts)

    conf_file = open('devlist-' + srv[1].replace(':', '-') + '.lst', 'w')

    dt_names = []
    for x in dts:
        db.execute('select name from devtype WHERE id=ANY(%s)', (x,))
        names = db.cur.fetchall()
        db.conn.commit()
        dt_name = '_'.join([y[0] for y in names])
        dt_names.append(dt_name)

        dt_file = open(dirName + "/" + dt_name + ".devtype", 'w')

        # may be better use select distinct
        db.execute('select array_agg(chan.name),array_agg(chan.units),chan.dtype,chan.dsize'
                   ' from devtype_chans,chan'
                   ' where devtype_chans.devtype_id=any(%s) and devtype_chans.chan_id=chan.id'
                   ' group by chan.dtype,chan.dsize'
                   ' order by chan.dtype,chan.dsize', (x,))

        chans = db.cur.fetchall()
        db.conn.commit()

        chan_data = []
        chan_names = []
        c_ind = 0
        for cg in chans:
            chan_data.append('w%d%s%d' % (len(cg[0]), dtypes[cg[2]], cg[3]))
            for cn in cg[0]:
                chan_names.append('%s %d' % (cn, c_ind))
                c_ind += 1

        dt_str = 'devtype ' + dt_name + ' ' + ','.join(chan_data) + ' {\n' + '\n'.join(chan_names) + '\n}\n\n'

        dt_file.write(dt_str)
        dt_file.close()
        conf_file.write('include(' + dirName + '/' + dt_name + '.devtype)\n')

    db.execute('select dev.id,dev.name,array_agg(devtype.id order by devtype.id)'
               ' from dev_devtype,devtype,dev,namesys where dev.id=dev_devtype.dev_id and dev_devtype.devtype_id=devtype.id'
               ' and devtype.soft and dev.namesys_id=namesys.id and namesys.id=%s'
               ' group by dev.id order by dev.ord', (srv[0],))
    devs = db.cur.fetchall()

    if srv == ext_srv:
        print('adding extension')
        db.execute('select dev.id,dev.name,array_agg(devtype.id order by devtype.id)'
                   ' from dev_devtype,devtype,dev,namesys where dev.id=dev_devtype.dev_id and dev_devtype.devtype_id=devtype.id'
                   ' and devtype.soft and dev.namesys_id=namesys.id and not namesys.soft'
                   ' group by dev.id order by dev.ord')
        devs = devs + db.cur.fetchall()

    for x in devs:
        ind = dts.index(x[2])
        # need to check for points in dev name
        if '.' in x[1]:
            dev_name = x[1].replace('.', '_')
            conf_file.write('dev %s %s/noop ~ -\n' % (dev_name, dt_names[ind]))
            conf_file.write('cpoint %s %s\n' % (x[1], dev_name))
        else:
            conf_file.write('dev %s %s/noop ~ -\n' % (x[1], dt_names[ind]))

    if 'sys_devs' in srv[2]:
        if srv[2]['sys_devs']:
            print("server for system devices, generating...")
            db.execute('select name from sys')
            systems = db.cur.fetchall()
            for x in systems:
                dev_name = x[0].replace('.', '_')
                conf_file.write('dev systems_%s system/noop ~ -\n' % (dev_name, ))

    db.conn.commit()

    conf_file.close()

# update files to server