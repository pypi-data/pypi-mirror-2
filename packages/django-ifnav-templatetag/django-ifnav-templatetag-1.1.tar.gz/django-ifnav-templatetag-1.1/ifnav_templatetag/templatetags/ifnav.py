# -*- coding: utf-8 -*-

import re

from django.conf import settings
from django.template import Library, TemplateSyntaxError
from django.template import Node, NodeList, Variable, VariableDoesNotExist

register = Library()


class IfNavNode(Node):

    def __init__(self, regex, nodelist_true, nodelist_false):
        self.regex_var = Variable(regex)
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false

    def __repr__(self):
        return '<IfNav node>'

    def __iter__(self):
        for node in nodelist_true:
            yield node
        for node in nodelist_false:
            yield node

    def render(self, context):
        if 'request' in context:
            regex = self.regex_var.resolve(context)
            path_info = context['request'].META['PATH_INFO']
            pattern = re.compile(regex)
            selected = pattern.search(path_info) is not None
        else:
            selected = False

        if selected:
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)


@register.tag
def ifnav(parser, token):
    args = token.split_contents()
    if len(args) != 2:
        raise TemplateSyntaxError(u"%r tag requires exactly one argument" % args[0])
    path = args[1]
    nodelist_true = parser.parse(('else', 'endifnav'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endifnav',))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    return IfNavNode(path, nodelist_true, nodelist_false)
