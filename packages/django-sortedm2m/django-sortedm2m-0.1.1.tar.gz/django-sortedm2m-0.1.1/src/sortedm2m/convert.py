def migrate_data(from_model, to_model, intermediary_model):
    related_field = from_model._meta.object_name.lower()
    count = 0
    for instance in intermediary_model._default_manager.all():
        to_model._default_manager.create(**{
            'id': instance.id,
            'object_id': getattr(instance, '%s_id' % related_field),
            'media_id': instance.media_id,
            to_model._sort_field_name: count,
        })
        count += 1
    return count


def auto_migrate_data(self, verbosity, **kwargs):
    # guess automatic intermediary model
    class Meta:
        db_table = '%s_%s_%s' % (
            self.from_model._meta.app_label.lower(),
            self.from_model._meta.object_name.lower(),
            self.field_name.lower(),
        )
        managed = False
    intermediary_model = type('_MigrateSortedMediaRelation', (models.Model,), {
        '__module__': 'mediastore.models',
        'Meta': Meta,
        'id': models.IntegerField(primary_key=True),
        self.from_model._meta.object_name.lower(): models.ForeignKey(self.from_model),
        'media': models.ForeignKey('mediastore.Media'),
    })
    try:
        if verbosity >= 1:
            print (
                "Migrating '%s.%s' to a sorted many to many "
                "relation ..." % (
                    self.from_model._meta.object_name,
                    self.field_name))
        count = migrate_data(
            self.from_model,
            self.rel.through_model,
            intermediary_model)
        if verbosity >= 1:
            print "   Successfully migrated %d relations" % count
            print (
                "   You may now delete the no more used database "
                "table '%s'" % (Meta.db_table))
    except Exception, e:
        if verbosity >= 1:
            print "Error during migration of '%s.%s': %s" % (
                self.from_model._meta.object_name,
                self.field_name,
                e)
