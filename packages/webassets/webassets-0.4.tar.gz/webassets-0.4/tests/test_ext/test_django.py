from django.conf import settings
from django.template import Template, Context
from django_assets import Bundle, register as django_env_register
from django_assets.env import get_env, reset as django_env_reset
from webassets.bundle import BuildError


AssetsNode = None

def setup_module():
    from django.conf import settings
    settings.configure(INSTALLED_APPS=['django_assets'])
    settings.INSTALLED_APPS += ('django_assets',)

    # After setting up Django properly, try to import the correct node
    # class, and make it globally available.
    try:
        from django.templatetags.assets import AssetsNode as Node
    except ImportError:
        # Since #12295, Django no longer maps the tags.
        from django_assets.templatetags.assets import AssetsNode as Node
    global AssetsNode
    AssetsNode = Node


class TestConfig(object):
    """The environment configuration is backed by the Django settings
    object.
    """

    def test_default_options(self):
        """The builtin options have different names within the Django
        settings, to make it obvious they belong to django-assets.
        """
        settings.ASSETS_EXPIRE = 'timestamp'
        assert get_env().config['expire'] == settings.ASSETS_EXPIRE

        settings.MEDIA_ROOT = 'FOO'
        assert get_env().directory == 'FOO'

        get_env().directory = 'BAR'
        assert settings.MEDIA_ROOT == 'BAR'

    def test_custom_options(self):
        settings.FOO = 42
        get_env().config['foo'] == 42
        # Also, we are caseless.
        get_env().config['foO'] == 42


class TestTemplateTag():

    def setup(self):
        test_instance = self
        class MockBundle(Bundle):
            urls_to_fake = ['foo']
            def __init__(self, *a, **kw):
                Bundle.__init__(self, *a, **kw)
                self.env = get_env()
                # Kind of hacky, but gives us access to the last Bundle
                # instance used by our Django template tag.
                test_instance.the_bundle = self
            def urls(self, *a, **kw):
                return self.urls_to_fake
        # Inject our mock bundle class
        self._old_bundle_class = AssetsNode.BundleClass
        AssetsNode.BundleClass = self.BundleClass = MockBundle

        # Reset the Django asset environment, init it with some
        # dummy bundles.
        django_env_reset()
        self.foo_bundle = Bundle()
        self.bar_bundle = Bundle()
        django_env_register('foo_bundle', self.foo_bundle)
        django_env_register('bar_bundle', self.bar_bundle)

    def teardown(self):
        AssetsNode.BundleClass = self._old_bundle_class
        del self._old_bundle_class

    def render_template(self, args, ctx={}):
        return Template('{% load assets %}{% assets '+args+' %}{{ ASSET_URL }};{% endassets %}').render(Context(ctx))

    def test_reference_bundles(self):
        self.render_template('"foo_bundle", "bar_bundle"')
        assert self.the_bundle.contents == (self.foo_bundle, self.bar_bundle)

    def test_reference_files(self):
        self.render_template('"file1", "file2", "file3"')
        assert self.the_bundle.contents == ('file1', 'file2', 'file3',)

    def test_reference_mixed(self):
        self.render_template('"foo_bundle", "file2", "file3"')
        assert self.the_bundle.contents == (self.foo_bundle, 'file2', 'file3',)

    def test_with_vars(self):
        self.render_template('var1 var2', {'var1': self.foo_bundle, 'var2': 'a_file'})
        assert self.the_bundle.contents == (self.foo_bundle, 'a_file',)

    def test_with_no_commas(self):
        """Using commas is optional.
        """
        self.render_template('"file1" "file2" "file3"')

    def test_output_urls(self):
        """Ensure the tag correcly spits out the urls the bundle returns.
        """
        self.BundleClass.urls_to_fake = ['foo', 'bar']
        assert self.render_template('"file1" "file2" "file3"') == 'foo;bar;'
