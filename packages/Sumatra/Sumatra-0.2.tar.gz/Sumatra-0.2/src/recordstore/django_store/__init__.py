"""
Handles storage of simulation/analysis records in a relational database, via the
Django object-relational mapper (ORM), which means that any database
supported by Django could in principle be used, although for now we assume
SQLite.
"""


from sumatra.recordstore import RecordStore
from django.conf import settings
from django.core import management
import os

recordstore_settings = {
    'DEBUG': True,
    'DATABASE_ENGINE': 'sqlite3',
    'INSTALLED_APPS': ('sumatra.recordstore.django_store',
                       'django.contrib.contenttypes', # needed for tagging
                       'tagging'),
}


class DjangoRecordStore(RecordStore):
    
    def __init__(self, db_file='.smt/smt.db'):
        self._db_file = os.path.abspath(db_file)
        recordstore_settings['DATABASE_NAME'] = self._db_file
        if not settings.configured:
            settings.configure(**recordstore_settings)
            management.setup_environ(settings)
            if not os.path.exists(os.path.dirname(self._db_file)):
                os.makedirs(os.path.dirname(self._db_file))
            if not os.path.exists(self._db_file):
                management.call_command('syncdb')
        else:
            assert settings.DATABASE_NAME == self._db_file, "%s != %s" % (settings.DATABASE_NAME, self._db_file)
                
    def __str__(self):
        return "Relational database record store using the Django ORM (database file=%s)" % self._db_file
        
    def __getstate__(self):
        return self._db_file
    
    def __setstate__(self, state):
        self.__init__(state)
    
    def _switch_db(self, db_file):
        # for testing
        settings._wrapped = None
        assert settings.configured == False
        if db_file:
            self.__init__(db_file)
    
    def _get_db_record(self, project_name, record):
        db_project = self._get_db_project(project_name)
        try:
            db_record = models.Record.objects.get(label=record.label,
                                                  project=db_project)
        except models.Record.DoesNotExist:
            db_record = models.Record(label=record.label, project=db_project)
        return db_record
    
    def _get_db_project(self, project_name):
        import models
        try:
            db_project = models.Project.objects.get(id=project_name)
        except models.Project.DoesNotExist:
            db_project = models.Project(id=project_name)
            db_project.save()
        return db_project
                                                                     
    def _get_db_obj(self, db_class, obj):
        cls = getattr(models, db_class)
        db_obj, created = cls.objects.get_or_create_from_sumatra_object(obj)
        if created:
            db_obj.save()
        return db_obj        
    
    def save(self, project_name, record):
        db_record = self._get_db_record(project_name, record)
        for attr in 'reason', 'duration', 'outcome', 'main_file', 'version', 'timestamp':
            value = getattr(record, attr)
            if value is not None:
                setattr(db_record, attr, value)
        db_record.data_key = str(record.data_key)
        db_record.executable = self._get_db_obj('Executable', record.executable)
        db_record.repository = self._get_db_obj('Repository', record.repository)
        db_record.launch_mode = self._get_db_obj('LaunchMode', record.launch_mode)
        db_record.datastore = self._get_db_obj('Datastore', record.datastore)
        db_record.parameters = self._get_db_obj('ParameterSet', record.parameters)
        db_record.user = record.user
        db_record.tags = ",".join(record.tags)
        # should perhaps check here for any orphan Tags, i.e., those that are no longer associated with any records, and delete them
        db_record.save() # need to save before using many-to-many relationship
        for dep in record.dependencies:
            #print "Adding dependency %s to db_record" % dep
            db_record.dependencies.add(self._get_db_obj('Dependency', dep))
        for pi in record.platforms:
            db_record.platforms.add(self._get_db_obj('PlatformInformation', pi))
        db_record.diff = record.diff
        #import django.db.models.manager
        #def debug(f):
        #    def _debug(model, values, **kwargs):
        #        print "model = ", model
        #        print "values = ", values
        #        print "kwargs = ", kwargs
        #        return f(model, values, **kwargs)
        #    return _debug
        #django.db.models.manager.insert_query = debug(django.db.models.manager.insert_query)
        db_record.save()
        
    def get(self, project_name, label):
        import models
        try:
            db_record = models.Record.objects.get(project__id=project_name, label=label)
        except models.Record.DoesNotExist:
            raise KeyError(label)
        return db_record.to_sumatra()
    
    def list(self, project_name, tags=None):
        import models
        db_records = models.Record.objects.filter(project__id=project_name)
        if tags:
            if not hasattr(tags, "__len__"):
                tags = [tags]
            for tag in tags:
                db_records = db_records.filter(tags__contains=tag)
        return [db_record.to_sumatra() for db_record in db_records]
    
    def delete(self, project_name, label):
        import models
        db_record = models.Record.objects.get(label=label, project__id=project_name)
        db_record.delete()
        
    def delete_by_tag(self, project_name, tag):
        import models
        db_records = models.Record.objects.filter(project__id=project_name, tags__contains=tag)
        n = db_records.count()
        for db_record in db_records:
            db_record.delete()
        return n
    
    def _dump(self, indent=2):
        """
        Dump the database contents to a JSON-encoded string
        """
        import sys, StringIO
        data = StringIO.StringIO()
        sys.stdout = data
        management.call_command('dumpdata', indent=indent)
        sys.stdout = sys.__stdout__
        data.seek(0)
        return data.read()
