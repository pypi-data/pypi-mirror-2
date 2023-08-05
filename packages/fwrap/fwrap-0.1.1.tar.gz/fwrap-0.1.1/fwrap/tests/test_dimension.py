#------------------------------------------------------------------------------
# Copyright (c) 2010, Kurt W. Smith
# 
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
#     * Neither the name of the Fwrap project nor the names of its contributors
#       may be used to endorse or promote products derived from this software
#       without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#------------------------------------------------------------------------------

from fwrap import pyf_iface as pyf

from nose.tools import raises, ok_, eq_

def _test_scal_int_expr():
    sie = pyf.ScalarIntExpr("kind('a')")
    eq_(sie.find_names(), set(['kind']))

def _setup(self):
    self.colon = pyf.Dim(':')
    self.colon_parsed = pyf.Dim(('',''))
    self.lbound = pyf.Dim('n:')
    self.lubound = pyf.Dim('10:20')
    self.lubound_parsed = pyf.Dim(('1', '1'))
    self.e1, self.e2 =('nx%y + 1', 'size(a, 3-N) + kind(NX%Z)')
    self.expr = pyf.Dim((self.e1, self.e2))
    self.explicit1 = pyf.Dim('10')
    self.explicit2 = pyf.Dim('anteohusatnheuo%asnotehusaeontuh')
    self.explicit3 = pyf.Dim(('LDIM',))

    self.assumed_size1 = pyf.Dim(('0:*'))
    self.assumed_size2 = pyf.Dim(('n','*'))

class test_dim(object):

    def setup(self):
        _setup(self)

    @raises(ValueError)
    def test_ubound(self):
        pyf.Dim(':10')

    def test_sizeexpr(self):
        eq_(self.colon.sizeexpr, None)
        eq_(self.colon_parsed.sizeexpr, None)
        eq_(self.lbound.sizeexpr, None)
        eq_(self.assumed_size1.sizeexpr, None)
        eq_(self.assumed_size2.sizeexpr, None)
        eq_(self.lubound.sizeexpr, '((20) - (10) + 1)')
        eq_(self.lubound_parsed.sizeexpr, '((1) - (1) + 1)')
        eq_(self.expr.sizeexpr, "((%s) - (%s) + 1)" % (self.e2.lower(), self.e1.lower()))
        eq_(self.explicit1.sizeexpr, "(10)")
        

    def test_names(self):
        epty = set()
        eq_(self.colon.depnames, epty)
        eq_(self.colon_parsed.depnames, epty)
        eq_(self.lbound.depnames, set(['n']))
        eq_(self.lubound.depnames, epty)
        eq_(self.expr.depnames, set(['nx', 'size', 'a', 'n', 'kind']))


    def test_isassumedshape(self):
        ok_(self.colon.is_assumed_shape)
        ok_(self.colon_parsed.is_assumed_shape)
        ok_(self.lbound.is_assumed_shape)
        ok_(not self.lubound.is_assumed_shape)
        ok_(not self.lubound_parsed.is_assumed_shape)
        ok_(not self.expr.is_assumed_shape)


class test_dimension(object):

    def setup(self):
        _setup(self)
        self.dims = pyf.Dimension((self.colon, self.lbound, self.lubound, self.expr))

    def test_names(self):
        eq_(self.dims.depnames, self.lbound.depnames.union(self.expr.depnames))

    def test_dimspec(self):
        eq_(self.dims.attrspec,
                ('dimension(:, n:, 10:20, %s:%s)' %
                    (self.e1.lower(), self.e2.lower())))

    def test_len(self):
        eq_(len(self.dims), 4)
