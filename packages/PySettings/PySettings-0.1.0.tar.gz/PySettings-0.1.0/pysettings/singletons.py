# Copyright (c) 2010, Robert Escriva
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of this project nor the names of its contributors may
#       be used to endorse or promote products derived from this software
#       without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


'''Utilities for simulating singletons in a thread-safe manner.

These utilities provide a global ``state`` that may be accessed to remember the
results of a callable.

Most notably, this can be used to provide singletons for an application in which
each thread may have a distinct global state.
'''


import weakref


__all__ = ['SingletonHolder']


class SingletonHolder(object):
    '''The SingletonHolder carries a "state" for storing singleton objects.

    It is common design to re-use objects in several places.  Often these
    objects are dependent upon the rest of the global state.  To avoid having to
    set up true singleton objects (and thus limit the ability of applications to
    handle two different configuration states), this object serves as a place
    holder to explicitly declare global objects that are dependent upon the
    configuration of an application.
    '''

    def __init__(self, settings):
        self._settings = weakref.ref(settings)
        self._instances = dict()

    def get(self, klass, *args, **kwargs):
        '''Save the result of calling ``klass`` with settings, args, kwargs.

        The ``klass`` object must be hashable and callable.

        The first call to any combination of (klass, args, kwargs) will call
        klass with (settings, *args, **kwargs) and save the result.  If
        ``klass`` needs to keep a reference to the settings, it should use a
        weak-reference.

        Calling :func:`get` with the same value of ``klass`` with different
        args/kwargs is an error.

            >>> s = Settings()
            >>> sh = SingletonHolder(s)
            >>> def klass(settings, *args, **kwargs):
            ...     print 'Called ``klass``'
            ...     return (args, kwargs)
            >>> sh.get(klass)
            Called ``klass``
            ((), {})
            >>> sh.get(klass)
            ((), {})

        Notice that this is an error as we called ``klass`` above with no
        options.

            >>> sh.get(klass, 1, 2, 3, foo='bar', baz='quux')
            Traceback (most recent call last):
            ValueError: ``klass`` already called with different values.

        If the weakreference is no longer valid, then a RuntimeError will be
        raised.

            >>> s = Settings()
            >>> sh = SingletonHolder(s)
            >>> del s
            >>> sh.get(lambda x: x)
            Traceback (most recent call last):
            RuntimeError: Weak reference to dead Settings object.

        '''
        if klass not in self._instances:
            settings = self._settings()
            if settings is None:
                raise RuntimeError("Weak reference to dead Settings object.")
            val = klass(settings, *args, **kwargs)
            self._instances[klass] = (val, args, kwargs)
        val, old_args, old_kwargs = self._instances[klass]
        if old_args != args or old_kwargs != kwargs:
            raise ValueError('``klass`` already called with different values.')
        return val


def _setUp(test):
    from pysettings.settings import Settings
    test.globs['Settings'] = Settings
