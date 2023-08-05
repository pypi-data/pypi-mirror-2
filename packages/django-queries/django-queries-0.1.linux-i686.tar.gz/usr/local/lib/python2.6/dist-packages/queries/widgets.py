"""
Form Widget classes specific to the Django query site.
"""

import copy
from qlogging import log
log.info('Loading widgets.py')
from django import forms
from django.forms.widgets import RadioFieldRenderer
from django.forms.util import flatatt
from django.utils.html import escape
from django.utils.text import truncate_words
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.conf import settings
from django.core.urlresolvers import reverse, NoReverseMatch
from queries import fields

class FilteredSelectMultiple(forms.SelectMultiple):
	"""
	A SelectMultiple with a JavaScript filter interface.

	Note that the resulting JavaScript assumes that the jsi18n
	catalog has been loaded in the page
	"""
	class Media:
		js = (settings.ADMIN_MEDIA_PREFIX + "js/core.js",
			  settings.ADMIN_MEDIA_PREFIX + "js/SelectBox.js",
			  settings.ADMIN_MEDIA_PREFIX + "js/SelectFilter2.js")

	def __init__(self, verbose_name, is_stacked, attrs=None, choices=()):
		self.verbose_name = verbose_name
		self.is_stacked = is_stacked
		super(FilteredSelectMultiple, self).__init__(attrs, choices)

	def render(self, name, value, attrs=None, choices=()):
		output = [super(FilteredSelectMultiple, self).render(name, value, attrs, choices)]
		output.append(u'<script type="text/javascript">addEvent(window, "load", function(e) {')
		# TODO: "id_" is hard-coded here. This should instead use the correct
		# API to determine the ID dynamically.
		output.append(u'SelectFilter.init("id_%s", "%s", %s, "%s"); });</script>\n' % \
			(name, self.verbose_name.replace('"', '\\"'), int(self.is_stacked), settings.ADMIN_MEDIA_PREFIX))
		return mark_safe(u''.join(output))

class QueryDateWidget(forms.TextInput):
	class Media:
		js = (settings.ADMIN_MEDIA_PREFIX + "js/calendar.js",
			  settings.ADMIN_MEDIA_PREFIX + "js/queries/DateTimeShortcuts.js")

	def __init__(self, attrs={}):
		super(QueryDateWidget, self).__init__(attrs={'class': 'vDateField', 'size': '10'})

class QueryDateWidgetFromTo(forms.SplitDateTimeWidget):
	def __init__(self, attrs=None):
		widgets = [QueryDateWidget, QueryTimeWidget]
		# Note that we're calling MultiWidget, not SplitDateTimeWidget, because
		# we want to define widgets.
		forms.MultiWidget.__init__(self, widgets, attrs)

class QueryTimeWidget(forms.TextInput):
	class Media:
		js = (settings.ADMIN_MEDIA_PREFIX + "js/calendar.js",
			  settings.ADMIN_MEDIA_PREFIX + "js/queries/DateTimeShortcuts.js")

	def __init__(self, attrs={}):
		super(QueryTimeWidget, self).__init__(attrs={'class': 'vTimeField', 'size': '8'})

class QuerySplitDateTime(forms.SplitDateTimeWidget):
	"""
	A SplitDateTime Widget that has some query-specific styling.
	"""
	def __init__(self, attrs=None):
		widgets = [QueryDateWidget, QueryTimeWidget]
		# Note that we're calling MultiWidget, not SplitDateTimeWidget, because
		# we want to define widgets.
		forms.MultiWidget.__init__(self, widgets, attrs)

	def format_output(self, rendered_widgets):
		return mark_safe(u'<p class="datetime">%s %s<br />%s %s</p>' % \
			(_('Date:'), rendered_widgets[0], _('Time:'), rendered_widgets[1]))

class QueryRadioFieldRenderer(RadioFieldRenderer):
	def render(self):
		"""Outputs a <ul> for this set of radio fields."""
		return mark_safe(u'<ul%s>\n%s\n</ul>' % (
			flatatt(self.attrs),
			u'\n'.join([u'<li>%s</li>' % force_unicode(w) for w in self]))
		)

class QueryRadioSelect(forms.RadioSelect):
	renderer = QueryRadioFieldRenderer

class QueryFileWidget(forms.FileInput):
	"""
	A FileField Widget that shows its current value if it has one.
	"""
	def __init__(self, attrs={}):
		super(QueryFileWidget, self).__init__(attrs)

	def render(self, name, value, attrs=None):
		output = []
		if value and hasattr(value, "url"):
			output.append('%s <a target="_blank" href="%s">%s</a> <br />%s ' % \
				(_('Currently:'), value.url, value, _('Change:')))
		output.append(super(QueryFileWidget, self).render(name, value, attrs))
		return mark_safe(u''.join(output))

class ForeignKeyRawIdWidget(forms.TextInput):
	"""
	A Widget for displaying ForeignKeys in the "raw_id" interface rather than
	in a <select> box.
	"""
	def __init__(self, rel, attrs=None):
		self.rel = rel
		super(ForeignKeyRawIdWidget, self).__init__(attrs)

	def render(self, name, value, attrs=None):
		if attrs is None:
			attrs = {}
		related_url = '../../../%s/%s/' % (self.rel.to._meta.app_label, self.rel.to._meta.object_name.lower())
		params = self.url_parameters()
		if params:
			url = '?' + '&amp;'.join(['%s=%s' % (k, v) for k, v in params.items()])
		else:
			url = ''
		if not attrs.has_key('class'):
			attrs['class'] = 'vForeignKeyRawIdQueryField' # The JavaScript looks for this hook.
		output = [super(ForeignKeyRawIdWidget, self).render(name, value, attrs)]
		# TODO: "id_" is hard-coded here. This should instead use the correct
		# API to determine the ID dynamically.
		output.append('<a href="%s%s" class="related-lookup" id="lookup_id_%s" onclick="return showRelatedObjectLookupPopup(this);"> ' % \
			(related_url, url, name))
		output.append('<img src="%simg/queries/selector-search.gif" width="16" height="16" alt="%s" /></a>' % (settings.ADMIN_MEDIA_PREFIX, _('Lookup')))
		if value:
			output.append(self.label_for_value(value))
		return mark_safe(u''.join(output))

	def base_url_parameters(self):
		params = {}
		if self.rel.limit_choices_to:
			items = []
			for k, v in self.rel.limit_choices_to.items():
				if isinstance(v, list):
					v = ','.join([str(x) for x in v])
				else:
					v = str(v)
				items.append((k, v))
			params.update(dict(items))
		return params

	def url_parameters(self):
		from queries.views.main import TO_FIELD_VAR
		params = self.base_url_parameters()
		params.update({TO_FIELD_VAR: self.rel.get_related_field().name})
		return params

	def label_for_value(self, value):
		key = self.rel.get_related_field().name
		obj = self.rel.to._default_manager.get(**{key: value})
		return '&nbsp;<strong>%s</strong>' % escape(truncate_words(obj, 14))

class ManyToManyRawIdWidget(ForeignKeyRawIdWidget):
	"""
	A Widget for displaying ManyToMany ids in the "raw_id" interface rather than
	in a <select multiple> box.
	"""
	def __init__(self, rel, attrs=None):
		super(ManyToManyRawIdWidget, self).__init__(rel, attrs)

	def render(self, name, value, attrs=None):
		attrs['class'] = 'vManyToManyRawIdQueryField'
		if value:
			value = ','.join([str(v) for v in value])
		else:
			value = ''
		return super(ManyToManyRawIdWidget, self).render(name, value, attrs)

	def url_parameters(self):
		return self.base_url_parameters()

	def label_for_value(self, value):
		return ''

	def value_from_datadict(self, data, files, name):
		value = data.get(name, None)
		if value and ',' in value:
			return data[name].split(',')
		if value:
			return [value]
		return None

	def _has_changed(self, initial, data):
		if initial is None:
			initial = []
		if data is None:
			data = []
		if len(initial) != len(data):
			return True
		for pk1, pk2 in zip(initial, data):
			if force_unicode(pk1) != force_unicode(pk2):
				return True
		return False

class QueryTextareaWidget(forms.Textarea):
	def __init__(self, attrs=None):
		final_attrs = {'class': 'vLargeTextField'}
		if attrs is not None:
			final_attrs.update(attrs)
		super(QueryTextareaWidget, self).__init__(attrs=final_attrs)

class QueryTextInputWidget(forms.TextInput):
	def __init__(self, attrs=None):
		final_attrs = {'class': 'vTextField'}
		if attrs is not None:
			final_attrs.update(attrs)
		super(QueryTextInputWidget, self).__init__(attrs=final_attrs)

class QueryURLFieldWidget(forms.TextInput):
	def __init__(self, attrs=None):
		final_attrs = {'class': 'vURLField'}
		if attrs is not None:
			final_attrs.update(attrs)
		super(QueryURLFieldWidget, self).__init__(attrs=final_attrs)

class QueryIntegerFieldWidget(forms.TextInput):
	def __init__(self, attrs=None):
		final_attrs = {'class': 'vIntegerField'}
		if attrs is not None:
			final_attrs.update(attrs)
		super(QueryIntegerFieldWidget, self).__init__(attrs=final_attrs)

class QueryIntegerFromToWidget(forms.MultiWidget):
	def __init__(self, attrs=None):
		widgets = [QueryIntegerFieldWidget, QueryIntegerFieldWidget()]
		super(QueryIntegerFromToWidget, self).__init__(widgets, attrs=attrs)

	def format_output(self, rendered_widgets):
		return mark_safe('%s %s %s %s' % (_('between'), rendered_widgets[0], _('and'), rendered_widgets[1]))

	def decompress(self, value):
		if value:
			values = value.split('|')
			return [values[0], values[1]]
		return [None, None]

