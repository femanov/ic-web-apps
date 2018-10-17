#!/usr/bin/env python3

import psycopg2
from settings.db import hosts_db
import ipaddress

try:
    conn = psycopg2.connect(None, **hosts_db)
except:
    print("unable to connect to DB")
    exit()
cur = conn.cursor()


cfg_text = """#
# DHCP Server Configuration file.
#   see /usr/share/doc/dhcp*/dhcpd.conf.example
#   see dhcpd.conf(5) man page
#
option domain-name "ic.local";
option domain-name-servers 192.168.129.2, 192.168.129.3;

default-lease-time 600;
max-lease-time 7200;

ddns-update-style none;
authoritative;

"""

# DHCP operates for all networks in our db

cur.execute('SELECT id,ip,mask,dhcp_options FROM net')
nets = cur.fetchall()
conn.commit()

for x in nets:
    net_def = ipaddress.ip_network('%s/%s' % (x[1], x[2]))
    nmask_str = str(net_def.netmask)
    cfg_text += "subnet %s netmask %s {\n%s}\n\n" % (x[1], nmask_str, x[3].replace('\r', ''))


cur.execute('SELECT name, mac, ip FROM host')
hosts = cur.fetchall()
conn.commit()



for x in hosts:
    cfg_text += """
host %s {
  hardware ethernet %s;
  fixed-address %s;
}
""" % x

cfg_text += '\n'

file = open('dhcpd.conf', 'w')

file.write(cfg_text)
file.close()



cur.close()
conn.close()
