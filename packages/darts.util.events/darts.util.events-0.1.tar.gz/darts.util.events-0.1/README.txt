
Preface
========

Introduction
-------------

This library provides a simple event dispatcher, similar to the
`event` construct provided by the C# language. The library has no
external dependencies.

It was intended for use cases, where the components emitting events 
and the components listening for events agree about the type of 
event and the semantics associated with it. This is true, for example,
for event handlers, which listen on "click" events signalled by
GUI button objects, or notifications signalled by objects, whenever
the value of some property changes. This differs from the approach
taken by, say, the `PyDispatcher`, which is more generic, and 
favours communication among weakly coupled components.


Compatibility
--------------

The code was written for and tested with Python 2.6. It should 
be compatible to 2.5 as well, but you might have to insert a few
`from __future__ import with_statement` lines here and there. It
should work (this has not been tested) with alternative implementations
of Python like Jython or IronPython. Note, though, that some of 
the test cases defined in this file might fail due to different
garbage collection implementations; this file was written with
CPython in mind.


Documentation
==============

Basic Usage
------------

    >>> from darts.lib.utils.event import Publisher, ReferenceRetention as RR
    >>> some_event = Publisher()

The `Publisher` is the main component. It acts as registry for 
callbacks/listeners. Let's define a listener

    >>> def printer(*event_args, **event_keys):
    ...     print event_args, event_keys

In order to receive notifications, clients must subscribe to a 
publisher. This can be as simple as

    >>> some_event.subscribe(printer)              #doctest: +ELLIPSIS
    <SFHandle ...>

The result of the call to `subscribe` is an instance of (some subclass
of) class `Subscription`. This value may be used later, in order to 
cancel the subscription, when notifications are no longer desired. The
actual subclass is an implementation detail you should normally not
care about. All you need to know (and are allowed to rely on, in fact)
is, that it will be an instance of class `Subscription`, and it will
provide whatever has been documented as public API of that class (right
now: only method `cancel`).

Now, let's signal an event and see what happens:

    >>> some_event.publish('an-event')
    ('an-event',) {}

As you can see, the `printer` has been notified of the event, and
duefully printed the its arguments to the console.


Cancelling subscriptions
-------------------------

As mentioned, the result of calling `subscribe` is a special subscription
object, which represents the registration of the listener with the 
publisher.

    >>> s1 = some_event.subscribe(printer)
    >>> some_event.publish('another-event')
    ('another-event',) {}
    ('another-event',) {}
    >>> s1.cancel()
    True
    >>> some_event.publish('yet-another-one')
    ('yet-another-one',) {}

The publisher is fully re-entrant. That means, that you can subscribe
to events from within a listener, and you can cancel subscriptions in
that context as well:

    >>> def make_canceller(subs):
    ...     def listener(*unused_1, **unused_2):
    ...         print "Cancel", subs, subs.cancel()
    ...     return listener
    >>> s1 = some_event.subscribe(printer)
    >>> s2 = some_event.subscribe(make_canceller(s1))
    >>> some_event.publish('gotta-go')             #doctest: +ELLIPSIS
    ('gotta-go',) {}
    ('gotta-go',) {}
    Cancel <SFHandle ...> True
    >>> some_event.publish('gone')                 #doctest: +ELLIPSIS
    ('gone',) {}
    Cancel <SFHandle ...> False
    >>> s1.cancel()
    False

The result of the call to `cancel` tells us, that the subscription had 
already been undone prior to the call (by our magic cancellation listener). 
Generally, calling `cancel` multiple times is harmless; all but the first 
call are ignored.

Let's now remove the magic I-can-cancel-stuff listener and move on:

    >>> s2.cancel()
    True


Reference Retention
---------------------

Whenever we made subscriptions above, we actually simplied things a
little bit. The full signature of the method is:

    def subscribe(listener[, method[, reference_retention]])

Let's explore the `method` argument first. Up to now, we only used
function objects as listeners. Basically, in fact, we might have used
any callable object. Remember, that any object is "callable" in Python,
if it provides a `__call__` method, so guess, what's the default value
of the `method` argument?

    >>> s1 = some_event.subscribe(printer, method='__call__')
    >>> some_event.publish('foo')
    ('foo',) {}
    ('foo',) {}
    >>> s1.cancel()
    True

Nothing new. So, now you might ask: when do I use a different method
name?

    >>> class Target(object):
    ...    def __init__(self, name):
    ...        self.name = name
    ...    def _callback(self, *args, **keys):
    ...        print self.name, args, keys
    >>> s1 = some_event.subscribe(Target('foo'))
    >>> some_event.publish('Bumm!')               #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: 'Target' object is not callable

Oops. Let's remove the offender, before someone notices our mistake:

    >>> s1.cancel()
    True
    >>> s1 = some_event.subscribe(Target('foo'), method='_callback')
    >>> some_event.publish('works!')
    ('works!',) {}
    foo ('works!',) {}

So, that's that. There is still an unexplored argument to `subscribe`
left, though: `reference_retention`. The name sounds dangerous, but what
does it do?

    >>> listener = Target('yummy')
    >>> s2 = some_event.subscribe(listener, method='_callback', reference_retention=RR.WEAK)
    >>> some_event.publish('yow')
    ('yow',) {}
    foo ('yow',) {}
    yummy ('yow',) {}

Hm. So far, no differences. Let's make a simple change:

    >>> listener = None
    >>> some_event.publish('yow')
    ('yow',) {}
    foo ('yow',) {}

Ah. Ok. Our `yummy` listener is gone. What happened? Well, by specifying
a reference retention policy of `WEAK`, we told the listener, that it should
use a weak reference to the listener just installed, instead of the default
strong reference. And after we released the only other known strong 
reference to the listener by setting `listener` to `None`, the listener
was actually removed from the publisher. Note, BTW., that the above example
may fail with python implementations other than CPython, due to different
policies with respect to garbage collection. The principle should remain
valid, though, in Jython as well as IronPython, but in those implementations,
there is no guarantee, that the listener is removed as soon as the last
reference to it is dropped. 

Of course, this all works too, if the method to be called is the default
one: `__call__`:

    >>> def make_listener(name):
    ...    def listener(*args, **keys):
    ...        print name, args, keys
    ...    return listener
    >>> listener = make_listener('weak')
    >>> s2 = some_event.subscribe(listener, reference_retention=RR.WEAK)
    >>> some_event.publish('event')
    ('event',) {}
    foo ('event',) {}
    weak ('event',) {}
    >>> listener = None
    >>> some_event.publish('event')
    ('event',) {}
    foo ('event',) {}

That's about all there is to know about the library. As I said above: it
is simple, and might not be useful for all scenarioes and use cases, but
it does what it was written to.


Error handling
----------------

The `Publisher` class may be subclassed. This is useful, for example, in
order to define the behaviour of instances, when a listener raises an
exception while being notified.

    >>> def toobad(event):
    ...    if event == 'raise':
    ...        raise ValueError
    >>> s1 = some_event.subscribe(toobad)
    >>> some_event.publish('harmless')
    ('harmless',) {}
    foo ('harmless',) {}
    >>> some_event.publish('raise')
    Traceback (most recent call last):
    ...
    ValueError

As you can see, the default behaviour is to re-raise the exception
from within `publish`. This might, however, not always be the desired
effect. So, let's define our own error handling:

    >>> class CarefulPublisher(Publisher):
    ...    def _handle_exception(self, exception, value, traceback, subscription, args, keys):
    ...        print "Caught", exception
    >>> publisher = CarefulPublisher()
    >>> publisher.subscribe(toobad)                    #doctest: +ELLIPSIS
    <SFHandle ...>
    >>> publisher.subscribe(printer)                   #doctest: +ELLIPSIS
    <SFHandle ...>
    >>> publisher.publish('harmless')
    ('harmless',) {}
    >>> publisher.publish('raise')
    Caught <type 'exceptions.ValueError'>
    ('raise',) {}

When subclassing `Publisher`, you may use the value of the `_lock`
property, which is a standard `threading.RLock` instance. Note, that 
the lock is *not* held during publishing (and in particular, it is not
held when your error handler method is called). If you need the lock
grabbed there, you have to grab it yourself.

Also note, that right now, `_handle_exception` is the only method
designed to be overridden by subclasses. You are on your own, if you
actually choose to override any other method in class `Publisher`.

XXX: I am planning to remove the method alltogether, and replace it
with an "error handling strategy" function, which you supply to the 
constructor of the publisher. Even better would be to be a way to 
supply an error handling strategy on calls to `publish`.


Famous last words
==================

The library is fully thread aware and thread safe. Thus, subscribing to
a listener shared across multiple threads is safe, and so is cancelling
subscriptions.

