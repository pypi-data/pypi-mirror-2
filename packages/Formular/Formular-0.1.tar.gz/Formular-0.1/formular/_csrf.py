#!/usr/bin/env python
# coding: utf-8
"""
    formular._csrf
    ~~~~~~~~~~~~~~

    Utilities for Cross-site request forgery protection.

    To be as independant as possible this library uses random tokens,
    instead of hashes of user specific data.

    :copyright: 2010 by Formular Team, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
import os
from zlib import adler32

def _get_random_token():
    """
    Returns a random token with a size of 10 bytes.
    """
    return os.urandom(10)

def _get_url_hash(url):
    """
    Returns a hash for the given `url`.
    """
    if isinstance(url, unicode):
        url = url.encode("utf-8")
    return adler32(url) & 0xffffffff

def _get_csrf_token(session, url, force_update=False, max_csrf_tokens=4):
    """
    Returns a CSRF token for the given `url` and stores it in the `session`.

    :param session:
        An object with a dict-like interface which can be used to store session
        specific data.
        
        This function will store a list of tuples as a value under the key
        ``"csrf_tokens"``. Each tuple will contain a string and an integer.

    :param url:
        The url under which the form is available.

    :param force_update:
        If `force_update` is ``True`` a new token is stored even if one is
        already available.

    :param max_csrf_tokens:
        A positive integer specifing the maximum number of tokens stored in the
        session.
        
        .. note:: If more tokens are stored then specified by this number they
                  won't be removed unless a new token is created.
    """
    url_hash = _get_url_hash(url)
    stored_tokens = session.setdefault("csrf_tokens", [])
    token = None
    if not force_update:
        for stored_url_hash, stored_token in stored_tokens:
            if stored_url_hash == url_hash:
                token = stored_token
                break
    if token is None:
        while len(stored_tokens) >= max_csrf_tokens:
            stored_tokens.pop(0)
        token = _get_random_token()
        stored_tokens.append((url_hash, token))
        session["csrf_tokens"] = stored_tokens
    return token.encode("hex")

def _remove_csrf_token(session, url):
    """
    Removes every ``(url_hash, csrf_token)`` tuple from the session for the
    given `url`. If no tuple is found this function does nothing.

    This function should be used to remove the csrf token from the session
    after the form was validated, to ensure that every token can be only used
    once.

    :param session:
        An object with a dict-like interface which can be used to store session
        specific data.

        This function will store a list of tuples as a value under the key
        ``"csrf_tokens"``. Each tuple will contain a string and an integer.

    :param url:
        The url under which the form is available.
    """
    url_hash = _get_url_hash(url)
    tokens = session.get("csrf_tokens", None)
    if tokens:
        session["csrf_tokens"] = [(h, t) for h, t in tokens if h != url_hash]

__all__ = ["_get_random_token", "_get_csrf_token", "_remove_csrf_token"]
