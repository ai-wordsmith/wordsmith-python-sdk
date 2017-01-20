__title__ = 'wordsmith'
__version__ = '0.5'
__author__ = 'John Hegele'
__copyright__ = 'Copyright 2016 Automated Insights'

from .wordsmith import Wordsmith
from .configuration import Configuration
from .project import Project
from .template import Template
from .narrative import Narrative, Batch
from .exceptions import (ProjectSlugError, TemplateSlugError, NarrativeGenerateError)
