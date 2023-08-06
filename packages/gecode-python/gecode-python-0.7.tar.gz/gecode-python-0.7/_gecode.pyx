## -*- cython -*-
##=============================================================================
## Copyright (C) 2011 by Denys Duchier
##
## This program is free software: you can redistribute it and/or modify it
## under the terms of the GNU Lesser General Public License as published by the
## Free Software Foundation, either version 3 of the License, or (at your
## option) any later version.
## 
## This program is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
## FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
## more details.
## 
## You should have received a copy of the GNU Lesser General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
##=============================================================================

from cython.operator import dereference, preincrement
from libc.stdlib cimport malloc, free

cdef extern from "gecode/int.hh" namespace "Gecode":

    cdef cppclass IntSet_ "::Gecode::IntSet":
        IntSet_()
        IntSet_(int,int)

    cdef cppclass IntVar_ "::Gecode::IntVar":
        int min()
        int max()
        int med()
        int val()
        unsigned int size()
        unsigned int width()
        unsigned int regret_min()
        unsigned int regret_max()
        bint range_()
        bint in_ "in"(int)
        bint assigned()

    cdef cppclass BoolVar_ "::Gecode::BoolVar":
        int min()
        int max()
        int med()
        int val()
        unsigned int size()
        unsigned int width()
        unsigned int regret_min()
        unsigned int regret_max()
        bint range_()
        bint in_ "in"(int)
        bint assigned()

    cdef cppclass IntVarRanges:
        IntVarRanges()
        IntVarRanges(IntVar_&)
        bint operator()()
        void operator++()
        int min()
        int max()

    cdef cppclass IntVarValues:
        IntVarValues()
        IntVarValues(IntVar_&)
        bint operator()()
        bint operator++()
        int val()

cdef extern from "gecode_python.icc" namespace "Gecode":
    
    IntSet_* gecode_intset_from_specarray(int*,int)

cdef extern from "gecode/set.hh" namespace "Gecode":

    cdef cppclass SetVar_ "::Gecode::SetVar":
        unsigned int glbSize()
        unsigned int lubSize()
        unsigned int unknownSize()
        unsigned int cardMin()
        unsigned int cardMax()
        int lubMin()
        int lubMax()
        int glbMin()
        int glbMax()
        bint contains(int)
        bint notContains(int)
        bint assigned()

    cdef cppclass SetVarGlbRanges:
        SetVarGlbRanges()
        SetVarGlbRanges(SetVar_&)
        bint operator()()
        void operator++()
        int min()
        int max()
        unsigned int width()

    cdef cppclass SetVarLubRanges:
        SetVarLubRanges()
        SetVarLubRanges(SetVar_&)
        bint operator()()
        void operator++()
        int min()
        int max()
        unsigned int width()

    cdef cppclass SetVarUnknownRanges:
        SetVarUnknownRanges()
        SetVarUnknownRanges(SetVar_&)
        bint operator()()
        void operator++()
        int min()
        int max()
        unsigned int width()

    cdef cppclass SetVarGlbValues:
        SetVarGlbValues()
        SetVarGlbValues(SetVar_&)
        bint operator()()
        void operator++()
        int val()

    cdef cppclass SetVarLubValues:
        SetVarLubValues()
        SetVarLubValues(SetVar_&)
        bint operator()()
        void operator++()
        int val()

    cdef cppclass SetVarUnknownValues:
        SetVarUnknownValues()
        SetVarUnknownValues(SetVar_&)
        bint operator()()
        void operator++()
        int val()

cdef extern from "gecode/kernel.hh" namespace "Gecode":
    cdef cppclass Space_ "::Gecode::Space"

cdef extern from "gecode-common.icc" namespace "generic_gecode":

    cdef cppclass GenericSpace

    cdef cppclass GenericEngine:
        GenericSpace* next()

    cdef cppclass GenericSpace:
        GenericSpace()
        Space_* space()
        IntVar_ get_ivar(int)
        BoolVar_ get_bvar(int)
        SetVar_ get_svar(int)
        GenericEngine* new_engine()
        int new_ivar(int, int)
        int new_ivar(IntSet_)
        int new_bvar()
        int new_svar(int,int,int,int,int,int)
        int new_svar(int,int,int,int,int)
        int new_svar(int,int,int,int)
        int new_svar(IntSet_,int,int,int,int)
        int new_svar(IntSet_,int,int,int)
        int new_svar(IntSet_,int,int)
        int new_svar(int,int,IntSet_,int,int)
        int new_svar(int,int,IntSet_,int)
        int new_svar(int,int,IntSet_)
        int new_svar(IntSet_,IntSet_,int,int)
        int new_svar(IntSet_,IntSet_,int)
        int new_svar(IntSet_,IntSet_)
        void minimize(int)
        void minimize(int,int)
        void maximize(int)
        void maximize(int,int)

cdef class IntSetSpecMatrix:
    cdef int N
    cdef int M
    cdef int* _array
    ## N=number of lines
    ## M=number of columns
    def __cinit__(self, int n, int m):
        self.N = n
        self.M = m
        self._array = <int*> malloc(n*m*sizeof(int))
    cdef int _index(self, int i, int j):
        return i*self.M + j
    cdef void put(self, int i, int j, int v):
        self._array[self._index(i,j)] = v
    cdef int get(self, int i, int j):
        return self._array[self._index(i,j)]
    def __dealloc__(self):
        free(self._array)

cdef class IntSet:

    cdef IntSet_* _intset

    def __init__(self,X=None,Y=None):
        if X is None:
            self._init_from_nothing()
        elif Y is None:
            self._init_from_specs(X)
        else:
            self._init_from_bounds(X,Y)

    cdef _init_from_nothing(self):
        self._intset = new IntSet_()

    cdef _init_from_bounds(self, int i, int j):
        self._intset = new IntSet_(i,j)

    cdef _init_from_specs(self, object l):
        cdef int n = len(l)
        cdef IntSetSpecMatrix m = IntSetSpecMatrix(n,2)
        cdef int k
        cdef int h
        for i in range(n):
            e = l[0]
            if type(e) is int:
                k = e
                m.put(i, 0, k)
                m.put(i, 1, k)
            else:
                k = e[0]
                h = e[1]
                m.put(i, 0, k)
                m.put(i, 1, h)
        self._intset = gecode_intset_from_specarray(m._array,n)

def intset(x=None, y=None):
    return IntSet(x,y)

cdef class Var:
    cdef int _index
    def __cinit__(self, int i):
        self._index = i

from gecode.boundvar import BoundIntVar, BoundBoolVar, BoundSetVar

cdef class IntVar(Var):
    def __call__(self, space):
        return BoundIntVar(space, self)
cdef class BoolVar(Var):
    def __call__(self, space):
        return BoundBoolVar(space, self)
cdef class SetVar(Var):
    def __call__(self, space):
        return BoundSetVar(space, self)

cdef class ProtoSpace:
    cdef Space_* _to_space_(self):
        return NULL
    cdef GenericSpace* _to_space(self):
        return NULL
    def intvar(self, x, y=None):
        cdef int i
        cdef int j
        cdef IntSet s
        if type(x)==int:
            i = x
            j = y
            return IntVar(self._to_space().new_ivar(i,j))
        s = x
        return IntVar(self._to_space().new_ivar(dereference(s._intset)))
    def boolvar(self):
        return BoolVar(self._to_space().new_bvar())
    def setvar(self,x1,x2,x3=None,x4=None,x5=None,x6=None):
        cdef int i1
        cdef int i2
        cdef int i3
        cdef int i4
        cdef int i5
        cdef int i6
        cdef IntSet s1
        cdef IntSet s2
        cdef IntSet s3
        if x6 is not None:
            i1 = x1
            i2 = x2
            i3 = x3
            i4 = x4
            i5 = x5
            i6 = x6
            return SetVar(self._to_space().new_svar(i1,i2,i3,i4,i5,i6))
        if x5 is not None:
            if type(x1)!=int:
                s1 = x1
                i2 = x2
                i3 = x3
                i4 = x4
                i5 = x5
                return SetVar(self._to_space().new_svar(
                        dereference(s1._intset),i2,i3,i4,i5))
            if type(x3)!=int:
                i1 = x1
                i2 = x2
                s3 = x3
                i4 = x4
                i5 = x5
                return SetVar(self._to_space().new_svar(
                        i1,i2,dereference(s3._intset),i4,i5))
            i1 = x1
            i2 = x2
            i3 = x3
            i4 = x4
            i5 = x5
            return SetVar(self._to_space().new_svar(i1,i2,i3,i4,i5))
        if x4 is not None:
            if type(x1)!=int:
                s1 = x1
                if type(x2)!=int:
                    s2 = x2
                    i3 = x3
                    i4 = x4
                    return SetVar(self._to_space().new_svar(
                            dereference(s1._intset),dereference(s2._intset),
                            i3,i4))
                i2 = x2
                i3 = x3
                i4 = x4
                return SetVar(self._to_space().new_svar(
                        dereference(s1._intset),i2,i3,i4))
            if type(x3)!=int:
                i1 = x1
                i2 = x2
                s3 = x3
                i4 = x4
                return SetVar(self._to_space().new_svar(
                        i1,i2,dereference(s3._intset),i4))
            i1 = x1
            i2 = x2
            i3 = x3
            i4 = x4
            return SetVar(self._to_space().new_svar(i1,i2,i3,i4))
        if x3 is not None:
            if type(x1)!=int:
                s1 = x1
                if type(x2)!=int:
                    s2 = x2
                    i3 = x3
                    return SetVar(self._to_space().new_svar(
                            dereference(s1._intset),
                            dereference(s2._intset),i3))
                i2 = x2
                i3 = x3
                return SetVar(self._to_space().new_svar(
                        dereference(s1._intset),i2,i3))
            i1 = x1
            i2 = x2
            s3 = x3
            return SetVar(self._to_space().new_svar(
                    i1,i2,dereference(s3._intset)))
        s1 = x1
        s2 = x2
        return SetVar(self._to_space().new_svar(
                dereference(s1._intset),dereference(s2._intset)))

    def intvars(self,n,*specs):
        cdef int i
        l = []
        for i in range(n):
            l.append(self.intvar(*specs))
        return l

    def boolvars(self,n):
        cdef int i
        l = []
        for i in range(n):
            l.append(self.boolvar())
        return l

    def setvars(self,n,*specs):
        cdef int i
        l = []
        for i in range(n):
            l.append(self.setvar(*specs))
        return l

    def bind(self, x):
        if isinstance(x, Var):
            return x(self)
        l = []
        for y in x:
            l.append(y(self))
        return l

    cdef IntVar_ _get_ivar(self, IntVar i):
        return self._to_space().get_ivar(i._index)
    cdef BoolVar_ _get_bvar(self, BoolVar b):
        return self._to_space().get_bvar(b._index)
    cdef SetVar_ _get_svar(self, SetVar s):
        return self._to_space().get_svar(s._index)

    cdef void _minimize1(self, IntVar i):
        self._to_space().minimize(i._index)
    cdef void _minimize2(self, IntVar i, IntVar j):
        self._to_space().minimize(i._index, j._index)
    cdef void _maximize1(self, IntVar i):
        self._to_space().maximize(i._index)
    cdef void _maximize2(self, IntVar i, IntVar j):
        self._to_space().maximize(i._index, j._index)

include "gecode_python_enum.pxi"

cdef extern from "gecode-common.icc" namespace "Gecode":

    cdef cppclass IntArgs_ "::Gecode::IntArgs":
        IntArgs_()
        IntArgs_(int)
        int& operator[](int)

    cdef cppclass IntSetArgs_ "::Gecode::IntSetArgs":
        IntSetArgs_()
        IntSetArgs_(int)
        IntSet_& operator[](int)

    cdef cppclass IntVarArgs_ "::Gecode::IntVarArgs":
        IntVarArgs_()
        IntVarArgs_(int)
        IntVar_& operator[](int)

    cdef cppclass BoolVarArgs_ "::Gecode::BoolVarArgs":
        BoolVarArgs_()
        BoolVarArgs_(int)
        BoolVar_& operator[](int)

    cdef cppclass SetVarArgs_ "::Gecode::SetVarArgs":
        SetVarArgs_()
        SetVarArgs_(int)
        SetVar_& operator[](int)

    cdef cppclass TaskTypeArgs_ "::Gecode::TaskTypeArgs":
        TaskTypeArgs_()
        TaskTypeArgs_(int)
        TaskType_& operator[](int)

include "gecode_python_pred.pxi"

cdef IntArgs_ intargs_from_list(l):
    cdef int n = len(l)
    cdef IntArgs_ a = IntArgs_(n)
    cdef int i = 0
    cdef int j
    for x in l:
        j = x
        a[i] = j
        i += 1
    return a

cdef IntSetArgs_ intsetargs_from_list(l):
    cdef int n = len(l)
    cdef IntSetArgs_ a = IntSetArgs_(n)
    cdef int i = 0
    cdef IntSet s
    for x in l:
        s = x
        a[i] = dereference(s._intset)
        i += 1
    return a

cdef TaskTypeArgs_ tasktypeargs_from_list(l):
    cdef int n = len(l)
    cdef TaskTypeArgs_ a = TaskTypeArgs_(n)
    cdef int i = 0
    cdef TaskType_ t
    for x in l:
        t = x
        a[i] = t
        i += 1
    return a

cdef IntVarArgs_ intvarargs_from_list(space,l):
    cdef ProtoSpace proto = space
    cdef int n = len(l)
    cdef IntVarArgs_ a = IntVarArgs_(n)
    cdef int i = 0
    cdef IntVar v
    for x in l:
        v = x
        a[i] = proto._get_ivar(v)
        i += 1
    return a

cdef BoolVarArgs_ boolvarargs_from_list(space,l):
    cdef ProtoSpace proto = space
    cdef int n = len(l)
    cdef BoolVarArgs_ a = BoolVarArgs_(n)
    cdef int i = 0
    cdef BoolVar v
    for x in l:
        v = x
        a[i] = proto._get_bvar(v)
        i += 1
    return a

cdef SetVarArgs_ setvarargs_from_list(space,l):
    cdef ProtoSpace proto = space
    cdef int n = len(l)
    cdef SetVarArgs_ a = SetVarArgs_(n)
    cdef int i = 0
    cdef SetVar v
    for x in l:
        v = x
        a[i] = proto._get_svar(v)
        i += 1
    return a

def is_list_or_tuple_of(l,t):
    if isinstance(l,(list,tuple)):
        for x in l:
            if not isinstance(x,t):
                return False
        return True
    return False

def is_IntVarArgs(l):
    return is_list_or_tuple_of(l, IntVar)
def is_BoolVarArgs(l):
    return is_list_or_tuple_of(l, BoolVar)
def is_SetVarArgs(l):
    return is_list_or_tuple_of(l, SetVar)

def is_IntArgs(l):
    return is_list_or_tuple_of(l, int)
def is_IntSetArgs(l):
    return is_list_or_tuple_of(l, IntSet)
def is_TaskTypeArgs(l):
    return is_list_or_tuple_of(l, TaskType)

include "gecode_python_api.pxi"

cdef extern from "gecode-common.icc" namespace "Gecode":

    cdef cppclass Disjunctor_ "::Gecode::Disjunctor":
        Disjunctor_(Space_&)

    cdef cppclass Clause_ "::Gecode::Clause":
        Clause_(Space_&, Disjunctor_)
        void forward(IntVar_, IntVar_)
        void forward(BoolVar_, BoolVar_)
        void forward(SetVar_, SetVar_)
        GenericSpace* generic_space()
        Space_* space()

cdef class Clause(ApiSpace)

cdef class Disjunctor:
    cdef ProtoSpace _proto
    cdef Disjunctor_* _disj
    def __cinit__(self, ProtoSpace s):
        cdef Space_* s_ = s._to_space_()
        self._proto = s
        self._disj = new Disjunctor_(dereference(s_))
    def __dealloc__(self):
        del self._disj
    cdef Disjunctor_* _to_disjunctor(self):
        return self._disj
    def clause(self):
        return Clause(self._proto, self)

cdef class Clause(ApiSpace):
    cdef ProtoSpace _proto
    cdef Clause_* _clause
    def __cinit__(self, ProtoSpace s, Disjunctor d):
        cdef Space_* s_ = s._to_space_()
        cdef Disjunctor_* d_ = d._to_disjunctor()
        self._proto = s
        self._clause = new Clause_(dereference(s_), dereference(d_))
    def __dealloc__(self):
        del self._clause
    cdef GenericSpace* _to_space(self):
        return self._clause.generic_space()
    cdef Space_* _to_space_(self):
        return self._clause.space()
    def forward(self, x ,y):
        cdef IntVar x_i
        cdef IntVar y_i
        cdef BoolVar x_b
        cdef BoolVar y_b
        cdef SetVar x_s
        cdef SetVar y_s
        if isinstance(x,IntVar):
            x_i = x
            y_i = y
            self._clause.forward(self._proto._get_ivar(x_i),
                                 self._get_ivar(y_i))
        elif isinstance(x,BoolVar):
            x_b = x
            y_b = y
            self._clause.forward(self._proto._get_bvar(x_b),
                                 self._get_bvar(y_b))
        elif isinstance(x,SetVar):
            x_s = x
            y_s = y
            self._clause.forward(self._proto._get_svar(x_s),
                                 self._get_svar(y_s))
        else:
            assert len(x)==len(y)
            for x_,y_ in zip(x,y):
                self.forward(x_,y_)

cdef class Space(ApiSpace):
    cdef GenericSpace* _space
    def __cinit__(self, alloc=True):
        if alloc:
            self._space = new GenericSpace()
    cdef _set_space(self, GenericSpace* s):
        self._space = s
    def __dealloc__(self):
        del self._space
    cdef GenericSpace* _to_space(self):
        return self._space
    cdef Space_* _to_space_(self):
        return self._space.space()

    def search(self):
        cdef GenericEngine* e_ = self._space.new_engine()
        cdef Engine e = Engine()
        e._set_engine(e_)
        return e

    def minimize(self, x, y=None):
        cdef IntVar x1 = x
        cdef IntVar y1
        if y is None:
            self._minimize1(x1)
        else:
            y1 = y
            self._minimize2(x1, y1)
        
    def maximize(self, x, y=None):
        cdef IntVar x1 = x
        cdef IntVar y1
        if y is None:
            self._maximize1(x1)
        else:
            y1 = y
            self._maximize2(x1, y1)

    def disjunctor(self):
        return Disjunctor(self)

    def assigned(self, x):
        cdef IntVar i
        cdef BoolVar b
        cdef SetVar s
        if isinstance(x,IntVar):
            i = x
            return self._get_ivar(i).assigned()
        if isinstance(x,BoolVar):
            b = x
            return self._get_bvar(b).assigned()
        if isinstance(x,SetVar):
            s = x
            return self._get_svar(s).assigned()
        l = []
        for y in x:
            l.append(self.assigned(y))
        return l

    def min(self, x, *rest):
        cdef IntVar i
        cdef BoolVar b
        if rest:
            return self._min(x, *rest)
        if isinstance(x,IntVar):
            i = x
            return self._get_ivar(i).min()
        if isinstance(x,BoolVar):
            b = x
            return self._get_bvar(b).min()
        l = []
        for y in x:
            l.append(self.min(y))
        return l

    def max(self, x, *rest):
        cdef IntVar i
        cdef BoolVar b
        if rest:
            return self._max(x, *rest)
        if isinstance(x,IntVar):
            i = x
            return self._get_ivar(i).max()
        if isinstance(x,BoolVar):
            b = x
            return self._get_bvar(b).max()
        l = []
        for y in x:
            l.append(self.max(y))
        return l

    def med(self, x):
        cdef IntVar i
        cdef BoolVar b
        if isinstance(x,IntVar):
            i = x
            return self._get_ivar(i).med()
        if isinstance(x,BoolVar):
            b = x
            return self._get_bvar(b).med()
        l = []
        for y in x:
            l.append(self.med(y))
        return l

    def val(self, x):
        cdef IntVar i
        cdef BoolVar b
        if isinstance(x,IntVar):
            i = x
            return self._get_ivar(i).val()
        if isinstance(x,BoolVar):
            b = x
            return self._get_bvar(b).val()
        l = []
        for y in x:
            l.append(self.val(y))
        return l

    def size(self, x):
        cdef IntVar i
        cdef BoolVar b
        if isinstance(x,IntVar):
            i = x
            return self._get_ivar(i).size()
        if isinstance(x,BoolVar):
            b = x
            return self._get_bvar(b).size()
        l = []
        for y in x:
            l.append(self.size(y))
        return l

    def width(self, x):
        cdef IntVar i
        cdef BoolVar b
        if isinstance(x,IntVar):
            i = x
            return self._get_ivar(i).width()
        if isinstance(x,BoolVar):
            b = x
            return self._get_bvar(b).width()
        l = []
        for y in x:
            l.append(self.width(y))
        return l

    def regret_min(self, x):
        cdef IntVar i
        cdef BoolVar b
        if isinstance(x,IntVar):
            i = x
            return self._get_ivar(i).regret_min()
        if isinstance(x,BoolVar):
            b = x
            return self._get_bvar(b).regret_min()
        l = []
        for y in x:
            l.append(self.regret_min(y))
        return l

    def regret_max(self, x):
        cdef IntVar i
        cdef BoolVar b
        if isinstance(x,IntVar):
            i = x
            return self._get_ivar(i).regret_max()
        if isinstance(x,BoolVar):
            b = x
            return self._get_bvar(b).regret_max()
        l = []
        for y in x:
            l.append(self.regret_max(y))
        return l

    cdef _get_intvar_ranges(self, IntVar v):
        cdef IntVar_ v_ = self._get_ivar(v)
        cdef IntVarRanges r = IntVarRanges(v_)
        cdef int i
        cdef int j
        l = []
        while dereference(&r)():
            i = r.min()
            j = r.max()
            l.append((i,j))
            preincrement(r)
        return l
    
    def ranges(self, x):
        if isinstance(x, IntVar):
            return self._get_intvar_ranges(x)
        l = []
        for y in x:
            l.append(self.ranges(y))
        return l

    def _get_intvar_values(self, IntVar v):
        cdef IntVar_ v_ = self._get_ivar(v)
        cdef IntVarValues* r = new IntVarValues(v_)
        cdef int i
        l = []
        try:
            while dereference(r)():
                i = r.val()
                l.append(i)
                preincrement(dereference(r))
        finally:
            del r
        return l

    def values(self, x):
        cdef IntVar i
        if isinstance(x,IntVar):
            i = x
            return self._get_intvar_values(i)
        l = []
        for y in x:
            l.append(self.values(y))
        return l

    def glbSize(self,x):
        cdef SetVar s
        if isinstance(x,SetVar):
            s = x
            return self._get_svar(s).glbSize()
        l = []
        for y in x:
            l.append(self.glbSize(y))
        return l

    def lubSize(self,x):
        cdef SetVar s
        if isinstance(x,SetVar):
            s = x
            return self._get_svar(s).lubSize()
        l = []
        for y in x:
            l.append(self.lubSize(y))
        return l

    def unknownSize(self,x):
        cdef SetVar s
        if isinstance(x,SetVar):
            s = x
            return self._get_svar(s).unknownSize()
        l = []
        for y in x:
            l.append(self.unknownSize(y))
        return l

    def cardMin(self,x):
        cdef SetVar s
        if isinstance(x,SetVar):
            s = x
            return self._get_svar(s).cardMin()
        l = []
        for y in x:
            l.append(self.cardMin(y))
        return l

    def cardMax(self,x):
        cdef SetVar s
        if isinstance(x,SetVar):
            s = x
            return self._get_svar(s).cardMax()
        l = []
        for y in x:
            l.append(self.cardMax(y))
        return l

    def lubMin(self,x):
        cdef SetVar s
        if isinstance(x,SetVar):
            s = x
            return self._get_svar(s).lubMin()
        l = []
        for y in x:
            l.append(self.lubMin(y))
        return l

    def lubMax(self,x):
        cdef SetVar s
        if isinstance(x,SetVar):
            s = x
            return self._get_svar(s).lubMax()
        l = []
        for y in x:
            l.append(self.lubMax(y))
        return l

    def glbMin(self,x):
        cdef SetVar s
        if isinstance(x,SetVar):
            s = x
            return self._get_svar(s).glbMin()
        l = []
        for y in x:
            l.append(self.glbMin(y))
        return l

    def glbMax(self,x):
        cdef SetVar s
        if isinstance(x,SetVar):
            s = x
            return self._get_svar(s).glbMax()
        l = []
        for y in x:
            l.append(self.glbMax(y))
        return l

    cdef _get_glb_ranges(self, SetVar s):
        cdef SetVar_ s_ = self._get_svar(s)
        cdef SetVarGlbRanges r = SetVarGlbRanges(s_)
        cdef int i
        cdef int j
        l = []
        while dereference(&r)():
            i = r.min()
            j = r.max()
            l.append((i,j))
            preincrement(r)
        return l

    def glb_ranges(self, x):
        if isinstance(x,SetVar):
            return self._get_glb_ranges(x)
        l = []
        for y in x:
            l.append(self.glb_ranges(y))
        return l

    glbRanges = glb_ranges

    cdef _get_lub_ranges(self, SetVar s):
        cdef SetVar_ s_ = self._get_svar(s)
        cdef SetVarLubRanges r = SetVarLubRanges(s_)
        cdef int i
        cdef int j
        l = []
        while dereference(&r)():
            i = r.min()
            j = r.max()
            l.append((i,j))
            preincrement(r)
        return l

    def lub_ranges(self, x):
        if isinstance(x,SetVar):
            return self._get_lub_ranges(x)
        l = []
        for y in x:
            l.append(self.lub_ranges(y))
        return l

    lubRanges = lub_ranges

    cdef _get_unknown_ranges(self, SetVar s):
        cdef SetVar_ s_ = self._get_svar(s)
        cdef SetVarUnknownRanges r = SetVarUnknownRanges(s_)
        cdef int i
        cdef int j
        l = []
        while dereference(&r)():
            i = r.min()
            j = r.max()
            l.append((i,j))
            preincrement(r)
        return l

    def unknown_ranges(self, x):
        if isinstance(x,SetVar):
            return self._get_unknown_ranges(x)
        l = []
        for y in x:
            l.append(self.unknown_ranges(y))
        return l

    unknownRanges = unknown_ranges

    cdef _get_glb_values(self, SetVar s):
        cdef SetVar_ s_ = self._get_svar(s)
        cdef SetVarGlbValues* r = new SetVarGlbValues(s_)
        cdef int i
        l = []
        try:
            while dereference(r)():
                i = r.val()
                l.append(i)
                preincrement(dereference(r))
        finally:
            del r
        return l

    def glb_values(self, x):
        if isinstance(x,SetVar):
            return self._get_glb_values(x)
        l = []
        for y in x:
            l.append(self.glb_values(y))
        return l

    glbValues = glb_values

    cdef _get_lub_values(self, SetVar s):
        cdef SetVar_ s_ = self._get_svar(s)
        cdef SetVarLubValues* r = new SetVarLubValues(s_)
        cdef int i
        l = []
        try:
            while dereference(r)():
                i = r.val()
                l.append(i)
                preincrement(dereference(r))
        finally:
            del r
        return l

    def lub_values(self, x):
        if isinstance(x,SetVar):
            return self._get_lub_values(x)
        l = []
        for y in x:
            l.append(self.lub_values(y))
        return l

    lubValues = lub_values

    cdef _get_unknown_values(self, SetVar s):
        cdef SetVar_ s_ = self._get_svar(s)
        cdef SetVarUnknownValues* r = new SetVarUnknownValues(s_)
        cdef int i
        l = []
        try:
            while dereference(r)():
                i = r.val()
                l.append(i)
                preincrement(dereference(r))
        finally:
            del r
        return l

    def unknown_values(self, x):
        if isinstance(x,SetVar):
            return self._get_unknown_values(x)
        l = []
        for y in x:
            l.append(self.unknown_values(y))
        return l

    unknownValues = unknown_values

def space():
    return Space()

cdef class Engine:
    cdef GenericEngine* _engine
    def __dealloc__(self):
        del self._engine
    def __iter__(self):
        return self
    def __next__(self):
        cdef GenericSpace* sol = self._engine.next()
        cdef Space s
        if sol is NULL:
            raise StopIteration
        s = Space(alloc=False)
        s._set_space(sol)
        return s
    cdef _set_engine(self, GenericEngine* e):
        self._engine = e
