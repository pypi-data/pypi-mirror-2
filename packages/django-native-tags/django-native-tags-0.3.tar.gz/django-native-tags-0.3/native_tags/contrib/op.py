import operator
from native_tags.decorators import comparison, function

# Comparison operators

def lt(a, b):
    return operator.lt(a, b)
lt = comparison(lt)
lt.__doc__ = operator.lt.__doc__
    
def le(a, b):
    return operator.le(a, b)
le = comparison(le)
    
def eq(a, b):
    return operator.eq(a, b)
eq = comparison(eq)
    
def ne(a, b):
    return operator.ne(a, b)
ne = comparison(ne)
    
def ge(a, b):
    return operator.ge(a, b)
ge = comparison(ge)
    
def gt(a, b):
    return operator.gt(a, b)
gt = comparison(gt)

def not_(a):
    return operator.not_(a)
not_ = comparison(not_, name='not')

def is_(a):
    return operator.is_(a)
is_ = comparison(is_, name='is')

def is_not(a):
    return operator.is_not(a)
is_not = comparison(is_not)

# Mathematical and bitwise operators

def abs(a):
    return operator.abs(a)
abs = function(comparison(abs))

def add(a, b):
    return operator.add(a, b)
add = function(comparison(add))
    
def and_(a, b):
    return operator.and_(a, b)
and_ = function(comparison(and_, name='and'))

def div(a, b):
    return operator.div(a, b)
div = function(comparison(div))
    
def floordiv(a, b):
    return operator.floordiv(a, b)
floordiv = function(comparison(floordiv))

def index(a):
    return operator.index(a)
index = function(comparison(index))

def inv(a):
    return operator.inv(a)
    
def lshift(a, b):
    return operator.lshift(a, b)
    
def mod(a, b):
    return operator.mod(a, b)
    
def mul(a, b):
    return operator.mul(a, b)
    
def neg(a):
    return operator.neg(a)
    
def or_(a, b):
    return operator.or_(a, b)
    
def pos(a):
    return operator.pos(a)
    
def pow(a, b):
    return operator.pow(a, b)
    
def rshift(a, b):
    return operator.rshift(a, b)
    
def sub(a, b):
    return operator.sub(a, b)
    
def truediv(a, b):
    return operator.truediv(a, b)
    
def xor(a, b):
    return operator.xor(a, b)
    
# Sequence operators
    
def concat(a, b):
    return operator.concat(a, b)

def contains(a, b):
    return operator.contains(a, b)
    
def countOf(a, b):
    return operator.countOf(a, b)
    
def delitem(a, b):
    return operator.delitem(a, b)
    
def delslice(a, b, c):
    return operator.delslice(a, b, c)
    
def getitem(a, b):
    return operator.getitem(a, b)
    
def getslice(a, b, c):
    return operator.getslice(a, b, c)
    
def indexOf(a, b):
    return operator.indexOf(a, b)
    
def repeat(a, b):
    return operator.repeat(a, b)
    
def setitem(a, b, c):
    return operator.setitem(a, b, c)
    
def setslice(a, b, c, v):
    return operator.setslice(a, b, c, v)