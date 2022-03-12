
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


class DevType:
    def __init__(self, ids, db):
        self.ids = ids
        self.db = db
        db.execute('select name from devtype WHERE id=ANY(%s)', (ids,))
        names = db.cur.fetchall()
        self.name = '_'.join([y[0] for y in names])
        self.chan_groups = self.get_chan_groups()

    def get_chan_groups(self):
        # may be better use select distinct
        db = self.db
        db.execute('select array_agg(chan.name),array_agg(chan.units),chan.dtype,chan.dsize'
                   ' from devtype_chans,chan'
                   ' where devtype_chans.devtype_id=any(%s) and devtype_chans.chan_id=chan.id'
                   ' group by chan.dtype,chan.dsize'
                   ' order by chan.dtype,chan.dsize', (self.ids,))
        return db.cur.fetchall()

    def save2file(self, path):
        filename = f"{path}/{self.name}.devtype"
        dt_file = open(filename, 'w')
        chan_data = []
        chan_strs = []
        c_ind = 0
        for cg in self.chan_groups:
            chan_data.append(f'w{len(cg[0])}{dtypes[cg[2]]}{cg[3]}')
            for l_ind in range(len(cg[0])):
                cstr = f'{cg[0][l_ind]} {c_ind}'
                params = []
                if cg[1][l_ind] != '':
                    params.append('units:' + cg[1][l_ind])
                if len(params) > 0:
                    cstr += ' ' + ' '.join(params)
                chan_strs.append(cstr)
                c_ind += 1

        dt_str = f'devtype {self.name} ' + ','.join(chan_data) + ' {\n' + '\n'.join(chan_strs) + '\n}\n\n'

        dt_file.write(dt_str)
        dt_file.close()
        return filename
