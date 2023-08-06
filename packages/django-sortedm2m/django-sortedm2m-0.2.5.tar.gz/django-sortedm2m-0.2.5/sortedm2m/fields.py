# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.fields.related import create_many_related_manager, ManyToManyField, ReverseManyRelatedObjectsDescriptor
from sortedm2m.forms import SortedMultipleChoiceField
from sortedm2m.utils import execute_after_model_is_loaded, get_model_label


SORT_VALUE_FIELD_NAME = 'sort_value'


def create_sorted_many_related_manager(superclass, rel):
    RelatedManager = create_many_related_manager(superclass, rel)

    class SortedRelatedManager(RelatedManager):
        def get_query_set(self):
            # We use ``extra`` method here because we have no other access to
            # the extra sorting field of the intermediary model. The fields
            # are hidden for joins because we set ``auto_created`` on the
            # intermediary's meta options.
            return super(SortedRelatedManager, self).\
                get_query_set().\
                extra(order_by=['%s.%s' % (
                    rel.through._meta.db_table,
                    rel.through._sort_field_name,
                )])

        def add(self, *objs):
            through = rel.through
            count = through._default_manager.count
            for obj in objs:
                related_name = rel.to._meta.object_name.lower()
                if not isinstance(obj, rel.to):
                    related_name = '%s_id' % related_name
                through._default_manager.create(**{
                    related_name: obj,
                    # using from model's name as field name
                    self.source_field_name: self.instance,
                    through._sort_field_name: count(),
                })
        add.alters_data = True

        def remove(self, *objs):
            through = rel.through
            for obj in objs:
                through._default_manager.filter(**{
                    '%s__in' % rel.to._meta.object_name.lower(): objs,
                    # using from model's name as field name
                    self.source_field_name: self.instance,
                }).delete()
        remove.alters_data = True

    return SortedRelatedManager


class ReverseSortedManyRelatedObjectsDescriptor(ReverseManyRelatedObjectsDescriptor):
    def __get__(self, instance, instance_type=None):
        if instance is None:
            return self

        # Dynamically create a class that subclasses the related
        # model's default manager.
        rel_model=self.field.rel.to
        superclass = rel_model._default_manager.__class__
        RelatedManager = create_sorted_many_related_manager(superclass, self.field.rel)

        manager = RelatedManager(
            model=rel_model,
            core_filters={'%s__pk' % self.field.related_query_name(): instance._get_pk_val()},
            instance=instance,
            symmetrical=(self.field.rel.symmetrical and isinstance(instance, rel_model)),
            source_field_name=self.field.m2m_field_name(),
            target_field_name=self.field.m2m_reverse_field_name(),
            reverse=False
        )

        return manager

    def __set__(self, instance, value):
        if instance is None:
            raise AttributeError, "Manager must be accessed via instance"

        manager = self.__get__(instance)
        manager.clear()
        manager.add(*value)


class SortedManyToManyField(ManyToManyField):
    '''
    Providing a many to many relation that remembers the order of related
    objects.

    Accept a boolean ``sorted`` attribute which specifies if relation is
    ordered or not. Default is set to ``True``. If ``sorted`` is set to
    ``False`` the field will behave exactly like django's ``ManyToManyField``.
    '''
    def __init__(self, to, sorted=True, **kwargs):
        self.sorted = sorted
        if self.sorted:
            # This is very hacky and should be removed if a better solution is
            # found.
            kwargs.setdefault('through', True)
        super(SortedManyToManyField, self).__init__(to, **kwargs)
        self.help_text = kwargs.get('help_text', None)

    def create_intermediary_model(self, cls, field_name):
        '''
        Create intermediary model that stores the relation's data.
        '''
        module = ''

        model_name = '%s_%s_%s' % (
            cls._meta.app_label,
            cls._meta.object_name,
            field_name)
        from_ = '%s.%s' % (
            cls._meta.app_label,
            cls._meta.object_name)

        def default_sort_value():
            model = models.get_model(cls._meta.app_label, model_name)
            return model._default_manager.count()

        # Using from and to model's name as field names for relations. This is
        # also django default behaviour for m2m intermediary tables.
        fields = {
            cls._meta.object_name.lower():
                models.ForeignKey(from_),
            # using to model's name as field name for the other relation
            self.rel.to._meta.object_name.lower():
                models.ForeignKey(self.rel.to),
            SORT_VALUE_FIELD_NAME:
                models.IntegerField(default=default_sort_value),
        }

        class Meta:
            db_table = '%s_%s_%s' % (
                cls._meta.app_label.lower(),
                cls._meta.object_name.lower(),
                field_name.lower())
            app_label = cls._meta.app_label
            ordering = (SORT_VALUE_FIELD_NAME,)
            auto_created = cls

        attrs = {
            '__module__': module,
            'Meta': Meta,
            '_sort_field_name': SORT_VALUE_FIELD_NAME,
            '__unicode__': lambda s: 'pk=%d' % s.pk,
        }

        attrs.update(fields)

        # Create the class, which automatically triggers ModelBase processing
        model = type(model_name, (models.Model,), attrs)

        return model

    def contribute_to_class(self, cls, name):
        if self.sorted:
            def set_everything_related(model, self, cls, name):
                self.rel.to = model
                self.rel.through = self.create_intermediary_model(cls, name)
                # overwrite default descriptor with reverse and sorted one
                super(SortedManyToManyField, self).contribute_to_class(cls, name)
                setattr(cls, self.name, ReverseSortedManyRelatedObjectsDescriptor(self))

            model_label = get_model_label(self.rel.to, cls._meta.app_label)
            execute_after_model_is_loaded(
                model_label,
                set_everything_related,
                args=(self, cls, name))
        else:
            super(SortedManyToManyField, self).contribute_to_class(cls, name)

    def formfield(self, **kwargs):
        defaults = {}
        if self.sorted:
            defaults['form_class'] = SortedMultipleChoiceField
        defaults.update(kwargs)
        return super(SortedManyToManyField, self).formfield(**defaults)
