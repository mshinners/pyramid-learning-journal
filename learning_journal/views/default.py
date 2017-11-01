from pyramid.response import Response
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(HERE, '../templates')


def list_view(request):
    """List of journal entries."""
    with open(os.path.join(TEMPLATES, 'index.html')) as file:
        return Response(file.read())


def detail_view(request):
    """A single journal entry."""
    with open(os.path.join(TEMPLATES, 'detail.html')) as file:
        return Response(file.read())


def create_view(request):
    """Create a new entry."""
    with open(os.path.join(TEMPLATES, 'new.html')) as file:
        return Response(file.read())


def update_view(request):
    """Update an existing entry."""
    with open(os.path.join(TEMPLATES, 'update.html')) as file:
        return Response(file.read())
