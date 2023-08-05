#!/usr/bin/python
# -*- coding: utf-8 -*-

import grokcore.component as grok
from beaker.session import SessionObject
from dolmen.beaker.interfaces import ISession, ISessionConfig, ENVIRON_KEY
from zope.component import queryUtility
from zope.publisher.interfaces import IEndRequestEvent
from zope.publisher.interfaces.http import IHTTPRequest
from zope.session.interfaces import ISession as IZopeSession, ISessionData
from zope.site.interfaces import IRootFolder
from zope.traversing.interfaces import IBeforeTraverseEvent
from zope.schema.fieldproperty import FieldProperty


@grok.adapter(IHTTPRequest)
@grok.implementer(ISession)
def BeakerSession(request):
    """Adapter factory from a Zope request to a beaker session
    """
    session = request._environ.get(ENVIRON_KEY, None)
    if session is not None:
        return session
    return initializeSession(request)


class NamespaceSessionData(object):
    """A session, prefixing keys with a namespace
    """
    grok.implements(ISessionData)

    lastAccessTime = FieldProperty(ISessionData['lastAccessTime'])
    
    def __init__(self, session, namespace):
        self.session = session
        self.namespace = namespace

    def getLastAccessTime(self):
        return self.lastAccessTime

    def setLastAccessTime(self):
        raise NotImplementedError

    def __getitem__(self, name):
        return self.session.__getitem__(
            "%s.%s" % (self.namespace, name))

    def get(self, name, default=None):
        if name in self:
            return self.__getitem__(name)
        return default

    def __setitem__(self, name, value):
        self.session["%s.%s" % (self.namespace, name)] = value
        self.session.save()

    def __contains__(self, name):
        return "%s.%s" % (self.namespace, name) in self.session

    def __delitem__(self, name):
        self.session.__delitem__("%s.%s" % (self.namespace, name))
        self.session.save()

    def setdefault(self, name, default=None):
        if name not in self:
            self.__setitem__(name, default)
        return self.__getitem__(name)


class ZopeSession(grok.Adapter):
    grok.context(IHTTPRequest)
    grok.implements(IZopeSession)

    def __init__(self, request):
        self.request = request
        self.session = ISession(request)
        if self.session is None:
            raise NotImplementedError

    def keys(self):
        return self.session.keys()

    def items(self):
        return self.session.items()

    def values(self):
        return self.session.values()

    def __getitem__(self, namespace):
        return NamespaceSessionData(self.session, namespace)

    def get(self, namespace, default=None):
        return NamespaceSessionData(self.session, namespace)

    def delete(self):
        self.session.delete()


def initializeSession(request, environ_key=ENVIRON_KEY):
    """Create a new session and store it in the request.
    """
    options = queryUtility(ISessionConfig)
    if options is not None:
        session = SessionObject(request, **options)
        request._environ[environ_key] = session
        return session
    return None


def closeSession(request):
    """Close the session, and, if necessary, set any required cookies
    """
    session = ISession(request, None)
    if session is not None:
        if session.accessed():
            session.persist()
            sessionInstructions = session.request
            if sessionInstructions.get('set_cookie', False):
                if sessionInstructions['cookie_out']:
                    cookieObj = session.cookie[session.key]
                    key = cookieObj.key
                    value = session.cookie.value_encode(cookieObj.value)[1]
                    args = dict([(k, v) for k, v in cookieObj.items() if v])
                    args.setdefault('path', session._path)
                    request.response.setCookie(key, value, **args)


@grok.subscribe(IRootFolder, IBeforeTraverseEvent)
def configureSession(obj, event):
    initializeSession(event.request)


@grok.subscribe(IEndRequestEvent)
def persistSession(event):
    closeSession(event.request)
