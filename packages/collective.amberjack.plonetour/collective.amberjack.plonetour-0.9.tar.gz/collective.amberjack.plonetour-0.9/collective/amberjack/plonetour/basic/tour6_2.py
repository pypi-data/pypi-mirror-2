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
               {'description': _(u"Now highlight that text with your mouse pointer and click the [External Link icon] in the toolbar. A pop-up window should now appear."),
               'idStep': u'button_external_link',
               'selector': u'',
               'text': u''},
               {'description': _(u"Notice the field containing the familiar http:// prefix. After the second forward slash, type 'www.plone.org'. You should now see the complete web address which looks like this: http://www.plone.org."),
               'idStep': u'text',
               'selector': u'input.kupu-toolbox-st,input.kupu-linkdrawer-input',
               'text': u'http://www.plone.org'},
                {'description': _(u"Now click the [Preview button] to check the link. Preview lets you confirm that you have the correct webpage before you commit the link."),
               'idStep': u'preview',
               'selector': u'',
               'text': u''},
               {'description': _(u"Click [OK] to create the hyperlink."),
               'idStep': u'button',
               'selector': u'#kupu-linkdrawer button.kupu-dialog-button:contains("Ok")',
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

