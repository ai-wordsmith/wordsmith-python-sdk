import pytest
from wordsmith import Wordsmith, ProjectSlugError
from tests.fixtures import TestWordsmith


class TestProject(TestWordsmith):

    def setup(self):
        self.ws = super().initialize()

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
            self.ws.project('fake project')

    '''
    TODO
    def test_schema
        project = Wordsmith::Project.find 'test'
        expected = {a: 'Number', b: 'Number', c: 'Number'}
        assert_equal expected, project.schema
      end

      def test_template_collection_exists
        project = Wordsmith::Project.find('test')
        assert_instance_of Wordsmith::TemplateCollection, project.templates
      end
    end
    '''
