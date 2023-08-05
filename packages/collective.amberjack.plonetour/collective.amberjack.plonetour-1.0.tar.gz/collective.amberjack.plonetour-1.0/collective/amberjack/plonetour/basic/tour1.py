from zope.i18nmessageid import MessageFactory

from collective.amberjack.core.validators import isManager
from collective.amberjack.plonetour.basic.common import isNotFolderCreated

_ = MessageFactory('collective.amberjack.plonetour')
PMF = MessageFactory('plone')


add_folder = {
    'validators': (isManager, isNotFolderCreated,),
    'url': u'/',
           'xpath': u'',
           'xcontent': u'',
           'title': _(u"Create a new folder"),
           'text': _(u"Folders are one of the most fundamental content types in Plone. You can use a folder to organize your documents much like you already do on your desktop computer. You can also use folders to create new sections of your website."),
           'steps': ({'description': _(u"If you don't want to perform the indicated step yourself, just click the '>>' link and it will be automatically done by your browser."),
                      'idStep': u'',
                      'selector': u'',
                      'text': u''},
                     {'description': _(u"Click the [Add new...] drop-down menu."),
                      'idStep': u'menu_add-new',
                      'selector': u'',
                      'text': u''},
                     {'description': _(u"Select [Folder] from the menu."),
                      'idStep': u'new_folder',
                      'selector': u'',
                      'text': u''})}

fill_out_the_fields = {'url': u'aj_any_url', #'url': u'/portal_factory/Folder/folder',
              'xpath': u'',
              'xcontent': u'',
              'title': _(u"Fill out the fields"),
              'text': u'',
              'steps': ({'description': _(u"In the [Title] field, type 'MyFolder'."),
                         'idStep': u'form_title',
                         'selector': u'',
                         'text': u'MyFolder'},
                        {'description': _(u"In the [Description] field, type 'This folder will be used to contain sample content as I work through each tutorial.'."),
                         'idStep': u'form_description',
                         'selector': u'',
                         'text': _("This folder will be used to contain sample content as I work through each tutorial.")},
                        {'description': _(u"Now click the [Save] button at the bottom of the page to save your new folder."),
                         'idStep': u'form_save',
                         'selector': u'',
                         'text': u''})}

publish_folder = {'url': u'/myfolder',
                 'xpath': u'',
                 'xcontent': u'',
                 'title': _(u"Publish the folder"),
                 'text' : _(u"You have now created a Folder for your Plone website. Before this folder can be viewed by anonymous site visitors, you must publish it."),
                 'steps': ({'description': _(u"Click the [State] drop-down menu."),
                            'idStep': u'menu_state',
                            'selector': u'',
                            'text': u''},
                           {'description': _(u"Select [Publish] from the menu."),
                            'idStep': u'content_publish',
                            'selector': u'',
                            'text': u''})}

all_done = {'url': u'/myfolder',
                 'xpath': u"#plone-contentmenu-workflow dt a span.state-published",
                 'xcontent': PMF(u"Published"),
                 'title': _(u"All done!"),
                 'text': _(u"You now have a folder on your Plone website. You will use this folder in the remaining tutorials as a place to put sample content. <strong>Do not delete or rename it</strong> until you are finished with all the tutorials!"),
                 'steps': ()}

ajTour = {'tourId': u'basic01_add_and_publish_a_folder',
          'title': _(u'Add and publish a Folder'),
          'steps': (add_folder,
                    fill_out_the_fields,
                    publish_folder,
                    all_done,
                   )}

