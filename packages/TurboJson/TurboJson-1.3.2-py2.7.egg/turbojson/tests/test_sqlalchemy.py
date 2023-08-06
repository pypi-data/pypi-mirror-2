from turbojson.jsonify import jsonify, encode

try:
    try:
        import sqlite3
    except ImportError: # Python < 2.5
        import pysqlite2
    from sqlalchemy import (MetaData, Table, Column, ForeignKey,
        Integer, String)
    from sqlalchemy.orm import create_session, mapper, relation

    metadata = MetaData('sqlite:///:memory:')

    test1 = Table('test1', metadata,
        Column('id', Integer, primary_key=True),
        Column('val', String(8)))

    test2 = Table('test2', metadata,
        Column('id', Integer, primary_key=True),
        Column('test1id', Integer, ForeignKey('test1.id')),
        Column('val', String(8)))

    test3 = Table('test3', metadata,
        Column('id', Integer, primary_key=True),
        Column('val', String(8)))

    test4 = Table('test4', metadata,
        Column('id', Integer, primary_key=True),
        Column('val', String(8)))

    metadata.create_all()

    class Test2(object):
        pass
    mapper(Test2, test2)

    class Test1(object):
        pass
    mapper(Test1, test1, properties={'test2s': relation(Test2)})

    class Test3(object):
        def __json__(self):
            return {'id': self.id, 'val': self.val, 'customized': True}
    mapper(Test3, test3)

    class Test4(object):
        pass
    mapper(Test4, test4)

    test1.insert().execute({'id': 1, 'val': 'bob'})
    test2.insert().execute({'id': 1, 'test1id': 1, 'val': 'fred'})
    test2.insert().execute({'id': 2, 'test1id': 1, 'val': 'alice'})
    test3.insert().execute({'id': 1, 'val': 'bob'})
    test4.insert().execute({'id': 1, 'val': 'alberto'})

except ImportError:
    from warnings import warn
    warn('SQLAlchemy or PySqlite not installed - cannot run these tests.')

else:

    def test_saobj():
        s = create_session()
        t = s.query(Test1).get(1)
        encoded = encode(t)
        assert encoded == '{"id": 1, "val": "bob"}'

    def test_salist():
        s = create_session()
        t = s.query(Test1).get(1)
        encoded = encode(t.test2s)
        assert encoded == ('[{"test1id": 1, "id": 1, "val": "fred"},'
            ' {"test1id": 1, "id": 2, "val": "alice"}]')

    def test_select_row():
        s = create_session()
        t = test1.select().execute()
        encoded = encode(t)
        assert encoded == '[{"id": 1, "val": "bob"}]'

    def test_select_rows():
        s = create_session()
        t = test2.select().execute()
        encoded = encode(t)
        assert encoded == ('[{"test1id": 1, "id": 1, "val": "fred"},'
            ' {"test1id": 1, "id": 2, "val": "alice"}]')

    def test_explicit_saobj():
        s = create_session()
        t = s.query(Test3).get(1)
        encoded = encode(t)
        assert encoded == '{"id": 1, "val": "bob", "customized": true}'

    def test_priority_override():
        s = create_session()
        t = s.query(Test4).get(1)
        encoded = encode(t)
        assert encoded == '{"id": 1, "val": "alberto"}'

        @jsonify.when((Test4,))
        def jsonify_test4(obj):
            return {'val': obj.val}

        encoded = encode(t)
        assert encoded == '{"val": "alberto"}'

