"""
wordsmith.wordsmith
~~~~~~~~~~~~~~~~~~~

This module implements the Wordsmith object.
"""

import json
import requests

from .configuration import Configuration
from .project import Project
from .exceptions import ProjectSlugError

class Wordsmith(object):
  """
  Constructs a :class:`Wordsmith <Wordsmith>` object.

  :param api_key: API key from Wordsmith.
  :param base_url: (optional) String representing the base URL for the Wordsmith API per documentation at http://wordsmith.readme.io/v1/docs
  :param user_agent: (optional) String representing the user agent that should be sent with each API request
  """

  def __init__(self, api_key, **kwargs):
    self.projects = []
    self.config = Configuration(api_key)
    if 'base_url' in kwargs:
      self.config.base_url = kwargs['base_url']
    if 'user_agent' in kwargs:
      self.config.user_agent = kwargs['user_agent']
    response = requests.get(self.config.base_url + '/projects', headers=self.config.get_headers())
    if response.status_code == 200:
      for project_data in json.loads(response.text)['data']:
        self.projects.append(Project(project_data['name'], project_data['slug'], project_data['schema'], project_data['templates'], self.config))

  def project(self, slug):
    """
    Get a Wordsmith project by slug

    :param slug: String representing the slug of the Wordmsith project
    :return: :class:`Wordsmith <Project>`
    :rtype: wordsmith.Project
    """
    matches = [project for project in self.projects if project.slug == slug]
    if len(matches) == 1:
      return matches[0]
    else:
      raise ProjectSlugError('{} is not a valid project slug.'.format(slug))

  def find_project(self, name):
    """
    Find Wordsmith projects by project name

    :param name: String representing the name of the Wordsmith project
    :return: :class:`list`
    :rtype: list
    """
    return [project for project in self.projects if project.name == name]
