#! /usr/bin/env python
# -*- coding: utf8 -*-
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

import unittest

from kpwrapper import Triple, uri, literal
from asibsync.sib_agent import to_rdf_instance, to_rdf_ontology, to_struct, recursivedefaultdict

def counter(start = 1):
    s = [start]
    def acc():
        t = s[0]
        s[0] += 1
        return t
    return acc

uid = '1234'
base_uri = 'http://cos.alpha.sizl.org/people'
user_uri = base_uri + '/ID#' + uid
addr_uri = base_uri + '#1'
avatar_uri = base_uri + '#2'
link_uri = base_uri + '#3'

class Test(unittest.TestCase):
    def setUp(self):
        self.d = dict(id='1234',
                      name='Eric',
                      favorite_food='eggs',
                      address=dict(street_address='Castle of Anthrax', postal_code='00001'),
                      avatar=dict(link=dict(href='http://python.org/favicon.ico', rel='self'), status='set'))
        
        self.ontology = [Triple('http://cos.alpha.sizl.org/people#Person', 'rdf:type', uri('rdfs:Class')),
                         Triple('http://cos.alpha.sizl.org/people#Address', 'rdf:type', uri('rdfs:Class')),
                         Triple('http://cos.alpha.sizl.org/people#Avatar', 'rdf:type', uri('rdfs:Class')),
                         Triple('http://cos.alpha.sizl.org/people#Link', 'rdf:type', uri('rdfs:Class')),
                         #properties...
                         ]
        
        self.rdf = [Triple(user_uri, 'rdf:type', uri('http://cos.alpha.sizl.org/people#Person')),
                    Triple(user_uri, 'http://cos.alpha.sizl.org/people#name', 'Eric'),
                    Triple(user_uri, 'http://cos.alpha.sizl.org/people#favorite_food', 'eggs'),
                    Triple(user_uri, 'http://cos.alpha.sizl.org/people#address', uri(addr_uri)),
                    Triple(user_uri, 'http://cos.alpha.sizl.org/people#avatar', uri(avatar_uri)),
                    Triple(addr_uri, 'rdf:type', uri('http://cos.alpha.sizl.org/people#Address')),
                    Triple(addr_uri, 'http://cos.alpha.sizl.org/people#street_address', 'Castle of Anthrax'),
                    Triple(addr_uri, 'http://cos.alpha.sizl.org/people#postal_code', '00001'),
                    Triple(avatar_uri, 'rdf:type', uri('http://cos.alpha.sizl.org/people#Avatar')),
                    Triple(avatar_uri, 'http://cos.alpha.sizl.org/people#link', uri(link_uri)),
                    Triple(avatar_uri, 'http://cos.alpha.sizl.org/people#status', 'set'),
                    Triple(link_uri, 'rdf:type', uri('http://cos.alpha.sizl.org/people#Link')),
                    Triple(link_uri, 'http://cos.alpha.sizl.org/people#href', 'http://python.org/favicon.ico'),
                    Triple(link_uri, 'http://cos.alpha.sizl.org/people#rel', 'self'),
                    ]

        rdf = self.rdf
        class DummySIBConnection():
            def query(self, q):
                return [triple for triple in rdf if ((q.subject is None or triple.subject==q.subject) and
                                                     (q.predicate is None or triple.predicate==q.predicate) and
                                                     (q.object is None or triple.object==q.object))]
        self.dsc = DummySIBConnection()

    def test_self_dsc(self):
        self.assertEquals(3, len(self.dsc.query(Triple(addr_uri, None, None))))
        self.assertEquals(4, len(self.dsc.query(Triple(None, 'rdf:type', None))))
        self.assertEquals(1, len(self.dsc.query(Triple(None, None, 'set'))))

    def test_recursivedefaultdict(self):
        d = recursivedefaultdict()
        d[1][2][3] = 4
        self.assertEquals(4, d[1][2][3])

    def test_to_rdf_ontology(self):
        self.assertEquals(sorted(self.ontology),
                          sorted(to_rdf_ontology(self.d, 'http://cos.alpha.sizl.org/people', 'Person')))

    def test_to_rdf_instance(self):
        self.assertEquals(sorted(self.rdf),
                          sorted(to_rdf_instance(self.d, 'http://cos.alpha.sizl.org/people', 'Person', 'id',
                                               counter())))

    def test_to_struct_flat(self):
        struct = dict(id='1234', name='Eric')
        query = Triple(user_uri, 'http://cos.alpha.sizl.org/people#name', 'Eric')
        self.assertEquals(struct, to_struct(self.dsc, query, base_uri))

    def test_to_struct_1_level(self):
        struct = dict(id='1234',
                      avatar=dict(status='set'))
        query = Triple(avatar_uri,
                       'http://cos.alpha.sizl.org/people#status',
                       'set')

        self.assertEquals(struct, to_struct(self.dsc, query, base_uri))

    def test_to_struct_2_levels(self):
        struct = dict(id='1234',
                      avatar=dict(link=dict(href='http://python.org/favicon.ico')))
        query = Triple(link_uri,
                       'http://cos.alpha.sizl.org/people#href',
                       'http://python.org/favicon.ico')

        self.assertEquals(struct, to_struct(self.dsc, query, base_uri))

if __name__ == "__main__":
    unittest.main()
