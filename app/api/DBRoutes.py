class DBRoutes:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'core':
            return 'sisac'
        if model._meta.app_label == 'mosaiq_app':
            return 'mosaiq'
        if model._meta.app_label == 'config':
            return 'config'
        return None
    
    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'core':
            return 'sisac'
        if model._meta.app_label == 'mosaiq_app':
            return 'mosaiq'
        if model._meta.app_label == 'config':
            return 'config'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'core' or \
           obj2._meta.app_label == 'core':
           return True
        if obj1._meta.app_label == 'mosaiq_app' or \
           obj2._meta.app_label == 'mosaiq_app':
           return True
        if obj1._meta.app_label == 'config' or \
           obj2._meta.app_label == 'config':
           return True
        return None            

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'core':
            return db == 'sisac'
        if app_label == 'mosaiq_app':
            return db == 'mosaiq'
        if app_label == 'config':
            return db == 'config'
        return None
        