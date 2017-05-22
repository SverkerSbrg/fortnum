from collections import OrderedDict, Sized


class FortnumException(Exception):
    pass


class DuplicatedFortnum(FortnumException):
    pass


class FortnumDoesNotExist(FortnumException):
    pass


class MultipleParents(FortnumException):
    pass


class class_property(classmethod):
    def __get__(self, instance, owner):
        return super().__get__(instance, owner)()


class FortnumRelation:
    def __init__(self, related_name, many=False):
        self.related_name = related_name
        self.many = many


class FortnumMeta(type):
    _registry = {}

    @classmethod
    def __prepare__(mcs, name, bases):
        return OrderedDict()

    def __new__(mcs, name, bases, classdict):
        if name in mcs._registry:
            raise DuplicatedFortnum()

        # Create Fortnum class and add to registry
        fortnum = type.__new__(mcs, name, bases, dict(classdict))
        mcs._registry[name] = fortnum

        # Identify children and register parent connections
        if fortnum.item_class:
            fortnum.children = OrderedDict((
                (key, value)
                for key, value in classdict.items()
                if issubclass(type(value), fortnum.item_class))
            )

            for index, child in enumerate(fortnum.children.values()):
                if child.parents is None:
                    child.parents = []
                child.parents.append(fortnum)
        else:
            fortnum.children = OrderedDict()

        # Find relations defined on base classes and add them to the objects.
        for base in bases:
            for key, relation in (
                    (key, relation)
                    for key, relation
                    in base.__dict__.items()
                    if issubclass(relation.__class__, FortnumRelation)
            ):
                related_fortnums = classdict[key] if relation.many else [classdict[key]]

                for related_fortnum in related_fortnums:
                    if related_fortnum:
                        if not hasattr(related_fortnum, relation.related_name):
                            setattr(related_fortnum, relation.related_name, set())
                        getattr(related_fortnum, relation.related_name).add(fortnum)

        return fortnum

    def __iter__(self):
        for fortnum in self.children.values():
            yield fortnum

    def __getitem__(self, item):
        return self.children.__getitem__(item)

    def __len__(self):
        return len(self.children)

    def __bool__(self):
        return True

    def serialize(cls):
        return cls.__name__

    def deserialize(cls, name):
        try:
            return cls._registry[name]
        except KeyError:
            raise FortnumDoesNotExist()

    def descendants(cls):
        for child in cls:
            yield child

            for descendant in child.descendants():
                yield descendant

    def __str__(self):
        return self.__name__

    def __repr__(self):
        return str(self)

    @property
    def choices(self):
        return ((str(item), str(item)) for item in self.__iter__())


class Fortnum(metaclass=FortnumMeta):
    parents = None  # Set by Metaclass
    children = None  # Set by Metaclass
    item_class = FortnumMeta

    def __new__(cls, name, **kwargs):
        # Allow fetching of already defined fortnums.
        try:
            return Fortnum.deserialize(name)
        except FortnumDoesNotExist:
            return FortnumMeta(name, (Fortnum,), kwargs)

    @classmethod
    def serialize(cls):
        return cls.__name__

    @classmethod
    def deserialize(cls, name):
        return FortnumMeta.deserialize(cls, name)

    @class_property
    def parent(cls):
        if not cls.parents:
            return None

        if len(cls.parents) == 1:
            return cls.parents[0]

        raise MultipleParents