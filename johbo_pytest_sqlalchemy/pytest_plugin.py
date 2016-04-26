import contextlib

import pytest
import sqlalchemy


@pytest.fixture(scope='session')
def testing_db(request, testing_db_url):
    """
    Create a testing database for the test session.

    Returns an instance of "TestingDB".
    """
    test_db = TestingDB(base_db_url=testing_db_url)
    test_db.create()
    request.addfinalizer(test_db.drop())
    return test_db


class TestingDB:
    """
    A test database used for a testing session.

    This class just provides an empty test database which then can be used to
    create the schema elements.
    """

    TEST_DB_PREFIX = "test_"

    def __init__(self, base_db_url):
        self._base_db_url = self._to_url(base_db_url)
        self._db_url = self._create_test_url()
        self._engine = sqlalchemy.create_engine(self._base_db_url)

    @property
    def url(self):
        return self._db_url

    def create(self):
        with self.connect() as conn:
            conn.execute("CREATE DATABASE {}".format(self._db_url.database))

    def drop(self):
        with self.connect() as conn:
            conn.execute("DROP DATABASE {}".format(self._db_url.database))

    @contextlib.contextmanager
    def connect(self):
        engine = sqlalchemy.create_engine(self._base_db_url)
        conn = engine.connect()
        conn.execution_options(autocommit=False)
        conn.execute("ROLLBACK")
        yield conn
        conn.close()
        engine.dispose()

    def _to_url(self, url):
        return sqlalchemy.engine.url.make_url(url)

    def _create_test_url(self):
        test_url = self._to_url(self._base_db_url)
        test_url.database = self.TEST_DB_PREFIX + self._base_db_url.database
        return test_url
