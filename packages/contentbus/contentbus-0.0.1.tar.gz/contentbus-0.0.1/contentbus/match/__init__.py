#
# This file is part Contentbus

# Contentbus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Contentbus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Contentbus.  If not, see <http://www.gnu.org/licenses/>.

'''Object matching related classes'''

from functools import partial
from inspect import getargspec

from .operator import register_builtin_operators

class UnknownOperator(Exception):
    pass

def negate(func):
    def f(*args, **kwargs):
        return not func(*args, **kwargs)

    f.func_name = func.func_name
    f.func_doc = func.func_doc

    return f

class MatchOperator(object):
    '''Match operator for on objects attributes'''

    NAME_TOKEN = '__'

    OPERATORS = {}

    def __init__(self, func):
        '''Create a MatchOperator from a function.

        Function signature must be as: foo(attr_name=None, obj=None, *args) -> bool
        '''

        # check function signature
        spec = getargspec(func)
        if not frozenset(('attr_name', 'obj')).issubset(spec.args) and spec.defaults != (None, None):
            raise ValueError("Function signature is not correct")

        self.func = func

    @staticmethod
    def register(op, name, overwrite=False):
        '''Register a match operator

        name must not contain '__'.

        If owerwrite is True, the operator will owerwrite a
        previously defined one.
        '''

        if not isinstance(op, MatchOperator):
            # we assume it's a callable, wrap it with a MatchOperator
            op = MatchOperator(op)

        if not name:
            raise ValueError("Can't register with empty name")

        if MatchOperator.NAME_TOKEN in name:
            raise ValueError("MatchOperator name can't contain '%s'", MatchOperator.NAME_TOKEN)

        if name in MatchOperator.OPERATORS and not owerwrite:
            raise AlreadyRegistered("MatchOperator already registered")

        MatchOperator.OPERATORS[name] = op

    @staticmethod
    def unregister(name):
        '''Unregister a match operator'''

        if name in MatchOperator.OPERATORS:
            del MatchOperator.OPERATORS[name]

    @staticmethod
    def get_operator(name):
        '''Return the named operator'''

        try:
            return MatchOperator.OPERATORS[name]
        except AttributeError:
            raise UnknownOperator("MatchOperator not registered: '%s'" % name)

    @staticmethod
    def operator(name):
        '''Decorator to register a function as operator with specified name.

        Operators registered via decorator overwrite any operator with same name.
        '''

        def operatorizer(func):
            MatchOperator.register(func, name, overwrite=True)
            return func

        return operatorizer

    def __call__(self, attr_name, params, negated=False):
        '''This returns a partial function, with attribute and
        parameters set.

        The resulting function will only take a keywork arg "obj"
        which is the object whose attribute must be match againts
        parameters.

        If negated is True, the boolean result will be negated
        '''

        return partial(self.func if not negated else negate(self.func),
                       *params, attr_name=attr_name)

class ObjectMatcher(object):
    '''A matcher for an object type'''

    def __init__(self, object_type, match_func=None, **match_params):
        self.object_type = object_type
        self.match_func = match_func
        self.match_conds = []
        negated = False

        for param, value in match_params.iteritems():
            if MatchOperator.NAME_TOKEN not in param:
                attr_name = param
                match_op_name = ""
            else:
                attr_name, match_op_name = param.rsplit(MatchOperator.NAME_TOKEN, 1)
                # handle inverse logic
                if match_op_name == 'not' or match_op_name.startswith('not_'):
                    match_op_name = match_op_name[4:]
                    negated = True

            if not match_op_name:
                match_op_name = 'eq'

            params = value if type(value) in (tuple, list) else (value, )

            self.match_conds.append(MatchOperator.get_operator(match_op_name)(attr_name, params, negated))

    def matches(self, obj):
        '''Match against an object'''

        assert isinstance(obj, self.object_type), "object is not instance of %s" % self.object_type

        # if no condition is provided, always match for the object type
        if not self.match_func and not self.match_conds:
            return True

        if self.match_func:
            return self.match_func(obj)

        # run all condition matchers
        try:
            return all(m(obj=obj) for m in self.match_conds)
        except Exception, e:
            return False # if any match raises an error, match is failed


# make builtin operators available globally
register_builtin_operators(MatchOperator)
