"""
Models and managers for generic tagging.
"""
# Python 2.3 compatibility
try:
    set
except NameError:
    from sets import Set as set

import logging

logger = logging.getLogger('tagging.models')

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import connection, models, IntegrityError
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _

from tagging import settings
from tagging.utils import calculate_cloud, get_tag_list, get_queryset_and_model, parse_tag_input
from tagging.utils import LOGARITHMIC

qn = connection.ops.quote_name

if settings.MULTILINGUAL_TAGS:
    import multilingual
    BaseManager = multilingual.Manager
else:
    BaseManager = models.Manager

############
# Managers #
############

class TagManager(BaseManager):
    def update_tags(self, obj, tag_names):
        """
        Update tags associated with an object.
        """
        ctype = ContentType.objects.get_for_model(obj)
        current_tags = list(self.filter(items__content_type__pk=ctype.pk,
                                        items__object_id=obj.pk))
        updated_tag_names = parse_tag_input(tag_names)
        if settings.FORCE_LOWERCASE_TAGS:
            updated_tag_names = [t.lower() for t in updated_tag_names]

        # Remove tags which no longer apply
        tags_for_removal = [tag for tag in current_tags \
                            if tag.name not in updated_tag_names]
        if len(tags_for_removal):
            TaggedItem._default_manager.filter(content_type__pk=ctype.pk,
                                               object_id=obj.pk,
                                               tag__in=tags_for_removal).delete()
        # Add new tags
        current_tag_names = [tag.name_any for tag in current_tags]
        for tag_name in updated_tag_names:
            if tag_name not in current_tag_names:
                tag, created = self.get_or_create(name=tag_name)
                TaggedItem._default_manager.create(tag=tag, object=obj)

    def add_tag(self, obj, tag_name):
        """
        Associates the given object with a tag.
        """
        tag_names = parse_tag_input(tag_name)
        if not len(tag_names):
            raise AttributeError(_('No tags were given: "%s".') % tag_name)
        if len(tag_names) > 1:
            raise AttributeError(_('Multiple tags were given: "%s".') % tag_name)
        tag_name = tag_names[0]
        if settings.FORCE_LOWERCASE_TAGS:
            tag_name = tag_name.lower()
        tag, created = self.get_or_create(name=tag_name)
        ctype = ContentType.objects.get_for_model(obj)
        TaggedItem._default_manager.get_or_create(
            tag=tag, content_type=ctype, object_id=obj.pk)

    def get_for_object(self, obj):
        """
        Create a queryset matching all tags associated with the given
        object.
        """
        ctype = ContentType.objects.get_for_model(obj)
        return self.filter(items__content_type__pk=ctype.pk,
                           items__object_id=obj.pk)

    def _get_usage(self, model, counts=False, min_count=None, extra_joins=None, extra_criteria=None, params=None):
        """
        Perform the custom SQL query for ``usage_for_model`` and
        ``usage_for_queryset``.
        """
        if min_count is not None: counts = True

        model_table = qn(model._meta.db_table)
        model_pk = '%s.%s' % (model_table, qn(model._meta.pk.column))
        query = """
        SELECT DISTINCT %(tag)s.id%(count_sql)s
        FROM
            %(tag)s
            INNER JOIN %(tagged_item)s
                ON %(tag)s.id = %(tagged_item)s.tag_id
            INNER JOIN %(model)s
                ON %(tagged_item)s.object_id = %(model_pk)s
            %%s
        WHERE %(tagged_item)s.content_type_id = %(content_type_id)s
            %%s
        GROUP BY %(tag)s.id
        %%s""" % {
            'tag': qn(self.model._meta.db_table),
            'count_sql': counts and (', COUNT(%s)' % model_pk) or '',
            'tagged_item': qn(TaggedItem._meta.db_table),
            'model': model_table,
            'model_pk': model_pk,
            'content_type_id': ContentType.objects.get_for_model(model).pk,
        }

        min_count_sql = ''
        if min_count is not None:
            min_count_sql = 'HAVING COUNT(%s) >= %%s' % model_pk
            params.append(min_count)

        cursor = connection.cursor()
        cursor.execute(query % (extra_joins, extra_criteria, min_count_sql), params)
        tags = []
        # TODO add ordering by name right here
        for row in cursor.fetchall():
            t = self.model.objects.get(pk = row[0])
            if counts:
                t.count = row[1]
            tags.append(t)
        tags.sort()
        return tags

    def usage_for_model(self, model, counts=False, min_count=None, filters=None):
        """
        Obtain a list of tags associated with instances of the given
        Model class.

        If ``counts`` is True, a ``count`` attribute will be added to
        each tag, indicating how many times it has been used against
        the Model class in question.

        If ``min_count`` is given, only tags which have a ``count``
        greater than or equal to ``min_count`` will be returned.
        Passing a value for ``min_count`` implies ``counts=True``.

        To limit the tags (and counts, if specified) returned to those
        used by a subset of the Model's instances, pass a dictionary
        of field lookups to be applied to the given Model as the
        ``filters`` argument.
        """
        if filters is None: filters = {}

        queryset = model._default_manager.filter()
        for f in filters.items():
            queryset.query.add_filter(f)
        usage = self.usage_for_queryset(queryset, counts, min_count)

        return usage

    def usage_for_queryset(self, queryset, counts=False, min_count=None):
        """
        Obtain a list of tags associated with instances of a model
        contained in the given queryset.

        If ``counts`` is True, a ``count`` attribute will be added to
        each tag, indicating how many times it has been used against
        the Model class in question.

        If ``min_count`` is given, only tags which have a ``count``
        greater than or equal to ``min_count`` will be returned.
        Passing a value for ``min_count`` implies ``counts=True``.
        """

        extra_joins = ' '.join(queryset.query.get_from_clause()[0][1:])
        where, params = queryset.query.where.as_sql()
        if where:
            extra_criteria = 'AND %s' % where
        else:
            extra_criteria = ''
        return self._get_usage(queryset.model, counts, min_count, extra_joins, extra_criteria, params)

    def related_for_model(self, tags, model, counts=False, min_count=None):
        """
        Obtain a list of tags related to a given list of tags - that
        is, other tags used by items which have all the given tags.

        If ``counts`` is True, a ``count`` attribute will be added to
        each tag, indicating the number of items which have it in
        addition to the given list of tags.

        If ``min_count`` is given, only tags which have a ``count``
        greater than or equal to ``min_count`` will be returned.
        Passing a value for ``min_count`` implies ``counts=True``.
        """
        if min_count is not None: counts = True
        tags = get_tag_list(tags)
        tag_count = len(tags)
        tagged_item_table = qn(TaggedItem._meta.db_table)
        query = """
        SELECT %(tag)s.id%(count_sql)s
        FROM %(tagged_item)s INNER JOIN %(tag)s ON %(tagged_item)s.tag_id = %(tag)s.id
        WHERE %(tagged_item)s.content_type_id = %(content_type_id)s
          AND %(tagged_item)s.object_id IN
          (
              SELECT %(tagged_item)s.object_id
              FROM %(tagged_item)s, %(tag)s
              WHERE %(tagged_item)s.content_type_id = %(content_type_id)s
                AND %(tag)s.id = %(tagged_item)s.tag_id
                AND %(tag)s.id IN (%(tag_id_placeholders)s)
              GROUP BY %(tagged_item)s.object_id
              HAVING COUNT(%(tagged_item)s.object_id) = %(tag_count)s
          )
          AND %(tag)s.id NOT IN (%(tag_id_placeholders)s)
        GROUP BY %(tag)s.id
        %(min_count_sql)s""" % {
            'tag': qn(self.model._meta.db_table),
            'count_sql': counts and ', COUNT(%s.object_id)' % tagged_item_table or '',
            'tagged_item': tagged_item_table,
            'content_type_id': ContentType.objects.get_for_model(model).pk,
            'tag_id_placeholders': ','.join(['%s'] * tag_count),
            'tag_count': tag_count,
            'min_count_sql': min_count is not None and ('HAVING COUNT(%s.object_id) >= %%s' % tagged_item_table) or '',
        }

        params = [tag.pk for tag in tags] * 2
        if min_count is not None:
            params.append(min_count)

        cursor = connection.cursor()
        cursor.execute(query, params)
        related = []
        for row in cursor.fetchall():
            tag = self.model.objects.get(pk = row[0])
            if counts is True:
                tag.count = row[1]
            related.append(tag)
        related.sort()
        return related

    def cloud_for_model(self, model, steps=4, distribution=LOGARITHMIC,
                        filters=None, min_count=None):
        """
        Obtain a list of tags associated with instances of the given
        Model, giving each tag a ``count`` attribute indicating how
        many times it has been used and a ``font_size`` attribute for
        use in displaying a tag cloud.

        ``steps`` defines the range of font sizes - ``font_size`` will
        be an integer between 1 and ``steps`` (inclusive).

        ``distribution`` defines the type of font size distribution
        algorithm which will be used - logarithmic or linear. It must
        be either ``tagging.utils.LOGARITHMIC`` or
        ``tagging.utils.LINEAR``.

        To limit the tags displayed in the cloud to those associated
        with a subset of the Model's instances, pass a dictionary of
        field lookups to be applied to the given Model as the
        ``filters`` argument.

        To limit the tags displayed in the cloud to those with a
        ``count`` greater than or equal to ``min_count``, pass a value
        for the ``min_count`` argument.
        """
        tags = list(self.usage_for_model(model, counts=True, filters=filters,
                                         min_count=min_count))
        return calculate_cloud(tags, steps, distribution)

    def process_rules(self, rules):
        for line in rules.split('\n'):
            self._process_line(line)
        return True

    def _process_line(self, line):
        logger.debug('processing line "%s"' % line)

        def join(tags):
            self.join([tag[0] for tag in tags if tag])

        if '==' in line:
            names = [name.strip() for name in line.split('==')]

            try:
                tag = self.get(name=names[0])
            except Tag.DoesNotExist:
                return

            for syn_name in names[1:]:
                try:
                    syn = Synonym(name=syn_name, tag=tag)
                    syn.save()
                except IntegrityError:
                    pass

            join([self.filter(name=name)[:1] for name in names])

        elif '=' in line:
            join([self.filter(name=name.strip())[:1] \
                  for name in line.split('=')])

        elif ':' in line:
            parts = line.split(';')
            if len(parts) > 0:
                changed = False
                head = [p.strip() for p in parts[0].split(':')][:2]
                tag_from = head[0]
                tag_to = (len(head)==2) and head[1] or head[0]

                try:
                    tag = self.get(name=tag_from)
                except Tag.DoesNotExist:
                    return

                if tag.name != tag_to:
                    tag.name = tag_to
                    changed = True

                names = [tuple(i.strip() for i in p.split(':')) for p in parts[1:]]
                for name in names:
                    if len(name) == 2 and getattr(tag, 'name_%s' % name[0], None) != name[1]:
                        setattr(tag, 'name_%s' % name[0], name[1])
                        changed = True

                if changed:
                    tag.save()

    def dumpAsText(self):
        tags = self.all()
        return '\n'.join(filter(lambda x: x, \
                [self.dumpSynonymsAsText(t) for t in tags] + \
                [self.dumpTagAsText(t) for t in tags]))

    def dumpTagAsText(self, tag):
        parts = [tag.name, ]
        for id, code in multilingual.languages.get_language_choices():
            name = tag.get_translation(id, 'name').name
            if name:
                parts.append('%s: %s' % (code, name))

        return '; '.join(parts)

    def dumpSynonymsAsText(self, tag):
        synonyms = tag.synonyms.all()
        if len(synonyms) > 0:
            return ' == '.join([tag.name, ] + [s.name for s in synonyms])
        return ''

    def join(self, query):
        """This method joins multiple tags together."""
        from tagging.utils import merge

        logger.info('Joining %s' % ','.join([unicode(obj) for obj in query]))
        tags = list(query)
        if len(tags) < 2:
            return

        first = tags[0]
        tags = tags[1:]
        for t in tags:
            merge(first, t)


class TaggedItemManager(models.Manager):
    """
    FIXME There's currently no way to get the ``GROUP BY`` and ``HAVING``
          SQL clauses required by many of this manager's methods into
          Django's ORM.

          For now, we manually execute a query to retrieve the PKs of
          objects we're interested in, then use the ORM's ``__in``
          lookup to return a ``QuerySet``.

          Now that the queryset-refactor branch is in the trunk, this can be
          tidied up significantly.
    """
    def get_by_model(self, queryset_or_model, tags):
        """
        Create a ``QuerySet`` containing instances of the specified
        model associated with a given tag or list of tags.
        """
        tags = get_tag_list(tags)
        tag_count = len(tags)
        if tag_count == 0:
            # No existing tags were given
            queryset, model = get_queryset_and_model(queryset_or_model)
            return model._default_manager.none()
        elif tag_count == 1:
            # Optimisation for single tag - fall through to the simpler
            # query below.
            tag = tags[0]
        else:
            return self.get_intersection_by_model(queryset_or_model, tags)

        queryset, model = get_queryset_and_model(queryset_or_model)
        content_type = ContentType.objects.get_for_model(model)
        opts = self.model._meta
        tagged_item_table = qn(opts.db_table)
        return queryset.extra(
            tables=[opts.db_table],
            where=[
                '%s.content_type_id = %%s' % tagged_item_table,
                '%s.tag_id = %%s' % tagged_item_table,
                '%s.%s = %s.object_id' % (qn(model._meta.db_table),
                                          qn(model._meta.pk.column),
                                          tagged_item_table)
            ],
            params=[content_type.pk, tag.pk],
        )

    def get_intersection_by_model(self, queryset_or_model, tags):
        """
        Create a ``QuerySet`` containing instances of the specified
        model associated with *all* of the given list of tags.
        """
        tags = get_tag_list(tags)
        tag_count = len(tags)
        queryset, model = get_queryset_and_model(queryset_or_model)

        if not tag_count:
            return model._default_manager.none()

        model_table = qn(model._meta.db_table)
        # This query selects the ids of all objects which have all the
        # given tags.
        query = """
        SELECT %(model_pk)s
        FROM %(model)s, %(tagged_item)s
        WHERE %(tagged_item)s.content_type_id = %(content_type_id)s
          AND %(tagged_item)s.tag_id IN (%(tag_id_placeholders)s)
          AND %(model_pk)s = %(tagged_item)s.object_id
        GROUP BY %(model_pk)s
        HAVING COUNT(%(model_pk)s) = %(tag_count)s""" % {
            'model_pk': '%s.%s' % (model_table, qn(model._meta.pk.column)),
            'model': model_table,
            'tagged_item': qn(self.model._meta.db_table),
            'content_type_id': ContentType.objects.get_for_model(model).pk,
            'tag_id_placeholders': ','.join(['%s'] * tag_count),
            'tag_count': tag_count,
        }

        cursor = connection.cursor()
        cursor.execute(query, [tag.pk for tag in tags])
        object_ids = [row[0] for row in cursor.fetchall()]
        if len(object_ids) > 0:
            return queryset.filter(pk__in=object_ids)
        else:
            return model._default_manager.none()

    def get_union_by_model(self, queryset_or_model, tags):
        """
        Create a ``QuerySet`` containing instances of the specified
        model associated with *any* of the given list of tags.
        """
        tags = get_tag_list(tags)
        tag_count = len(tags)
        queryset, model = get_queryset_and_model(queryset_or_model)

        if not tag_count:
            return model._default_manager.none()

        model_table = qn(model._meta.db_table)
        # This query selects the ids of all objects which have any of
        # the given tags.
        query = """
        SELECT %(model_pk)s
        FROM %(model)s, %(tagged_item)s
        WHERE %(tagged_item)s.content_type_id = %(content_type_id)s
          AND %(tagged_item)s.tag_id IN (%(tag_id_placeholders)s)
          AND %(model_pk)s = %(tagged_item)s.object_id
        GROUP BY %(model_pk)s""" % {
            'model_pk': '%s.%s' % (model_table, qn(model._meta.pk.column)),
            'model': model_table,
            'tagged_item': qn(self.model._meta.db_table),
            'content_type_id': ContentType.objects.get_for_model(model).pk,
            'tag_id_placeholders': ','.join(['%s'] * tag_count),
        }

        cursor = connection.cursor()
        cursor.execute(query, [tag.pk for tag in tags])
        object_ids = [row[0] for row in cursor.fetchall()]
        if len(object_ids) > 0:
            return queryset.filter(pk__in=object_ids)
        else:
            return model._default_manager.none()

    def get_related(self, obj, queryset_or_model, num=None):
        """
        Retrieve a list of instances of the specified model which share
        tags with the model instance ``obj``, ordered by the number of
        shared tags in descending order.

        If ``num`` is given, a maximum of ``num`` instances will be
        returned.
        """
        queryset, model = get_queryset_and_model(queryset_or_model)
        model_table = qn(model._meta.db_table)
        content_type = ContentType.objects.get_for_model(obj)
        related_content_type = ContentType.objects.get_for_model(model)
        query = """
        SELECT %(model_pk)s, COUNT(related_tagged_item.object_id) AS %(count)s
        FROM %(model)s, %(tagged_item)s, %(tag)s, %(tagged_item)s related_tagged_item
        WHERE %(tagged_item)s.object_id = %%s
          AND %(tagged_item)s.content_type_id = %(content_type_id)s
          AND %(tag)s.id = %(tagged_item)s.tag_id
          AND related_tagged_item.content_type_id = %(related_content_type_id)s
          AND related_tagged_item.tag_id = %(tagged_item)s.tag_id
          AND %(model_pk)s = related_tagged_item.object_id"""
        if content_type.pk == related_content_type.pk:
            # Exclude the given instance itself if determining related
            # instances for the same model.
            query += """
          AND related_tagged_item.object_id != %(tagged_item)s.object_id"""
        query += """
        GROUP BY %(model_pk)s
        ORDER BY %(count)s DESC
        %(limit_offset)s"""
        query = query % {
            'model_pk': '%s.%s' % (model_table, qn(model._meta.pk.column)),
            'count': qn('count'),
            'model': model_table,
            'tagged_item': qn(self.model._meta.db_table),
            'tag': qn(self.model._meta.get_field('tag').rel.to._meta.db_table),
            'content_type_id': content_type.pk,
            'related_content_type_id': related_content_type.pk,
            # Hardcoding this for now just to get tests working again - this
            # should now be handled by the query object.
            'limit_offset': num is not None and 'LIMIT %s' or '',
        }

        cursor = connection.cursor()
        params = [obj.pk]
        if num is not None:
            params.append(num)
        cursor.execute(query, params)
        object_ids = [row[0] for row in cursor.fetchall()]
        if len(object_ids) > 0:
            # Use in_bulk here instead of an id__in lookup, because id__in would
            # clobber the ordering.
            object_dict = queryset.in_bulk(object_ids)
            return [object_dict[object_id] for object_id in object_ids \
                    if object_id in object_dict]
        else:
            return []

##########
# Models #
##########

class Tag(models.Model):
    """
    A tag.
    """
    if settings.MULTILINGUAL_TAGS:
        class Translation(multilingual.Translation):
            name = models.CharField(_('name'), max_length=50, unique=True, db_index=True)
    else:
        name = models.CharField(_('name'), max_length=50, unique=True, db_index=True)

    objects = TagManager()

    class Meta:
        if not settings.MULTILINGUAL_TAGS:
            ordering = ('name',)
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __unicode__(self):
        return self.name or 'tag-with-id: %d' % self.id

    def __lt__(self, other):
        return self.name < other.name

    def delete(self, update = True):
        if update:
            self._updateLinkedObjects(remove_this = True)
        return super(Tag, self).delete()

    def save(self, *args, **kwargs):
        result = super(Tag, self).save(*args, **kwargs)
        self._updateLinkedObjects()
        return result

    def _updateLinkedObjects(self, remove_this = False):
        """Updates TagField's for all objects with this tag."""
        for item in TaggedItem.objects.filter(tag=self):
            item._updateLinkedObjects(remove_this=remove_this)

if settings.MULTILINGUAL_TAGS:
    """Monkey-patching for translation getter,
       to fallback to another translation."""

    from multilingual.translation import getter_generator
    _orig_name_getter = Tag.get_name
    def _my_get_name(self, language_id = None, fallback = False):
        value = _orig_name_getter(self, language_id, fallback)
        if value is None and language_id is None:
            #print 'BLAH BLAH for lang_id: %s' % language_id
            value = _orig_name_getter(self, settings.FALLBACK_LANGUAGE, fallback)
            #print 'New value for lang_id=%s is %s' % (settings.FALLBACK_LANGUAGE, value)
        return value
    _my_get_name.short_description = getattr(Tag.name, 'verbose_name', 'name')
    setattr(Tag, 'get_name', _my_get_name)

class TaggedItem(models.Model):
    """
    Holds the relationship between a tag and the item being tagged.
    """
    tag          = models.ForeignKey(Tag, verbose_name=_('tag'), related_name='items')
    content_type = models.ForeignKey(ContentType, verbose_name=_('content type'))
    object_id    = models.PositiveIntegerField(_('object id'), db_index=True)
    object       = generic.GenericForeignKey('content_type', 'object_id')

    objects = TaggedItemManager()

    class Meta:
        # Enforce unique tag association per object
        unique_together = (('tag', 'content_type', 'object_id'),)
        verbose_name = _('tagged item')
        verbose_name_plural = _('tagged items')

    def __unicode__(self):
        return u'%s [%s]' % (self.object, self.tag)

    def _updateLinkedObjects(self, remove_this = False):
        from tagging.fields import TagField
        object_tags = [ tag.name_any \
                      for tag in Tag.objects.get_for_object(self.object) \
                              if not remove_this or tag.id != self.tag_id ]
        tags_as_string = ', '.join(object_tags)

        for field in self.object._meta.fields:
            if isinstance(field, TagField):
                setattr(self.object, field.attname, tags_as_string)
                self.object.save()
                break

    def delete(self, update = True):
        if update:
            self._updateLinkedObjects(remove_this=True)
        return super(TaggedItem, self).delete()

class Synonym(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)
    tag = models.ForeignKey(Tag, related_name='synonyms')

    def __unicode__(self):
        return u'%s, synonym for %s' % (self.name, self.tag)

    class Meta:
        verbose_name = _("Tag's synonym")
        verbose_name_plural = _("Tags' synonyms")
        ordering = ('name',)

