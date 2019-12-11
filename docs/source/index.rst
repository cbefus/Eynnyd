.. EYNNYD documentation master file, created by
   sphinx-quickstart on Mon Dec  9 20:09:45 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

The EYNNYD Web Framework
========================

Eynnyd (pronounced [Ey-nahyd]) is an acronym for **Everything You Need, Nothing You Don't**. It is a
light-weight WSGI compliant python 3 web framework. Eynnyd was designed with the primary goal to
not impose bad engineering decisions on it's users. It is also designed to not overstep or assume
the wants of it's user.

Other frameworks weigh you down with extraneous dependencies, unnecessary inheritance, highly coupled
design, forced restrictions into REST, forced function naming, magic global singletons, and so much more.

.. code:: python

    from eynnyd import RoutesBuilder
    from eynnyd import EynnydWebappBuilder
    from eynnyd import ResponseBuilder

     def hello_world(request):
         return ResponseBuilder() \
             .set_utf8_body("Hello World") \
             .build()

     routes = \
         RoutesBuilder() \
             .add_handler("GET", "/hello", hello_world) \
             .build()

     application = \
         EynnydWebappBuilder() \
             .set_routes(routes) \
             .build()


Why Use Eynnyd?
---------------
Eynnyd was created to provide all the power of a WSGI web framework without imposing extraneous decision
restricting your design.  You can use Eynnyd with minimal interaction with the framework.

The priorities when building Eynnyd are as follows:

1. **Readable:** By using intention revealing names, small functions with single
levels of abstraction, pushing conditionals up the stack, avoiding exceptions for control flow, and all the
other core principles of good software engineering (found in
`Clean Code <https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship-dp-0132350882/dp/0132350882>`__),
the code in Eynnyd is designed to be easily read and understood by other developers (or even just ourselves in
the future).  Given that it should be easy to read our code, it should be easy to extend, fix bugs, test, and
improve over time; thus why this is our top priority.

2. **Flexible:** Our framework was fueled from a frustration of restrictive engineering decisions being
imposed upon users from other frameworks.  Our goal was freedom for you to design your own implementations, your
way. With our framework you can:

   * Use Object-oriented, procedural, or functional design.
   * Use REST, REST-like, or completely ad-hoc API design.
   * Name your functions anything you like, allowing you to be expressive with your naming.
   * Use dependency injection, or don't.
   * Have as many interceptors (both request and response) as you like and restrict the routes they wrap.
   * Pick whatever libraries are best for your dependencies (Not some selection we made for you).
   * And pretty much anything else you want to do.

3. **Extensible:** Designed following the **SOLID** principles, adding new features should be easily done
without having to dig through miles of coupled code.  This means that we can address feature requests quickly
and maintain confidence in our backwards compatibility.

4. **Reliable:** To add confidence to our code we have an extensive suite of unittests covering our framework.
While we don't actually believe in the validity of code coverage measurements (bad tests are worse than no
tests) we purposely pushed our coverage to 100% (Largely this was for marketing purposes).  But the important
paths of execution in our code are heavily covered in layers of well designed tests. In doing so we
wrote highly decoupled tests which all follow the F.I.R.S.T. principles of good unittests.  With these tests we
can address bugs and add features with high confidence that we are not introducing new bugs.

5. **Predictable:** With Eynnyd you get pretty-much-what-you-expect.  We don't bury exceptions, or assume
implementation. We wont parse your body into JSON for you or any other magic.  We also work hard to provide
you with a strong-borders-free-society environment; by doing validation at the edge we can raise errors as close
to their implementation as possible, instead of deep in the belly of unrelated logic.

6. **Fast:** Let's be honest, when dealing with HTTP overhead speed is a luxury.  Certainly the various
frameworks range in their speed, and handle very specific situation better or worse than each other, but the
best any WSGI framework can do is match the speed of raw WSGI.  With the other priorities on this list
maximized we will continue to re-evaluate our design and speed to make progress here, but never at the cost
of higher priority items.  Our goal is to not be wasteful with our speed.  We will follow up with actual
comparisons between our framework and others soon.  However, if you absolutely need something faster than
Eynnyd, you probably should look into non HTTP type frameworks or at least non WSGI frameworks.


Documentation
-------------
.. toctree::
   :maxdepth: 3

   guide/index
   api/index
