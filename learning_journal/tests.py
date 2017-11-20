"""Unit tests for all view functions."""

from __future__ import unicode_literals
# from pyramid.testing import DummyRequest
import pytest
from pyramid import testing
import transaction
from learning_journal.models import (
    Entry,
    get_tm_session,
)
from learning_journal.models.meta import Base
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest
from faker import Faker
import random
# import os

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
    """Create an entry for testing."""
    SessionFactory = testapp.app.registry["dbsession_factory"]
    with transaction.manager:
        dbsession = get_tm_session(SessionFactory, transaction.manager)
        dbsession.add_all(ENTRIES)

ENTRIES = []
for i in range(20):
    new_entry = Entry(
        title='title #{}'.format(i),
        body=random.random() * 0,
        creation_date=FAKE.date_time()
    )
    ENTRIES.append(new_entry)


def test_home_route_has_all_entries(testapp, fill_the_db):
    """Test that the page on the home route has all journal entries."""
    response = testapp.get('/')
    assert len(ENTRIES) == len(response.html.find_all('hr')) - 1


def test_detail_route_has_one_entry(testapp):
    """Test that the page on the detail route has one journal entry."""
    response = testapp.get('/journal/1')
    assert 1 == len(response.html.find_all('h2'))
    assert 'title #0' in str(response.html.find('h2'))


def test_to_dict_puts_all_properties_in_a_dictionary(test_entry):
    """Test that all properties of an Entry are in to_dict dictionary."""
    entry_dict = test_entry.to_dict()
    assert all(prop in entry_dict for prop in ['id', 'title', 'body', 'creation_date'])


def test_to_dict_leaves_body_in_markdown(test_entry):
    """Test that an Entry's body is in markdown in to_dict dictionary."""
    entry_dict = test_entry.to_dict()
    assert entry_dict['body'] == test_entry.body


def test_to_dict_converts_date_to_string(test_entry):
    """Test that an Entry's creation_date is a string in to_dict dicitonary."""
    entry_dict = test_entry.to_dict()
    assert isinstance(entry_dict['creation_date'], str)


""" UNIT TESTS FOR VIEW FUNCTIONS """


def test_list_view_returns_list(dummy_request, add_entries):
    """Test that the list view function returns a list of the entries."""
    from learning_journal.views.default import list_view
    response = list_view(dummy_request)
    assert 'entries' in response
    assert isinstance(response['entries'], list)


def test_list_view_returns_all_entries_in_db(dummy_request):
    """Test that the list view function returns all entries in database."""
    from learning_journal.views.default import list_view
    from learning_journal.models import Entry
    response = list_view(dummy_request)
    query = dummy_request.dbsession.query(Entry)
    assert len(response['entries']) == query.count()


def test_detail_view_raises_httpnotfound_for_bad_id(dummy_request):
    """Test that detail_view raises HTTPNotFound if index out of bounds."""
    from learning_journal.views.default import detail_view
    dummy_request.matchdict['id'] = 99
    with pytest.raises(HTTPNotFound):
        detail_view(dummy_request)


def test_create_view_post_incompelete_data_is_bad_request(dummy_request):
    """Test that create_view POST with incomplete data is invalid."""
    from learning_journal.views.default import create_view
    entry_data = {
        'title': 'not Test Entry'
    }
    dummy_request.method = 'POST'
    dummy_request.POST = entry_data
    with pytest.raises(HTTPBadRequest):
        create_view(dummy_request)


def test_update_view_get_raises_httpnotfound_for_bad_id(dummy_request, add_entries):
    """Test that update_view raises HTTPNotFound if index out of bounds."""
    from learning_journal.views.default import update_view
    dummy_request.matchdict['id'] = 99
    with pytest.raises(HTTPNotFound):
        update_view(dummy_request)


def test_update_view_post_raises_httpnotfound_for_bad_id(dummy_request, add_entry):
    """Test that update_view raises HTTPNotFound if index out of bounds."""
    from learning_journal.views.default import update_view
    entry_data = {
        'title': 'Test Entry',
        'body': 'This is a test. This is only a test.'
    }
    dummy_request.matchdict['id'] = 99
    dummy_request.method = 'POST'
    dummy_request.POST = entry_data
    with pytest.raises(HTTPNotFound):
        update_view(dummy_request)


def test_create_post_route_auth_adds_a_new_entry(testapp, empty_the_db, testapp_session):
    """Test that POST to create route creates a new entry."""
    from learning_journal.models import Entry
    assert len(testapp_session.query(Entry).all()) == 0
    entry_data = {
        'title': 'Test Entry',
        'body': 'This is a test. This is only a test.'
    }
    testapp.post("/journal/new-entry", entry_data)
    assert len(testapp_session.query(Entry).all()) == 1


def test_create_post_route_auth_has_a_302_status_code(testapp, empty_the_db):
    """Test that POST to create route gets a 302 status code."""
    entry_data = {
        'title': 'Test Entry',
        'body': 'This is a test. This is only a test.'
    }
    response = testapp.post("/journal/new-entry", entry_data)
    assert response.status_code == 302


def test_create_post_route_auth_redirects_to_home_route(testapp, empty_the_db):
    """Test that POST to create route redirects to home route."""
    entry_data = {
        'title': 'Test Entry',
        'body': 'This is a test. This is only a test.'
    }
    response = testapp.post("/journal/new-entry", entry_data)
    home = testapp.app.routes_mapper.get_route('home').path
    assert response.location.endswith(home)


def test_create_post_route_auth_allows_access_to_detail_page(testapp, empty_the_db):
    """Test that the new entry has an available detail page."""
    assert testapp.get("/journal/1", status=404)

    entry_data = {
        'title': 'Test Entry',
        'body': 'This is a test. This is only a test.'
    }
    testapp.post("/journal/new-entry", entry_data)
    testapp.get("/journal/1")


def test_create_post_route_auth_has_400_error_for_incomplete_data(testapp):
    """Test that POST of incomplete data to create causes 400 error."""
    entry_data = {
        'title': 'Test Entry'
    }
    assert testapp.post("/journal/new-entry", entry_data, status=400)


def test_logout_route_auth_removes_auth_tkt_cookie(testapp):
    """Test that the logout route removes the auth_tkt cookie."""
    testapp.get("/logout")
    assert 'auth_tkt' not in testapp.cookies
