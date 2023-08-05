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

from __future__ import print_function

__author__ = 'eemeli.kantola@iki.fi (Eemeli Kantola)'

import sys
import smart_m3.discovery as discovery
from datetime import datetime

discovery._old_discover = discovery.discover
def discover(type = "Manual", name = None):
    if type == "preconfigured":
        return discover_preconfigured_tcp()
    else:
        return discovery._old_discover(type, name)

discovery.discover = discover

debug = True

def log(*objs):
    sys.stderr.write('[%s] kpwrapper: %s\n' % (datetime.now(),
                                               ' '.join([str(obj) for obj in objs])))

def debug_log(*objs):
    if debug:
        log(*objs)

def discover_preconfigured_tcp():
    import os
    try:
        conffile = os.getenv("HOME") + "/.kprc"
        debug_log("Preconfigured discovery using config from %s" % conffile)
        node_params = eval(open(conffile).read())
        debug_log("Got params: " + str(node_params))
        return node_params
    except Exception, e:
        log("Reading config failed: %s" % e)
        log("Falling back to manual discovery")
        return discovery.discover_Manual_TCP()
