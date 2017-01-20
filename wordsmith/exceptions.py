"""
wordsmith.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains Wordsmith's custom exceptions.
"""

class ProjectSlugError(ValueError):
  """An invalid project slug was passed."""

  def __init__(self, msg):
    self.msg = msg

class TemplateSlugError(ValueError):
  """An invalid template slug was passed."""

  def __init__(self, msg):
    self.msg = msg

class NarrativeGenerateError(Exception):
  """The Wordsmith platform responded with an error code when attempting to generate narrative."""

  def __init__(self, response, data):
    """Initialize with the HTTP response object"""
    self.http_status_code = response.status_code
    self.http_reason = response.reason
    self.data = data
    try:
      self.details = [str(e['detail']) for e in response.json()['errors']]
      self._details_reported = True
    except KeyError:
      self.details = ['Wordsmith reported an error but no details were provided.']
      self._details_reported = False
    self.msg = '\nError generating narrative.' + \
               '\nHTTP Status Code: {}'.format(self.http_status_code) + \
               '\nHTTP Reason: {}'.format(self.http_reason) + \
               '\nNumber of errors reported by Wordsmith: {}'.format(len(self.details) if self._details_reported else 0)
    super(NarrativeGenerateError, self).__init__(self.msg)
