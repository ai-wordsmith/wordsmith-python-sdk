import pytest
from wordsmith import TemplateSlugError
from tests.fixtures import TestWordsmith


class TestProject(TestWordsmith):

    def setup(self):
        self.ws = super().initialize()

    def test_bad_template_raises_error(self):
        with pytest.raises(TemplateSlugError):
            self.ws.project('test').template('fake template')

    def test_find_project_by_name(self):
        matches = self.ws.find_project('Test')
        assert matches[0].name == 'Test'

    def test_find_template_that_exists(self):
        matches = self.ws.project('test').find_template('Test')
        assert len(matches) > 0

    def test_find_template_that_doesnt_exist(self):
        matches = self.ws.project('test').find_template('Fake Template')
        assert len(matches) == 0

    def test_generate_narrative(self):
        data = {'a': 1, 'b': 1, 'c': 1}
        narr = self.ws.project('test')\
            .template('test').generate_narrative(data).text
        assert narr == 'The value of A is 1.'
