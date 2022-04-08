
from accdb.models import Devtype, Chan


class SumDevtype:
    def __init__(self, dts):
        self.dts = dts
        self.name = "_".join([d.name for d in dts])
        self.driver = 'noop'
        if len(dts) == 1:
            if dts[0].driver != "":
                self.driver = dts[0].driver

    # almost the same code as in models definitions
    def cx_str(self):
        cs = Chan.objects.filter(devtype__in=self.dts)
        cgs = {}
        for x in cs:
            ts = x.cx_type_sig()
            if ts in cgs:
                cgs[ts].append(x)
            else:
                cgs[ts] = [x]
        cg_ts = [f"w{len(cgs[x])}{x}" for x in cgs]
        dt_strs = [f"devtype {self.name} {','.join(cg_ts)}{' {'}"]
        c_count = 0
        for x in cgs:
            for c in cgs[x]:
                dt_strs.append(c.cx_str_for_dt(c_count))
                c_count += 1
        dt_strs.append('}')
        return '\n'.join(dt_strs)

