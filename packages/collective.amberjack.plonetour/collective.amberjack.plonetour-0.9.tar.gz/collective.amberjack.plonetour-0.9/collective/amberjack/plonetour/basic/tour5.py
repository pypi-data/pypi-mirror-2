from tour2 import go_to_folder
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('collective.amberjack.plonetour')
PMF = MessageFactory('plone')

welcome = go_to_folder.copy()
welcome['title'] = _(u"Format a page using the visual editor")
welcome['text'] = _(u"In this tutorial, you will revisit a page that you already created and learn how to format content on the page.")

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
    'url': u'aj_any_url',
    'xpath': u'#contentview-edit a',
    'xcontent': PMF(u'Edit'),
    'title': _(u"Edit My Page'"),
    'text': _(u""),
    'steps': ({'description': _(u"Click the [Edit] tab to begin editing."),
               'idStep': u'contentview_edit',
               'selector': u'',
               'text': u''},
               )}


format_page = {
    'url': u'/myfolder/my-page/edit',
    'xpath': u'',
    'xcontent': u'',
    'title': _(u"Add and format page content"),
    'text': u'Now that you are editing your page, you can add content and formatting to it. You will learn how to apply bold, italics, text alignment, and paragraph styles to the page.',
    'steps': ({'description': _(u"Type the following text into the [Body Text] field: 'The quick brown fox jumps over the lazy dog.'"),
               'idStep': u'form_text',
               'selector': u'#archetypes-fieldname-text iframe',
               'text': _(u'The quick brown fox jumps over the lazy dog.')},
               {'description': _(u"Now highlight the phrase 'brown fox' with your mouse pointer and select the [Bold icon] from the formatting toolbar."),
               'idStep': u'button_bold',
               'selector': u'',
               'text': u''},
               {'description': _(u"Next, highlight the phrase 'lazy dog' with your mouse pointer and select the [Italics icon] from the formatting toolbar."),
               'idStep': u'button_italic',
               'selector': u'',
               'text': u''},
               {'description': _(u"To change text alignment, highlight the entire sentence and select any of the three [text alignment icons] (left, center, or right)."),
               'idStep': u'button_justify_center',
               'selector': u'',
               'text': u''},
               {'description': _(u"Now type the word 'Introduction' above your sentence. Highlight 'Introduction' and click the text formatting [drop-down menu] and select Subheading. Notice that the text you selected appears larger and bolder than Normal Paragraph text."),
               'idStep': u'',
               'selector': u'select',
               'text': u'h3|'},
               {'description': _(u"Type more text of your own choosing and experiment with the other text styles in the formatting menu."),
               'idStep': u'',
               'selector': u'',
               'text': u''},
               {'description': _(u"When you are all done, click the [Save] button at the bottom of the page."),
               'idStep': u'form_save',
               'selector': u'',
               'text': u''},     
             )}

all_done = {
    'url': u'/myfolder/my-page',
    'xpath': u'',
    'xcontent': u'',
    'title': _(u"All done!"),
    'text': _(u"This tutorial has been a brief introduction into the various ways you can format a page. Subsequent tutorials will teach you how to insert hyperlinks and images."),
    'steps': ()}

ajTour = {'tourId': u'basic05_format_a_page_using_the_visual_editor',
          'title': _(u"Format a page using the visual editor"),
          'steps': (welcome,
                    go_to_page,
                    edit_page,
                    format_page,
                    all_done
                   )}

