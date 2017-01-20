"""
wordsmith.project
~~~~~~~~~~~~~~~~~~~

This module implements the Wordsmith project object.
"""
from .template import Template
from .exceptions import TemplateSlugError

class Project(object):

  def __init__(self, name, slug, schema, templates, config):
    self._config = config
    self.templates = []
    self.name = name
    self.slug = slug
    self.schema = schema
    for template_data in templates:
      self.templates.append(Template(self.slug, template_data['name'], template_data['slug'], self._config))

  def template(self, slug):
    """
    Get a Wordsmith template by slug

    :param slug: String representing the slug of the Wordmsith template
    :return: :class:`Wordsmith <Template>`
    :rtype: wordsmith.Template
    """
    matches = [template for template in self.templates if template.slug == slug]
    if len(matches) == 1:
      return matches[0]
    else:
      raise TemplateSlugError('{} is not a valid template slug.'.format(slug))

  def find_template(self, name):
    """
    Find Wordsmith templates by template name

    :param name: String representing the name of the Wordsmith template
    :return: :class:`list`
    :rtype: list
    """
    return [template for template in self.templates if template.name == name]
