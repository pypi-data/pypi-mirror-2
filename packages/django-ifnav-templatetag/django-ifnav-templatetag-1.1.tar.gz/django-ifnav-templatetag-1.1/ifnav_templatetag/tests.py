import unittest

from django.template import Template, Context


class TestRequest(object):
    def __init__(self, path):
        self.META = {'PATH_INFO': path}

class TestContext(Context):
    def __init__(self, path):
        super(TestContext, self).__init__({'request': TestRequest(path)})


class IfNavTestCase(unittest.TestCase):

    def assert_renders(self, template, context, value):
        template = Template(template)
        self.assertEqual(template.render(context), value)

    def assert_nav_true(self, regex, path):
        tpl = '{%% load ifnav %%}{%% ifnav "%s" %%}X{%% endifnav %%}' % regex
        self.assert_renders(tpl, TestContext(path), 'X')

    def assert_nav_false(self, regex, path):
        tpl = '{%% load ifnav %%}{%% ifnav "%s" %%}X{%% endifnav %%}' % regex
        self.assert_renders(tpl, TestContext(path), '')

    def test_true(self):
        # exact
        self.assert_nav_true('^/$', '/')
        self.assert_nav_true('^/foo/bar/$', '/foo/bar/')
        # startswith
        self.assert_nav_true('^/foo/', '/foo/bar/')
        # endswith
        self.assert_nav_true('/bar/$', '/foo/bar/')

    def test_false(self):
        self.assert_nav_false('^$', '/')
        self.assert_nav_false('^/foo/$', '/')
        self.assert_nav_false('^/bar/$', '/foo/')

    def test_else(self):
        tpl = '{% load ifnav %}{% ifnav "^/foo/$" %}1{% else %}0{% endifnav %}'
        self.assert_renders(tpl, TestContext('/foo/'), '1')
        self.assert_renders(tpl, TestContext('/bar/'), '0')

    def test_invalid_use(self):
        # no 'request' object in context should never match the regex
        tpl = '{% load ifnav %}{% ifnav "^$" %}X{% endifnav %}'
        self.assert_renders(tpl, Context(), '')
