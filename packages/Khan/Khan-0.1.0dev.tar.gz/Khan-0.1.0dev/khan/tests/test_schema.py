# -*- coding: utf-8 -*-

from khan.schema import *
from khan.utils.testing import *

class SchemaEntity(Schema):

    a = String()
    a_ = String(default = 'b_value')
    b = Int()
    b_ = Int(default = 1)
    c = Unicode()
    c_ = Unicode(default = u'd_value')
    d = Boolean()
    d_ = Boolean(default = True)
    e = SBoolean()
    e_ = SBoolean(default = 'on')
    f = Float()
    f_ = Float(default = .1)
    g = Double()
    g_ = Double(default = .2)
    h = Choice(range(0, 100))
    j = DateTime()
    j_ = DateTime(default = "2009-12-12 12:12:12")
    k = List(Int())
    k_ = List(Int(), default = range(20, 30))
    l = Set(Int())
    l_ = Set(Int(), default = set(range(40, 50)))
    m = PlainText()
    m_ = PlainText(default = 'abcd1234')
    n = Email()
    n_ = Email(default = 'test@test.com')
    o = URL()
    o_ = URL(default = 'http://test.com')

class TestSchema(TestCase):

    def setUp(self):
        self.schema = SchemaEntity()

    def test_string(self):
        self.assertEqual('base string', String().convert('base string'), 'string convert failed')
        self.assertEqual(u'unicode string', String().convert(u'unicode string'),
                         'string convert unicode failed')
        self.assertEqual('中文', String().convert(u'中文'), 'string convert unicode failed')
        self.assertEqual('中文', String(default = '中文').convert(None), 'string convert failed')

        # other type to str
        self.assertEqual('1', String().convert(1), 'string convert failed')
        self.assertEqual('True', String().convert(True), 'string convert failed')
        self.assertRaises(ValidationError, lambda x:String(required = True).convert(None), 'string convert failed')
        self.assertRaises(ValidationError, lambda x:String(min = 2).convert("1"), 'string convert failed')
        self.assertRaises(ValidationError, lambda x:String(max = 2).convert("123"), 'string convert failed')
        self.assertRaises(ValidationError, lambda x:String(min = 1, max = 3).convert("1234"), 'string convert failed')

    def test_unicode(self):
        self.assertEqual('base string', Unicode().convert('base string'), 'unicode convert failed')
        self.assertEqual(u'unicode string', Unicode().convert(u'unicode string'),
                         'unicode convert unicode failed')
        self.assertEqual(u'中文', Unicode().convert(u'中文'), 'unicode convert unicode failed')
        self.assertEqual(u'中文', Unicode(default = u'中文').convert(None), 'unicode convert failed')
        self.assertEqual(u'中文', Unicode(default = u'中文').convert(None), 'unicode convert failed')
        # default not encode
        self.assertEqual('中文', Unicode(default = '中文').convert(None), 'default not encode')

        # other type
        self.assertEqual('1', Unicode().convert(1), 'unicode convert failed')
        self.assertEqual(u'1', Unicode().convert(1), 'unicode convert failed')
        self.assertEqual('True', Unicode().convert(True), 'unicode convert failed')
        self.assertEqual(u'True', Unicode().convert(True), 'unicode convert failed')
        self.assertRaises(ValidationError, lambda x:Unicode(required = True).convert(None), 'unicode convert failed')
        
    def test_int(self):
        self.assertEqual(1, Int().convert(1), 'int convert failed')
        self.assertEqual(1, Int(default = 1).convert(None), 'int convert failed')

    def test_boolean(self):
        self.assertEqual(True, Boolean().convert(True), 'boolean convert failed')
        self.assertNotEqual(True, Boolean().convert(False), 'boolean convert failed')
        self.assertNotEqual(True, Boolean(default = True).convert(None), 'boolean convert failed')

    def test_sbool(self):
        for i in ['on', 'true', 'True', 'tRuE', -1, .1, True]:
            self.assertEqual(True, SBool().convert(i), 'boolean convert failed')

        for i in ['off', 'false', 'False', 'fAlSe', '', None]:
            self.assertEqual(False, SBool().convert(i), 'boolean convert failed')

        for i in ['other str', 'base string']:
            self.assertRaises(ValidationError, lambda x:SBool().convert(i),
                              'boolean convert failed')

    def test_float(self):
        self.assertEqual(.1, Float().convert(.1), 'float convert failed')
        self.assertEqual(1.0, Float().convert(1), 'float convert failed')
        self.assertRaises(ValidationError, lambda x:Float().convert('str'), 'float convert failed')

    def test_double(self):
        self.assertEqual(.1, Double().convert(.1), 'float convert failed')
        self.assertEqual(1.0, Double().convert(1), 'float convert failed')
        self.assertEqual(1.0, Double(default = 1.0).convert(None), 'float convert failed')
        self.assertRaises(ValidationError, lambda x:Double().convert('str'), 'float convert failed')

    def test_choice(self):
        self.assertEqual(1, Choice(range(0, 100)).convert(1), 'choice convert failed')
        self.assertRaises(ValidationError, lambda x:Choice(range(0, 10)).convert(100), 'choice convert failed')

    def test_datetime(self):
        import datetime
        self.assertEqual(
            datetime.datetime(2009, 12, 12, 12, 12, 12),
            DateTime().convert('2009-12-12 12:12:12'), 'datetime convert failed')
        self.assertEqual(
            datetime.datetime(2009, 12, 12),
            DateTime(fmt='%Y-%m-%d').convert('2009-12-12'), 'datetime convert failed')
        
        self.assertRaises(ValidationError, lambda x:DateTime().convert('2009-12-12 12:12'), 'datetime convert failed')

    def test_list(self):
        self.assertEqual(range(0, 100), List(Int()).convert(range(0, 100)), 'list convert failed')
        self.assertEqual(['str', 'other'], List(String()).convert(['str', 'other']), 'list convert failed')

        self.assertRaises(ValidationError, lambda x:List(Int()).convert(['str', 'other']), 'list convert with type')
        self.assertEqual(['1', '2'], List(String()).convert(range(1, 3)), 'list convert with type')
        self.assertEqual(['', '1'], List(String()).convert(range(0, 2)), 'list convert with type')

    def test_set(self):
        self.assertEqual(set(range(0, 100)), Set(Int()).convert(range(0, 100)), 'list convert failed')
        self.assertEqual(set(['str', 'other']), Set(String()).convert(['str', 'other']), 'list convert failed')

        self.assertRaises(ValidationError, lambda x:Set(Int()).convert(['str', 'other']), 'list convert with type')
        self.assertEqual(set(['1', '2']), Set(String()).convert(range(1, 3)), 'list convert with type')
        self.assertEqual(set(['', '1']), Set(String()).convert(range(0, 2)), 'list convert with type')

        # 与List不同，每个值唯一
        self.assertEqual(set(range(0, 3)), Set(Int()).convert([0, 1, 2, 2]), 'list convert failed')
        self.assertEqual(set(['str', 'other']), Set(String()).convert(['str', 'str', 'other']), 'list convert failed')

    def test_email(self):
        self.assertEqual('test@test.com', Email().convert('test@test.com'), 'email convert failed')
        self.assertEqual('test@default.com', Email(default = 'test@default.com').convert(None), 'email convert failed')

    def test_url(self):
        self.assertEqual('http://www.khan.com', URL().convert('http://www.khan.com'), 'url convert failed')
        self.assertRaises(ValidationError, lambda x:URL().convert('http://'), 'url convert failed')

    def test_plain_text(self):
        self.assertEqual('abcd1234_-', PlainText().convert('abcd1234_-'), 'plaintext convert failed')

    def test_Schema(self):
        import datetime
        obj = dict(
            a = 'a', 
            b = 1, 
            c = u'中文',
            d = True,
            e = 'on',
            f = .1,
            g = .2,
            h = 1,
            j = "2009-12-12 12:12:12",
            k = range(20, 30),
            l = set(range(40, 50)),
            m = 'abcd',
            n = 'test@test.com',
            o = 'http://test.com'
           )
        self.assertEqual({
            'n_': 'test@test.com',
            'l_': set([40, 41, 42, 43, 44, 45, 46, 47, 48, 49]),
            'f_': 0.10000000000000001, 'g_': 0.20000000000000001,
            'e_': False,
            'c_': u'd_value',
            'a_': 'b_value',
            'o_': 'http://test.com',
            'b': 1,
            'm_':'abcd1234',
            'k_': [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
            'a': 'a',
            'c': u'\u4e2d\u6587',
            'j_': '2009-12-12 12:12:12',
            'e': True,
            'd': True,
            'g': 0.20000000000000001,
            'f': 0.10000000000000001,
            'h': 1,
            'k': [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
            'j': datetime.datetime(2009, 12, 12, 12, 12, 12),
            'm': 'abcd',
            'l': set([40, 41, 42, 43, 44, 45, 46, 47, 48, 49]),
            'o': 'http://test.com',
            'n': 'test@test.com',
            'd_': False,
            'b_': 1
            }, self.schema.convert(obj), 'Schema convert failed')
        
    
        class MySchema(Schema):
            s = String()
            b = Bool()
            
        myschema = MySchema()
        result = myschema.convert({"s" : 1, "b" : "b", "d" : "extra"})
        self.assertTrue(result == {"s" : "1", "b" : True, "d" : "extra"})
        
        myschema = MySchema(allow_extra_fields = False)
        cb = lambda : myschema.convert({"s" : 1, "b" : "b", "d" : "extra"})
        self.assertRaises(SchemaError, cb)
        
        myschema = MySchema(allow_extra_fields = True, filter_extra_fields = True)
        result = myschema.convert({"s" : 1, "b" : "b", "d" : "extra"})
        self.assertTrue(result == {"s" : "1", "b" : True})
        
        myschema = MySchema(default = {"default" : 1})
        result = myschema.convert(123)
        self.assertTrue(result == {"default" : 1})
        