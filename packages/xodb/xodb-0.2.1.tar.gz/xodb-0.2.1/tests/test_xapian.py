import shutil
import datetime
import xodb
import tempfile
import xapian
from xodb import MultipleValueRangeProcessor

from nose.tools import assert_raises


class _TestDatabase(object):

    db_factory = None

    def setup(self):
        self.db = self.db_factory()
        assert self.db.backend.get_doccount() == 0

    def teardown(self):
        if self.db.db_path:
            shutil.rmtree(self.db.db_path)

    def test_stored_prefixes(self):
        t = tempfile.mkdtemp()
        x = xapian.WritableDatabase(t, xapian.DB_CREATE_OR_OVERWRITE)
        x.set_metadata("_XODB_RP_Foo", "bar")
        x.set_metadata("_XODB_BP_Ding", "dong")
        x.flush()
        xdb = xodb.Database(x)
        assert xdb.relevance_prefixes['Foo'] == 'bar'
        assert xdb.boolean_prefixes['Ding'] == 'dong'

    def test_stored_values(self):
        db = self.db
        assert db.value_count == 0
        assert db.add_value('foo')
        assert db.value_count == 1
        assert db.add_value('foo')
        assert db.value_count == 1
        assert db.add_value('bar')
        assert db.value_count == 2


class TestXapianFile(_TestDatabase):
    db_factory = staticmethod(xodb.temp)


class TestXapianInMem(_TestDatabase):
    db_factory = staticmethod(xodb.inmemory)


def test_value_range_processor():
    vp = MultipleValueRangeProcessor(dict(foo=1, bar=2), str.upper)
    assert vp('foo:abc', 'def') == (1, 'ABC', 'DEF')
    assert vp('bar:news', 'def') == (2, 'NEWS', 'DEF')
    assert vp('bar:', 'def') == (2, '', 'DEF')
    assert vp('bar', 'def') == (xapian.BAD_VALUENO, 'bar', 'def')
    assert vp('baz:foo', 'def') == (xapian.BAD_VALUENO, 'baz:foo', 'def')

    qp = xapian.QueryParser()
    db = xodb.temp()
    qp.set_database(db.backend)
    qp.add_valuerangeprocessor(vp)

    query = qp.parse_query('foo:abc..def')
    assert str(query) == 'Xapian::Query(VALUE_RANGE 1 ABC DEF)'

    query = qp.parse_query('bar:abc..def')
    assert str(query) == 'Xapian::Query(VALUE_RANGE 2 ABC DEF)'

    query = qp.parse_query('bar:3..4')
    assert str(query) == 'Xapian::Query(VALUE_RANGE 2 3 4)'

    assert_raises(xapian.QueryParserError, qp.parse_query, 'baz:abc..def')
