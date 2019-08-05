
# Eynnyd WebServer
Eynnyd (pronounced [Ey-nahyd]) is an acronym for **Everything You Need, Nothing
You Don't**. It is a light-weight wsgi compliant python 3 web server framework.
Eynnyd was designed with the primary goal to not impose bad engineering decisions
on it's users.

It is also designed to not overstep or assume the wants of it's user.
Therefore, it does't provide things like "smart" media decoding of request bodies,
as this should be done by the end user. Unlike many other frameworks, it does not
try to push its users towards a strict REST design, nor does it prevent it.  It
does not make dependency injection difficult.

## Notes
must use python >3.2 (functools.lru_cache())
