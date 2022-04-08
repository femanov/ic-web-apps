#!/usr/bin/env python3

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")
django.setup()

from accdb.models import Namesys, Dev, Devtype, Bridge, SrvMirror

from devtype import SumDevtype

print('Generation config-files for CX-servers')

conf_dir = './configs'
dts_basedir = f"{conf_dir}/types"

# storage for host:[server-numbers]
cx_srvs = {}


def add_srv(namesys):
    cx_host = namesys.cx_host()
    srv_num = namesys.cx_srvnum()
    if cx_host in cx_srvs:
        if srv_num in cx_srvs[cx_host]:
            print("WARNING: few namespaces in the same cx-server. Case support not yet implemented")
        else:
            cx_srvs[cx_host].append(srv_num)
    else:
        cx_srvs[cx_host] = [srv_num]


soft_srvs = Namesys.objects.filter(soft=True)

for srv in soft_srvs:
    print(srv)
    add_srv(srv)

    fname = srv.name.replace(':', '-')
    srv_devs_dir = f"{dts_basedir}/{fname}"
    if not os.path.exists(srv_devs_dir):
        os.mkdir(srv_devs_dir)

    conf_file = open(f'{conf_dir}/devlist-{fname}.lst', 'w')

    # get regular devices of server
    devs = list(Dev.objects.filter(namesys=srv))
    dts = {}
    dev_dtns = {}
    for d in devs:
        dt = SumDevtype(Devtype.objects.filter(dev=d))
        dev_dtns[d.name] = dt.name
        if dt.name not in dts:
            dts[dt.name] = dt

    # get extension devices in case it's default software server
    if srv.def_soft:
        print('default software devices server, adding extension devs')
        ext_devs = [d for d in Dev.objects.filter(namesys__soft=False, devtype__soft=True)]
        for d in ext_devs:
            # extensions uses only software devtypes
            dt = SumDevtype(d.devtype.filter(soft=True))
            dev_dtns[d.name] = dt.name
            if dt.name not in dts:
                dts[dt.name] = dt
        devs += ext_devs

    # this will not work if bridging device from the same server, but not needed
    brgs = [b for b in Bridge.objects.filter(namesys=srv)]
    for b in brgs:
        print("bridge: ", b.name)
        for d in b.devs.all():
            dt = SumDevtype(Devtype.objects.filter(dev=d))
            dev_dtns[d.name] = dt.name
            if dt.name not in dts:
                dts[dt.name] = dt

    # generating devtype configs
    for dt_n in dts:
        with open(f"{srv_devs_dir}/{dt_n}.devtype", 'w') as f_dt:
            f_dt.write(dts[dt_n].cx_str())
        conf_file.write(f'include(./types/{fname}/{dt_n}.devtype)\n')

    # adding devices to server config
    for d in devs:
        dt_name = dev_dtns[d.name]
        dt = dts[dt_name]

        if '.' in d.name:
            dev_name = d.name.replace('.', '_')
            conf_file.write(f'dev {dev_name} {dt_name}/{dt.driver} ~ - {d.params}\n')
            conf_file.write(f'cpoint {d.name} {dev_name}\n')
        else:
            conf_file.write(f'dev {d.name} {dev_dtns[d.name]}/{dt.driver} ~ - {d.params}\n')

    # Bridge devices configuration
    for b in brgs:
        ro = '!' if b.readonly else ''
        upd = '' if b.on_update else '~'
        for d in b.devs.all():
            if '.' in d.name:
                dev_name = d.name.replace('.', '_')
                conf_file.write(f'dev {dev_name} {ro}{dev_dtns[d.name]}/bridge ~ - @*{upd}:{d.namesys.name}.{d.name}\n')
                conf_file.write(f'cpoint {d.name} {dev_name}\n')
            else:
                conf_file.write(f'dev {d.name} {ro}{dev_dtns[d.name]}/bridge ~ - @*{upd}:{d.namesys.name}.{d.name}\n')

    conf_file.close()


print("\ngenerating config files for mirror servers:")

# generate configs for full-server mirror
# really it's not full server, but namespace
s_mirrors = SrvMirror.objects.all()
for sm in s_mirrors:
    ro = '!' if sm.readonly else ''
    upd = '' if sm.on_update else '~'
    print(f'{sm.name}  src: {sm.source.name}')

    add_srv(sm)

    fname = sm.name.replace(':', '-')
    srv_devs_dir = f"{dts_basedir}/{fname}"
    if not os.path.exists(srv_devs_dir):
       os.mkdir(srv_devs_dir)

    conf_file = open(f'{conf_dir}/devlist-{fname}.lst', 'w')

    # get regular devices of server
    devs = [d for d in Dev.objects.filter(namesys=sm.source)]
    dts = {}
    dev_dtns = {}
    for d in devs:
        dt = SumDevtype(Devtype.objects.filter(dev=d))
        dev_dtns[d.name] = dt.name
        if dt.name not in dts:
            dts[dt.name] = dt

    # get extension devices in case it's default software server
    if sm.source.def_soft:
        ext_devs = [d for d in Dev.objects.filter(namesys__soft=False, devtype__soft=True)]
        for d in ext_devs:
            # extensions uses only software devtypes
            dt = SumDevtype(d.devtype.filter(soft=True))
            dev_dtns[d.name] = dt.name
            if dt.name not in dts:
                dts[dt.name] = dt
        devs += ext_devs

    # this will not work if bridging device from the same server, but not needed
    brgs = [b for b in Bridge.objects.filter(namesys=sm.source)]
    for b in brgs:
        print("bridge: ", b.name)
        brg_devs = [d for d in b.devs.all()]
        for d in brg_devs:
            dt = SumDevtype(d.devtype.all())
            dev_dtns[d.name] = dt.name
            if dt.name not in dts:
                dts[dt.name] = dt
        devs += brg_devs

    # generating devtype configs
    for dt_n in dts:
        with open(f"{srv_devs_dir}/{dt_n}.devtype", 'w') as f_dt:
            f_dt.write(dts[dt_n].cx_str())
        conf_file.write(f'include(./types/{fname}/{dt_n}.devtype)\n')

    # devices configuration
    for d in devs:
        if '.' in d.name:
            dev_name = d.name.replace('.', '_')
            conf_file.write(f'dev {dev_name} {ro}{dev_dtns[d.name]}/bridge ~ - @*{upd}:{sm.source.name}.{d.name}\n')
            conf_file.write(f'cpoint {d.name} {dev_name}\n')
        else:
            conf_file.write(f'dev {d.name} {ro}{dev_dtns[d.name]}/bridge ~ - @*{upd}:{sm.source.name}.{d.name}\n')

    conf_file.close()

print('generate configs for cx services starter')
print(cx_srvs)
print('\nWarning: cx-servers-HOST.conf files not supposed to be copied derectly to servers,')
print('since some cx-servers can be configured separatly')

for h in cx_srvs:
    with open(f'{conf_dir}/cx-servers-{h}.conf', 'w') as cf:
        cf.write(' '.join(cx_srvs[h]))


