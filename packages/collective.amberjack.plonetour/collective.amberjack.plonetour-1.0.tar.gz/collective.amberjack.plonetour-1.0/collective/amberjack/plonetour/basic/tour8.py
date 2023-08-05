from tour2 import go_to_folder
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('collective.amberjack.plonetour')
PMF = MessageFactory('plone')


welcome = go_to_folder.copy()
welcome['title'] = _(u"Insert image on a page")
welcome['text'] = _(u"In this tutorial, you will revisit a page that you already created and learn how insert an image into that page.")

go_to_page = {
    'url': u'/myfolder',
    'xpath': u'',
    'xcontent': u'',
    'title': _(u"Open 'My Page'"),
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
    'title': _(u"Edit 'My Page'"),
    'text': _(u""),
    'steps': ({'description': _(u"Click the [Edit] tab to begin editing."),
               'idStep': u'contentview_edit',
               'selector': u'',
               'text': u''},
               )}

insert_image = {
    'url': u'/myfolder/my-page/edit',
    'xpath': u'',
    'xcontent': u'',
    'title': _(u"Insert an Image"),
    'text': u"Position your cursor in the [Body Text] field where you'd like to insert the image. Find or write a paragraph of text and place the cursor to the left of the first character in the paragraph.",
    'steps': ({'description': _(u"Now click the [Insert Image] icon in the editor toolbar (it looks like a tree)."),
               'idStep': u'tiny_button_click',
               'selector': u'',
               'text': u'image'},
               {'description': _(u"A pop-up window should appear. [Browse] to the location of an image you would like to insert. You should have at least one image already in MyFolder from a previous tutorial."),
               'idStep': u'',
               'selector': u'',
               'text': u''},
               {'description': _(u"Select the image by [clicking the radio button] next to it."),
               'idStep': u'',
               'selector': u'',
               'text': u''},
               {'description': _(u"Notice in the right-hand column of the pop-up window that a preview of the image you have selected appears."),
               'idStep': u'',
               'selector': u'',
               'text': u''},
               {'description': _(u"Choose [Left] alignment and a [Dimension] from the size menu. You can leave the [Image description] field as-is, or change the text if you wish. This is the 'alt' text for the image which aids in site accessibility, search, and indexing."),
               'idStep': u'iframe_select',
               'selector': u'#classes',
               'text': u'image-left'},
               {'description': _(u"Click [Insert] to complete the image insert."),
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
    'xpath': u'#content img',
    'xcontent': u'aj_xpath_exists',
    'title': _(u"All done!"),
    'text': _(u"You have now successfully inserted an image onto a page. You can edit the page again and insert more images, move existing images around, or change their alignment."),
    'steps': ()}

ajTour = {'tourId': u'basic08_insert_image_on_a_page',
          'title': _(u"Insert image on a page"),
          'steps': (welcome,
                    go_to_page,
                    edit_page,
                    insert_image,
                    all_done,
                   )}

