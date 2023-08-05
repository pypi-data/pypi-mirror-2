from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from queries.util import quote
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode
from django.utils.safestring import mark_safe

ADDITION = 1
CHANGE = 2
DELETION = 3

