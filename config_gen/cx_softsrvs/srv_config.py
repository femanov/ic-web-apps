from devtype import DevType
from bridge import Bridge
import os
import sys


class SrvConfig:
    def __init__(self, sid, db):
        self.sid = sid
        self.db = db
        db.execute('select name,def_soft from namesys where id=%s', (sid,))
        row = db.cur.fetchall()[0]
        self.name = row[0]
        self.def_soft = row[1]
        self.fname = self.name.replace(':', '_')
        self.brgs = self.bridges()
        self.dt_ids = self.devtype_ids()
        self.dts = self.create_dts()
        self.devs = self.devs_of_srv()

    def create_devs_dir(self):
        dirName = f"./types/{self.fname}"
        if not os.path.exists(dirName):
            os.mkdir(dirName)
            print("Directory ", dirName, " Created ")
        else:
            print("Directory ", dirName, " already exists")

    def bridges(self):
        db = self.db
        db.execute('select bridge.id from bridge where namesys_id=%s', (self.sid,))
        br_ids = db.cur.fetchall()
        return [Bridge(x[0], self.db) for x in br_ids]

    def devtype_ids(self):
        db = self.db
        db.execute('select distinct array_agg(devtype.id order by devtype.id) '
                   ' from dev_devtype, devtype, dev, namesys where dev_devtype.devtype_id=devtype.id and devtype.soft'
                   ' and dev_devtype.dev_id=dev.id and dev.namesys_id=namesys.id and namesys.soft and namesys.id=%s'
                   ' group by dev_devtype.dev_id', (self.sid,))
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
        return [DevType(x, self.db) for x in self.dt_ids]

    def devs_of_srv(self):
        db = self.db
        db.execute('select dev.id,dev.name,array_agg(devtype.id order by devtype.id)'
                   ' from dev_devtype,devtype,dev,namesys where dev.id=dev_devtype.dev_id and dev_devtype.devtype_id=devtype.id'
                   ' and devtype.soft and dev.namesys_id=namesys.id and namesys.id=%s'
                   ' group by dev.id order by dev.ord', (self.sid,))
        devs = db.cur.fetchall()
        if self.def_soft:
            # devices for default soft server, aka extensions
            db.execute('select dev.id,dev.name,array_agg(devtype.id order by devtype.id)'
                       ' from dev_devtype,devtype,dev,namesys where dev.id=dev_devtype.dev_id and dev_devtype.devtype_id=devtype.id'
                       ' and devtype.soft and dev.namesys_id=namesys.id and not namesys.soft'
                       ' group by dev.id order by dev.ord')
            devs = devs + db.cur.fetchall()
        return devs

    def save2file(self):
        conf_file = open(f'devlist-{self.fname}.lst', 'w')
        # need to check if ./types exists
        dirName = f"./types/{self.fname}"
        if not os.path.exists(dirName):
            os.mkdir(dirName)
            print("Directory ", dirName, " Created ")
        else:
            print("Directory ", dirName, " already exists")

        for x in self.dts:
            dt_file = x.save2file(dirName)
            conf_file.write(f'include({dt_file})\n')

        # devices
        for x in self.devs:
            ind = self.dt_ids.index(x[2])
            # need to check for points in dev name
            if '.' in x[1]:
                dev_name = x[1].replace('.', '_')
                conf_file.write(f'dev {dev_name} {self.dts[ind].name}/noop ~ -\n')
                conf_file.write(f'cpoint {x[1]} {dev_name}\n')
            else:
                conf_file.write(f'dev {x[1]} {self.dts[ind].name}/noop ~ -\n')

        # bridged devices
        for b in self.brgs:
            ro = '!' if b.readonly else ''
            upd = '' if b.on_update else '~'
            for d in b.devs:
                ind = self.dt_ids.index(d[2])
                if '.' in d[1]:
                    dev_name = d[1].replace('.', '_')
                    conf_file.write(f'dev {dev_name} {ro}{self.dts[ind].name}/bridge ~ - @*{upd}:{d[3]}.{d[1]}\n')
                    conf_file.write(f'cpoint {d[1]} {dev_name}s\n')
                else:
                    conf_file.write(f'dev {d[1]} {ro}{self.dts[ind].name}/bridge ~ - @*{upd}:{d[3]}.{d[1]}\n')

        conf_file.close()
