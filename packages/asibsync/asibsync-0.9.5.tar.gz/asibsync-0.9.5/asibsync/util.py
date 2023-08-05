# Copyright (c) 2010, Nokia Corp.
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
import types
from datetime import datetime

def bind_logging(instance, debug):
    def log(self, *objs):
        sys.stderr.write('[%s] %s: %s\n' % (datetime.now(), self.__class__.__name__,
                                            ' '.join([str(obj) for obj in objs])))
    
    def noop(self, *objs):
        pass
    
    instance.log = types.MethodType(log, instance, instance.__class__)
    
    instance.debug_log = types.MethodType((log if debug else noop), instance, instance.__class__)
    instance.debug_log('Debug mode enabled')

def profile(*methods):
    for method in methods:
        instance = method.im_self
        profiled_func = profiled(method.__func__, header_str = method.im_class.__name__ + '.')
        profiled_method = types.MethodType(profiled_func, instance, instance.__class__)
        setattr(instance, method.__func__.__name__, profiled_method)

def profiled(function, header_str = ''):
    def profiled_function(*args, **kwargs):
        start_time = datetime.now()

        retval = function(*args, **kwargs)

        now = datetime.now()
        delta = now - start_time
        sys.stderr.write('[%s] %s processed in %i.%06i s\n' %
                         (now, header_str + function.__name__,
                          delta.seconds, delta.microseconds))

        return retval

    return profiled_function
