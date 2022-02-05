

class Bridge:
    def __init__(self, id, db):
        self.id = id
        self.db = db
        db.execute('select name,readonly,on_update from bridge WHERE id=%s', (id,))
        self.name, self.readonly, self.on_update = db.cur.fetchall()[0]
        self.dt_ids = self.devtypes()
        self.devs = self.devs_info()

    def devtypes(self):
        db = self.db
        db.execute('select distinct array_agg(devtype.id order by devtype.id) from dev_devtype, devtype, dev,'
                   ' bridge_devs where dev_devtype.devtype_id=devtype.id and dev_devtype.dev_id=dev.id'
                   ' and dev.id=bridge_devs.dev_id and bridge_devs.bridge_id=%s group by dev_devtype.dev_id ', (self.id,))
        ret = db.cur.fetchall()
        return [x[0] for x in ret]

    def devs_info(self):
        db = self.db
        db.execute('select dev.id,dev.name, array_agg(devtype.id order by devtype.id),namesys.name '
                   'from bridge_devs,dev,dev_devtype,devtype,namesys where bridge_devs.bridge_id=%s '
                   'and dev_devtype.devtype_id=devtype.id and dev_devtype.dev_id=dev.id and '
                   'bridge_devs.dev_id=dev.id and dev.namesys_id=namesys.id group by dev.id,namesys.name',
                   (self.id,))
        return db.cur.fetchall()
