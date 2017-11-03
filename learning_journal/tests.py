"""Unit tests for all view functions."""

import pytest
from pyramid.testing import DummyRequest
from pyramid.exceptions import HTTPNotFound


@pytest.fixture
def dummy_req():
    """Make a dummy GET request."""
    return DummyRequest()


def test_list_view_returns_list_of_entries_in_dict(dummy_req):
    """Test list view returns a list of all the entries as dicts."""
    from learning_journal.views.default import list_view
    response = list_view(dummy_req)
    assert 'entries' in response
    assert isinstance(response['entries'], list)


def test_detail_view_returns_details_of_entry_in_dict(dummy_req):
    """Test detail view returns the details of one entry as dict."""
    from learning_journal.views.default import detail_view
    dummy_req.matchdict['id'] = 1
    response = detail_view(dummy_req)
    assert 'entry' in response
    assert isinstance(response['entry'], dict)


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


@pytest.fixture
def testapp():
    """Create a copy of the WSGI app for testing purposes."""
    from webtest import TestApp
    from pyramid.config import Configurator

    def main():
        config = Configurator()
        config.include('pyramid_jinja2')
        config.include('.routes')
        config.scan()
        return config.make_wsgi_app()

    app = main()
    return TestApp(app)


def test_home_route_has_all_entries(testapp):
    """Test that the page on the home route has all journal entries."""
    from learning_journal.data.entry_history import ENTRIES
    response = testapp.get('/')
    assert len(ENTRIES) == len(response.html.find_all('hr')) - 1


def test_detail_route_has_one_entry(testapp):
    """Test that the page on the detail route has one journal entry."""
    from learning_journal.data.entry_history import ENTRIES
    response = testapp.get('/journal/1')
    assert 1 == len(response.html.find_all('h2'))
    assert ENTRIES[-1]['title'] in str(response.html.find_all('h2')[0])


def test_create_route_has_empty_form(testapp):
    """Test that the page on the create route has empty form."""
    response = testapp.get('/journal/new-entry')
    assert 1 == len(response.html.find_all('form'))
    assert 0 == len(response.html.find_all(value='value'))


def test_update_route_has_filled_form(testapp):
    """Test that the page on the update route has filled form."""
    from learning_journal.data.entry_history import ENTRIES
    response = testapp.get('/journal/1/edit-entry')
    assert 1 == len(response.html.find_all('form'))
    assert ENTRIES[-1]['title'] in str(response.html.find_all('input')[0])
