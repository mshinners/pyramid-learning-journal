"""Unit tests for all view functions."""

import pytest
from pyramid.testing import DummyRequest
from pyramid.response import Response


@pytest.fixture
def dummy_req():
    """Create a dummy GET request."""
    return DummyRequest()


def test_list_view_returns_response(dummy_req):
    """Test that the list view returns a Response."""
    from learning_journal.views.default import list_view
    assert isinstance(list_view(dummy_req), Response)


def test_list_view_respondes_with_200_status_code(dummy_req):
    """Test that the list view responds with the proper 200 status code."""
    from learning_journal.views.default import list_view
    assert list_view(dummy_req).status_code == 200


def test_list_view_has_proper_content(dummy_req):
    """Test that the list view Response has proper content."""
    from learning_journal.views.default import list_view
    assert 'Blog</title>' in list_view(dummy_req).text


def test_detail_view_returns_response(dummy_req):
    """Test that the detail view returns a Response."""
    from learning_journal.views.default import detail_view
    assert isinstance(detail_view(dummy_req), Response)


def test_detail_view_respondes_with_200_status_code(dummy_req):
    """Test that the detail view responds with the proper 200 status code."""
    from learning_journal.views.default import detail_view
    assert detail_view(dummy_req).status_code == 200


def test_detail_view_has_proper_content(dummy_req):
    """Test that the detail view Response has proper content."""
    from learning_journal.views.default import detail_view
    assert 'Detail</title>' in detail_view(dummy_req).text


def test_create_view_returns_response(dummy_req):
    """Test that the create view returns a Response."""
    from learning_journal.views.default import create_view
    assert isinstance(create_view(dummy_req), Response)


def test_create_view_respondes_with_200_status_code(dummy_req):
    """Test that the create view responds with the proper 200 status code."""
    from learning_journal.views.default import create_view
    assert create_view(dummy_req).status_code == 200


def test_create_view_has_proper_content(dummy_req):
    """Test that the create view Response has proper content."""
    from learning_journal.views.default import create_view
    assert 'Form</title>' in create_view(dummy_req).text


def test_update_view_returns_response(dummy_req):
    """Test that the update view returns a Response."""
    from learning_journal.views.default import update_view
    assert isinstance(update_view(dummy_req), Response)


def test_update_view_respondes_with_200_status_code(dummy_req):
    """Test that the update view responds with the proper 200 status code."""
    from learning_journal.views.default import update_view
    assert update_view(dummy_req).status_code == 200


def test_update_view_has_proper_content(dummy_req):
    """Test that the update view Response has proper content."""
    from learning_journal.views.default import update_view
    assert '<body>' not in update_view(dummy_req).text
