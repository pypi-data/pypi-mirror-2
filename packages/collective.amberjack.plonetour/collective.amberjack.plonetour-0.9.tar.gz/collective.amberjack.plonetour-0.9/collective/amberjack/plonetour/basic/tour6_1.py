from tour2 import go_to_folder
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('collective.amberjack.plonetour')
PMF = MessageFactory('plone')

welcome = go_to_folder.copy()
welcome['title'] = _(u"Create internal links")
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
    'title': _(u"Edit My Page'"),
    'text': _(u""),
    'steps': ({'description': _(u"Click the [Edit] tab to begin editing."),
               'idStep': u'contentview_edit',
               'selector': u'',
               'text': u''},
               )}

insert_internal_link = {
    'url': u'/myfolder/my-page/edit',
    'xpath': u'',
    'xcontent': u'',
    'title': _(u"Insert an internal link"),
    'text': _(u"An internal link is for linking to any page, news item, event, image, file or other content type within your Plone site. Look for the icon in the editing toolbar. It should look like a small piece of chain."),
    'steps': ({'description': _(u"Type the following text in the [Body Text] field 'Visit the Homepage'."),
               'idStep': u'form_text',
               'selector': u'#archetypes-fieldname-text iframe',
               'text': u'Visit the Homepage'},
               {'description': _(u"Now highlight that text with your mouse pointer and click the [Internal Link icon] in the toolbar. A pop-up window should now appear."),
               'idStep': u'button_internal_link',
               'selector': u'',
               'text': u''},
               {'description': _(u"This pop-up window allows you to browse the content of your site. Notice the links in the left-hand column. Click on [Home] to browse to the root directory of your site."),
               'idStep': u'link_to_home',
               'selector': u'',
               'text': u''},
                {'description': _(u"Find the page titled 'Welcome to Plone' and select the [radio button] next to it."),
               'idStep': u'',
               'selector': u'div[title="Congratulations! You have successfully installed Plone."] input[name="drawer-item-radio"]',
               'text': u''},
               {'description': _(u"Ignore the [link to anchor] menu in the right-hand column. Anchors will be covered in a future tutorial."),
               'idStep': u'',
               'selector': u'',
               'text': u''},
               {'description': _(u"Click [OK] to create the hyperlink."),
               'idStep': u'',
               'selector': u'#kupu-librarydrawer div.kupu-dialogbuttons button.kupu-dialog-button',
               'text': u''},
               {'description': _(u"Click [Save] to finish."),
               'idStep': u'form_save',
               'selector': u'',
               'text': u''},
             )}



test_link = {
    'url': u'/myfolder/my-page',
    'xpath': u'#content a.internal-link',
    'xcontent': u'aj_xpath_exists',
    'title': _(u"Test your link"),
    'text': _(u"Now that you have created the internal link and saved the page, try clicking on the link. You should arrive at the default 'Welcome to Plone' homepage."),
    'steps':  ({'description': _(u"[Click] your new 'Visit the Homepage' link. You should be taken directly to the homepage of your site."),
               'idStep': u'link',
               'selector': u'#content a.internal-link',
               'text': u''},
               )}


all_done = {
    'url': u'/front-page',
    'xpath': u'',
    'xcontent': u'',
    'title': _(u"All done!"),
    'text': _(u"You have now learned how to create a type of hyperlink in Plone: Internal for linking to items within you site."),
    'steps': ()}

ajTour = {'tourId': u'basic06_1_create_internal_links',
          'title': _(u"Create internal links"),
          'steps': (welcome,
                    go_to_page,
                    edit_page,
                    insert_internal_link,
                    test_link,
                    all_done,
                   )}

