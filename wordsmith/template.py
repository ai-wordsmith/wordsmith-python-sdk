"""
wordsmith.template
~~~~~~~~~~~~~~~~~~~

This module implements the Wordsmith template object.
"""

import requests
import json
from multiprocessing.dummy import Pool

from .narrative import Narrative, Batch

class Template(object):
  """
  Constructs a :class:`Wordsmith <Template>` object.

  :param project_slug: String representing the slug of the parent project of this template
  :param template_data: Dictionary representation of the template data for a single project in the project list JSON response from Wordsmith.
  :param config: wordsmith.Configuration object containing configuration details
  """

  def __init__(self, project_slug, name, slug, config):
    self.project_slug = project_slug
    self.name = name
    self.slug = slug
    self._config = config

  def generate_narrative(self, data):
    """
    Generate a single narrative from this template

    :param data: Dictionary of key, value pairs where the value represents the Wordsmith column name and the value represents the value of that column
    :rtype: wordsmith.narrative.Narrative
    """
    return Narrative(self.project_slug, self.slug, data, self._config)

  def batch_narrative(self, data_list):
    """
    Bulk generate multiple rows of data using multithreaded processing

    :param data_list: List of dictionaries where key, value pairs represent the Wordsmith column name and column value respectively
    :param pool_size: (optional) Int representing the number of workers to allocate to this job
    :return: :class:`list`
    :rtype: wordsmith.narrative.NarrativeBatch
    """
    return Batch(self.project_slug, self.slug, data_list, self._config)
