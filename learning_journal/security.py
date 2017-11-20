"""Configure and hold all security information for the learning journal.
Documents from Expense Tracker, by N. Hunt-Walker & class, used to learn how to
implement this new code. Source can be found at:
https://github.com/codefellows/expense_tracker_401d7/commit/9e0621753bc7da875028c1e6910d73728ddf19a7
"""


import os
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Authenticated, Allow
from pyramid.session import SignedCookieSessionFactory
from passlib.apps import custom_app_context as pwd_context


class MyRoot(object):
    """Root for Learning Journal Auth."""

    def __init__(self, request):
        """Create a new root."""
        self.request = request

    __acl__ = [
        (Allow, Authenticated, 'secret'),
    ]


def is_authenticated(username, password):
    """Check if the user's credentials are approved."""
    if username == os.environ.get('AUTH_USERNAME', ''):
        if pwd_context.verify(password, os.environ.get('AUTH_PASSWORD', '')):
            return True
    return False


def includeme(config):
    """Set up the authentication process."""
    auth_secret = os.environ.get('AUTH_SECRET', '')
    authn_policy = AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg='sha512'
    )
    config.set_authentication_policy(authn_policy)

    # Set up authorization
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)
    config.set_root_factory(MyRoot)

    # CSRF
    session_secret = os.environ.get('SESSION_SECRET', '')
    session_factory = SignedCookieSessionFactory(session_secret)
    config.set_session_factory(session_factory)
    config.set_default_csrf_options(recuire_csrf=True)
