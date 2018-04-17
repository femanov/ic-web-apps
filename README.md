# ic-web-apps
django-based web apps for ic controls. DB admin

## parts

* db_routers - router definitions to separate django and apps databases
* accdb - app for acceletator controls config database
* netdb - app for network information editing
* config_gen -  non-django configuration files generation for named, dhcpd, CXv4 soft servers


## requirements:

* django 2.
* treebeard (moving to MP trees now)
* postgresql 9.5+ (may be 9.4 is ok, json support required)

