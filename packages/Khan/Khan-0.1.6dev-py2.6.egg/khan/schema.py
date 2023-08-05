# -*- coding: utf-8 -*-

"""
数据转换与校验
=================================

索引
=================================

* :class:`SchemaType`
* :class:`String`
* :class:`Unicode`
* :class:`Regex`
* :class:`PlainText`
* :class:`Email`
* :class:`URL`
* :class:`Bool`
* :class:`SBool`
* :class:`Int`
* :class:`Float`
* :class:`Numeric`
* :class:`Choice`
* :class:`DateTime`
* :class:`List`
* :class:`Set`
* :class:`File`
* :class:`AsSet`
* :class:`AsList`
* :class:`Any`
* :class:`All`
* :class:`ValidationError`
* :class:`SchemaError`
* :class:`Schema`
* :class:`SchemaMapper`

=================================

.. autoclass:: SchemaType
.. autoclass:: String
.. autoclass:: Unicode
.. autoclass:: Regex
.. autoclass:: PlainText
.. autoclass:: Email
.. autoclass:: URL
.. autoclass:: Bool
.. autoclass:: SBool
.. autoclass:: Int
.. autoclass:: Float
.. autoclass:: Numeric
.. autoclass:: Choice
.. autoclass:: DateTime
.. autoclass:: List
.. autoclass:: Set
.. autoclass:: File
.. autoclass:: AsSet
.. autoclass:: AsList
.. autoclass:: Any
.. autoclass:: All
.. autoclass:: ValidationError
.. autoclass:: SchemaError
.. autoclass:: Schema
.. autoclass:: SchemaMapper
"""

import re, inspect, os
from datetime import datetime
from UserDict import DictMixin
from khan.utils import isiterable, NoDefault
from khan.utils.mapping import ismapping
from khan.utils.i18n import _

__all__ = ["String", "Unicode", "Bool", "Boolean", "SBool", "SBoolean", "Int", "Integer", "Float", 
           "Double", "Choice", "DateTime", "List", "Set", "AsList", "AsSet", "PlainText", 
           "Email", "URL", "All", "Any", "Regex", "File", "SchemaMapper", 
           "ValidationError", "SchemaError", "Schema", "SchemaType"]

class ValidationError(Exception): pass
    
def _setclassattr(self, name, kargs, default):
    if hasattr(self, name):
        setattr(self, name, kargs.pop(name, getattr(self, name)))
    else:
        self.__dict__[name] = kargs.pop(name, default) 
    
class SchemaTypeMeta(type):
    
    def __new__(cls, classname, bases, classdict):
        cls = type.__new__(cls, classname, bases, classdict)
        orig_init = cls.__init__
        def __init__(self, *args, **kargs):
            if not hasattr(self, "__SchemaTypeMeta__"):
                _setclassattr(self, "default", kargs, default = NoDefault)
                # FIXME: `nullable` 这个参数只是为了兼容以前的代码，请不要再使用
                _setclassattr(self, "nullable", kargs, default = True)
                _setclassattr(self, "required", kargs, default = not self.nullable)
                self.nullable = not self.required
                _setclassattr(self, "ignore", kargs, default = True)
                self.__SchemaTypeMeta__ = True
            orig_init(self, *args, **kargs)
        cls.__init__ = __init__
        return cls
        
class SchemaType(object):
    """
    子类的构造函数有如下 5 个参数::
        
        1. default - 默认值
        2. required - 被转换的值是否可为 None, 请使用 `required` 代替本参数名
        3. ignore - 当转换失败并且有设定 ``default`` 参数时，用 ``default`` 作为返回值
    
    TODO: 
    
        default 指定的值是否同样要校验一次? 比如 Int(default = "ssss").convert(None) 应该抛出异常, 
        因为 default 指定的值同样不能通过 Int 的转换, zope.schema 就是那么做的 
    """
    
    __metaclass__ = SchemaTypeMeta
    
    def convert(self, value):
        """
        将给出的值转换为某种 Python 类型
        
        :raise: 当转换失败应该抛出 :class:`Invalid`
        """
        
        if self.isnull(value):
            if self.nullable:
                if self.default is NoDefault:
                    return value
                else:
                    if callable(self.default):
                        return self.default()
                    else:
                        return self.default
            else:
                # FIXME: 这里是不是应该当 value = None，nullable = False 并且提供了默认值的时候，返回默认值?
                raise ValidationError(_("value %r invalid" % value))
        else:
            try:
                return self._to_python(value)
            except:
                if self.default is not NoDefault and self.ignore:
                    if callable(self.default):
                        return self.default()
                    else:
                        return self.default
                else:
                    raise
    
    def isnull(self, value):
        return value is None
    
    def convert_from(self, value):
        if self.isnull(value) and self.nullable:
            if self.default is NoDefault:
                raise ValidationError(_("value invalid"))
            else:
                if callable(self.default):
                    return self.default()
                else:
                    return self.default
        else:
            try:
                return self._from_python(value)
            except:
                if self.default is not NoDefault and self.ignore:
                    if callable(self.default):
                        return self.default()
                    else:
                        return self.default
                else:
                    raise
        
    def _to_python(self, value):
        """
        将给出的值转换为某种 Python 类型, 所有子类都应该实现本方法
        
        :raise: 当转换失败应该抛出 :class:`Invalid`
        """
        raise NotImplementedError
    
    def _from_python(self, value):
        return value
    
    def __or__(self, other_schema_type):
        return Any(self, other_schema_type)
    
    def __and__(self, other_schema_type):
        return All(self, other_schema_type)
    
class StringTypeMeta(SchemaTypeMeta):
    
    def __new__(cls, classname, bases, classdict):
        cls = SchemaTypeMeta.__new__(cls, classname, bases, classdict)
        orig_init = cls.__init__
        orig_to_python = cls._to_python
        def __init__(self, *args, **kargs):
            if not hasattr(self, "__StringTypeMeta__"):
                _setclassattr(self, "min", kargs, default = None)
                _setclassattr(self, "max", kargs, default = None)
                _setclassattr(self, "strip", kargs, default = False)
                self.__StringTypeMeta__ = True
            orig_init(self, *args, **kargs)
        def _to_python(self, value):
            if self.strip and isinstance(value, basestring):
                value = value.strip()
            value = orig_to_python(self, value)
            if self.max is not None and len(value) > self.max:
                raise ValidationError(_("value greater than %(max)i characters long") % dict(max = self.max))
            if self.min is not None and (len(value) < self.min):
                raise ValidationError(_("value less than %(min)i characters long") % dict(min = self.min))
            return value
        cls.__init__ = __init__
        cls._to_python = _to_python
        return cls
        
class BaseString(SchemaType):
    
    __metaclass__ = StringTypeMeta
     
class String(BaseString):
    
    def __init__(self, encoding = "utf-8"):
        self.encoding = encoding
        
    def _to_python(self, value):
        if not value:
            value = ""
        if not isinstance(value, basestring):
            try:
                value = str(value)
            except UnicodeEncodeError:
                value = unicode(value)
        if self.encoding is not None and isinstance(value, unicode):
            value = value.encode(self.encoding)
        return value
    
class Unicode(String):

    encoding = "utf-8"
    
    iencoding = NoDefault

    def __init__(self, **kw):
        super(Unicode, self).__init__(**kw)
        if self.iencoding is NoDefault:
            self.iencoding = self.encoding

    def _to_python(self, value):
        # String 转换器
        value = super(Unicode, self)._to_python(value)
        if not value:
            return u""
        if isinstance(value, unicode):
            return value
        if not isinstance(value, unicode):
            if hasattr(value, "__unicode__"):
                value = unicode(value)
                return value
            else:
                value = str(value)
        if self.iencoding:
            try:
                value = unicode(value, self.iencoding)
            except UnicodeDecodeError:
                raise ValidationError(_("Invalid data or incorrect encoding"))
            except TypeError:
                raise ValidationError(_("The `value` must be a string (not a %(type)s: %(value)r)" 
                                %(dict(type = type(value), value = value))))
        return value

class Regex(BaseString):
    
    def __init__(self, pattern):
        self.regex = re.compile(pattern)
        
    def _to_python(self, value):
        if not isinstance(value, (str, unicode)):
            raise ValidationError(_("The `value` must be a string (not a %(type)s: %(value)r)") 
                          % dict(type = type(value), value = value))
        if not self.regex.search(value):
            raise ValidationError(_('Value invalid'))
        return value
    
class PlainText(Regex):

    pattern = r"^[a-zA-Z_\-0-9]*$"
    
    def __init__(self):
        super(PlainText, self).__init__(self.pattern)
   
class Email(BaseString):

    usernameRE = re.compile(r"^[^ \t\n\r@<>()]+$", re.I)
    domainRE = re.compile(r'''
        ^(?:[a-z0-9][a-z0-9\-]{0,62}\.)+ # (sub)domain - alpha followed by 62max chars (63 total)
        [a-z]{2,}$                       # TLD
    ''', re.I | re.VERBOSE)

    def _to_python(self, value):
        if not value:
            raise ValidationError(_("Email address invalid"))
        value = value.strip()
        splitted = value.split('@', 1)
        try:
            username, domain=splitted
        except ValueError:
            raise ValidationError(_("An email address must contain a single @"))
        if not self.usernameRE.search(username):
            raise ValidationError(_('The username portion of the email address is invalid (the portion before the @: %(username)s)') 
                          % dict(username=username))
        if not self.domainRE.search(domain):
            raise ValidationError(_('The domain portion of the email address is invalid (the portion after the @: %(domain)s)') 
                          % dict(domain = domain))
        return value.strip()

class URL(BaseString):

    add_http = True
    require_tld = True

    url_re = re.compile(r'''
        ^(http|https)://
        (?:[%:\w]*@)?                           # authenticator
        (?P<domain>[a-z0-9][a-z0-9\-]{1,62}\.)* # (sub)domain - alpha followed by 62max chars (63 total)
        (?P<tld>[a-z]{2,})                      # TLD
        (?::[0-9]+)?                            # port

        # files/delims/etc
        (?P<path>/[a-z0-9\-\._~:/\?#\[\]@!%\$&\'\(\)\*\+,;=]*)?
        $
    ''', re.I | re.VERBOSE)

    scheme_re = re.compile(r'^[a-zA-Z]+:')

    def _to_python(self, value):
        value = value.strip()
        if self.add_http:
            if not self.scheme_re.search(value):
                value = 'http://' + value
        match = self.scheme_re.search(value)
        if not match:
            raise ValidationError(_('You must start your URL with http://, https://, etc'))
        value = match.group(0).lower() + value[len(match.group(0)):]
        match = self.url_re.search(value)
        if not match:
            raise ValidationError(_('That is not a valid URL'))
        if self.require_tld and not match.group('domain'):
            raise ValidationError(_('You must provide a full domain name (like %(domain)s.com)') 
                          % dict(domain = match.group('tld')))
        return value
                
class Bool(SchemaType):
    
    def _to_python(self, value):
        return bool(value)
    
    def isnull(self, value):
        return False
    
Boolean = Bool

class SBool(Bool):

    true_values = ['true', 't', 'yes', 'y', 'on', '1']
    false_values = ['false', 'f', 'no', 'n', 'off', '0']

    def _to_python(self, value):
        if isinstance(value, (str, unicode)):
            value = value.strip().lower()
            if value in self.true_values:
                return True
            if \
                   not value or \
                   value in self.false_values:
                return False
            raise ValidationError(_("Value should be %(true)r or %(false)r" % 
                            dict(true = self.true_values[0], false = self.false_values[0])))
        return bool(value)
    
SBoolean = SBool

class NumberRangeType(SchemaType):
    
    def __init__(self, min = None, max = None):
        self.min = min
        self.max = max
    
    def try_to_convert(self, value):
        raise NotImplementedError
    
    def _to_python(self, value):
        value = self.try_to_convert(value)
        self.validate(value)
        return value
    
    def validate(self, value):
        if self.min is not None:
            if value < self.min:
                raise ValidationError(_("Please enter a number that is %(min)s or greater") % dict(min = self.min))
        if self.max is not None:
            if value > self.max:
                raise ValidationError(_("Please enter a number that is %(max)s or smaller") % dict(max = self.max))
        
class Int(NumberRangeType):
    
    def try_to_convert(self, value):
        try:
            return int(value)
        except:
            raise ValidationError(_("Value should be a integer"))
    
Integer = Int

class Float(NumberRangeType):
    
    def try_to_convert(self, value):
        try:
            return float(value)
        except:
            raise ValidationError(_("Value should be a float number"))
    
Double = Float

class Numeric(NumberRangeType):
    
    def try_to_convert(self, value):
        try:
            value = float(value)
            try:
                int_value = int(value)
            except OverflowError:
                int_value = None
            if value == int_value:
                return int_value
            return value
        except ValueError:
            raise ValidationError(_("Please enter a number"))
            
class Choice(SchemaType):

    def __init__(self, values):
        assert isiterable(values), ValueError("`values` not iterable.")
        self.elements = values
    
    def _to_python(self, value):
        if value in self.elements:
            return value
        else:
            raise ValidationError(_("Value %(value)r not in range(%(rg)r)") % dict(value = value, rg = self.elements))
    
class DateTime(SchemaType):
    
    FORMAT = "%Y-%m-%d %H:%M:%S"
    
    def __init__(self, fmt = FORMAT):
        self.fmt = fmt
    
    def _to_python(self, value):
        try:
            return datetime.strptime(value, self.fmt)
        except:
            raise ValidationError(value)

class List(SchemaType):
    '''

    Example::
    
       a = List(String())
       b = List(String(), default = range(0, 100)) # raise ValidationError
       b = List(Int(), default = range(0, 100)) # success
       
    '''
    
    def __init__(self, type):
        self._type = type

    def container(self, value):
        return list
    
    def _to_python(self, value):
        assert isiterable(value), ValidationError(_("Value not iterable."))
        return self.container(value)(map(lambda x : self._type.convert(x), value))
    
    def _from_python(self, value):
        assert isiterable(value), ValidationError(_("Value not iterable."))
        return self.container(value)(map(lambda x : self._type.convert_from(x), value))

class Set(List):
    
    def container(self, value):
        return set

class File(SchemaType):
    '''
    f = File()                   # supported any type to upload
    f = File("png,jpeg,gif,jpg") # only supported file type in "png, jpeg, gif, jpg"
    '''

    def __init__(self, types_supported=None):
        if not types_supported is None:
            self._types_supported = '\.(%s)$' % \
                '|'.join([str(t).strip() for t in types_supported.split(',')])

    def _is_supported(self, path):
        return not self._types_supported is None and \
                   not re.search(self._types_supported, path) is None
        
    def _to_python(self, val):
        fname = os.path.abspath(val)
        if os.path.isfile(fname):
            if not self._is_supported(fname):
                raise ValidationError(_("file types not supported: '%s'") % fname)
            
            return file(fname)
        else:
            raise ValidationError(_("no such file '%s'") % fname)
    
    def _from_python(self, val):
        if hasattr(val, "read") and hasattr(val, "name") and val.name:
            if not self._is_supported(val.name):
                raise ValidationError(_("file types not supported: '%s'") % val.name)
            return val.name
        else:
            raise ValidationError(_("file object %r invalid") % val)
        
class AsList(List):
    
    def __init__(self, type, sep = None):
        self.sep = sep
        super(AsList, self).__init__(type)
        
    def _to_python(self, value):
        assert isinstance(value, basestring), ValidationError(_("Value is not a string."))
        value = value.strip()
        value = value.split(self.sep)
        return super(AsList, self)._to_python(value)
    
    def _from_python(self, value):
        value = super(AsList, self)._from_python(value)
        sep = self.sep or " "
        return sep.join(value)
        
class AsSet(AsList):
    
    def container(self, value):
        return set
    
class Any(SchemaType):
    
    def __init__(self, *types):
        assert types, ValueError("`types` invalid.")
        self.types = types
    
    def _to_python(self, value):
        errors = []
        for t in self.types:
            try:
                return t.convert(value)
            except ValidationError, e:
                errors.append(e)
        raise errors[0]
    
class All(SchemaType):
    
    def __init__(self, *types):
        assert types, ValueError("`types` invalid.")
        self.types = types
    
    def _to_python(self, value):
        results = []
        for t in self.types:
            try:
                results.append(t.convert(value))
            except ValidationError, e:
                raise e
        return results[0]
    
class SchemaError(ValidationError):
    
    def __init__(self, name, field = None, e = None):
        self.name = name
        self.field = field
        if e:
            msg = "`%(name)s` filed error - %(invalid)s" % dict(name = name, invalid = e)
            self.exception = e
        else:
            msg = "'%(name)s' filed error" % name 
            self.exception = Exception(msg)
        super(SchemaError, self).__init__(msg)
            
    def __repr__(self):
        return "<%(name)s field> - %(invalid)s" % dict(name = self.name, invalid = self.exception)
        
class Schema(SchemaType, DictMixin):
    """
    Example::
        
        from schema import Schema, SchemaError
        
        class MySchema(Schema):
        
            name = String(default = "a")
            desc = String(default = lambda : "sss")
        
        schema = MySchema()
        
        try:
            result = schema.convert(req.POST)
        except SchemaError, e:
            pass
    """
    
    def __init__(self, *args, **kargs):
        self.__dict__["allow_extra_fields"] = kargs.pop("allow_extra_fields", True)
        self.__dict__["filter_extra_fields"] = kargs.pop("filter_extra_fields", False)
        self.__dict__.update(dict(*args, **kargs))
    
    def __repr__(self):
        return "<%s %s>" % (self.__class__, repr(dict(self)))
    
    def __setitem__(self, name, value):
        assert isinstance(name, basestring) and not name.startswith("_"), \
            ValueError("`name` must not starts with '_'")
        if not isinstance(value, SchemaType):
            raise TypeError(name)
        setattr(self, name, value)
        
    def __getitem__(self, name):
        value = getattr(self, name)
        if not isinstance(value, SchemaType):
            raise KeyError(name)
        return value
    
    def __delitem__(self, name):
        self.__getitem__(name)
        delattr(self, name)
    
    def keys(self):
        return dict(filter(lambda x : not x[0].startswith("_") and isinstance(x[1], SchemaType), 
                           inspect.getmembers(self))).keys()
    
    def isnull(self, value):
        return False
    
    def _to_python(self, data):
        if not data:
            data = {}
        members = self.keys()
        result = {}
        keys = set(data.keys() + members)
        for k in keys:
            if k in members:
                convertter = getattr(self, k)
                if k not in data:
                    try:
                        result[k] = convertter.convert(None)
                    except ValidationError, e:
                        raise SchemaError(k, convertter, e)
                    except:
                        # FIXME: 这里是否需要转换成 SchemaError 抛出？
                        raise
                    continue
                else:
                    v = data[k]
                if not isinstance(convertter, SchemaType):
                    if self.allow_extra_fields:
                        if not self.filter_extra_fields:
                            result[k] = v
                            continue
                    else:
                        raise SchemaError(k, convertter, Exception("unknown field '%s'" % k))
                try:
                    result[k] = convertter.convert(v)
                except ValidationError, e:
                    raise SchemaError(k, convertter, e)
                except:
                    # FIXME: 这里是否需要转换成 SchemaError 抛出？
                    raise
            else:
                if self.allow_extra_fields:
                    if not self.filter_extra_fields:
                        result[k] = data[k]
                else:
                    raise SchemaError(k, None, Exception("unknown field '%s'" % k))
        return result

class SchemaMapper(DictMixin, object):
    """
    Example::
        
        from khan.schema import Schema, Invalid
        from khan.store import XMLStore 
        
        class MySchema(Schema):
        
            id = Integer()
            desc = String(default = lambda : "sss")
        
        data = SchemaMapper(MySchema(), XMLStore("/tmp/a.xml"))
        data["id"] = 1
        data["id"] = "a" # raised Invalid exception
    """
    
    def __init__(self, schema, source):
        assert isinstance(schema, Schema), TypeError("`schema` should be a ``Schema`` instance")
        self.schema = schema
        self.source = source
        self.data = schema.convert(source)
        if self.data:
            self.__dict__.update(self.data)
    
    def __setitem__(self, key, val):
        schema = self.schema
        if key not in schema:
            raise AttributeError("member %(name)s not exists." % dict(name = key))
        schema_type = schema[key]
        new_val = None
        try:
            new_val = schema_type.convert_from(val)
        except:
            raise AttributeError(key)
        setattr(self, key, new_val)
        self.source[key] = new_val
        self.data[key] = new_val
    
    def __getitem__(self, key):
        val = getattr(self, key)
        if ismapping(val):
            if key in self.schema:
                sub_schema = self.schema[key]
                return SchemaMapper(sub_schema, val)
            else:
                raise KeyError(key)
        else:
            return val
        
    def __delitem__(self, key):
        delattr(self, key)
        del self.data[key]
        del self.source[key]
        
    def keys(self):
        return self.data.keys()
