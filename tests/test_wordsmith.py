import pytest
from wordsmith import (Wordsmith,
                       ProjectSlugError,
                       TemplateSlugError,
                       NarrativeGenerateError)
from tests.fixtures import TestWordsmith


class TestSomeStuff(TestWordsmith):

    def setup(self):
        self.ws = super().initialize()

    def test_config_specifying_base_url(self):
        ws = Wordsmith(self.ws.config.api_key,
                       user_agent='python sdk test suite',
                       base_url='https://api.automatedinsights.com/v1')

    def test_list_all_projects(self):
        projects = [project.name for project in self.ws.projects]
        assert projects == ['Test']

    def test_list_all_projects_with_custom_base_url(self):
        ws = Wordsmith(self.ws.config.api_key,
                       user_agent='python sdk test suite',
                       base_url='https://api.automatedinsights.com/v1')
        projects = [project.name for project in ws.projects]
        assert projects == ['Test']

    def test_find_project_by_slug(self):
        project = self.ws.project('test')
        assert project.name == 'Test'

    def test_bad_project_raises_error(self):
        with pytest.raises(ProjectSlugError):
            project = self.ws.project('fake project')

    def test_bad_template_raises_error(self):
        with pytest.raises(TemplateSlugError):
            template = self.ws.project('test').template('fake template')

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

    def test_batch_generate_narrative(self):
        data = [{'a': i, 'b': i, 'c': i} for i in range(10)]
        expected_outputs = ['The value of A is {}.'.format(i)
                            for i in range(10)]
        narrs = self.ws.project('test').template('test').batch_narrative(data)
        narrs.generate()
        for expected, actual in zip(expected_outputs, narrs.narratives):
            assert expected == actual.text

    def test_bad_batch_generate_no_break(self):
        data = [
            {'a': 1, 'b': 1, 'c': 1},
            {'d': 1, 'e': 1},
            {'a': 1, 'b': 1, 'c': 1}
        ]
        narrs = self.ws.project('test').template('test').batch_narrative(data)
        narrs.break_on_error = False
        narrs.generate()
        expected_narratives = ['The value of A is 1.',
                               None,
                               'The value of A is 1.']
        actual_narratives = []
        for n in narrs.narratives:
            actual_narratives.append(n.text if n is not None else None)
        assert (expected_narratives == actual_narratives)\
            and (len(narrs.errors) == 1)

    def test_bad_batch_generate_break(self):
        with pytest.raises(NarrativeGenerateError):
            data = [
                {'a': 1, 'b': 1, 'c': 1},
                {'d': 1, 'e': 1},
                {'a': 1, 'b': 1, 'c': 1}
            ]
            narrs = self.ws.project('test')\
                .template('test').batch_narrative(data)
            narrs.break_on_error = True
            narrs.generate()

    def test_wordsmith_400_error(self):
        with pytest.raises(NarrativeGenerateError):
            data = {'not_a_valid_column': 0}
            narr = self.ws.project('test')\
                .template('test').generate_narrative(data)
