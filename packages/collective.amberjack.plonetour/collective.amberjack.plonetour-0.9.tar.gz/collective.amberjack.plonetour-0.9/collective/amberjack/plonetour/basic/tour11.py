from zope.i18nmessageid import MessageFactory

from collective.amberjack.plonetour.basic.tour2 import go_to_folder

_ = MessageFactory('collective.amberjack.plonetour')
PMF = MessageFactory('plone')


step_open_display_menu = {'description': _(u"Click the [Display] drop-down menu."),
                      'idStep': u'menu_display',
                      'selector': u'',
                      'text': u''}

welcome = go_to_folder.copy()
welcome['title'] = _(u"Using the Display menu")
welcome['text'] = _(u"A folder is a special content type in Plone because it can contain other content items. The way that those contained items will appear on the screen can be changed using the Display drop-down menu.")

change_in_summary_view = {'url': u'/myfolder',
              'xpath': u'',
              'xcontent': u'',
              'title': _(u"Use summary view"),
              'text': u'',
              'steps': (step_open_display_menu,
                        {'description': _(u"Select [Summary view]."),
                      'idStep': u'view_summary',
                      'selector': u'',
                      'text': u''}
                        )}

summary_view = {'url': u'/myfolder',
                 'xpath': u'body.template-folder_summary_view',
                 'xcontent': u'aj_xpath_exists',
                 'title': _(u"Summary view"),
                 'text' : _(u"Up to this point MyFolder has been using the Standard view. Standard view lists each item in the order it happens to be in the folder. Summary view is similar except that each entry is separated by a horizontal line and a Read More... link is automatically generated. If an item has an attached thumbnail image (such as a News Item) the image will also appear in the Summary view."),
                 'steps': (step_open_display_menu,
                           {'description': _(u"Select [Tabular view]."),
                          'idStep': u'view_tabular',
                          'selector': u'',
                          'text': u''})}

tabular_view = {'url': u'/myfolder',
                 'xpath': u'body.template-folder_tabular_view',
                 'xcontent': u'aj_xpath_exists',
                 'title': _(u"Tabular View"),
                 'text' : _(u"The Tabular view is similar to what you see in the Contents tab, except that you cannot perform administrative tasks such copy, cut, delete or reorder. The tabular view only displays the Title and Item Type to anonymous site visitors."),
                 'steps': (step_open_display_menu,
                           {'description': _(u"Select [content item as default view]."),
                          'idStep': u'default_page',
                          'selector': u'',
                          'text': u''})}

content_item_view = {'url': u'/myfolder/select_default_page',
              'xpath': u'',
              'xcontent': u'',
              'title': _(u"Select default page"),
              'text': _(u"So far you have seen the various ways that a folder in Plone can display its contents. However, in many cases you may wish to choose a single item such as a Page to act as the 'landing page' for the folder. This is common in cases where the folder is intended to be a subsection of the site."),
              'steps': ({'description': _(u"Select [My Page] as the default page for MyFolder."),
                      'idStep': u'radio',
                      'selector': u'#my-page',
                      'text': u'checked'},
                      {'description':_(u"Click the [Save] button to finish."),
                       'idStep':'form_save_default_page',
                       'selector':u'',
                       'text':u''
                       }
                        )}

all_done = {'url': u'/myfolder',
                 'xpath': u"body.template-document_view",
                 'xcontent': u'aj_xpath_exists',
                 'title': _(u"All done!"),
                 'text': _(u"In this tutorial you have explored some of the ways that a folder can display its contents. On your own, try out the Thumbnail view by uploading several images to a folder. This view is used to create a simple photo gallery."),
                 'steps': ()}

ajTour = {'tourId': u'basic11_using_display_menu',
          'title': _(u"Using the Display menu"),
          'steps': (welcome,
                    change_in_summary_view,
                    summary_view,
                    tabular_view,
                    content_item_view,
                    all_done,
                   )}

