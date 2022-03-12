import os

class SrvMirrorConfig:
    def __init__(self, smid, db, **kwargs):
        self.m_id = smid
        self.db = db
        db.execute("select name,on_update,readonly from srvmirror where id=%s", (self.m_id,))
        self.name, self.on_update, self.readonly = db.cur.fetchall()[0]
        self.fname = self.name.replace(':', '_')

        self.src_srv = kwargs.get('src_srv', None)
        print(f'mirror: {self.name} for server: {self.src_srv.name}')
        self.save2file()

    def save2file(self):
        conf_file = open(f'devlist-{self.fname}.lst', 'w')
        dirName = f"./types/{self.fname}"
        if not os.path.exists(dirName):
            os.mkdir(dirName)
            print("Directory ", dirName, " Created ")
        else:
            print("Directory ", dirName, " already exists")

        dts = self.src_srv.dts
        for x in dts:
            dt_file = x.save2file(dirName)
            conf_file.write(f'include({dt_file})\n')

        ro = '!' if self.readonly else ''
        upd = '' if self.on_update else '~'

        # devices
        devs = self.src_srv.devs
        dt_ids = self.src_srv.dt_ids
        for x in devs:
            ind = dt_ids.index(x[2])
            # need to check for points in dev name
            if '.' in x[1]:
                dev_name = x[1].replace('.', '_')
                #conf_file.write(f'dev {dev_name} {self.dts[ind].name}/noop ~ -\n')
                #conf_file.write(f'cpoint {x[1]} {dev_name}\n')
                conf_file.write(f'dev {dev_name} {ro}{dts[ind].name}/bridge ~ - @*{upd}:{self.src_srv.name}.{dev_name}\n')
                conf_file.write(f'cpoint {x[1]} {dev_name}s\n')
            else:
                #conf_file.write(f'dev {x[1]} {self.dts[ind].name}/noop ~ -\n')
                conf_file.write(f'dev {x[1]} {ro}{dts[ind].name}/bridge ~ - @*{upd}:{self.src_srv.name}.{x[1]}\n')

        # bridged devices
        brgs = self.src_srv.brgs
        for b in brgs:
            for d in b.devs:
                ind = dt_ids.index(d[2])
                if '.' in d[1]:
                    dev_name = d[1].replace('.', '_')
                    conf_file.write(f'dev {dev_name} {ro}{dts[ind].name}/bridge ~ - @*{upd}:{self.src_srv.name}.{d[1]}\n')
                    conf_file.write(f'cpoint {d[1]} {dev_name}s\n')
                else:
                    conf_file.write(f'dev {d[1]} {ro}{dts[ind].name}/bridge ~ - @*{upd}:{self.src_srv.name}.{d[1]}\n')

        conf_file.close()

