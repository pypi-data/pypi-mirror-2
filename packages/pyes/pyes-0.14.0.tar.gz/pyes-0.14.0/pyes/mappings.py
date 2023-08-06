#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Alberto Paro'

check_values = [
                ('index', ['no', 'analyzed', 'not_analyzed']),
                ('term_vector', ['no', 'yes', 'with_offsets', 'with_positions', 'with_positions_offsets']),
                ('type', ['float', 'double', 'integer', 'long']),
                ]
from utils import keys_to_string
import threading

_thread_locals = threading.local()
#store threadsafe data


class AbstractField(object):
    def __init__(self, index="not_analyzed", store = "no", boost=1.0, 
                 term_vector="no", omit_norms=True, 
                 omit_term_freq_and_positions=True, 
                 type=None, index_name=None,
                 index_analyzer=None,
                 search_analyzer=None, 
                 name=None):
        self.store = store
        self.boost = boost
        self.term_vector = term_vector
        self.index = index
        self.omit_norms = omit_norms
        self.omit_term_freq_and_positions = omit_term_freq_and_positions
        self.index_name = index_name
        self.type = type
        self.index_analyzer = index_analyzer
        self.search_analyzer = search_analyzer
        self.name = name

    def to_json(self):
        result = {"type":self.type,
                  'index':self.index}
        if self.store != "no":
            if isinstance(self.store, bool):
                if self.store:
                    result['store'] = "yes"
                else:
                    result['store'] = "no"
            else:
                result['store'] = self.store
        if self.boost != 1.0:
            result['boost'] = self.boost
        if self.term_vector != "no":
            result['term_vector'] = self.term_vector
        if self.omit_norms != True:
            result['omit_norms'] = self.omit_norms
        if self.omit_term_freq_and_positions != True:
            result['omit_term_freq_and_positions'] = self.omit_term_freq_and_positions
        if self.index_name:
            result['index_name'] = self.index_name
        if self.index_analyzer:
            result['index_analyzer'] = self.index_analyzer
        if self.search_analyzer:
            result['search_analyzer'] = self.search_analyzer

        return result

class StringField(AbstractField):
    def __init__(self, null_value=None, include_in_all=None, *args, **kwargs):
        super(StringField, self).__init__(**kwargs)
        self.null_value = null_value
        self.include_in_all = include_in_all        
        self.type = "string"
        
    def to_json(self):
        result = super(StringField, self).to_json()
        if self.null_value is not None:
            result['null_value'] = self.null_value
        if self.include_in_all is not None:
            result['include_in_all'] = self.include_in_all
        return result

class NumericFieldAbstract(AbstractField):
    def __init__(self, null_value=None, include_in_all=None, precision_step=4,
                 **kwargs):
        super(NumericFieldAbstract, self).__init__(**kwargs)
        self.null_value = null_value
        self.include_in_all = include_in_all 
        self.precision_step = precision_step

    def to_json(self):
        result = super(NumericFieldAbstract, self).to_json()
        if self.null_value is not None:
            result['null_value'] = self.null_value
        if self.include_in_all is not None:
            result['include_in_all'] = self.include_in_all
        if self.precision_step!=4:
            result['precision_step'] = self.precision_step
        return result

class IntegerField(NumericFieldAbstract):
    def __init__(self, *args, **kwargs):
        super(IntegerField, self).__init__(*args, **kwargs)
        self.type = "integer"

class LongField(NumericFieldAbstract):
    def __init__(self, *args, **kwargs):
        super(LongField, self).__init__(*args, **kwargs)
        self.type = "long"

class DoubleField(NumericFieldAbstract):
    def __init__(self, *args, **kwargs):
        super(DoubleField, self).__init__(*args, **kwargs)
        self.type = "double"

class DateField(NumericFieldAbstract):
    def __init__(self, format=None, **kwargs):
        super(DateField, self).__init__(**kwargs)
        self.format = format
        self.type = "date"

    def to_json(self):
        result = super(DateField, self).to_json()
        if self.format:
            result['format'] = self.format
        return result
    
class BooleanField(AbstractField):
    def __init__(self, null_value=None, include_in_all=None, *args, **kwargs):
        super(BooleanField, self).__init__(*args, **kwargs)
        self.null_value = null_value
        self.include_in_all = include_in_all
        self.type = "boolean"
        
    def to_json(self):
        result = super(BooleanField, self).to_json()
        if self.null_value is not None:
            result['null_value'] = self.null_value
        if self.include_in_all is not None:
            result['include_in_all'] = self.include_in_all
        return result

class MultiField(object):
    def __init__(self, name=None, type=None, path=None, fields=None):
        self.name = name
        self.type = "multi_field"
        self.path = path
        self.fields = {}
        if fields:
            self.fields = dict([(name, get_field(name, data)) for name, data in fields.items()])
        
    def to_json(self):
        result = {"type": self.type,
                  "fields": {}}
        if self.fields:
            for name, value in self.fields.items():
                result['fields'][name]=value.to_json()
        return result

class ObjectField(object):
    def __init__(self, name=None, type=None, path=None, properties=None, 
                 dynamic=None, enabled=None, include_in_all=None):
        self.name = name
        self.type = "object"
        self.path = path
        self.properties = properties
        self.include_in_all = include_in_all
        self.dynamic = dynamic
        self.enabled = enabled
        if properties:
            self.properties = dict([(name, get_field(name, data)) for name, data in properties.items()])
        else:
            self.properties = {}

    def add_property(self, prop):
        """
        Add a property to the object
        """
        self.properties[prop.name] = prop

    def to_json(self):
        result = {"type": self.type,
                  "properties": {}}
        if self.dynamic is not None:
            result['dynamic'] = self.dynamic
        if self.enabled is not None:
            result['enabled'] = self.enabled
        if self.include_in_all is not None:
            result['include_in_all'] = self.include_in_all
        if self.path is not None:
            result['path'] = self.path
            
        if self.properties:
            for name, value in self.properties.items():
                result['properties'][name]=value.to_json()
        return result

class DocumentObjectField(object):
    def __init__(self, name=None, type=None, path=None, properties=None, 
                 dynamic=None, enabled=None, _all=None, _boost=None, _id=None,
                 _index=None, _source=None, _type=None, date_formats=None):
        self.name = name
        self.type = "object"
        self.path = path
        self.properties = properties
        self.dynamic = dynamic
        self.enabled = enabled
        self._all = _all
        self._boost = _boost
        self._id = _id
        self._index = _index
        self._source = _source
        self._type = _type
        self.date_formats = date_formats
        if properties:
            self.properties = dict([(name, get_field(name, data)) for name, data in properties.items()])

    def to_json(self):
        result = {"type": self.type,
                  "properties": {}}
        if self.dynamic is not None:
            result['dynamic'] = self.dynamic
        if self.enabled is not None:
            result['enabled'] = self.enabled
        if self.path is not None:
            result['path'] = self.path
        if self._all is not None:
            result['_all'] = self._all
        if self._boost is not None:
            result['_boost'] = self._boost
        if self._id is not None:
            result['_id'] = self._id
        if self._index is not None:
            result['_index'] = self._index
        if self._source is not None:
            result['_source'] = self._source
        if self._type is not None:
            result['_type'] = self._type
        
        if self.properties:
            for name, value in self.properties.items():
                result['properties'][name]=value.to_json()
        return result
    
    def __unicode__(self):
        return "<DocumentObjectField:%s>" % self.to_json()

def get_field(name, data):
    data = keys_to_string(data)
    type = data.get('type', 'object')
    if type=="string":
        return StringField(name=name, **data)
    elif type=="boolean":
        return BooleanField(name=name, **data)
    elif type=="integer":
        return IntegerField(name=name, **data)
    elif type=="long":
        return LongField(name=name, **data)
    elif type=="double":
        return DoubleField(name=name, **data)
    elif type=="date":
        return DateField(name=name, **data)
    elif type=="multi_field":
        return MultiField(name=name, **data)
    elif type=="object":
        if '_all' in data:
            return DocumentObjectField(name=name, **data)
            
        return ObjectField(name=name, **data)
    raise RuntimeError("Invalid type: %s"%type)
        
class Mapper(object):
    def __init__(self, data):
        self.indexes = {}
        self._process(data)
    
    def _process(self, data):
        """
        Process indexer data
        """
        for indexname, indexdata in data.items():
            self.indexes[indexname] = {}
            for docname, docdata in indexdata.items():
                self.indexes[indexname][docname] = get_field(docname, docdata)
                
    def get_doctype(self, index, name):
        """
        Returns a doctype given an index and a name
        """
        return self.indexes[index][name]
    
        
            
#u'index_name': u'id',
#u'precision_step': 4,
#u'type': u'long'

#class IndexData(object):
#    pass
#
#class IndexedType(object):
#    pass
#
#class Field(object):
#    def  __init__(self, name, 
#                  index=u'analyzed', type=u'string', 
#                  omit_term_freq_and_positions=False, omit_norms=False, 
#                  index_name=u'name', 
#                  term_vector=u'no', boost=1.0, store=u'no',
#                  analyzer = None, index_analyzer=None, search_analyzer=None):
#        self.name = name
#        self.index = index  
#        self.type = type
#        self.omit_term_freq_and_positions = omit_term_freq_and_positions
#        self.omit_norms = omit_norms
#        self.index_name = index_name
#        self.term_vector = term_vector
#        self.boost = boost
#        self.store = store
#        self.analyzer = analyzer
#        self.index_analyzer = index_analyzer
#        self.index_analyzer = index_analyzer
#        self.null_value = None
#        
#    def serialize(self):
#        self._validate()
#        parameters = []
#        return {
#                self.name:{
#                    'index' : self.index,
#                    'type' : self.type,
#                    'omit_term_freq_and_positions' : self.omit_term_freq_and_positions,
#                    'omit_norms' : self.omit_norms,
#                    'index_name' : self.index_name,
#                    'term_vector' : self.term_vector,
#                    'boost' : self.boost,
#                    'store' : self.store,
#                    }
#                }