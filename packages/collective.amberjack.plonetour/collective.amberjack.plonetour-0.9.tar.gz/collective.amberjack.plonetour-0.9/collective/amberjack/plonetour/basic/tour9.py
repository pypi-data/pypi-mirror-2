from tour2 import go_to_folder
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('collective.amberjack.plonetour')
PMF = MessageFactory('plone')

welcome = go_to_folder.copy()
welcome['title'] = _(u"Create a File")
welcome['text'] = _(u"A File in Plone is any binary file such as a PDF, DOC, XLS, PPT, RTF, or other file type that you wish to upload to your site. You can also link to a file to allow your site visitors the chance to download the file.")

add_file = {
    'url': u'/myfolder',
    'xpath': u'',
    'xcontent': u'',
    'title': _(u"Add a new File to MyFolder"),
    'text': _(u""),
    'steps': ({'description': _(u"Click the [Add New...] drop-down menu and select File from the menu."),
               'idStep': u'menu_add-new',
               'selector': u'',
               'text': u''},
               {'description': _(u"Select [File] from the menu."),
               'idStep': u'new_file',
               'selector': u'',
               'text': u''},
             )}



choose_file = {
    'url': u'/myfolder/portal_factory/File',
    'xpath': u'',
    'xcontent': u'',
    'title': _(u"Choose a file"),
    'text': u'Simply provide a title, description, and select the file you wish to upload.',
    'steps': ({'description': _(u'Provide a [Title] (i.e. \\"My File.\\")'),
               'idStep': u'form_title',
               'selector': u'',
               'text': u'My File'},
               {'description': _(u"Provide a [Description]. The description will appear in site searches and in summary listings of files on your site."),
               'idStep': u'form_description',
               'selector': u'',
               'text': _(u'A description for this file')},
               {'description': _(u"Click the [Browse] button."),
               'idStep': u'',
               'selector': u'',
               'text': u''},
               {'description': _(u"Select a file from your desktop computer."),
               'idStep': u'',
               'selector': u'',
               'text': u''},
               {'description': _(u"Click [Save] to complete the upload."),
               'idStep': u'form_save',
               'selector': u'',
               'text': u''},     
             )}

link_to_file = {
    'url': u'aj_any_url',
    'xpath': u'',
    'xcontent': u'',
    'title': _(u"Link to the File"),
    'text': _(u"You now have a file on your Plone website. You should now create a link to the file from a page to allow a site visitor to download the file. Otherwise, a site visitor would have to know the web address for the file or happen to search for it."),
    'steps': ({'description': _(u"Navigate to [My Page]"),
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
    'steps': ({'description': _(u"Click the [Edit] tab."),
               'idStep': u'contentview_edit',
               'selector': u'',
               'text': u''},
               )}

insert_internal_link = {
    'url': u'/myfolder/my-page/edit',
    'xpath': u'',
    'xcontent': u'',
    'title': _(u"Insert an internal link"),
    'text': _(u"When linking to a file, you should indicate that the link will begin the download of a file and you should indicate the file type and size in the link text as well. For example you might say: Download this report [PDF 1.2 Mb]."),
    'steps': ({'description': _(u"Type some link text in the [Body Text] field of the page (i.e. Download this report)."),
               'idStep': u'',
               'selector': u'#archetypes-fieldname-text iframe',
               'text': u'Download this report [PDF 1.2 Mb]'},
               {'description': _(u"Now highlight the link text and click the [Internal Link] icon in the editor toolbar (it looks like a piece of chain link)."),
               'idStep': u'button_internal_link',
               'selector': u'',
               'text': u''},
               {'description': _(u"Use the [pop-up window] to browse to the location of the file you just uploaded."),
               'idStep': u'',
               'selector': u'',
               'text': u''},
               {'description': _(u"Select the file by [clicking the radio button] next to it."),
               'idStep': u'',
               'selector': u'',
               'text': u''},
               {'description': _(u"Click [OK] to create the hyperlink."),
               'idStep': u'button_dialog_ok',
               'selector': u'',
               'text': u''},
               {'description': _(u"Click [Save] to finish."),
               'idStep': u'form_save',
               'selector': u'',
               'text': u''},
             )}

all_done = {
    'url': u'/myfolder/my-page',
    'xpath': u'#content a.internal-link',
    'xcontent': u'aj_xpath_exists',
    'title': _(u"All done!"),
    'text': _(u"You now have a linked file on your Plone website. Try clicking the link to see what the download process looks like. Note that the browser settings of each site visitor will determine whether the file opens in an application or if the Save As dialog box appears. You cannot control this behavior from within Plone."),
    'steps': ()}

ajTour = {'tourId': u'basic09_upload_and_link_to_a_file',
          'title': _(u"Upload and link to a File"),
          'steps': (welcome,
                    add_file,
                    choose_file,
                    link_to_file,
                    edit_page,
                    insert_internal_link,
                    all_done,
                   )}

