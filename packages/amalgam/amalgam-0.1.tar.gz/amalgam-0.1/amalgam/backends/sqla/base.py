from sqlalchemy import exc, orm
from sqlalchemy.ext import declarative

from amalgam.utils import classproperty
from amalgam.backends.sqla.process import preprocess


class Meta(object):
    @classproperty
    def columns(cls):
        return cls.cls.__mapper__.iterate_properties


def create_meta(cls, bases, attrs):
    '''Add cls.Meta object for storing meta information
    '''
    meta = attrs.get('Meta') or type('Meta', (object, ), {})
    meta.cls = cls

    metabases = tuple(b.Meta for b in bases if hasattr(b, 'Meta')) + (Meta, )
    for mb in metabases:
        for k, v in mb.__dict__.items():
            if not k.startswith('_') and not hasattr(meta, k):
                setattr(meta, k, v)
    return meta


class DeclarativeMeta(declarative.DeclarativeMeta):
    def __init__(cls, name, bases, attrs):
        cls.Meta = create_meta(cls, bases, attrs) # everybody needs Meta

        # Quick check if it is model and not model base class. According to
        # SQLAlchemy docs, only base class will have 'metadata' attribute.
        if 'metadata' in attrs:
            return super(DeclarativeMeta, cls).__init__(name, bases, attrs)

        for k, v in preprocess(cls, attrs):
            if v is not None:
                setattr(cls, k, v)
            else:
                delattr(cls, k)

        super(DeclarativeMeta, cls).__init__(name, bases, attrs)


class Base(object):
    # Query interface
    query = None

    IntegrityError = exc.IntegrityError
    NotFound = orm.exc.NoResultFound
    MultipleResults = orm.exc.MultipleResultsFound

    @declarative.declared_attr
    def __tablename__(cls):
        prefix = getattr(cls.Meta, 'tableprefix', '')
        if prefix:
            prefix += '_'
        tablename = getattr(cls.Meta, 'tablename', cls.__name__.lower())
        return prefix + tablename

    def __unicode__(self):
        return unicode(self.pk)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self)

    @property
    def pk(self):
        return self.id # FIXME: try to find pk

    def save(self, flush=False):
        self.query._add(self, flush=flush)

    def delete(self):
        self.query._delete(self)
