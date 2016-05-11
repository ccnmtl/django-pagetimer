import base64
import hashlib

from django.db import models
from django.utils.encoding import smart_bytes


def process_session_key(session_key):
    """ with cookie based sessions, the `session_key` is a really
    long, ugly string. We don't actually care about the value;
    we just want to use it as a unique identifier. So we
    hash it down to something smaller and easier to eyeball."""
    if session_key is None:
        return "None"
    return base64.b64encode(hashlib.sha1(smart_bytes(session_key)).digest())


class PageVisitManager(models.Manager):
    def log_visit(self, username, session_key, path, ipaddress):
        if username == "":
            username = "anonymous"
        p = PageVisit(
            username=username,
            session_key=process_session_key(session_key),
            path=path,
            ipaddress=ipaddress,
        )
        p.save()
        return p

    def earliest(self):
        f = self.all().order_by("visited").first()
        if f is None:
            return None
        return f.visited

    def latest(self):
        l = self.all().order_by("-visited").first()
        if l is None:
            return None
        return l.visited

    def summarize(self):
        return dict(
            count=self.all().count(),
            earliest=self.earliest(),
            latest=self.latest(),
            users=self.values('username').distinct().count(),
            sessions=self.values('session_key').distinct().count(),
            ipaddresses=self.values('ipaddress').distinct().count(),
            paths=self.values('path').distinct().count(),
        )


class PageVisit(models.Model):
    username = models.TextField(default="anonymous")
    ipaddress = models.GenericIPAddressField()
    path = models.TextField(default="/")
    visited = models.DateTimeField(auto_now_add=True)
    session_key = models.TextField(default="")

    objects = PageVisitManager()

    class Meta:
        ordering = ["-visited"]
