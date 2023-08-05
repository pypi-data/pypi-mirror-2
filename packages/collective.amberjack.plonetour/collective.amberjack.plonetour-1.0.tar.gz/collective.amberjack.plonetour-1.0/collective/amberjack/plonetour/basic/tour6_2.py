from tour2 import go_to_folder
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('collective.amberjack.plonetour')
PMF = MessageFactory('plone')

welcome = go_to_folder.copy()
welcome['title'] = _(u"Create external links")
welcome['text'] = _(u"In this tutorial, you will revisit a page that you already created and learn how insert hyperlinks into the page.")

go_to_page = {
    'url': u'/myfolder',
    'xpath': u'',
    'xcontent': u'',
    'title': _(u"Edit an existing page"),
    'text': _(u""),
    'steps': ({'description': _(u"Navigate to [My Page] that you created from the previous tutorial."),
               'idStep': u'link',
               'selector': u'#portal-column-one a[href$="/myfolder/my-page"]',
               'text': u''},
             )}

edit_page = {
    'url': u'/myfolder/my-page',
    'xpath': u'',
    'xcontent': u'',
    'title': _(u"Edit an existing page"),
    'text': _(u""),
    'steps': ({'description': _(u"Click the [Edit] tab to begin editing."),
               'idStep': u'contentview_edit',
               'selector': u'',
               'text': u''},
               )}

insert_external_link = {
    'url': u'/myfolder/my-page/edit',
    'xpath': u'',
    'xcontent': u'',
    'title': _(u"Insert an external link"),
    'text': _(u"An external link is used to link to other webpages, documents or resources online. Find the external link icon in the toolbar before we continue (it looks like a tiny Earth)."),
    'steps': ({'description': _(u"Type the following text into the [Body Text] field: 'Visit Plone.Org'."),
               'idStep': u'form_text',
               'selector': u'',
               'text': u'Visit Plone.org'},
               {'description': _(u"Now highlight that text with your mouse pointer and click the [Link icon] in the toolbar. A pop-up window should now appear."),
               'idStep': u'tiny_button_click',
               'selector': u'',
               'text': u'link'},
               {'description': _(u"This pop-up window allows you to browse the content of your site. Notice the links in the left-hand column. Click on [External] to insert a web address."),
               'idStep': u'iframe_click',
               'selector': u'.configlets a:contains("External")',
               'text': u''},
               {'description': _(u"Notice the select box containing the familiar http:// prefix. In the empty text field type 'www.plone.org'."),
               'idStep': u'iframe_text',
               'selector': u'#externalurl',
               'text': u'www.plone.org'},
                {'description': _(u"Now click the [Preview button] to check the link. Preview lets you confirm that you have the correct webpage before you commit the link."),
               'idStep': u'iframe_click',
               'selector': u'#preview',
               'text': u''},
               {'description': _(u"Click [Insert] to create the hyperlink."),
               'idStep': u'iframe_click',
               'selector': u'#insert',
               'text': u''},
               {'description': _(u"Click [Save] to finish."),
               'idStep': u'form_save',
               'selector': u'',
               'text': u''},
             )}


all_done = {
    'url': u'/myfolder/my-page',
    'xpath': u'#content a.external-link',
    'xcontent': u'aj_xpath_exists',
    'title': _(u"All done!"),
    'text': _(u"You have now learned how to create a type of hyperlink in Plone: Internal for linking to items within you site."),
    'steps': ()}

ajTour = {'tourId': u'basic06_2_create_external_links',
          'title': _(u"Create external links"),
          'steps': (welcome,
                    go_to_page,
                    edit_page,
                    insert_external_link,
                    all_done,
                   )}

