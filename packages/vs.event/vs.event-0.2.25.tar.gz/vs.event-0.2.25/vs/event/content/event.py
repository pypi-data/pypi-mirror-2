# -*- coding: utf-8 -*-
# $Id: event.py 388 2009-06-13 09:32:31Z ajung $



from AccessControl import ClassSecurityInfo
from zope.interface import implements

from DateTime.DateTime import DateTime
from Products.ATContentTypes.content.event import ATEvent
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn
from Products.DataGridField.CheckboxColumn import CheckboxColumn

from Products.CMFCore.permissions import View

try:
    from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
except ImportError:
    from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget\
         import ReferenceBrowserWidget

from dateutil.rrule import YEARLY, MONTHLY, WEEKLY, DAILY

from vs.event.config import *
from vs.event.interfaces import IVSEvent, IVSSubEvent
from vs.event import MessageFactory as _
from vs.event import validators
from vs.event.fieldsandwidgets.calendarwidget import VSCalendarWidget
import event_util

try:
    from Products.LinguaPlone import public as atapi
except ImportError:
    from Products.Archetypes import atapi


from logging import getLogger
log = getLogger(">> event : ")

VSEventSchema = atapi.Schema((

    atapi.ReferenceField(
        name='subEvents',
        allowed_types=('VSSubEvent',),
        multiValued=True,
        relationship='isSubEvent',
        widget=ReferenceBrowserWidget(
            visible={'view': 'invisible', 'edit':'invisible'},
        ),
    ),
    atapi.LinesField(
        name='weekdays',
        schemata='recurrence',
        vocabulary=atapi.DisplayList((
            ('0', _(u'vs_label_mo', 'Monday')),
            ('1', _(u'vs_label_di', 'Tuesday')),
            ('2', _(u'vs_label_mi', 'Wednesday')),
            ('3', _(u'vs_label_do', 'Thursday')),
            ('4', _(u'vs_label_fr', 'Friday')),
            ('5', _(u'vs_label_sa', 'Saturday')),
            ('6', _(u'vs_label_so', 'Sunday')),
        )),
        widget=atapi.MultiSelectionWidget(
            format="checkbox",
            label=_(u'vs_event_label_weekdays', 'Weekdays'),
            description=_(u'vs_event_help_weekdays', 'Select weekdays'),
        ),
    ),
    atapi.StringField(
        name='bysetpos',
        schemata='recurrence',
        validators=('isLineOfInts',),
        widget=atapi.StringWidget(
            label=_(u'vs_event_label_bysetpos', 'Occurrence'),
            description=_(u'vs_event_help_bysetpos', 'Comma separated list of '
                           'numbers. If this event is on first and third '
                           'Monday of the month, enter "1,3" and select '
                           'appropriate day of the week above. For the last '
                           'day of the month, enter "-1", select Monday '
                           'through Friday above and monthly recurrence.'),
        ),
    ),
    atapi.LinesField(
        name='exceptions',
        schemata='recurrence',
        validators=('linesOfDates',),
        widget=atapi.LinesWidget(
            label=_(u'vs_event_label_exceptions', 'Exceptions'),
            description=_(u'vs_event_help_exceptions', 'Please enter exceptions to recurrence. One date per line in format YYYY-MM-DD'),
        ),
    ),

    atapi.IntegerField('frequency',
         schemata="recurrence",
         required=True,
         i18n_domain = "vs.event",
         vocabulary=atapi.IntDisplayList((
            (-1, _(u'Does not repeat')),
            (YEARLY, _(u'Yearly')),
            (MONTHLY, _(u'Monthly')),
            (WEEKLY, _(u'Weekly')),
            (DAILY, _(u'Daily'))
        )),
         default=-1,
         widget=atapi.SelectionWidget(label=_(u"vs_event_label_frequency", 'Frequency'),
                                     )
         ),
    atapi.IntegerField('interval',
         schemata="recurrence",
         required=True,
         default=1,
         widget=atapi.IntegerWidget(label=_(u"vs_event_label_interval", 'Interval'),
                                    )
         ),
    atapi.DateTimeField('until',
         schemata="recurrence",
         widget=VSCalendarWidget(label=_(u"vs_event_label_repeat_until", "Repeat until"),
                                 description=_(u"vs_event_description_repeat__until", "Event repeats until this date."),
                                 with_time=1)
         ),
    atapi.IntegerField('count',
          schemata="recurrence",
          widget=atapi.IntegerWidget(label=_(u"vs_event_label_count", 'Count'),
                                     description=_(u"vs_event_description_count", "Maxinum number of times the event repeats"),
                                    ),
          ),
))

VSEventSchema = VSEventSchema + ATEvent.schema.copy()
finalizeATCTSchema(VSEventSchema, folderish=False, moveDiscussion=True)


def modifyEventSchema(schema):
    schema.addField(atapi.BooleanField('wholeDay',
                                       description_msg='help_whole_day_event',
                                       widget=atapi.BooleanWidget(
                                           label='Whole day event',
                                           label_msgid='label_whole_day_event',
                                           i18n_domain='vs.event'),
                                       ))
    schema.addField(atapi.BooleanField('useEndDate',
                                       default=True,
                                       description_msg='help_has_end_date',
                                       widget=atapi.BooleanWidget(
                                           label='useEndDate',
                                           label_msgid='label_use_end_date',
                                           i18n_domain='vs.event'),
                                       ))
    schema.moveField('wholeDay', before='startDate')
    schema.moveField('useEndDate', after='wholeDay')
    schema['startDate'].widget = VSCalendarWidget(description= "",
                                                description_msgid = "help_event_start",
                                                label="Event Starts",
                                                label_msgid = "label_event_start",
                                                i18n_domain="vs.event",
                                                with_time=1,
                                                with_popup=1,
                                                js_shortcuts=0,
                                                ignore_unset_time=1)

    schema['endDate'].widget = VSCalendarWidget(description = "",
                                              description_msgid = "help_event_end",
                                              label = "Event Ends",
                                              label_msgid = "label_event_end",
                                              i18n_domain = "vs.event",
                                              with_time=1,
                                              with_popup=1,
                                              js_shortcuts=0,
                                              ignore_unset_time=1)

    del schema['until']
    schema.addField(atapi.DateTimeField('until',
                                 schemata='recurrence',
                                 widget=VSCalendarWidget(description=u"Event repeats until this date",
                                 description_msgid="vs_event_event_repeats_until_date",
                                 label="Repeat until",
                                 label_msgid="vs_event_label_repeat_until",
                                 i18n_domain="vs.event",
                                 with_time=1)))

    schema.addField(atapi.ReferenceField(name='attachments',
                                allowed_types=('Link','File'),
                                multiValued=1,
                                relationship='aAttachment',
                                widget=ReferenceBrowserWidget(
                                    show_review_state=1,
                                    allow_sorting=1,
                                    force_close_on_insert=1,
                                    base_query = {'Type':['Link','File']},
                                    i18n_domain="vs.event",
                                    label='Attachments',
                                    label_msgid='vs_event_label_attachments',
                                ),
                            ))

    del schema['attendees']
    schema.addField(DataGridField(name="attendees",
                            columns=('name', 'mail','role', 'show'),
                            schemata='attendees',
                            widget = DataGridWidget(
                                label=_(u'vs_event_label_roleAttendees', "Attendees and roles"),
                                columns={
                                    'name':     Column(_(u'vs_event_label_nameColumn', "Name")),
                                    'mail':     Column(_(u'vs_event_label_mailColumn', "e-Mail")),
                                    'role':     SelectColumn(_(u'vs_event_label_roleColumn', "Role"), vocabulary='getAttendeeRoles'),
                                    'show':     CheckboxColumn(_(u'vs_event_label_showColumn', "Show")),
                                }),
                            ))
    return schema

class VSEvent(ATEvent):
    """ vs.event """

    security = ClassSecurityInfo()
    implements(IVSEvent)
    meta_type = 'VSEvent'
    _at_rename_after_creation = True
    schema = modifyEventSchema(VSEventSchema)

    security.declareProtected(View, 'getICal')
    def getICal(self):
        """get iCal data """
        return event_util.getICal(self)

    security.declareProtected(View, 'getVCal')
    def getVCal(self):
        """get VCal data """
        return event_util.getVCal(self)


    def at_post_edit_script(self):
        """ Ensure that for single-day dates without an end date
            the end date is equal to the start date.
        """

        self.setExcludeFromNav(True)

        if not self.getUseEndDate():
            self.setEndDate(self.start())

        if self.getWholeDay():
            self.setStartDate(DateTime(self.start().strftime('%Y/%m/%d 00:00:00')))
            self.setEndDate(DateTime(self.end().strftime('%Y/%m/%d 23:59:00')))

    def getAttendeeRoles(self):
        """ """
        return atapi.DisplayList((
            ('chair',_(u'vs_event_label_chair')),
            ('observer',_(u'vs_event_label_observer')),
            ('participant',_(u'vs_event_label_participant')),
            ('opt_participant',_(u'vs_event_label_opt_participant')),
        ))

    security.declareProtected(View, 'post_validate')
    def post_validate(self, REQUEST=None, errors=None):
        """ Trigger original ATEvent.post_validate_method() for
            dates having an end date.
        """
        if REQUEST.get('useEndDate', True) == True:
            return super(VSEvent, self).post_validate(REQUEST=REQUEST,
                                                      errors=errors)

atapi.registerType(VSEvent, PROJECTNAME)


def modifySubEventSchema(schema):
    # remove unwanted fields for subevents

    for id in ('attendees', 'contactName', 'contactEmail', 'contactPhone',
               'eventType', 'eventUrl'):
        # Products.ATContentTypes in PLONE 4 dropped eventType in favor of
        # subject...
        if id in schema:
            schema[id].widget.visible = False
    for field in schema.fields():
        if field.schemata in ('dates', 'categorization', 'ownership', 'settings'):
            field.widget.visible = False

    schema.addField(atapi.BooleanField('wholeDay',
                                       default=False,
                                       description_msg='help_whole_day_event',
                                       label=_(u'label_whole_day_event', 'Whole day event'),
                                       ))
    schema.addField(atapi.BooleanField('useEndDate',
                                       default=True,
                                       description_msg='help_has_end_date',
                                       label=_(u'label_use_end_date', 'Use end date?'),
                                       ))
    schema.moveField('wholeDay', before='startDate')
    schema.moveField('useEndDate', after='wholeDay')

    schema['startDate'].widget = VSCalendarWidget(description= "",
                                                description_msgid = "help_event_start",
                                                label="Event Starts",
                                                label_msgid = "label_event_start",
                                                i18n_domain = "vs.event",
                                                with_time=1,
                                                with_popup=1,
                                                js_shortcuts=0,
                                                ignore_unset_time=1)

    schema['endDate'].widget = VSCalendarWidget(description = "",
                                              description_msgid = "help_event_end",
                                              label = "Event Ends",
                                              label_msgid = "label_event_end",
                                              i18n_domain = "vs.event",
                                              with_time=1,
                                              with_popup=1,
                                              js_shortcuts=0,
                                              ignore_unset_time=1)

    return schema

VSSubEventSchema = ATEvent.schema.copy()
finalizeATCTSchema(VSSubEventSchema, folderish=False, moveDiscussion=True)

class VSSubEvent(VSEvent):
    """ vs.event """

    implements(IVSSubEvent)
    meta_type = 'VSSubEvent'
    schema = modifySubEventSchema(VSSubEventSchema)

atapi.registerType(VSSubEvent, PROJECTNAME)
