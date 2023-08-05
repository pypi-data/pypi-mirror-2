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


'''Objects for storing settings.

These objects will store the collection of settings for the application.
'''


class Settings(object):
    '''A collection of settings for an application.

    This object contains settings in a mutable, key-value way.

    Initialize the settings with key-value pairs.

        >>> s = Settings(FOO='hello', BAR='world', baz='lowercase too')
        >>> s.FOO
        'hello'
        >>> s.BAR
        'world'
        >>> s.baz
        'lowercase too'

    Dictionaries can be used too.

        >>> d = {'FOO':'hello', 'BAR':'world'}
        >>> e = {'baz':'lowercase too'}
        >>> s = Settings(d, e)
        >>> s.FOO
        'hello'
        >>> s.BAR
        'world'
        >>> s.baz
        'lowercase too'

    Mixing dictionaries and key-value pairs is OK too.  When mixing, the
    key-value pairs take precedence.

        >>> d = {'FOO':'hello', 'BAR':'world'}
        >>> s = Settings(d, BAR='earth', baz='lowercase too')
        >>> s.FOO
        'hello'
        >>> s.BAR
        'earth'
        >>> s.baz
        'lowercase too'
        >>> s.quux
        Traceback (most recent call last):
        AttributeError: 'Settings' object has no attribute 'quux'

    Notice that key names may not start with an underscore.

        >>> s = Settings(_foo='invalid')
        Traceback (most recent call last):
        ValueError: Settings' keys may not begin with '_'.

    '''

    def __init__(self, *args, **kwargs):
        if len(filter(lambda k: k.startswith('_'), kwargs.keys())) > 0:
            raise ValueError("Settings' keys may not begin with '_'.")
        self._values = dict()
        for arg in args:
            self._values.update(arg)
        self._values.update(kwargs)

    def __getattr__(self, name):
        if name in self._values:
            return self._values[name]
        else:
            error = "'Settings' object has no attribute '%s'" % name
            raise AttributeError(error)
