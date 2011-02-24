from django.db.models import Q

from tmapi.exceptions import IllegalArgumentException
from tmapi.indices.index import Index
from tmapi.models import Name, Occurrence, Topic
from tmapi.models.variant import Variant


class ScopedIndex (Index):

    def get_associations (self, themes=None, match_all=False):
        """Returns the `Association`s in the topic map whose scope
        property contains at least one of the specified `themes`.

        If `themes` is None, all `Association`s in the unconstrained
        scope are returned.

        If `match_all` is True, the scope property of an association
        must match all `themes`.

        The return value may be empty but must never be None.

        :param themes: scope of the `Association`s to be returned
        :type themes: `Topic` or list of `Topic`s
        :param match_all: whether an `Association`'s scope property
          must match all `themes`
        :type match_all: boolean
        :rtype: `QuerySet` of `Association`s

        """
        associations = self.topic_map.get_associations()
        if themes is not None:
            if isinstance(themes, Topic):
                associations = associations.filter(scope=themes)
            elif match_all:
                for theme in themes:
                    associations = associations.filter(scope=theme)
            else:
                query = None
                for theme in themes:
                    if query is None:
                        query = Q(scope=theme)
                    else:
                        query = query | Q(scope=theme)
                associations = associations.filter(query)
        else:
            if match_all:
                raise IllegalArgumentException(
                    'match_all must not be specified if themes is None')
            associations = associations.filter(scope=None)
        return associations.distinct()

    def get_association_themes (self):
        """Returns the topics in the topic map used in the scope
        property of `Association`s.

        The return value may be empty but must never be None.

        :rtype: `QuerySet` of `Topic`s

        """
        return self.topic_map.get_topics().exclude(scoped_associations=None)

    def get_names (self, themes=None, match_all=False):
        """Returns the `Name`s in the topic map whose scope
        property contains at least one of the specified `themes`.

        If `themes` is None, all `Name`s in the unconstrained
        scope are returned.

        If `match_all` is True, the scope property of a name
        must match all `themes`.

        The return value may be empty but must never be None.

        :param themes: scope of the `Name`s to be returned
        :type themes: `Topic` or list of `Topic`s
        :param match_all: whether a `Name`'s scope property must match
          all `themes`
        :type match_all: boolean
        :rtype: `QuerySet` of `Name`s

        """
        names = Name.objects.filter(topic__topic_map=self.topic_map)
        if themes is not None:
            if isinstance(themes, Topic):
                names = names.filter(scope=themes)
            elif match_all:
                for theme in themes:
                    names = names.filter(scope=theme)
            else:
                query = None
                for theme in themes:
                    if query is None:
                        query = Q(scope=theme)
                    else:
                        query = query | Q(scope=theme)
                names = names.filter(query)
        else:
            if match_all:
                raise IllegalArgumentException(
                    'match_all must not be specified if themes is None')
            names = names.filter(scope=None)
        return names.distinct()

    def get_name_themes (self):
        """Returns the topics in the topic map used in the scope
        property of `Name`s.

        The return value may be empty but must never be None.

        :rtype: `QuerySet` of `Topic`s

        """
        return self.topic_map.get_topics().exclude(scoped_names=None)

    def get_occurrences (self, themes=None, match_all=False):
        """Returns the `Occurrence`s in the topic map whose scope
        property contains at least one of the specified `themes`.

        If `themes` is None, all `Occurrence`s in the unconstrained
        scope are returned.

        If `match_all` is True, the scope property of an occurrence
        must match all `themes`.

        The return value may be empty but must never be None.

        :param themes: scope of the `Occurrence`s to be returned
        :type themes: `Topic` or list of `Topic`s
        :param match_all: whether a `Occurrence`'s scope property must
          match all `themes`
        :type match_all: boolean
        :rtype: `QuerySet` of `Occurrence`s

        """
        occurrences = Occurrence.objects.filter(topic__topic_map=self.topic_map)
        if themes is not None:
            if isinstance(themes, Topic):
                occurrences = occurrences.filter(scope=themes)
            elif match_all:
                for theme in themes:
                    occurrences = occurrences.filter(scope=theme)
            else:
                query = None
                for theme in themes:
                    if query is None:
                        query = Q(scope=theme)
                    else:
                        query = query | Q(scope=theme)
                occurrences = occurrences.filter(query)
        else:
            if match_all:
                raise IllegalArgumentException(
                    'match_all must not be specified if themes is None')
            occurrences = occurrences.filter(scope=None)
        return occurrences.distinct()

    def get_occurrence_themes (self):
        """Returns the topics in the topic map used in the scope
        property of `Occurrence`s.

        The return value may be empty but must never be None.

        :rtype: `QuerySet` of `Topic`s

        """
        return self.topic_map.get_topics().exclude(scoped_occurrences=None)

    def get_variants (self, themes, match_all=False):
        """Returns the `Variant`s in the topic map whose scope
        property contains the specified `theme`, or one of the
        specified `themes` (if `match_all` is False), or all of the
        specified `themes` (if `match_all` is True).

        The return value may be empty but must never be None.

        :param theme: the `Topic` that must be part of the scope
        :type theme: `Topic`
        :param themes: scope of the `Variant`s to be returned
        :type themes: list of `Topic`s
        :param match_all: whether a `Variant`'s scope property must
          match all `themes`
        :type match_all: boolean
        :rtype: `QuerySet` of `Variant`s

        """
        variants = Variant.objects.filter(name__topic__topic_map=self.topic_map)
        if themes is not None:
            if isinstance(themes, Topic):
                variants = variants.filter(Q(scope=themes) |
                                           Q(name__scope=themes))
            elif match_all:
                for theme in themes:
                    variants = variants.filter(Q(scope=theme) |
                                               Q(name__scope=theme))
            else:
                query = None
                for theme in themes:
                    if query is None:
                        query = Q(scope=theme) | Q(name__scope=theme)
                    else:
                        query = query | Q(scope=theme) | Q(name__scope=theme)
                variants = variants.filter(query)
        else:
            raise IllegalArgumentException('themes must not be None')
        return variants.distinct()

    def get_variant_themes (self):
        """Returns the topics in the topic map used in the scope
        property of `Variant`s.

        The return value may be empty but must never be None.

        :rtype: `QuerySet` of `Topic`s

        """
        return self.topic_map.get_topics().exclude(scoped_variants=None,
                                                   scoped_names=None)
