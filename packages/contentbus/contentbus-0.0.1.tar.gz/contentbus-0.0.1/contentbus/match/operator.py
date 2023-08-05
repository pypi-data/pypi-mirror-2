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

'''Match operators'''

BUILTIN_OPERATORS = {}

def register_operator(name):
    def reg(op):
        BUILTIN_OPERATORS[name] = op

    return reg

def register_builtin_operators(registry):
    '''Register operators to specified registry'''

    for name, op in BUILTIN_OPERATORS.iteritems():
        registry.register(op, name, overwrite=True)

@register_operator('eq')
def op_eq(val, attr_name=None, obj=None):
    return getattr(obj, attr_name) == val

@register_operator('is')
def op_is(val, attr_name=None, obj=None):
    return getattr(obj, attr_name) is val

@register_operator('exists')
def op_exists(val, attr_name=None, obj=None):
    return not(hasattr(obj, attr_name) ^ val)

@register_operator('in_range')
def op_in_range(start, end, attr_name=None, obj=None):
    return start <= getattr(obj, attr_name) <= end

@register_operator('len')
def op_len(length, attr_name=None, obj=None):
    return len(getattr(obj, attr_name)) == length
