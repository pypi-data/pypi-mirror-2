from django.test import TestCase
from django import template
from representations.templatetags import represent
from django.utils.safestring import SafeString
from representations import settings
import mock


class TestReTag(TestCase):
    """Test my re_tag decorator"""
    def test_noargs(self):
        """Tests the requirement that a re tag have arguments"""

        # Create the requirements for a call to a compilation function
        parser = template.Parser("")
        token = template.Token(template.TOKEN_BLOCK,"fake")

        # Define a sample regexp, this isn't really important to test the
        # requirement that re_tag's have arguments
        re = r"as (.+)"

        # Create a mock function so that we can see what the re_tag decorator
        # passes to the compilation function
        Mock = mock.Mock()

        # Decorate our mock compilation function
        do_func = represent.re_tag(re)(Mock)

        # Assert that a call to the decorated compilation function when
        # that tag token has no arguments raises a TemplateSyntaxError
        self.assertRaises(template.TemplateSyntaxError, do_func, parser, token)

    def test_badargs(self):
        """Tests that a TemplateSyntaxError is raised when the re pattern
doesn't match"""
        # Create the requirements for a call to a compilation function
        parser = template.Parser("")
        # This token will not match the pattern below
        token = template.Token(template.TOKEN_BLOCK,"fake limit fart")

        # Create a pattern that will not match our token
        re = r"limit (\d+)"

        # Create a mock compilation function
        Mock = mock.Mock()

        # Decorate our mock compilation function
        do_func = represent.re_tag(re)(Mock)

        # Assert that if the pattern isn't matched, it raises a
        # TemplateSyntaxError
        self.assertRaises(template.TemplateSyntaxError, do_func, parser, token)

    def test_kwargs(self):
        """Tests a pattern with kwargs"""

        # Create the requirements for a call to a compilation function
        parser = template.Parser("")
        token = template.Token(template.TOKEN_BLOCK,"fake limit=10 offset=5")

        # Define a regular function with kwargs
        re = r"limit=(?P<limit>\d+)( offset=(?P<offset>\d+))?"

        # Create a mock compilation function so we can extract the kwargs
        # for testing
        Mock = mock.Mock()

        # Decorate our mock compilation function
        do_func = represent.re_tag(re)(Mock)

        # Call our decorated compilation function
        do_func(parser, token)

        # Extract the args and kwargs used in our compilation function
        args, kwargs = Mock.call_args

        # Assert that the args and kwargs were passed correctly
        self.assertEqual(args, (parser, token, ))
        self.assertEqual(kwargs, {'limit': '10', 'offset': '5'})

    def test_args(self):
        # Create the requirements for a call to a compilation function
        parser = template.Parser("")
        token = template.Token(template.TOKEN_BLOCK,'fake limit=10')

        # Define a regular expession that has args
        re = r"limit=(\d+)"

        # Create a mock compilation function
        Mock = mock.Mock()

        # Decorate our mock compilation function
        do_func = represent.re_tag(re)(Mock)

        # Call our decorated mock compilation function
        do_func(parser, token)

        # Extract the args and kwargs from the mock compilation function
        args, kwargs = Mock.call_args

        self.assertEqual(args, (parser, token, "10"))


class TestDoRepresent(TestCase):

    @mock.patch("representations.templatetags.represent.RepresentNode"
                ".__init__")
    def test_stringtemplate(self, Mock):
        """This asserts that a string works as the representation argument
for the template tag"""
        Mock.return_value = None

        tsrc = """{% load represent %}
{% represent model as "headline.html" %}"""

        t = template.Template(tsrc)

        model_exp, template_exp = Mock.call_args[0]

        self.assertEqual(model_exp.token, "model")
        self.assertEqual(template_exp.token, '"headline.html"')

    @mock.patch("representations.templatetags.represent.RepresentNode"
                ".__init__")
    def test_varkwargs(self, mock):
        """This asserts that a variable name with filters will work as the
the two arguments of the represent tag"""
        mock.return_value = None

        tsrc = """{% load represent %}
{% represent model.section_set.1|safe as bucket.represent_template|safe %}"""

        t = template.Template(tsrc)

        model_exp, template_exp = mock.call_args[0]

        self.assertEqual(model_exp.token,
                         "model.section_set.1|safe")
        self.assertEqual(template_exp.token,
                         'bucket.represent_template|safe')


class TestRepresentNodeRender(TestCase):

    def test_not_a_model(self):
        """Tests that if an object is passed to the template tag as a model
when it's not a model that an TemplateSyntaxError is raised"""
        model = object()

        representation = '"test.html"'
        parser = template.Parser('')

        model_exp = template.FilterExpression("model", parser)
        representation_exp = template.FilterExpression(representation,
                                              parser)


        context = template.Context({'model': model })

        node = represent.RepresentNode(model_exp,
                                       representation_exp)

        result = self.assertRaises(template.TemplateSyntaxError,
                                   node.render, context)


    @mock.patch("representations.templatetags.represent"
                ".get_representation_content")

    def test_allgood(self, Mock):
        """Tests that the expected behaviour happens when all the parameters
are valid"""
        Mock.return_value = "This is a test."

        model = mock.Mock()
        model._meta = True

        representation = '"test.html"'
        parser = template.Parser('')

        model_exp = template.FilterExpression("model", parser)
        representation_exp = template.FilterExpression(representation,
                                              parser)


        context = template.Context({'model': model })

        node = represent.RepresentNode(model_exp,
                                        representation_exp)

        result = node.render(context)

        self.assertEqual(Mock.call_args[0][0], model)
        self.assertEqual(Mock.call_args[0][1], u"test.html")
        self.assertTrue(isinstance(result, SafeString))
        self.assertEqual(unicode(result), u"This is a test.")


class TestDoDefineObject(TestCase):
    @mock.patch("representations.templatetags.represent"
                ".DefineObjectNode.__init__")
    def test_allgood(self, Mock):
        Mock.return_value = None

        tsrc = u"""{% load represent %}
{% define_object as "obj" %}"""

        t = template.Template(tsrc)

        (varname_exp, ) = Mock.call_args[0]

        self.assertEqual(varname_exp.token, u'"obj"')


class TestDefineObjectNode(TestCase):
    def test_render(self):
        parser = template.Parser(u"")
        object_name_exp = template.FilterExpression(u'"obj"', parser)

        context = template.Context({
                represent.OBJECT_VAR_NAME: u"Testing"
                })

        node = represent.DefineObjectNode(object_name_exp)

        node.render(context)

        self.assertEqual(context['obj'], u"Testing")


class TestGetRepresentationContent(TestCase):

    @mock.patch("django.template.loader.select_template")
    def test_generic_representation(self, Mock):
        Mock.retern_value = template.Template("Hello, World")

        model = mock.Mock()
        model._meta = mock.Mock()
        model._meta.app_label = "app_label"
        model._meta.object_name = "object_name"

        representation = "dummy.html"
        settings.REPRESENTATIONS_GENERIC_REPRESENTATION =\
            "representations/default.html"
        represent.get_representation_content(model, representation)

        template_list = Mock.call_args[0][0]
        expect = ["representations/app_label.object_name/dummy.html",
                  settings.REPRESENTATIONS_GENERIC_REPRESENTATION]

        self.assertEqual(expect, template_list)

    @mock.patch("django.template.loader.select_template")
    def test_context(self, Mock):
        t = template.Template("Hello, World")
        Mock.return_value = t

        RenderMock = mock.Mock()
        RenderMock.return_value = "Hello, World"
        t.render = RenderMock

        model = mock.Mock()
        model._meta = mock.Mock()
        model._meta.app_label = "app_label"
        model._meta.object_name = "object_name"

        representation = "dummy.html"
        context = template.Context({})
        represent.get_representation_content(model, representation,
                                             context=context)
        result = RenderMock.call_args[0][0]
        expect = context

        self.assertEqual(expect, result)

    @mock.patch("django.template.loader.select_template")
    def test_context_sideeffect_free(self, Mock):
        """This tests to make sure that if something in the represent
template overwrites a variable in the context that after the render, the
old value is preserved"""
        t = template.Template("{% regroup people by name as somevar %}")
        Mock.return_value = t

        RenderMock = mock.Mock()
        RenderMock.return_value = "Hello, World"
        t.render = RenderMock

        model = mock.Mock()
        model._meta = mock.Mock()
        model._meta.app_label = "app_label"
        model._meta.object_name = "object_name"

        representation = "dummy.html"
        data = [{'name': 'Aiden', 'age': 4}, {'name': 'Ethan', 'age': 1}]

        context = template.Context({
                'people': data,
                'somevar': 'Hello'
                })

        represent.get_representation_content(model, representation,
                                             context=context)

        # Let's make sure the value is preserved
        result = context['somevar']
        expect = "Hello"

        self.assertEqual(expect, result)
