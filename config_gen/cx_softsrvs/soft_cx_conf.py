#!/usr/bin/env python3

from acc_db.db import AccConfig
import os
import sys


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


class DevType:
    def __init__(self, ids):
        self.ids = ids
        db.execute('select name from devtype WHERE id=ANY(%s)', (ids,))
        names = db.cur.fetchall()
        self.name = '_'.join([y[0] for y in names])
        self.chan_groups = self.get_chan_groups()

    def get_chan_groups(self):
        # may be better use select distinct
        db.execute('select array_agg(chan.name),array_agg(chan.units),chan.dtype,chan.dsize'
                   ' from devtype_chans,chan'
                   ' where devtype_chans.devtype_id=any(%s) and devtype_chans.chan_id=chan.id'
                   ' group by chan.dtype,chan.dsize'
                   ' order by chan.dtype,chan.dsize', (self.ids,))
        return db.cur.fetchall()

    def save2file(self, dir):
        dt_file = open(dir + "/" + self.name + ".devtype", 'w')
        chan_data = []
        chan_strs = []
        c_ind = 0
        for cg in self.chan_groups:
            chan_data.append('w%d%s%d' % (len(cg[0]), dtypes[cg[2]], cg[3]))
            for l_ind in range(len(cg[0])):
                cstr = cg[0][l_ind] + ' ' + str(c_ind)
                params = []
                if cg[1][l_ind] != '':
                    params.append('units:' + cg[1][l_ind])
                if len(params) > 0:
                    cstr +=' ' + ' '.join(params)
                chan_strs.append(cstr)
                c_ind += 1

        dt_str = 'devtype ' + self.name + ' ' + ','.join(chan_data) + ' {\n' + '\n'.join(chan_strs) + '\n}\n\n'

        dt_file.write(dt_str)
        dt_file.close()


class Bridge:
    def __init__(self, id):
        self.id = id
        db.execute('select name,readonly,on_update from bridge WHERE id=%s', (id,))
        self.name,self.readonly,self.on_update = db.cur.fetchall()[0]
        self.dt_ids = self.devtypes()
        self.devs = self.devs_info()

    def devtypes(self):
        db.execute('select distinct array_agg(devtype.id order by devtype.id) from dev_devtype, devtype, dev,'
                   ' bridge_devs where dev_devtype.devtype_id=devtype.id and dev_devtype.dev_id=dev.id'
                   ' and dev.id=bridge_devs.dev_id and bridge_devs.bridge_id=%s group by dev_devtype.dev_id ', (self.id,))
        ret = db.cur.fetchall()
        return [x[0] for x in ret]

    def devs_info(self):
        db.execute('select dev.id,dev.name, array_agg(devtype.id order by devtype.id),namesys.name '
                   'from bridge_devs,dev,dev_devtype,devtype,namesys where bridge_devs.bridge_id=%s '
                   'and dev_devtype.devtype_id=devtype.id and dev_devtype.dev_id=dev.id and '
                   'bridge_devs.dev_id=dev.id and dev.namesys_id=namesys.id group by dev.id,namesys.name',
                   (self.id,))
        return db.cur.fetchall()


class SrvConfig:
    def __init__(self, id):
        self.id = id
        db.execute('select name,def_soft from namesys where id=%s', (id,))
        row = db.cur.fetchall()[0]
        self.name = row[0]
        self.def_soft = row[1]
        print(self.name, self.def_soft)
        self.brgs = self.bridges()
        self.dt_ids = self.devtype_ids()
        print(self.dt_ids)
        self.dts = self.create_dts()
        self.devs = self.devs_of_srv()
        self.save2file()

    def create_devs_dir(self):
        dirName = "./types/" + srv[1].replace(':', '_')
        if not os.path.exists(dirName):
            os.mkdir(dirName)
            print("Directory ", dirName, " Created ")
        else:
            print("Directory ", dirName, " already exists")

    def bridges(self):
        db.execute('select bridge.id from bridge where namesys_id=%s', (self.id,))
        br_ids = db.cur.fetchall()
        return [Bridge(x[0]) for x in br_ids]

    def devtype_ids(self):
        db.execute('select distinct array_agg(devtype.id order by devtype.id) '
                   ' from dev_devtype, devtype, dev, namesys where dev_devtype.devtype_id=devtype.id and devtype.soft'
                   ' and dev_devtype.dev_id=dev.id and dev.namesys_id=namesys.id and namesys.soft and namesys.id=%s'
                   ' group by dev_devtype.dev_id', (self.id,))
        dts = db.cur.fetchall()
        if self.def_soft:
            db.execute(
                'select distinct array_agg(devtype.id order by devtype.id)'
                ' from dev_devtype, devtype, dev, namesys where dev_devtype.devtype_id=devtype.id and devtype.soft'
                ' and dev_devtype.dev_id=dev.id and dev.namesys_id=namesys.id and not namesys.soft'
                ' group by dev_devtype.dev_id')
            exts = db.cur.fetchall()
            dts = dts + exts

        ids = [x[0] for x in dts]

        for b in self.brgs:
            ids.extend(b.dt_ids)
        # there can be dublicates, which will cause bad cx-server config
        return ids

    def create_dts(self):
        return [DevType(x) for x in self.dt_ids]

    def devs_of_srv(self):
        db.execute('select dev.id,dev.name,array_agg(devtype.id order by devtype.id)'
                   ' from dev_devtype,devtype,dev,namesys where dev.id=dev_devtype.dev_id and dev_devtype.devtype_id=devtype.id'
                   ' and devtype.soft and dev.namesys_id=namesys.id and namesys.id=%s'
                   ' group by dev.id order by dev.ord', (self.id,))
        devs = db.cur.fetchall()
        if self.def_soft:
            print('adding extension')
            db.execute('select dev.id,dev.name,array_agg(devtype.id order by devtype.id)'
                       ' from dev_devtype,devtype,dev,namesys where dev.id=dev_devtype.dev_id and dev_devtype.devtype_id=devtype.id'
                       ' and devtype.soft and dev.namesys_id=namesys.id and not namesys.soft'
                       ' group by dev.id order by dev.ord')
            devs = devs + db.cur.fetchall()
        return devs

    def save2file(self):
        srv_str = self.name.replace(':', '-')
        conf_file = open('devlist-' + srv_str + '.lst', 'w')

        dirName = "./types/" + srv_str
        if not os.path.exists(dirName):
            os.mkdir(dirName)
            print("Directory ", dirName, " Created ")
        else:
            print("Directory ", dirName, " already exists")
        for x in self.dts:
            x.save2file(dirName)
            conf_file.write('include(' + dirName + '/' + x.name + '.devtype)\n')

        # devices
        for x in self.devs:
            ind = self.dt_ids.index(x[2])
            # need to check for points in dev name
            if '.' in x[1]:
                dev_name = x[1].replace('.', '_')
                conf_file.write('dev %s %s/noop ~ -\n' % (dev_name, self.dts[ind].name))
                conf_file.write('cpoint %s %s\n' % (x[1], dev_name))
            else:
                conf_file.write('dev %s %s/noop ~ -\n' % (x[1], self.dts[ind].name))

        # dridged devices
        for b in self.brgs:
            ro = '!' if b.readonly else ''
            upd = '' if b.on_update else '~'
            for d in b.devs:
                ind = self.dt_ids.index(d[2])
                if '.' in d[1]:
                    dev_name = d[1].replace('.', '_')
                    conf_file.write('dev ' + dev_name + ' ' + ro + self.dts[ind].name +  '/bridge ~ - @*' + upd + ':'
                                    + d[3] + '.' + d[1] + '\n')
                    conf_file.write('cpoint %s %s\n' % (d[1], dev_name))
                else:
                    conf_file.write('dev ' + d[1] + ' ' + ro + self.dts[ind].name +  '/bridge ~ - @*' + upd + ':'
                                    + d[3] + '.' + d[1] + '\n')

        conf_file.close()

# software servers:
print('CXv4 software servers db-based config generator')

db.execute('select id, name, info from namesys where soft order by name')
srvs = db.cur.fetchall()

print('printing by cls --------')
for srv in srvs:
    s = SrvConfig(srv[0])

print('------------------------')

