import contextlib

import pytest
import sqlalchemy


def pytest_addoption(parser):
    parser.addini(
        name="drop_existing_test_db",
        help=(
            "If set to True, an existing database with the test database "
            "name will be dropped."),
        type="bool",
        default=False)


@pytest.fixture(scope='session')
def test_db(request, test_db_url):
    """
    Create a testing database for the test session.

    Returns an instance of "TestingDB".
    """
    test_db = TestingDB(
        base_db_url=test_db_url,
        drop_existing=request.config.getini('drop_existing_test_db'))
    test_db.create()
    request.addfinalizer(test_db.drop)
    return test_db


@pytest.fixture(scope='session')
def test_engine(request, test_db):
    """
    A database Engine connected to the testing database.
    """
    engine = test_db.create_engine()

    @request.addfinalizer
    def cleanup():
        engine.dispose()

    return engine


class TestingDB:
    """
    A test database used for a testing session.

    This class just provides an empty test database which then can be used to
    create the schema elements.
    """

    TEST_DB_PREFIX = "test_"

    def __init__(self, base_db_url, drop_existing=False):
        self._base_db_url = self._to_url(base_db_url)
        self._db_url = self._create_test_url()
        self._drop_existing = drop_existing

    @property
    def url(self):
        return self._db_url

    def create(self):
        with self.connect() as conn:
            if self._drop_existing:
                self._try_drop(conn)
            conn.execute("CREATE DATABASE {}".format(self._db_url.database))

    def _try_drop(self, conn):
        try:
            conn.execute("DROP DATABASE {}".format(self._db_url.database))
        except sqlalchemy.exc.ProgrammingError:
            pass
        finally:
            conn.execute("ROLLBACK")

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

    def create_engine(self):
        """
        Create an Engine for the test database.
        """
        return sqlalchemy.create_engine(self.url)

    def _to_url(self, url):
        # Ensure to create a copy actually
        url = str(url)
        return sqlalchemy.engine.url.make_url(url)

    def _create_test_url(self):
        test_url = self._to_url(self._base_db_url)
        test_url.database = self.TEST_DB_PREFIX + self._base_db_url.database
        return test_url
