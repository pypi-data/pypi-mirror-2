from zope.i18nmessageid import MessageFactory

from collective.amberjack.plonetour.basic.tour2 import go_to_folder

_ = MessageFactory('collective.amberjack.plonetour')
PMF = MessageFactory('plone')


welcome = go_to_folder.copy()
welcome['title'] = _(u"Add and publish a News Item")
welcome['text'] = _(u"In this tutorial, you'll create a new News Item and publish it on your Plone-powered website.")

create_it = {
    'url': u'/myfolder',
    'xpath': u'',
    'xcontent': u'',
    'title': _(u"Create a News Item"),
    'text': u'',
    'steps': ({'description': _(u"Click the [Add new...] drop-down menu."),
               'idStep': u'menu_add-new',
               'selector': u'',
               'text': u''},
              {'description': _(u"Select [News Item] from the menu."),
               'idStep': u'new_news',
               'selector': u'',
               'text': u''},
             )}

fill_out_the_fields = {
    'url': u'/myfolder/portal_factory/News Item',
    'xpath': u'',
    'xcontent': u'',
    'title': _(u"Fill out the fields"),
    'text': _(u"Now that you selected the News Item content type, you need to supply some information about it."),
    'steps': ({'description': _(u"Provide a [Title]: [My News]."),
               'idStep': u'form_title',
               'selector': u'',
               'text': u'My News'},
              {'description': _(u"Provide a [Description] for your News Item. <br />The description will appear in site searches and in summary listings of news on your site."),
               'idStep': u'form_description',
               'selector': u'',
               'text': _(u'The description of My News item')},
              {'description': _(u"Put some content in the [Body Text] field."),
               'idStep': u'form_text',
               'selector': u'',
               'text': _(u'The News item')},
              {'description': _(u"Notice the [Image] field at the bottom of the page. You can attach an image to a News Item which will appear in summary listings of News Items. You can also caption the image."),
               'idStep': u'',
               'selector': u'',
               'text': u''},
              {'description': _(u"Click [Save] to finish."),
               'idStep': u'form_save',
               'selector': u'',
               'text': u''},
             )}

publish_it = {
    'url': u'/myfolder/my-news',
    'xpath': u'',
    'xcontent': u'',
    'title': _(u"Publish the news item"),
    'text': _(u"In order for anonymous site visitors to see your news item you must publish it first. Publishing also makes your news item available in the News portlet and News folder."),
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
    'url': u'/myfolder/my-news',
    'xpath': u'#plone-contentmenu-workflow dt a span.state-published',
    'xcontent': PMF(u"Published"),
    'title': _(u"All done!"),
    'text': _(u"You now have a published news item in your folder."),
    'steps': ()}

ajTour = {'tourId': u'basic03_add_and_publish_a_news_item',
          'title': _(u"Add and publish a News Item"),
          'steps': (welcome,
                    create_it,
                    fill_out_the_fields,
                    publish_it,
                    all_done,
                   )}

