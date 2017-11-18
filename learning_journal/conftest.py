"""Fixtures for the pyramid_learning_journal tests."""

from __future__ import unicode_literals
import pytest
from pyramid import testing
from pyramid_learning_journal.models.meta import Base
from pyramid_learning_journal.models import Entry, get_tm_session
from passlib.apps import custom_app_context as pwd_context
import transaction
import os


@pytest.fixture
def test_entry():
    """Create a new Entry."""
    return Entry(
        title='Test Entry',
        body='This is a test. This is only a test.'
    )


@pytest.fixture(scope='session')
def configuration(request):
    """Setup database for testing."""
    config = testing.setUp(settings={
        'sqlalchemy.url': os.environ['TEST_DATABASE_URL']
    })
    config.include('learning_journal.models')
    config.include("learning_journal.routes")

    def teardown():
        testing.tearDown()
    request.addfinalizer(teardown)
    return config


@pytest.fixture
def db_session(configuration, request):
    """Create database session."""
    SessionFactory = configuration.registry['dbsession_factory']
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)
    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    """Create dummy GET request with dbsession."""
    return testing.DummyRequest(dbsession=db_session)


@pytest.fixture
def add_entry(dummy_request, test_entry):
    """Create new Entry and add to db."""
    dummy_request.dbsession.add(test_entry)
    return test_entry


@pytest.fixture
def add_entries(dummy_request, test_entries):
    """Create new Entry and add to db."""
    dummy_request.dbsession.add_all(test_entries)
    return test_entries


@pytest.fixture(scope="session")
def testapp(request):
    """Functional test for app."""
    from webtest import TestApp
    from pyramid.config import Configurator

    def main():
        settings = {
            'sqlalchemy.url': os.environ['TEST_DATABASE_URL']
        }
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2')
        config.include('learning_journal.routes')
        config.include('learning_journal.models')
        config.include('learning_journal.security')
        config.scan()
        return config.make_wsgi_app()

    app = main()

    SessionFactory = app.registry["dbsession_factory"]
    engine = SessionFactory().bind
    Base.metadata.create_all(bind=engine)

    def tearDown():
        Base.metadata.drop_all(bind=engine)
    request.addfinalizer(tearDown)
    return TestApp(app)


@pytest.fixture(scope='session')
def test_entries():
    """Create list of Entry objects to be added to db."""
    return [
        Entry(
            title='Day {}'.format(i),
            body='words ' * (i + 1)
        ) for i in range(20)
    ]


@pytest.fixture(scope='session')
def fill_the_db(testapp, test_entries):
    """Fill test db with dummy entries."""
    SessionFactory = testapp.app.registry['dbsession_factory']
    with transaction.manager:
        dbsession = get_tm_session(SessionFactory, transaction.manager)
        dbsession.add_all(test_entries)


@pytest.fixture
def empty_the_db(testapp):
    """Tear down database and add new table."""
    SessionFactory = testapp.app.registry["dbsession_factory"]
    engine = SessionFactory().bind
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture
def testapp_session(testapp, request):
    """Create session to interact with db."""
    SessionFactory = testapp.app.registry["dbsession_factory"]
    session = SessionFactory()
    engine = session.bind

    def teardown():
        session.transaction.rollback()
    request.addfinalizer(teardown)
    return session


@pytest.fixture
def username():
    """Set username for testing."""
    os.environ['AUTH_USERNAME'] = 'name'
    return 'name'


@pytest.fixture
def password():
    """Set password for testing."""
    os.environ['AUTH_PASSWORD'] = pwd_context.hash('password')
    return 'password'


@pytest.fixture(scope='session')
def csrf_token(testapp):
    """Get CSRF token for POST requests."""
    response = testapp.get('/login')
    return response.html.find('input', {'name': 'csrf_token'}).attrs['value']
