.. _faq:

Frequently Asked Questions
==========================

* **Another WSGI web framework? Why not just fix (or add on to) an existing one?**
We tried that first.  We pared our merge request down to only a minor element of Eynnyd and still our contribution
was deemed "too big" to merge.  To get the framework we always wished we had we decided the more direct route
was to build our own.

* **What about speed? How fast are you compared to other frameworks?**
We are first prioritizing code quality and correctness. Once we nail those we will worry about speed. Our goal is
not now, nor will it ever be, to be the fastest framework out there, however we do aim to perform within the range
of other frameworks, such that Eynnyd is an acceptable solution for production applications.

* **What python versions do you support and why?**
We use functools.lru_cache() which limits us to python >3.2 but since python 2 is about to be deprecated we feel
this isn't a limiting constraint. We may add a different caching system, or backwards compatibility for python 2
in the near future, but this does not feel like a major priority.
