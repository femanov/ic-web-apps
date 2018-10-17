#!/usr/bin/env python3

import psycopg2
from settings.db import hosts_db
import ipaddress

import math


def net_ip_prefix(ip_text, mask_length):
    length = math.ceil(mask_length/8)
    return '.'.join((ip_text.split('.'))[:length])

try:
    conn = psycopg2.connect(None, **hosts_db)
except:
    print("unable to connect to DB")
    exit()
cur = conn.cursor()

all_file = open('named.conf.local', 'w')


cur.execute('SELECT id,name, admin_mail,dns_serial,dns_options,nameservers,static_records FROM domain')
domains = cur.fetchall()
conn.commit()


for x in domains:
    d_id, dname, admin_mail, dns_serial, dns_options, nameservers, static_records = \
        x[0], x[1], x[2].replace('@', '.'), x[3], x[4].replace('\r', ''), x[5].replace('\r', ''), x[6].replace('\r', '')

    dns_serial +=1
    cur.execute('UPDATE domain set dns_serial=%s WHERE id=%s', (dns_serial, d_id))
    conn.commit

    cfg_text = '$TTL 604800\n@ IN SOA %s. %s. (%s; serial\n%s\n);\n\n' % (dname, admin_mail, dns_serial, dns_options)

    cfg_text += '; name servers - NS records\n'
    nsrvs = nameservers.split('\n')
    for srv in nsrvs:
        cfg_text += ' IN NS %s.%s.\n' % (srv, dname)

    cfg_text += '\n; services\n'
    cfg_text += static_records

    cfg_text += '\n\n; A records\n'

    cur.execute('SELECT host.name,host.ip,host.aliases FROM host,net WHERE host.net_id=net.id and net.domain_id=%s', (d_id,))
    hosts = cur.fetchall()
    conn.commit()

    for host in hosts:
        cfg_text += '%s IN A %s\n' % (host[0], host[1])
        if host[2] != '':
            aliases = host[2].split(';')
            for a in aliases:
                cfg_text += "%s IN A %s\n" % (a, host[1])

    file = open('db.%s' % (dname,), 'w')
    file.write(cfg_text)
    file.close()

    # reverse zones generation
    cur.execute('SELECT id,ip,mask FROM net where net.domain_id=%s', (d_id,))
    nets = cur.fetchall()
    conn.commit()

    all_file.write('zone "%s" { type master; file \"/etc/named/zones/db.%s\"; };\n' % (dname, dname))

    for net in nets:
        n_id, n_ip, n_mask = net
        ip_prefix = net_ip_prefix(n_ip, n_mask)

        cfg_text = '$TTL 604800\n@ IN SOA %s. %s. (%s; serial\n%s\n);\n\n' % (dname, admin_mail, dns_serial, dns_options)

        cfg_text += '; name servers - NS records\n'
        nsrvs = nameservers.split('\n')
        for srv in nsrvs:
            cfg_text += ' IN NS %s.%s.\n' % (srv, dname)

        cur.execute('SELECT name,ip FROM host WHERE host.net_id=%s ORDER BY ip', (n_id,))
        n_hosts = cur.fetchall()
        conn.commit()

        cfg_text += '\n\n; PTR records\n'

        for host in n_hosts:
            # host[1].split('.')[-1] - correct only for C-class networks
            cfg_text += '%s IN PTR %s.%s.\n' % (host[1].split('.')[-1], host[0], dname)

        file = open('db.%s' % (ip_prefix,), 'w')
        file.write(cfg_text)
        file.close()

        rev_ip = '.'.join(ip_prefix.split('.')[::-1])
        all_file.write('zone "%s.in-addr.arpa" {type master;file \"/etc/named/zones/db.%s\";};\n' % (rev_ip, ip_prefix))



all_file.close()
