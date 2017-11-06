"""Unit tests for all view functions."""

from __future__ import unicode_literals
from pyramid.testing import DummyRequest
import pytest
from pyramid import testing
import transaction
from learning_journal.models import (
    Entry,
    get_tm_session,
)
from learning_journal.models.meta import Base
from datetime import datetime
from pyramid.httpexceptions import HTTPNotFound, HTTPFound, HTTPBadRequest
from faker import Faker
import random

FAKE = Faker()


@pytest.fixture(scope='session')
def configuration(request):
    """Config stuff for testing."""
    config = testing.setUp(settings={
        'sqlalchemy.url': 'postgres://localhost:5432/test-learning-journal'
    })
    config.include('learning_journal.models')

    def teardown():
        testing.tearDown()
    request.addfinalizer(teardown)
    return config


@pytest.fixture
def db_session(configuration, request):
    """Set up the db session for testing purposes."""
    SessionFactory = configuration.registry["dbsession_factory"]
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)
    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_req(db_session):
    """Make a dummy GET request."""
    return testing.DummyRequest(dbsession=db_session)


def test_list_view_returns_list_of_entries_in_dict(dummy_req):
    """Test list view returns a list of all the entries as dicts."""
    from learning_journal.views.default import list_view
    response = list_view(dummy_req)
    assert 'entries' in response
    assert isinstance(response['entries'], list)


def test_entry_exisits_and_is_in_list(dummy_req):
    """Test that a dummy request creates a new entry."""
    from learning_journal.views.default import list_view
    from learning_journal.models import Entry
    new_entry = Entry(
        title='Title Here',
        body='This is a test of the body.'
    )
    dummy_req.dbsession.add(new_entry)
    dummy_req.dbsession.commit()
    response = list_view(dummy_req)
    assert new_entry.to_dict() in response['entries']


def test_detail_view_returns_details_of_entry_in_dict(dummy_req):
    """Test detail view returns the details of one entry as dict."""
    from learning_journal.views.default import detail_view
    from learning_journal.models import Entry
    new_entry = Entry(
        title='Title Here',
        body='This is a test of the body.'
    )
    dummy_req.dbsession.add(new_entry)
    dummy_req.dbsession.commit()
    dummy_req.matchdict['id'] = 1
    response = detail_view(dummy_req)
    assert 'entry' in response
    assert isinstance(response['entry'], Entry)


def test_detail_view_raises_httpnotfound_for_invalid_id(dummy_req):
    """Test detail view raises HTTPNotFound for invalid id."""
    from learning_journal.views.default import detail_view
    dummy_req.matchdict['id'] = -1
    with pytest.raises(HTTPNotFound):
        detail_view(dummy_req)


def test_create_view_returns_empty_dict(dummy_req):
    """Test create view returns an empty dict."""
    from learning_journal.views.default import create_view
    response = create_view(dummy_req)
    assert not response
    assert isinstance(response, dict)


def test_update_view_returns_current_details_of_entry_in_dict(dummy_req):
    """Test update view returns the current details of one entry as dict."""
    from learning_journal.views.default import update_view
    from learning_journal.models import Entry
    new_entry = Entry(
        title='Title Here',
        body='This is a test of the body.'
    )
    dummy_req.dbsession.add(new_entry)
    dummy_req.dbsession.commit()
    dummy_req.matchdict['id'] = 1
    response = update_view(dummy_req)
    assert 'entry' in response
    assert isinstance(response['entry'], dict)


def test_update_view_raises_httpnotfound_for_invalid_id(dummy_req):
    """Test update view raises HTTPNotFound for invalid id."""
    from learning_journal.views.default import update_view
    dummy_req.matchdict['id'] = -1
    with pytest.raises(HTTPNotFound):
        update_view(dummy_req)


@pytest.fixture(scope="session")
def testapp(request):
    """Create a copy of the WSGI app for testing purposes."""
    from webtest import TestApp
    from pyramid.config import Configurator

    def main():
        config = Configurator()
        settings = {
            'sqlalchemy.url': 'postgres://localhost:5432/test-learning-journal'
        }
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2')
        config.include('.routes')
        config.include('.models')
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


@pytest.fixture(scope="session")
def fill_the_db(testapp):
    SessionFactory = testapp.app.registry["dbsession_factory"]
    with transaction.manager:
        dbsession = get_tm_session(SessionFactory, transaction.manager)
        dbsession.add_all(ENTRIES)

ENTRIES = []
for i in range(20):
    new_entry = Entry(
        title='title #{}'.format(i),
        body=random.random() * 1000, 
        creation_date=FAKE.date_time()
    )
    ENTRIES.append(new_entry)


def test_home_route_has_all_entries(testapp, fill_the_db):
    """Test that the page on the home route has all journal entries."""
    response = testapp.get('/')
    assert len(ENTRIES) == len(response.html.find_all('hr')) - 1


def test_create_route_has_empty_form(testapp):
    """Test that the page on the create route has empty form."""
    response = testapp.get('/journal/new-entry')
    assert 1 == len(response.html.find_all('form'))
    assert 0 == len(response.html.find_all(value='value'))


# def test_create_adds_new_entry_to_list(testapp):
#     """Test that create function adds a new entry properly."""
#     response = testapp.get('/journal/new-entry')
#     assert 1 == len(response.html.find_all('form'))
#     assert 0 == len(response.html.find_all(value='value'))


def test_detail_route_has_one_entry(testapp):
    """Test that the page on the detail route has one journal entry."""
    response = testapp.get('/journal/1')
    assert 1 == len(response.html.find_all('h2'))
    assert 'title #0' in str(response.html.find('h2'))


def test_update_route_has_filled_form(testapp):
    """Test that the page on the update route has filled form."""
    response = testapp.get('/journal/1/edit-entry')
    assert 1 == len(response.html.find_all('form'))
    assert 'title #0' in str(response.html.find('input'))


# def test_update_does_update_an_existing_entry(testapp):
#     """Test that the update function correctly updates the original."""
#     response = testapp.get('/journal/1/edit-entry')
#     assert 1 == len(response.html.find_all('form'))
#     assert '