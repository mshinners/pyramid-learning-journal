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
from datetime import datetime
from pyramid.httpexceptions import HTTPNotFound, HTTPFound, HTTPBadRequest
from faker import Faker
import random
# import os

FAKE = Faker()


# pragma: no cover


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


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


def test_create_route_has_empty_form(testapp):
    """Test that the page on the create route has empty form."""
    response = testapp.get('/journal/new-entry')
    assert 1 == len(response.html.find_all('form'))
    assert 0 == len(response.html.find_all(value='value'))


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


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


""" UNIT TESTS FOR MODELS """


def test_constructed_entry_with_no_date_added_to_database(db_session):
    """Test that Entry constructed with no date gets added to the database."""
    from learning_journal.models import Entry
    assert len(db_session.query(Entry).all()) == 0
    entry = Entry(
        title='test 1',
        body='this is a test'
    )
    db_session.add(entry)
    assert len(db_session.query(Entry).all()) == 1


def test_constructed_entry_with_date_added_to_database(db_session):
    """Test that Entry constructed with no date gets added to the database."""
    from learning_journal.models import Entry
    assert len(db_session.query(Entry).all()) == 0
    entry = Entry(
        title='test 1',
        body='this is a test',
        creation_date=datetime(2017, 10, 12, 1, 30)
    )
    db_session.add(entry)
    assert len(db_session.query(Entry).all()) == 1


def test_constructed_entry_with_date_has_given_date():
    """Test that Entry constructed with date uses it for creation_date."""
    from learning_journal.models import Entry
    entry = Entry(
        title='test 1',
        body='this is a test',
        creation_date=datetime(2017, 10, 12, 1, 30)
    )
    date = datetime(2017, 10, 12, 1, 30)
    assert date.strftime('%c') == entry.creation_date.strftime('%c')


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


def test_to_html_dict_puts_all_properties_in_a_dictionary(test_entry):
    """Test that all properties of an Entry are in to_html_dict dictionary."""
    entry_dict = test_entry.to_html_dict()
    assert all(prop in entry_dict for prop in ['id', 'title', 'body', 'creation_date'])


def test_to_html_dict_leaves_body_in_markdown(test_entry):
    """Test that an Entry's body is in markdown in to_html_dict."""
    entry_dict = test_entry.to_html_dict()
    assert entry_dict['body'].startswith('<p>')
    assert entry_dict['body'].endswith('</p>')


def test_to_html_dict_converts_date_to_string(test_entry):
    """Test that an Entry's creation_date is a string in to_html_dict."""
    entry_dict = test_entry.to_html_dict()
    assert isinstance(entry_dict['creation_date'], str)


""" UNIT TESTS FOR VIEW FUNCTIONS """


def test_list_view_returns_list(dummy_request, add_entries):
    """Test that the list view function returns a list of the entries."""
    from learning_journal.views.default import list_view
    response = list_view(dummy_request)
    assert 'entries' in response
    assert isinstance(response['entries'], list)


def test_list_view_returns_entries_in_list(dummy_request, add_entries):
    """Test that the list view function returns entries as dicitonaries."""
    from learning_journal.views.default import list_view
    response = list_view(dummy_request)
    assert add_entries[0].to_html_dict() in response['entries']


def test_list_view_returns_all_entries_in_db(dummy_request, add_entries):
    """Test that the list view function returns all entries in database."""
    from learning_journal.views.default import list_view
    from learning_journal.models import Entry
    response = list_view(dummy_request)
    query = dummy_request.dbsession.query(Entry)
    assert len(response['entries']) == query.count()


def test_detail_view_returns_one_entry_detail(dummy_request, add_entries):
    """Test that the detail view function returns the data of one entry."""
    from learning_journal.views.default import detail_view
    dummy_request.matchdict['id'] = 1
    response = detail_view(dummy_request)
    assert add_entries[0].to_html_dict() == response['entry']


def test_detail_view_returns_correct_entry_detail(dummy_request, add_entries):
    """Test that the detail view function returns the correct entry data."""
    from learning_journal.views.default import detail_view
    dummy_request.matchdict['id'] = 1
    response = detail_view(dummy_request)
    assert response['entry']['id'] == 1


def test_detail_view_raises_httpnotfound_for_bad_id(dummy_request, add_entries):
    """Test that detail_view raises HTTPNotFound if index out of bounds."""
    from learning_journal.views.default import detail_view
    dummy_request.matchdict['id'] = 99
    with pytest.raises(HTTPNotFound):
        detail_view(dummy_request)


def test_create_view_get_returns_only_the_page_title(dummy_request):
    """Test that the new entry function returns only page title for GET."""
    from learning_journal.views.default import create_view
    response = create_view(dummy_request)
    assert 'page_title' in response
    assert 'New Entry' == response['page_title']


def test_create_view_post_creates_new_entry(dummy_request):
    """Test that the new entry is created on create_view POST."""
    from learning_journal.views.default import create_view
    from learning_journal.models import Entry
    entry_data = {
        'title': 'Test Entry',
        'body': 'This is a test. This is only a test.'
    }
    dummy_request.method = 'POST'
    dummy_request.POST = entry_data
    create_view(dummy_request)
    assert dummy_request.dbsession.query(Entry).count() == 1


def test_create_view_post_creates_new_entry_with_given_info(dummy_request):
    """Test that new entry created uses POST info on create_view POST."""
    from learning_journal.views.default import create_view
    from learning_journal.models import Entry
    entry_data = {
        'title': 'Test Entry',
        'body': 'This is a test. This is only a test.'
    }
    dummy_request.method = 'POST'
    dummy_request.POST = entry_data
    create_view(dummy_request)
    entry = dummy_request.dbsession.query(Entry).get(1)
    assert entry.title == entry_data['title']
    assert entry.body == entry_data['body']


def test_create_view_post_has_302_status_code(dummy_request):
    """Test that create_view POST has 302 status code."""
    from learning_journal.views.default import create_view
    entry_data = {
        'title': 'Test Entry',
        'body': 'This is a test. This is only a test.'
    }
    dummy_request.method = 'POST'
    dummy_request.POST = entry_data
    response = create_view(dummy_request)
    assert response.status_code == 302


def test_create_view_post_redirects_to_home_with_httpfound(dummy_request):
    """Test that create_view POST redirects to home with httpfound."""
    from learning_journal.views.default import create_view
    entry_data = {
        'title': 'Test Entry',
        'body': 'This is a test. This is only a test.'
    }
    dummy_request.method = 'POST'
    dummy_request.POST = entry_data
    response = create_view(dummy_request)
    assert isinstance(response, HTTPFound)
    assert response.location == dummy_request.route_url('home')


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


def test_update_view_get_returns_only_one_entry_detail(dummy_request, add_entries):
    """Test that the Update view function returns one entry by id."""
    from learning_journal.views.default import update_view
    dummy_request.matchdict['id'] = 1
    response = update_view(dummy_request)
    assert add_entries[0].to_dict() == response['entry']


def test_update_view_get_returns_correct_entry_details(dummy_request, add_entries):
    """Test that the update view function returns the correct entry data."""
    from learning_journal.views.default import update_view
    dummy_request.matchdict['id'] = 1
    response = update_view(dummy_request)
    assert response['entry']['id'] == 1


def test_update_view_get_raises_httpnotfound_for_bad_id(dummy_request, add_entries):
    """Test that update_view raises HTTPNotFound if index out of bounds."""
    from learning_journal.views.default import update_view
    dummy_request.matchdict['id'] = 99
    with pytest.raises(HTTPNotFound):
        update_view(dummy_request)


def test_update_view_post_updates_entry(dummy_request, add_entry):
    """Test that the entry is updated on update_view POST, not created."""
    from learning_journal.views.default import update_view
    from learning_journal.models import Entry
    entry_data = {
        'title': 'Test Entry',
        'body': 'This is a test. This is only a test.'
    }
    dummy_request.matchdict['id'] = 1
    dummy_request.method = 'POST'
    dummy_request.POST = entry_data
    update_view(dummy_request)
    assert dummy_request.dbsession.query(Entry).count() == 1


def test_update_view_post_updates_entry_with_given_info(dummy_request, add_entry):
    """Test that entry updated uses POST info on update_view POST."""
    from learning_journal.views.default import update_view
    from learning_journal.models import Entry
    entry_data = {
        'title': 'Test Entry',
        'body': 'This is a test. This is only a test.'
    }
    dummy_request.matchdict['id'] = 1
    dummy_request.method = 'POST'
    dummy_request.POST = entry_data

    old_entry = dummy_request.dbsession.query(Entry).get(1).to_dict()
    update_view(dummy_request)
    entry = dummy_request.dbsession.query(Entry).get(1)
    assert entry.title == entry_data['title']
    assert entry.body == entry_data['body']
    assert entry.title != old_entry['title']
    assert entry.body != old_entry['body']


def test_update_view_post_has_302_status_code(dummy_request, add_entry):
    """Test that update_view POST has 302 status code."""
    from learning_journal.views.default import update_view
    entry_data = {
        'title': 'Test Entry',
        'body': 'This is a test. This is only a test.'
    }
    dummy_request.matchdict['id'] = 1
    dummy_request.method = 'POST'
    dummy_request.POST = entry_data
    response = update_view(dummy_request)
    assert response.status_code == 302


def test_update_view_post_redirects_to_detail_with_httpfound(dummy_request, add_entry):
    """Test that update_view POST redirects to detail of id with httpfound."""
    from learning_journal.views.default import update_view
    entry_data = {
        'title': 'Test Entry',
        'body': 'This is a test. This is only a test.'
    }
    dummy_request.matchdict['id'] = 1
    dummy_request.method = 'POST'
    dummy_request.POST = entry_data
    response = update_view(dummy_request)
    assert isinstance(response, HTTPFound)
    assert response.location == dummy_request.route_url('detail', id=1)


def test_update_view_post_incomplete_data_is_bad_request(dummy_request, add_entry):
    """Test that update_view POST with incomplete data is invalid."""
    from learning_journal.views.default import update_view
    entry_data = {
        'title': 'not Test Entry'
    }
    dummy_request.matchdict['id'] = 1
    dummy_request.method = 'POST'
    dummy_request.POST = entry_data
    with pytest.raises(HTTPBadRequest):
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


def test_login_get_returns_only_the_page_title_for_unauthenticated_user(dummy_request):
    """Test that the login function returns only page title for unauthN GET."""
    from learning_journal.views.default import login
    response = login(dummy_request)
    assert 'page_title' in response
    assert 'Login' == response['page_title']


def test_login_post_incomplete_data_is_bad_request(dummy_request, username, password):
    """Test that login POST with incomplete data is invalid."""
    from learning_journal.views.default import login
    data = {
        'username': 'jack'
    }
    dummy_request.method = 'POST'
    dummy_request.POST = data
    with pytest.raises(HTTPBadRequest):
        login(dummy_request)


def test_login_post_incorrect_data_returns_dict_with_error(dummy_request):
    """Test that login POST with incorrect data is invalid."""
    from learning_journal.views.default import login
    data = {
        'username': 'jack',
        'password': 'work'
    }
    dummy_request.method = 'POST'
    dummy_request.POST = data
    response = login(dummy_request)
    assert 'error' in response
    assert 'The username and/or password are incorrect.' == response['error']


def test_login_post_correct_data_returns_302_status_code(dummy_request, username, password):
    """Test that login POST with correct data gets 302 status code."""
    from learning_journal.views.default import login
    data = {
        'username': username,
        'password': password
    }
    dummy_request.method = 'POST'
    dummy_request.POST = data
    response = login(dummy_request)
    assert response.status_code == 302


def test_login_post_correct_data_redirects_to_home_with_httpfound(dummy_request, username, password):
    """Test that login POST with correct data redirects to home page."""
    from learning_journal.views.default import login
    data = {
        'username': username,
        'password': password
    }
    dummy_request.method = 'POST'
    dummy_request.POST = data
    response = login(dummy_request)
    assert isinstance(response, HTTPFound)
    assert response.location == dummy_request.route_url('home')


def test_logout_returns_302_status_code(dummy_request):
    """Test that logout gets 302 status code."""
    from learning_journal.views.default import logout
    response = logout(dummy_request)
    assert response.status_code == 302


def test_logout_redirects_to_home_with_httpfound(dummy_request):
    """Test that logout redirects to home page."""
    from learning_journal.views.default import logout
    response = logout(dummy_request)
    assert isinstance(response, HTTPFound)
    assert response.location == dummy_request.route_url('home')


""" FUNCTIONAL TESTS FOR ROUTES """


def test_home_route_unauth_gets_200_status_code(testapp, fill_the_db):
    """Test that the home route gets 200 status code for unauthN user."""
    response = testapp.get("/")
    assert response.status_code == 200


def test_home_route_unauth_has_all_journal_entries(testapp, test_entries):
    """Test that the home route all journal entries."""
    response = testapp.get("/")
    assert len(test_entries) == len(response.html.find_all('div', 'card'))


def test_home_route_unauth_has_login_tab(testapp):
    """Test that the home route has only a login tab."""
    response = testapp.get("/")
    assert len(response.html.find_all('li', 'nav-item')) == 2
    assert 'Login' in str(response.html.find_all('li', 'nav-item')[1])


def test_detail_route_unauth_has_one_entry(testapp):
    """Test that the detail route shows one journal entry."""
    response = testapp.get("/journal/1")
    assert len(response.html.find_all('div', 'card')) == 1


def test_detail_route_unauth_for_valid_id_gets_200_status_code(testapp):
    """Test that the detail route of a valid gets 200 status code."""
    response = testapp.get("/journal/1")
    assert response.status_code == 200


def test_detail_route_unauth_has_correct_entry(testapp):
    """Test that the detail route shows correct journal entry."""
    response = testapp.get("/journal/1")
    assert 'Day 0' in response.html.find('h2')


def test_detail_route_unauth_has_no_edit_button(testapp):
    """Test that the detail route has not edit button for unauthN user."""
    response = testapp.get("/journal/1")
    assert not response.html.find('a', 'edit')


def test_detail_route_unauth_goes_to_404_page_for_invalid_id(testapp):
    """Test that the detail route redirects to 404 page for invalid id."""
    response = testapp.get("/journal/100", status=404)
    assert 'Oops' in str(response.html.find('h1'))


def test_update_get_route_unauth_gets_403_status_code(testapp):
    """Test that the update GET route gets 403 status code for unauthN user."""
    assert testapp.get("/journal/1/edit-entry", status=403)


def test_update_post_route_unauth_gets_403_status_code(testapp):
    """Test that the update POST route gets 403 status code for unauthN user."""
    assert testapp.post("/journal/1/edit-entry", status=403)


def test_create_get_route_unauth_gets_403_status_code(testapp):
    """Test that the create GET route gets 403 status code for unauthN user."""
    assert testapp.get("/journal/new-entry", status=403)


def test_create_post_route_unauth_gets_403_status_code(testapp):
    """Test that the create POST route gets 403 status code for unauthN user."""
    assert testapp.post("/journal/new-entry", status=403)


def test_logout_route_unauth_gets_403_status_code(testapp):
    """Test that the logout route gets 403 status code for unauthN user."""
    assert testapp.get("/logout", status=403)


def test_login_get_route_unauth_gets_200_status_code(testapp):
    """Test that the login GET route gets 200 status code."""
    response = testapp.get("/login")
    assert response.status_code == 200


def test_login_get_route_unauth_has_login_form(testapp):
    """Test that the login GET route gets 200 status code."""
    response = testapp.get("/login")
    assert len(response.html.find_all('input')) == 2
    assert 'Username' in str(response.html.find('input'))


def test_login_post_route_unauth_incompelete_data_has_400_error(testapp):
    """Test that POST of incomplete data to login route gets a 400 error."""
    data = {
        'username': 'jack'
    }
    assert testapp.post("/login", data, status=400)


def test_login_post_route_unauth_wrong_data_has_200_status_code(testapp):
    """Test that POST of wrong data to login route gets a 200 status code."""
    data = {
        'username': 'jack',
        'password': 'work'
    }
    response = testapp.post("/login", data)
    assert response.status_code == 200


def test_login_post_route_unauth_wrong_data_has_error_message(testapp):
    """Test that POST of wrong data to login route has an error message."""
    data = {
        'username': 'jack',
        'password': 'work'
    }
    response = testapp.post("/login", data)
    assert 'incorrect' in str(response.html.find('div', 'alert'))


def test_login_post_route_unauth_correct_data_has_302_status_code(testapp, username, password):
    """Test that POST of correct data to login route has 302 status code."""
    data = {
        'username': username,
        'password': password
    }
    response = testapp.post("/login", data)
    assert response.status_code == 302


def test_logout_route_auth_gets_302_status_code(testapp):
    """Test that the logout route gets 302 status code for authN user."""
    response = testapp.get("/logout")
    assert response.status_code == 302


def test_login_post_route_unauth_correct_data_redirects_to_home(testapp, username, password):
    """Test that POST of correct data to login route redirects to home page."""
    data = {
        'username': username,
        'password': password
    }
    response = testapp.post("/login", data)
    home = testapp.app.routes_mapper.get_route('home').path
    assert response.location.endswith(home)


def test_logout_route_auth_redirects_to_home(testapp):
    """Test that the logout route redirects to home page."""
    response = testapp.get("/logout")
    home = testapp.app.routes_mapper.get_route('home').path
    assert response.location.endswith(home)


def test_login_post_route_unauth_correct_data_home_has_logout_tab(testapp, username, password):
    """Test that POST of correct data to login route has home page with logout tab."""
    data = {
        'username': username,
        'password': password
    }
    response = testapp.post("/login", data)
    next_page = response.follow()
    assert len(next_page.html.find_all('li', 'nav-item')) == 3
    assert 'Logout' in str(next_page.html.find_all('li', 'nav-item')[2])


def test_logout_route_auth_home_has_login_tab(testapp):
    """Test that the logout route has home page with login."""
    response = testapp.get("/logout")
    next_page = response.follow()
    assert len(next_page.html.find_all('li', 'nav-item')) == 2
    assert 'Login' in str(next_page.html.find_all('li', 'nav-item')[1])


def test_login_post_route_unauth_correct_data_adds_auth_tkt_cookie(testapp, username, password):
    """Test that POST of correct data to login route adds auth_tkt cookie."""
    data = {
        'username': username,
        'password': password
    }
    testapp.post("/login", data)
    assert 'auth_tkt' in testapp.cookies


def test_login_get_route_auth_has_302_status_code(testapp):
    """Test that GET to login route has 302 status code."""
    response = testapp.get("/login")
    assert response.status_code == 302


def test_login_get_route_auth_redirects_to_home(testapp):
    """Test that GET to login route redirects to home page."""
    response = testapp.get("/login")
    home = testapp.app.routes_mapper.get_route('home').path
    assert response.location.endswith(home)


def test_login_get_route_auth_home_still_has_logout_tab(testapp):
    """Test that GET to login route has home page with logout tab."""
    response = testapp.get("/login")
    next_page = response.follow()
    assert len(next_page.html.find_all('li', 'nav-item')) == 3
    assert 'Logout' in str(next_page.html.find_all('li', 'nav-item')[2])


def test_login_get_route_auth_keeps_auth_tkt_cookie(testapp):
    """Test that GET to login route adds auth_tkt cookie."""
    assert 'auth_tkt' in testapp.cookies
    testapp.get("/login")
    assert 'auth_tkt' in testapp.cookies


def test_login_post_route_auth_has_302_status_code(testapp):
    """Test that POST to login route has 302 status code."""
    response = testapp.post("/login")
    assert response.status_code == 302


def test_login_post_route_auth_redirects_to_home(testapp):
    """Test that POST to login route redirects to home page."""
    response = testapp.post("/login")
    home = testapp.app.routes_mapper.get_route('home').path
    assert response.location.endswith(home)


def test_login_post_route_auth_home_still_has_logout_tab(testapp):
    """Test that POST to login route has home page with logout tab."""
    response = testapp.post("/login")
    next_page = response.follow()
    assert len(next_page.html.find_all('li', 'nav-item')) == 3
    assert 'Logout' in str(next_page.html.find_all('li', 'nav-item')[2])


def test_login_post_route_auth_keeps_auth_tkt_cookie(testapp):
    """Test that POST to login route adds auth_tkt cookie."""
    assert 'auth_tkt' in testapp.cookies
    testapp.post("/login")
    assert 'auth_tkt' in testapp.cookies


def test_home_route_auth_gets_200_status_code(testapp):
    """Test that the home route gets 200 status code."""
    response = testapp.get("/")
    assert response.status_code == 200


def test_home_route_auth_has_all_journal_entries(testapp, test_entries):
    """Test that the home route all journal entries."""
    response = testapp.get("/")
    assert len(test_entries) == len(response.html.find_all('div', 'card'))


def test_detail_route_auth_has_one_entry(testapp):
    """Test that the detail route shows one journal entry."""
    response = testapp.get("/journal/1")
    assert len(response.html.find_all('div', 'card')) == 1


def test_detail_route_auth_for_valid_id_gets_200_status_code(testapp):
    """Test that the detail route of a valid gets 200 status code."""
    response = testapp.get("/journal/1")
    assert response.status_code == 200


def test_detail_route_auth_has_correct_entry(testapp):
    """Test that the detail route shows correct journal entry."""
    response = testapp.get("/journal/1")
    assert 'Day 0' in response.html.find('h2')


def test_detail_route_auth_goes_to_404_page_for_invalid_id(testapp):
    """Test that the detail route redirects to 404 page for invalid id."""
    response = testapp.get("/journal/100", status=404)
    assert 'Oops' in str(response.html.find('h1'))


def test_update_get_route_auth_for_valid_id_gets_200_status_code(testapp):
    """Test that GET to update route of a valid gets 200 status code."""
    response = testapp.get("/journal/1/edit-entry")
    assert response.status_code == 200


def test_update_get_route_auth_has_filled_form(testapp):
    """Test that the Update page has a filled form."""
    response = testapp.get("/journal/1/edit-entry")
    assert len(response.html.find_all('input', attrs={"type": "text"})) == 1
    assert 'value="Day 0"' in str(response.html.find('input', attrs={"type": "text"}))


def test_update_get_route_auth_has_an_update_button(testapp):
    """Test that the Update page has a 'Update' button."""
    response = testapp.get("/journal/1/edit-entry")
    assert len(response.html.find_all('button', attrs={"type": "submit"})) == 1
    assert "Update" in response.html.find('button', attrs={"type": "submit"})


def test_update_get_route_auth_goes_to_404_page_for_invalid_id(testapp):
    """Test that the update GET route redirects to 404 page for invalid id."""
    response = testapp.get("/journal/100/edit-entry", status=404)
    assert 'Oops' in str(response.html.find('h1'))


def test_update_post_route_auth_updates_correct_entry(testapp, testapp_session):
    """Test that POST to update route updates a entry."""
    from learning_journal.models import Entry
    entry_data = {
        'title': 'so it begins',
        'body': 'the beginning of change'
    }
    old_entry = testapp_session.query(Entry).get(1).to_dict()
    testapp.post("/journal/1/edit-entry", entry_data)
    entry = testapp_session.query(Entry).get(1)
    assert entry.title == entry_data['title']
    assert entry.body == entry_data['body']
    assert entry.title != old_entry['title']
    assert entry.body != old_entry['body']


def test_update_post_route_auth_has_a_302_status_code(testapp):
    """Test that POST to update route gets a 302 status code."""
    entry_data = {
        'title': 'Test Entry',
        'body': 'This is a test. This is only a test.'
    }
    response = testapp.post("/journal/1/edit-entry", entry_data)
    assert response.status_code == 302


def test_update_post_route_auth_redirects_to_detail_route_for_id(testapp):
    """Test that POST to update route redirects to detail for the given id."""
    entry_data = {
        'title': 'Test Entry 2',
        'body': 'This is a test. This is only a test. x 2'
    }
    response = testapp.post("/journal/1/edit-entry", entry_data)
    detail = testapp.app.routes_mapper.get_route('detail').generate({'id': 1})
    assert response.location.endswith(detail)


def test_update_post_route_auth_adds_new_entry_to_home(testapp):
    """Test that the new entry is on the home page after POST to update."""
    entry_data = {
        'title': 'Test Entry 4',
        'body': 'This is a test. This is only a test. x 4'
    }
    response = testapp.post("/journal/1/edit-entry", entry_data)
    next_page = response.follow()
    assert entry_data['title'] in next_page.html.find('h2')
    assert entry_data['body'] in str(next_page.html.find('div', 'card-text'))


def test_update_post_route_auth_has_400_error_for_incomplete_data(testapp):
    """Test that POST of incomplete data to update causes 400 error."""
    entry_data = {
        'title': 'Test Entry 8'
    }
    assert testapp.post("/journal/1/edit-entry", entry_data, status=400)


def test_update_post_route_auth_goes_to_404_page_for_invalid_id(testapp):
    """Test that the update POST route redirects to 404 page for invalid id."""
    entry_data = {
        'title': 'the end',
        'body': 'last of the updates.'
    }
    response = testapp.post("/journal/100/edit-entry", entry_data, status=404)
    assert 'Oops' in str(response.html.find('h1'))


def test_create_get_route_auth_gets_200_status_code(testapp):
    """Test that GET to create route gets 200 status code."""
    response = testapp.get("/journal/new-entry")
    assert response.status_code == 200


def test_create_get_route_auth_has_empty_form(testapp):
    """Test that the Create page has an empty form."""
    response = testapp.get("/journal/new-entry")
    assert len(response.html.find_all('input', attrs={"type": "text"})) == 1
    assert 'value' not in response.html.find('input', attrs={"type": "text"})


def test_create_get_route_auth_has_a_create_button(testapp):
    """Test that the Create page has a 'Create' button."""
    response = testapp.get("/journal/new-entry")
    assert len(response.html.find_all('button', attrs={"type": "submit"})) == 1
    assert "Create" in response.html.find('button', attrs={"type": "submit"})


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


def test_create_post_route_auth_adds_new_entry_to_home(testapp, empty_the_db):
    """Test that the new entry is on the home page after POST to create."""
    entry_data = {
        'title': 'Test Entry',
        'body': 'This is a test. This is only a test.'
    }
    response = testapp.post("/journal/new-entry", entry_data)
    next_page = response.follow()
    assert entry_data['title'] in next_page.html.find('h2')
    assert entry_data['body'] in str(next_page.html.find('div', 'card-text'))


def test_create_post_route_auth_allows_access_to_detail_page(testapp, empty_the_db):
    """Test that the new entry has an available detail page."""
    assert testapp.get("/journal/1", status=404)

    entry_data = {
        'title': 'Test Entry',
        'body': 'This is a test. This is only a test.'
    }
    testapp.post("/journal/new-entry", entry_data)
    testapp.get("/journal/1")


def test_create_post_route_auth_new_detail_page_has_new_info(testapp, empty_the_db):
    """Test that the detail page for new entry has the correct info."""
    entry_data = {
        'title': 'Test Entry',
        'body': 'This is a test. This is only a test.'
    }
    testapp.post("/journal/new-entry", entry_data)
    response = testapp.get("/journal/1")
    assert entry_data['title'] in response.html.find('h2')
    assert entry_data['body'] in str(response.html.find('div', 'card-text'))


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
