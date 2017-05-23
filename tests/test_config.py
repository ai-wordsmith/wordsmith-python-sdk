import pytest
from wordsmith import (Wordsmith,
                       ProjectSlugError,
                       TemplateSlugError,
                       NarrativeGenerateError)
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
