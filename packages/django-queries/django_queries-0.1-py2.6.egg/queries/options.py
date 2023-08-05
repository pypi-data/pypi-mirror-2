# vim: set ts=4 sw=4 :
from django import forms, template
from django.forms.models import modelform_factory, modelformset_factory, inlineformset_factory, _get_foreign_key
from django.forms.models import BaseInlineFormSet
from queries import widgets
from queries.util import unquote, flatten_fieldsets, get_deleted_objects, model_ngettext, model_format_dict
from django.db import models, transaction
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.functional import update_wrapper
from django.utils.functional import curry
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext, ugettext_lazy
from django.template import Context, Template
from django.template.loader import select_template
try:
	set
except NameError:
	from sets import Set as set	 # Python 2.3 fallback
def log(*p, **kw):
	for l in p:
		try:
			print l
		except:
			pass
	for k in kw:
		try:
			print '%s: %s' % k, kw[k]
		except:
			pass

HORIZONTAL, VERTICAL = 1, 2
# returns the <ul> class for a given radio_query field
get_ul_class = lambda x: 'radiolist%s' % ((x == HORIZONTAL) and ' inline' or '')

class IncorrectLookupParameters(Exception):
	pass

# Defaults for formfield_overrides. ModelQuery subclasses can change this
# by adding to ModelQuery.formfield_overrides.

FORMFIELD_FOR_DBFIELD_DEFAULTS = {
	models.DateTimeField: {
		'form_class': forms.SplitDateTimeField,
		'widget': widgets.QuerySplitDateTime
	},
	models.DateField:	{'widget': widgets.QueryDateWidget},
	models.TimeField:	{'widget': widgets.QueryTimeWidget},
	models.TextField:	{'widget': widgets.QueryTextInputWidget},
	models.URLField:	 {'widget': widgets.QueryURLFieldWidget},
	models.IntegerField: {'widget': widgets.QueryIntegerFieldWidget},
	models.CharField:	{'widget': widgets.QueryTextInputWidget},
}


class BaseModelQuery(object):
	"""Functionality common to both ModelQuery and InlineQuery."""

	raw_id_fields = ()
	fields = None
	exclude = None
	fieldsets = None
	form = forms.ModelForm
	radio_fields = {}
	formfield_overrides = {}

	def __init__(self):
		self.formfield_overrides = dict(FORMFIELD_FOR_DBFIELD_DEFAULTS, **self.formfield_overrides)

	def formfield_for_dbfield(self, db_field, **kwargs):
		request = kwargs.pop("request", None)

		# If the field specifies choices, we don't need to look for special
		# query widgets - we just need to use a select widget of some kind.
		if db_field.choices:
			return self.formfield_for_choice_field(db_field, request, **kwargs)

		# ForeignKey or ManyToManyFields
		if isinstance(db_field, (models.ForeignKey, models.ManyToManyField)):
			# Combine the field kwargs with any options for formfield_overrides.
			# Make sure the passed in **kwargs override anything in
			# formfield_overrides because **kwargs is more specific, and should
			# always win.
			if db_field.__class__ in self.formfield_overrides:
				kwargs = dict(self.formfield_overrides[db_field.__class__], **kwargs)

			# Get the correct formfield.
			if isinstance(db_field, (models.ForeignKey, models.ManyToManyField)):
				formfield = self.formfield_for_foreignkey(db_field, request, **kwargs)
				formfield.help_text=''

			# For non-raw_id fields, wrap the widget with a wrapper that adds
			# extra HTML -- the "add other" interface -- to the end of the
			# rendered output. formfield can be None if it came from a
			# OneToOneField with parent_link=True or a M2M intermediary.

			return formfield

		# If we've got overrides for the formfield defined, use 'em. **kwargs
		# passed to formfield_for_dbfield override the defaults.
		for klass in db_field.__class__.mro():
			if klass in self.formfield_overrides:
				kwargs = dict(self.formfield_overrides[klass], **kwargs)
				return db_field.formfield(**kwargs)

		# For any other type of field, just call its formfield() method.
		return db_field.formfield(**kwargs)

	def formfield_for_choice_field(self, db_field, request=None, **kwargs):
		"""
		Get a form Field for a database Field that has declared choices.
		"""
		# If the field is named as a radio_field, use a RadioSelect
		if db_field.name in self.radio_fields:
			# Avoid stomping on custom widget/choices arguments.
			if 'widget' not in kwargs:
				kwargs['widget'] = widgets.QueryRadioSelect(attrs={
					'class': get_ul_class(self.radio_fields[db_field.name]),
				})
			if 'choices' not in kwargs:
				kwargs['choices'] = db_field.get_choices(
					include_blank = db_field.blank,
					blank_choice=[('', _('None'))]
				)
		return db_field.formfield(**kwargs)

	def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
		"""
		Get a form Field for a ForeignKey.
		"""
		if db_field.name in self.raw_id_fields:
			kwargs['widget'] = widgets.ForeignKeyRawIdWidget(db_field.rel)
		elif db_field.name in self.radio_fields:
			kwargs['widget'] = widgets.QueryRadioSelect(attrs={
				'class': get_ul_class(self.radio_fields[db_field.name]),
			})
			kwargs['empty_label'] = db_field.blank and _('None') or None

		kwargs['widget'] = forms.SelectMultiple(attrs={'size':4})
		return db_field.formfield(**kwargs)

class ModelQuery(BaseModelQuery):
	"Encapsulates all query options and functionality for a given model."
	__metaclass__ = forms.MediaDefiningClass

	list_display = ('__str__',)
	list_filter = ()
	list_select_related = False
	list_per_page = 100
	list_editable = ()
	inlines = []
	search_fields = ()
	date_hierarchy = None
	save_as = False
	save_on_top = False
	ordering = None

	# Custom templates (designed to be over-ridden in subclasses)
	change_form_template = None
	filter_site_template = None
	search_results_template = None
	results_template = None
	delete_confirmation_template = None
	object_history_template = None

	def __init__(self, model, query_site): # {{{
		self.model = model
		self.opts = model._meta
		self.query_site = query_site
		self.inline_instances = []
		for inline_class in self.inlines:
			inline_instance = inline_class(self.model, self.query_site)
			self.inline_instances.append(inline_instance)
		super(ModelQuery, self).__init__() # }}}

	def get_urls(self): # {{{
		from django.conf.urls.defaults import patterns, url

		def wrap(view):
			def wrapper(*args, **kwargs):
				return self.query_site.query_view(view)(*args, **kwargs)
			return update_wrapper(wrapper, view)

		info = self.model._meta.app_label, self.model._meta.module_name

		urlpatterns = patterns('',
			url(r'^$',
				wrap(self.filter_view),
				name='%s_%s_changelist' % info),
		)
		return urlpatterns # }}}

	def urls(self): # {{{
		return self.get_urls()
	urls = property(urls) # }}}

	def _media(self): # {{{ # {{{
		from django.conf import settings

		js = ['js/core.js', 'js/queries/RelatedObjectLookups.js']
		if self.actions is not None:
			js.extend(['js/getElementsBySelector.js', 'js/actions.js'])
		if self.opts.get_ordered_objects():
			js.extend(['js/getElementsBySelector.js', 'js/dom-drag.js' , 'js/queries/ordering.js'])

		return forms.Media(js=['%s%s' % (settings.ADMIN_MEDIA_PREFIX, url) for url in js])
	media = property(_media) # }}} # }}}

	def get_model_perms(self, request): # {{{
		"""
		Returns a dict of all perms for this model. This dict has the keys
		``add``, ``change``, and ``delete`` mapping to the True/False for each
		of those actions.
		"""
		return {
			'add': True,
			'change': True,
			'delete': True,
		} # }}}

	def get_formsets(self, request): # {{{
		for inline in self.inline_instances:
			yield inline.get_formset(request) # }}}

	def get_search_form(self, request, **kwargs): # {{{
		defaults = {
				"formfield_callback": curry(self.formfield_for_dbfield, request=request),
				}
		defaults.update(kwargs)
		tf =  modelform_factory(self.model,
			fields=self.fields, 
			**defaults)
		return tf # }}}

	def message_user(self, request, message): # {{{
		"""
		Send a message to the user. The default implementation
		posts a message using the auth Message object.
		"""
		request.user.message_set.create(message=message) # }}}

	def filter_view(self, request, extra_context=None): # {{{
		"The 'change list' query view for this model."
		opts = self.model._meta
		app_label = opts.app_label

		# Remove action checkboxes if there aren't any actions available.
		list_display = list(self.list_display)
		try:
			list_display.remove('action_checkbox')
		except ValueError:
			pass

		search_form = self.get_search_form(request)(data=None, initial=None, empty_permitted=True)
		search_form._meta.exclude = self.fields # exclude all fields from validation

		for f in search_form.fields:
			field_type = self.model._meta.get_field_by_name('%s' % f)[0]
			if isinstance(field_type, (models.ForeignKey, models.ManyToManyField)):
				search_form.fields[f].initial = request.REQUEST.getlist(f)
			else:
				search_form.fields[f].initial = request.REQUEST.get(f, '')
			search_form.fields[f].required = False
			search_form.fields[f].null = True

		search_results = self.model.objects.all()
		filter_params = {}
		for field_name in self.fields:
			query_text_list = request.REQUEST.getlist(field_name)

			field_type = self.model._meta.get_field_by_name('%s' % field_name)[0]
			if len(query_text_list)>0:
				if query_text_list[0]:
					if isinstance(field_type, (models.ForeignKey, models.ManyToManyField)):
						filter_params['%s__pk__in'%field_name] = query_text_list
					else:
						filter_params['%s__icontains'%field_name] = query_text_list[0]
		search_results = search_results.filter(**filter_params)

		for il in self.inlines:
			filter_params = {}
			filter_this = False
			for field_name in il.fields:
				query_text_list = request.REQUEST.getlist('%s-%s' % (il.model._meta.module_name, field_name))
				field_type = il.model._meta.get_field_by_name('%s' % field_name)[0] # Type of searched model-field
				if len(query_text_list)>0:
					if query_text_list[0]:
						filter_this = True
						if isinstance(field_type, (models.ForeignKey, models.ManyToManyField)):
							filter_params['%s__pk__in'%field_name] = query_text_list
						else:
							filter_params['%s__icontains'%field_name] = query_text_list[0]
			if filter_this: # This inline formular contained query, so filter by these values
				inline_objects = il.model.objects.all()
				fk = _get_foreign_key(self.model, il.model, None, True) # FK:
				inline_objects = inline_objects.filter(**filter_params)
				inline_fks = [x.__getattribute__('%s' % fk.name).pk for x in inline_objects]
				pk_in_inlinefks = {'pk__in':inline_fks}
				search_results = search_results.filter(**pk_in_inlinefks)

		if not search_results:
			self.message_user(request, _('No %s found') % self.model._meta.verbose_name_plural)

		formsets = []
		new_object = self.model()
		prefixes = {}
		for FormSet in self.get_formsets(request):
			prefix = FormSet._meta.model._meta.module_name
			prefixes[prefix] = prefixes.get(prefix, 0) + 1
			if prefixes[prefix] != 1:
				prefix = "%s-%s" % (prefix, prefixes[prefix])
			formset = FormSet(data=None, initial=None, files=None, prefix=prefix, empty_permitted=True)
			formset._meta.exclude = self.fields
			for f in formset.fields:
				field_type = formset._meta.model._meta.get_field_by_name(f)[0]
				formset.fields[f].required = False
				formset.fields[f].null = True

				if isinstance(field_type, (models.ForeignKey, models.ManyToManyField)):
					rp = request.REQUEST.getlist('%s-%s' % (prefix, f))
					if rp:
						formset.fields[f].initial = rp
				else:
					rp = request.REQUEST.get('%s-%s' % (prefix, f), '')
					if rp:
						formset.fields[f].initial = request.REQUEST.get('%s-%s' % (prefix, f), '')
			formsets.append(formset)

		context = {
			'title': _('Filter %(model_name_plural)s') % {'model_name_plural':self.model._meta.verbose_name_plural},
			'media': self.media,
			'root_path': self.query_site.root_path,
			'meta': self.model._meta,
			'app_label': app_label,
			'query_form': search_form,
			'object_list': search_results,
			'inline_query_forms': formsets,
			'results_template': self.results_template or 'queries/result.html'
		}
		result_list = select_template(self.search_results_template or [
			'queries/%s/%s/search_results.html' % (app_label, opts.object_name.lower()),
			'queries/%s/search_results.html' % app_label,
			'queries/search_results.html']).render(Context(context))

		context.update({
			'result_list': result_list,
			})
		context.update(extra_context or {})
		context_instance = template.RequestContext(request, current_app=self.query_site.name)
		return render_to_response(self.filter_site_template or [
			'queries/%s/%s/filter_site.html' % (app_label, opts.object_name.lower()),
			'queries/%s/filter_site.html' % app_label,
			'queries/filter_site.html'
		], context, context_instance=context_instance) # }}}

	# DEPRECATED methods. # {{{
	#
	def __call__(self, request, url):
		"""
		DEPRECATED: this is the old way of URL resolution, replaced by
		``get_urls()``. This only called by QuerySite.root(), which is also
		deprecated.

		Again, remember that the following code only exists for
		backwards-compatibility. Any new URLs, changes to existing URLs, or
		whatever need to be done up in get_urls(), above!

		This function still exists for backwards-compatibility; it will be
		removed in Django 1.3.
		"""
		# Delegate to the appropriate method, based on the URL.
		if url is None:
			return self.filter_view(request)
		else:
			raise 'A' # }}}

class InlineModelQuery(BaseModelQuery):
	"""
	Options for inline editing of ``model`` instances.
	"""
	model = None
	formset = BaseInlineFormSet
	template = None
	verbose_name = None
	verbose_name_plural = None

	def __init__(self, parent_model, query_site):
		self.query_site = query_site
		self.parent_model = parent_model
		self.opts = self.model._meta
		super(InlineModelQuery, self).__init__()
		if self.verbose_name is None:
			self.verbose_name = self.model._meta.verbose_name
		if self.verbose_name_plural is None:
			self.verbose_name_plural = self.model._meta.verbose_name_plural

	def get_formset(self, request):
		defaults = {
			"formfield_callback": curry(self.formfield_for_dbfield, request=request),
		}
		search_form = modelform_factory(self.model, fields=self.fields, **defaults)
		search_form.verbose_name = self.model._meta.verbose_name
		search_form.verbose_name_plural = self.model._meta.verbose_name_plural
		return search_form 
