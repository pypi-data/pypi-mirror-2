from zope.i18nmessageid import MessageFactory

from collective.amberjack.core.validators import isManager
from collective.amberjack.plonetour.basic.common import isFolderCreated

_ = MessageFactory('collective.amberjack.plonetour')
PMF = MessageFactory('plone')


go_to_folder = {
    'validators': (isManager, isFolderCreated,),
    'url': u'/',
    'xpath': u'',
    'xcontent': u'',
    'title': _(u"Add and publish a Page"),
    'text': _(u"In this tutorial, you'll create a new Page and publish it on your Plone-powered website."),
    'steps': ({'description': _(u"Navigate to the folder called [MyFolder] that you created in a previous tutorial."),
               'idStep': u'link',
               'selector': u'#portaltab-myfolder a',
               'text': u''},
             )}

welcome = go_to_folder.copy()

create_it = {
    'url': u'/myfolder',
    'xpath': u'',
    'xcontent': u'',
    'title': _(u"Add a Page"),
    'text': u'',
    'steps': ({'description': _(u"Click the [Add new...] drop-down menu."),
               'idStep': u'menu_add-new',
               'selector': u'',
               'text': u''},
              {'description': _(u"Select [Page] from the menu."),
               'idStep': u'new_document',
               'selector': u'',
               'text': u''},
             )}

fill_out_the_page_fields = {
    'url': u'/myfolder/portal_factory/Document',
    'xpath': u'',
    'xcontent': u'',
    'title': _(u"Fill out the fields"),
    'text': _(u"Now that you selected the Page content type, you need to supply some information about it."),
    'steps': ({'description': _(u"Provide a [Title]: My Page."),
               'idStep': u'form_title',
               'selector': u'',
               'text': u'My Page'},
              {'description': _(u"Provide a [Description]: This is my first Plone page."),
               'idStep': u'form_description',
               'selector': u'',
               'text': _(u"This is my first Plone page.")},
              {'description': _(u"Add some page content in the [Body Text] field (you can come back and edit this later)."),
               'idStep': u'form_text',
               'selector': u'',
               'text': _(u'This is the text of My Page')},
              {'description': _(u"[Save] the page."),
               'idStep': u'form_save',
               'selector': u'',
               'text': u''},
             )}

publish_it = {
    'url': u'/myfolder/my-page',
    'xpath': u'',
    'xcontent': u'',
    'title': _(u"Publish the page"),
    'text': _(u"You have now created a Page for your Plone website. Before this page can be viewed by anonymous site visitors, you must publish it. Publishing also makes your page available in the Navigation portlet."),
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
    'url': u'/myfolder/my-page',
    'xpath': u'#plone-contentmenu-workflow dt a span.state-published',
    'xcontent': PMF(u"Published"),
    'title': _(u"All done!"),
    'text': _(u"You now have a published page in your folder."),
    'steps': ()}

ajTour = {'tourId': u'basic02_add_and_publish_a_page',
          'title': _(u"Add and publish a Page"),
          'steps': (welcome,
                    create_it,
                    fill_out_the_page_fields,
                    publish_it,
                    all_done,
                   )}

