from resolver import app
from resolver.database import db
from resolver.model import Document
from resolver.util import log
import resolver.kvstore as kvstore

data_formats = ('html', 'json', 'xml', 'pdf')

class Data(Document):
    __tablename__ = 'data'
    id = db.Column(db.Integer, db.ForeignKey('document.id'), primary_key=True)
    _format = db.Column('format', db.Enum(*data_formats, name='Format'))

    __mapper_args__ = {
        'polymorphic_identity':'data'
    }

    def __init__(self, entity, format, url=None, enabled=True, notes=None):
        super(Data, self).__init__(entity, url=url, enabled=enabled, notes=notes)
        if format in data_formats:
            self.format = format
        else:
            raise Exception("Incorrect data format")

    def __repr__(self):
        return '<Data(%s), entity=%s, format=%s, url=%s>' %\
            (self.id, self.entity_id, self.format, self.url)

    @property
    def persistent_uri(self):
        uri = app.config['BASE_URL']
        uri += '/collection/%s/data/%s/%s' % (self.entity.type, self.entity_id,
                                              self.format)

        if kvstore.get('titles_enabled'):
            return [uri, uri+'/'+self.entity.slug]
        else:
            return [uri]

    def to_dict(self):
        dict = super(Data, self).to_dict()
        dict['format'] = self.format
        return dict

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, value):
        if value not in data_formats:
            raise Exception("Incorrect data format")
        if self._format != value:
            log(self.entity_id, "Changed format from '%s' to '%s' for %s" %
                (self._format, value, self))

        self._format = value

    format = db.synonym('_format', descriptor=format)
