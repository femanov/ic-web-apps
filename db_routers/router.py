

class DjangoRouter(object):
    def db_for_read(self, model, **hints):
        return 'default'

    def db_for_write(self, model, **hints):
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'django' or obj2._meta.app_label == 'django':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True


class AccdbRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'accdb':
            return 'icdata'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'accdb':
            return 'icdata'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'accdb' or obj2._meta.app_label == 'accdb':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'accdb':
            return db == 'icdata'
        elif db == 'icdata':
            return False
        return None


class AccmodeRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'accmode':
            return 'accmode'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'accmode':
            return 'accmode'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'accmode' or obj2._meta.app_label == 'accmode':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'accmode':
            return db == 'accmode'
        elif db == 'accmode':
            return False
        return None


# class NetdbRouter(object):
#     def db_for_read(self, model, **hints):
#         if model._meta.app_label == 'netdb':
#             return 'netdata'
#         return None
#
#     def db_for_write(self, model, **hints):
#         if model._meta.app_label == 'netdb':
#             return 'netdata'
#         return None
#
#     def allow_relation(self, obj1, obj2, **hints):
#         if obj1._meta.app_label == 'netdb' or obj2._meta.app_label == 'netdb':
#             return True
#         return None
#
#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         if app_label == 'netdb':
#             return db == 'netdata'
#         elif db == 'netdata':
#             return False
#         return None
