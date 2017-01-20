"""
wordsmith.narrative
~~~~~~~~~~~~~~~~~~~

This module implements the Wordsmith template object.
"""

import requests
import json
import six
from multiprocessing.dummy import Pool
from .exceptions import NarrativeGenerateError

class Narrative(object):
  """
  Constructs a :class:`Wordsmith <Narrative>` object.

  :param project_slug: String representing the slug of the parent project of this narrative
  :param template_slug: String representing the slug of the parent template of this narrative
  :param data: Dictionary representation of the row data to be passed to the Wordsmith platform
  :param config: wordsmith.Configuration object containing configuration details
  """

  def __init__(self, project_slug, template_slug, data, config):
    self.project_slug = project_slug
    self.template_slug = template_slug
    self.data = data
    self._config = config
    self.post_url = '{}/projects/{}/templates/{}/outputs'.format(self._config.base_url, self.project_slug, self.template_slug)
    headers = self._config.get_headers()
    headers['Content-Type'] = 'application/json'
    for header, value in six.iteritems(data):
      if value is None:
        data[header] = ''
    ws_data = {
      'data' : data
    }
    response = requests.post(self.post_url, data=json.dumps(ws_data), headers=headers)
    if response.status_code == 200:
      self.text = json.loads(response.text)['data']['content']
    else:
      self.text = None
      raise NarrativeGenerateError(response, data)

    def __str__(self):
      return self.text

class Batch(object):
  """
  Constructs a :class:`Wordsmith <NarrativeBatch>` object.

  :param project_slug: String representing the slug of the parent project of this narrative
  :param template_slug: String representing the slug of the parent template of this narrative
  :param data_list: List of dictionary representations of the row data to be passed to the Wordsmith platform
  :param config: wordsmith.Configuration object containing configuration details
  """

  def __init__(self, project_slug, template_slug, data_list, config):
    self.project_slug = project_slug
    self.template_slug = template_slug
    self.data_list = data_list
    self._config = config
    self.break_on_error = False
    self.pool_size = 8
    self.narratives = []
    self.errors = []

  def _generate_narrative(self, data):
    narrative = None
    try:
      narrative = Narrative(self.project_slug, self.template_slug, data, self._config)
    except NarrativeGenerateError as e:
      if self.break_on_error:
        raise e
      else:
        self.errors.append(e)
    return narrative

  def generate(self):
    self._index = 0
    thread_pool = Pool(self.pool_size)
    self.narratives = thread_pool.map(self._generate_narrative, self.data_list)
    thread_pool.close()
    thread_pool.join()
