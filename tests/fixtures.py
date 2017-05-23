import pytest
from wordsmith import (Wordsmith,
                       ProjectSlugError,
                       TemplateSlugError,
                       NarrativeGenerateError)

API_KEY = '923b278a6088675262af64ceb437bab31d7ebc6b07aaf89f88b0b88dd4fe2a97'


class TestWordsmith(object):

    def initialize(self, **kwargs):
        return Wordsmith(API_KEY, user_agent='python sdk test suite', **kwargs)
