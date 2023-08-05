##############################################################################
#
# Copyright (c) Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

import decimal
import pytz
import rwproperty
import zc.ajaxform.interfaces
import zc.form.interfaces
import zc.sourcefactory.basic
import zope.app.form
import zope.app.form.browser.interfaces
import zope.app.form.browser.widget
import zope.app.form.interfaces
import zope.cachedescriptors.property
import zope.component
import zope.html.field
import zope.interface
import zope.schema.interfaces


class Base(zope.app.form.InputWidget):

    zope.interface.implements(zc.ajaxform.interfaces.IInputWidget)

    widget_constructor = None

    def __init__(self, context, request):
        self.custom_type = None
        self.id = context.__name__
        super(Base, self).__init__(context, request)

    def js_config(self, **kw):
        config = dict(
            fieldLabel = self.label,
            fieldHint = self.hint,
            name = self.id,
            id = self.id,
            required = self.required,
            **kw)

        display_options = zope.component.queryAdapter(
            self, zc.ajaxform.interfaces.IDisplayOptions)
        if display_options:
            config['display_options'] = display_options

        if not self.widget_constructor:
            raise ValueError(
                'widget_constructor not defined.')

        config['widget_constructor'] = self.widget_constructor

        if self._renderedValueSet():
            value = self.formValue(self._data)
            if value is not None:
                config['value'] = value
        
        return config 

    def formValue(self, v):
        if v == self.context.missing_value:
            return None
        return unicode(v)

    def value(self, raw):
        return self._toValue(raw)
    
    def _toValue(self, v):              # for backward compat for a while
        return v

    def hasInput(self):
        return self.id in self.request.form

    def _is_missing(self, raw):
        return False

    def _get_raw(self):
        return self.request.form[self.id]

    def getInputValue(self):
        if not self.hasInput():
            raise zope.app.form.interfaces.MissingInputError(
                self.id, self.label, self.label+': Missing Input')

        raw = self._get_raw()
        if self._is_missing(raw):
            if self.required:
                raise zope.app.form.interfaces.MissingInputError(
                    self.id, self.label, self.label+': Missing Input')
            else:
                return self.context.missing_value
            
        value = self.value(raw)
        
        # value must be valid per the field constraints
        try:
            self.context.validate(value)
        except zope.schema.interfaces.ValidationError, v:
            raise zope.app.form.interfaces.WidgetInputError(
                self.context.__name__, self.label, v)
            
        return value
 
    @zope.cachedescriptors.property.Lazy
    def required(self):
        return self.context.required

class BasicDisplay(zope.app.form.browser.widget.DisplayWidget):

    zope.component.adapts(
        zope.schema.interfaces.ITextLine,
        zc.ajaxform.interfaces.IAjaxRequest,
        )

    widget_constructor = 'zc.ajaxform.widgets.BasicDisplay'

    def __init__(self, context, request):
        self.id = context.__name__
        super(BasicDisplay, self).__init__(context, request)

    def formValue(self, v):
        if v == self.context.missing_value:
            return None
        return unicode(v)

    def js_config(self, **kw):
        # XXX needs tests.
        config = dict(
            fieldLabel = self.label,
            fieldHint = self.hint,
            name = self.id,
            id = self.id,
            required = self.required,
            **kw)

        if not self.widget_constructor:
            raise ValueError(
                'widget_constructor not defined.')

        display_options = zope.component.queryAdapter(
            self, zc.ajaxform.interfaces.IDisplayOptions)
        if display_options:
            config['display_options'] = display_options

        config['widget_constructor'] = self.widget_constructor

        if self._renderedValueSet():
            value = self._data
            if value is not None:
                config['value'] = value

        return config

class RichTextDisplay(BasicDisplay):

    zope.component.adapts(
        zope.schema.interfaces.IText,
        zc.ajaxform.interfaces.IAjaxRequest,
        )

    widget_constructor = 'zc.ajaxform.widgets.RichTextDisplay'

class InputBool(Base):

    zope.component.adapts(
        zope.schema.interfaces.IBool,
        zc.ajaxform.interfaces.IAjaxRequest,
        )

    widget_constructor = 'zope.schema.Bool'

    def hasInput(self):
        return True
        
    def getInputValue(self):
        return self.request.form.get(self.id, '') == 'on'

    def formValue(self, v):
        if v == self.context.missing_value:
            return None
        return bool(v)


class InputChoiceIterable(Base):

    zope.component.adapts(
        zope.schema.interfaces.IChoice,
        zope.schema.interfaces.IIterableSource,
        zc.ajaxform.interfaces.IAjaxRequest,
        )

    widget_constructor = 'zope.schema.Choice'

    def __init__(self, context, source, request):
        Base.__init__(self, context, request)
        self.source = source

    @rwproperty.getproperty
    def terms(self):
        return zope.component.getMultiAdapter(
            (self.source, self.request),
            zope.app.form.browser.interfaces.ITerms)

    def _is_missing(self, raw):
        return not raw

    def js_config(self, **kw):
        result = Base.js_config(self, **kw)

        result['values'] = [
            [term.token, term.title]
            for term in (self.terms.getTerm(v) for v in self.source)
            ]

        if self.required:
            result['allowBlank'] = False

        return result

    def formValue(self, v):
        if v == self.context.missing_value:
            return None
        return self.terms.getTerm(v).token

    def value(self, v):
        return self.terms.getValue(v)


class InputChoiceTokenized(InputChoiceIterable):

    zope.component.adapts(
        zope.schema.interfaces.IChoice,
        zope.schema.interfaces.IVocabularyTokenized,
        zc.ajaxform.interfaces.IAjaxRequest,
        )

    def js_config(self, **kw):
        result = Base.js_config(self, **kw)
        result['hiddenName'] = result['name']+'.value'

        result['values'] = [
            [term.token, term.title or unicode(term.value)]
            for term in self.source
            ]
        
        if self.required:
            result['allowBlank'] = False

        return result

    def formValue(self, v):
        if v == self.context.missing_value:
            return None
        return self.source.getTerm(v).token

    def value(self, v):
        return self.source.getTermByToken(v).value


class InputTimeZone(InputChoiceTokenized):

    zope.component.adapts(
        zope.schema.interfaces.IChoice,
        zc.form.interfaces.AvailableTimeZones,
        zc.ajaxform.interfaces.IAjaxRequest
        )

    _timezones = sorted([(tzname, pytz.timezone(tzname))
                        for tzname in pytz.all_timezones])

    def __init__(self, context, source, request):
        source = zope.schema.vocabulary.SimpleVocabulary.fromItems(
                                                            self._timezones)
        InputChoiceIterable.__init__(self, context, source, request)


class InputInt(Base):

    zope.component.adapts(
        zope.schema.interfaces.IInt,
        zc.ajaxform.interfaces.IAjaxRequest,
        )

    widget_constructor = 'zope.schema.Int'

    def js_config(self, **kw):
        config = Base.js_config(self, **kw)

        if self.required:
            config['allowBlank'] = False
        
        if self.context.min is not None:
            config['field_min'] = self.context.min
        if self.context.max is not None:
            config['field_max'] = self.context.max

        return config

    def _is_missing(self, raw):
        return not raw

    def value(self, v):
        try:
            return int(v)
        except:
            raise zope.app.form.interfaces.ConversionError(
                u"Invalid integer: %r" % v
                )

class NumberSpinner(InputInt):

    zope.component.adapts(
        zc.ajaxform.interfaces.INumberSpinner,
        zc.ajaxform.interfaces.IAjaxRequest,
        )

    widget_constructor = 'zc.ajaxform.widgets.NumberSpinner'

class InputDecimal(Base):

    zope.component.adapts(
        zope.schema.interfaces.IDecimal,
        zc.ajaxform.interfaces.IAjaxRequest)

    widget_constructor = 'zope.schema.Decimal'

    def js_config(self, **kw):
        result = Base.js_config(self, **kw)
        if self.required:
            result['allowBlank'] = False
        return result

    def _is_missing(self, raw):
        return not raw

    def _toForm(self, v):
        return str(v)

    def value(self, v):
        try:
            return decimal.Decimal(v)
        except decimal.InvalidOperation:
            raise zope.app.form.interfaces.ConversionError(
                u"Invalid decimal: %r" % v)

    def getInputValue(self):
        v = super(InputDecimal, self).getInputValue()
        return str(v)

class InputTextLine(Base):

    zope.component.adapts(
        zope.schema.interfaces.ITextLine,
        zc.ajaxform.interfaces.IAjaxRequest,
        )

    widget_constructor = 'zope.schema.TextLine'

    def _is_missing(self, raw):
        return (not raw) and self.required

    def js_config(self, **kw):
        config = Base.js_config(self, **kw)
        if self.context.min_length is not None:
            config['minLength'] = self.context.min_length
            if self.context.min_length > 0 and self.required:
                config['allowBlank'] = False

        if self.context.max_length is not None:
            config['maxLength'] = self.context.max_length

        return config


class InputPassword(InputTextLine):

    zope.component.adapts(
        zope.schema.interfaces.IPassword,
        zc.ajaxform.interfaces.IAjaxRequest,
        )

    widget_constructor = 'zope.schema.Password'


class InputText(InputTextLine):

    zope.component.adapts(
        zope.schema.interfaces.IText,
        zc.ajaxform.interfaces.IAjaxRequest,
        )

    widget_constructor = 'zope.schema.Text'


class InputRichText(InputText):

    zope.component.adapts(
        zope.html.field.IHtmlFragmentField,
        zc.ajaxform.interfaces.IAjaxRequest,
        )

    widget_constructor = 'zc.ajaxform.widgets.RichText'


class ComboBox(InputChoiceIterable, InputTextLine):

    widget_constructor = 'zc.ajaxform.widgets.ComboBox'

    def __init__(self, context, source, request):
        InputChoiceIterable.__init__(self, context, source, request)

    js_config = InputChoiceIterable.js_config

    def formValue(self, v):
        if not v:
            return None
        else:
            return v

    def value(self, v):
        return InputTextLine.value(self, v)


class Hidden(Base):

    widget_constructor = 'zc.ajaxform.widgets.Hidden'

class RecordList(Base):

    zope.component.adapts(
        zope.schema.interfaces.IList,
        zc.ajaxform.interfaces.IAjaxRequest,
        )

    widget_constructor = 'zope.schema.List'

    @property
    def record_schema(self):
        try:
            record_schema = zope.formlib.form.FormFields(
                self.context.value_type.schema)
        except TypeError:
            record_schema = self.context.value_type.schema
        return record_schema

    def setUpRecordWidgets(self):
        record_widgets = zope.formlib.form.setUpWidgets(
            self.record_schema, self.id, self.context.context,
            self.request,
            ignore_request=True)
        return record_widgets

    def js_config(self, **kw):
        record_widgets = self.setUpRecordWidgets()
        config = Base.js_config(self, **kw)
        for widget in record_widgets:
            assert hasattr(widget, 'js_config'), (
                    'Could not find a js widget for %r' % widget.name)

        config['record_schema'] = dict(
            widgets=[widget.js_config() for widget in record_widgets],
            readonly = self.context.readonly
            )
        return config

    def hasInput(self):
        return True

    def _get_record_components(self, idx):
        record_widgets = self.setUpRecordWidgets()
        str_num = '.%d' % idx
        prefix = '%s.' % self.id
        # ensure all widget components are present
        # if not, all records have been accumulated
        component_vals = [
            wid for wid in record_widgets
            if ('%s%s%s' % (prefix, wid.id, str_num)) in self.request.form]
        if not component_vals:
            return None
        record = {}
        for wid in record_widgets:
            wid.id = '%s%s%s' % (prefix, wid.id, str_num)
            value = wid.getInputValue()
            name = wid.id[len(prefix):len(wid.id)-len(str_num)]
            record[name] = value
        return record

    def _get_raw(self):
        form_len = (self.request.form)
        i = 0
        raw = {}
        while True:
            record = self._get_record_components(i)
            if record is None:
                break
            raw[i] = record
            i += 1
            if i >= form_len:
                break
        if not raw and self.required:
            raise zope.app.form.interfaces.MissingInputError(
                self.id, self.label, self.label+': Missing Input')
        return [raw_data for raw_data in raw.values()]

    def validate(self, value):
        try:
            keys = [field.__name__ for field in self.record_schema]
            for item in value:
                for key in item:
                    if key not in keys:
                        raise zope.schema.interfaces.ValidationError(
                            '%s is not part of the recordschema' % (key))
        except TypeError:
            raise zope.schema.interfaces.ValidationError(
                '%s is not a properly formatted value for a list field' % (
                    value))

    def getInputValue(self):
        if not self.hasInput():
            raise zope.app.form.interfaces.MissingInputError(
                self.id, self.label, self.label+': Missing Input')

        raw = self._get_raw()
        value = self.value(raw)

        # value must be valid per the field constraints
        try:
            self.validate(value)
        except zope.schema.interfaces.ValidationError, v:
            raise zope.app.form.interfaces.WidgetInputError(
                self.context.__name__, self.label, v)

        return value

    def formValue(self, value):
        record_widgets = self.setUpRecordWidgets()
        new_value = []
        if value:
            for item in value:
                new_value.append(
                    dict([(widget.id, widget.formValue(item.get(widget.id)))
                    for widget in record_widgets]))
        return new_value
