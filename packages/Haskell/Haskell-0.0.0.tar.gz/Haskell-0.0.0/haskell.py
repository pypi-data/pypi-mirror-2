# Copyright (c) 2010, Rev Johnny Healey <rev.null@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright notice, 
#      this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright 
#      notice, this list of conditions and the following disclaimer in the 
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the Reverend nor the names of its contributors
#      may be used to endorse or promote products derived from this software 
#      without specific prior written permission.
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
"""This module implements Haskell-style currying in python.  It is borderline
useless and probably unsafe for production and/or hobby systems.

Enjoy!"""

import opcode

__all__ = ['curry','curry_apply']

def curry_apply(fn,*args):
    "A function to apply multiple arguments to a curried function"
    return reduce(lambda f,x: f(x), args, fn)

FC_ARGS = ['argcount', 'nlocals', 'stacksize', 'flags', 'codestring', 
    'constants', 'names', 'varnames', 'filename', 'name', 'firstlineno', 
    'lnotab','freevars', 'cellvars']

def _modify_func_code(old_fc, **newvals):
    fc_dict = {
        'argcount': old_fc.co_argcount,
        'nlocals': old_fc.co_nlocals,
        'stacksize': old_fc.co_stacksize,
        'flags': old_fc.co_flags, 
        'codestring': old_fc.co_code,
        'constants': old_fc.co_consts,
        'names': old_fc.co_names,
        'varnames': old_fc.co_varnames,
        'filename': old_fc.co_filename,
        'name': old_fc.co_name,
        'firstlineno': old_fc.co_firstlineno,
        'lnotab': old_fc.co_lnotab,
        'freevars': old_fc.co_freevars,
        'cellvars': old_fc.co_cellvars
    }
    fc_dict.update(newvals)
    args = tuple(fc_dict[k] for k in FC_ARGS)
    return type(old_fc)(*args)

def _modify_base_co_code(fc):
    i = 0

    old_code = fc.co_code
    new_code = ""
    max_arg = fc.co_argcount - 1

    while i < len(old_code):
        op = ord(old_code[i])
        
        i += 1
        extended_arg = 0
        if op >= opcode.HAVE_ARGUMENT:
            oparg = ord(old_code[i]) + ord(old_code[i+1])*256

            if op == opcode.opmap['LOAD_FAST']:
                if oparg == max_arg:
                    new_code += chr(opcode.opmap['LOAD_FAST'])+chr(0)+chr(0)
                else:
                    new_code += chr(opcode.opmap['LOAD_DEREF'])+chr(oparg%256)+chr(oparg/256)
            else:
                new_code += old_code[i-1:i+2]

            i = i+2
        else:
            new_code += old_code[i-1]
    
    return _modify_func_code(fc, argcount=1, codestring=new_code, 
        nlocals = fc.co_nlocals - max_arg, flags = 19,
        freevars=fc.co_varnames[:-1], varnames=fc.co_varnames[-1:])

def _curry_wrap(base, depth=0):
    if depth == len(base.co_freevars):
        return base

    child_fn = _curry_wrap(base, depth+1)

    code = ""
    for i in range(depth+1):
        code += chr(opcode.opmap['LOAD_CLOSURE'])+chr(i)+chr(0)
    code += chr(opcode.opmap['BUILD_TUPLE']) + chr(depth+1) + chr(0)
    code += chr(opcode.opmap['LOAD_CONST']) + chr(0) + chr(0)
    code += chr(opcode.opmap['MAKE_CLOSURE']) + chr(0) + chr(0)
    code += chr(opcode.opmap['RETURN_VALUE'])

    return type(base)(
        1,
        1,
        2,
        19,
        code,
        (child_fn,),
        (),
        (base.co_freevars[depth],),
        base.co_filename,
        base.co_name,
        base.co_firstlineno,
        base.co_lnotab,
        base.co_freevars[:depth],
        (base.co_freevars[depth],)
    )

def curry(fn):
    """This decorator takes a function and rewrites it as a haskell-style 
    curried function.  It will fail in unexpected ways where args and kwargs
    are used."""
    base = _modify_base_co_code(fn.func_code)
    new_fc = _curry_wrap(base)

    return type(fn)(new_fc, fn.func_globals)

# an example on how to use this module
#@curry
#def add(x,y):
#    return x+y
#
#print add
#print add(1)
#print add(1)(2)

