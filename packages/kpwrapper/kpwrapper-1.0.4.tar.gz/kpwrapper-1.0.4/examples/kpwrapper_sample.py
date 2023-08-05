#! /usr/bin/env python
#
# Copyright (c) 2009, Nokia Corp.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Nokia nor the names of its contributors may be
#       used to endorse or promote products derived from this software without
#       specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED THE COPYRIGHT HOLDERS AND CONTRIBUTORS ''AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

__author__ = 'eemeli.kantola@iki.fi (Eemeli Kantola)'

from kpwrapper import SIBConnection, Triple

if __name__ == '__main__':
    with SIBConnection('SIB console', 'preconfigured') as sc:
        results = sc.query(Triple('Space', 'has', None))
        contents = [triple.object for triple in results]
        print('Space has %s' % contents)
        # prints "Space has []"

        sc.insert(Triple('Space', 'has', 'space_junk'))

        results = sc.query(Triple('Space', 'has', None))
        new_contents = [triple.object for triple in results]
        print('Now space has %s' % new_contents)
        # prints "Now space has [literal('space_junk')]"

        sc.remove([Triple('Space', 'has', x) for x in new_contents])
        results = sc.query(Triple('Space', 'has', None))
        contents = [triple.object for triple in results]
        print('Extra junk removed, now Space has again %s' % contents)
        # prints "Extra junk removed, now Space has again []"
