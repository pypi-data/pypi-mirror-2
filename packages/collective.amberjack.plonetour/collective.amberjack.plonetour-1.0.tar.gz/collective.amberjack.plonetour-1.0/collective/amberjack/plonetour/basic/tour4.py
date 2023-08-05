from zope.i18nmessageid import MessageFactory

from collective.amberjack.plonetour.basic.tour2 import go_to_folder

_ = MessageFactory('collective.amberjack.plonetour')
PMF = MessageFactory('plone')


welcome = go_to_folder.copy()
welcome['title'] = _(u"Add and publish an Event")
welcome['text'] = _(u"In this tutorial, you'll create a new Event and publish it on your Plone-powered website.")

create_it = {
    'url': u'/myfolder',
    'xpath': u'',
    'xcontent': u'',
    'title': _(u"Create a Event"),
    'text': _("Events are useful for posting announcements about upcoming events. Events function much like a page, with additional fields for adding information about an event."),
    'steps': ({'description': _(u"Click the [Add new...] drop-down menu."),
               'idStep': u'menu_add-new',
               'selector': u'',
               'text': u''},
              {'description': _(u"Select [Event] from the menu."),
               'idStep': u'new_event',
               'selector': u'',
               'text': u''},
             )}

fill_out_the_fields = {
    'url': u'/myfolder/portal_factory/Event',
    'xpath': u'',
    'xcontent': u'',
    'title': _(u"Fill out the fields"),
    'text': _(u"Now that you selected the Event content type, you need to supply some information about it."),
    'steps': ({'description': _(u"Provide a [Title]: My Event."),
               'idStep': u'form_title',
               'selector': u'',
               'text': u'My Event'},
              {'description': _(u"Provide a [Description] for your Event. <br />The description will appear in site searches and in summary listings of events on your site."),
               'idStep': u'form_description',
               'selector': u'',
               'text': _(u'The description of My Event')},
              {'description': _(u"Provide an [Event Location]. The location is the physical location of the event. You can describe the address or provide directions in the Body Text field."),
               'idStep': u'form_location',
               'selector': u'',
               'text': _(u'Location of Event')},
              {'description': _(u"Provide the event [Start and End] dates."),
               'idStep': u'',
               'selector': u'#fieldset-default .plone_jscalendar select',
               'text': u''},
              {'description': _(u"Put some content in the [Body Text] field. This is the best place to add directions to your event, information about what to expect, images, etc."),
               'idStep': u'form_text',
               'selector': u'',
               'text': _(u'Information about your event.')},
              {'description': _(u"Manage the type: open the [Categorization] tab."),
               'idStep': u'button',
               'selector': u'a[href="#fieldsetlegend-categorization"]',
               'text': u''},
              {'description': _(u"then provide an [Event Type] by typing in the New Categories field. Typical event types include: Fundraiser, Auction, Sale, Concert, Performance, etc. Once you have added a new event type, it will appear for selection in the Existing Categories field the next time you create an event."),
               'idStep': u'',
               'selector': u'#subject_keywords',
               'text': u''},
               {'description': _(u"Provide contact information in the remaining fields."),
               'idStep': u'',
               'selector': u'',
               'text': u''},
              {'description': _(u"Click [Save] to finish."),
               'idStep': u'form_save',
               'selector': u'',
               'text': u''},
             )}

publish_it = {
    'url': u'/myfolder/my-event',
    'xpath': u'',
    'xcontent': u'',
    'title': _(u"Publish the event"),
    'text': _(u"In order for anonymous site visitors to see your event you must publish it first. Publishing also makes your event available in the Upcoming Events portlet and Events folder."),
    'steps': ({'description': _(u"Click the [State] drop-down menu."),
               'idStep': u'menu_state',
               'selector': u'',
               'text': u''},
              {'description': _(u"Select [Publish] from the menu."),
               'idStep': u'content_publish',
               'selector': u'',
               'text': u''},
             )}

all_done = {
    'url': u'/myfolder/my-event',
    'xpath': u'#plone-contentmenu-workflow dt a span.state-published',
    'xcontent': PMF(u"Published"),
    'title': _(u"All done!"),
    'text': _(u"You now have a published event in your folder."),
    'steps': ()}

ajTour = {'tourId': u'basic04_add_and_publish_an_event',
          'title': _(u"Add and publish an Event"),
          'steps': (welcome,
                    create_it,
                    fill_out_the_fields,
                    publish_it,
                    all_done,
                   )}

