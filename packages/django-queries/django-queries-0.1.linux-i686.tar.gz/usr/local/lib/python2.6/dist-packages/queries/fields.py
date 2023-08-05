from django import forms
from qlogging import log
from django.forms import models, fields

class BaseQueryField:
	"""
	This is the base class for ALL query fields. It defines
	the default function for finding instances in the model.
	"""
	def add_filters(self, name, value):
		f = [('%s__istartswith'%name, value)]
		return f

class QueryModelChoiceField(models.ModelChoiceField, BaseQueryField):
	"Default for foreign keys."
	def add_filters(self, name, value):
		f = [('%s__pk__in'%name, value)]
		log.info(f)
		return f

class QueryCharField(fields.CharField, BaseQueryField):
	pass

class QueryDateTimeField(forms.SplitDateTimeField, BaseQueryField):
	pass

class QueryFromToField(forms.MultiValueField, BaseQueryField):
	"""
	From-To-fields need special attention when adding the filters. It can be
	- no filters added (when nothing is entered)
	- filter for <min> entered, then objects are found, whose <field> is greater than <value>
	- filter for <max> entered, then objects are found whose <field> is smaller than <value>
	- or both.
	"""
	def add_filters(self, name, value):
		f = []
		if value[0]:#min
			f.append(('%s__gte'%name, value[0]))
		if value[1]:#max
			f.append(('%s__lte'%name, value[1]))
		return f

	def compress(self, data_list):
		if data_list:
			return '%s' % data_list
		return None

# a class like this has to be written if you want to create own From-To fields.
class QueryIntegerFromToField(QueryFromToField):
	def __init__(self, required=False, widget=None, label=None, initial=None, **kwargs):
		fields = [forms.IntegerField(), forms.IntegerField()]
		super(QueryIntegerFromToField, self).__init__(fields, required, widget, label, initial)

class QueryCharFromToField(QueryFromToField):
	def __init__(self, required=False, widget=None, label=None, initial=None, **kwargs):
		fields = [forms.CharField(), forms.CharField()]
		super(QueryCharFromToField, self).__init__(fields, required, widget, label, initial)
