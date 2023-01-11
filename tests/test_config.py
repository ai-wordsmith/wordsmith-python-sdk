from wordsmith import Wordsmith
from tests.fixtures import TestWordsmith


class TestConfig(TestWordsmith):

    def setup(self):
        self.ws = super().initialize()

    def test_set_token_value(self):
        token = 'my_token'
        ws = Wordsmith(token)
        assert ws.config.api_key == token

    def test_default_url(self):
        assert self.ws.config.base_url \
            == 'https://api.automatedinsights.com/v1'

    def test_set_new_version(self):
        new_version = 'a_new_version'
        ws = Wordsmith('my_token', version=new_version)
        assert ws.config.version == new_version
