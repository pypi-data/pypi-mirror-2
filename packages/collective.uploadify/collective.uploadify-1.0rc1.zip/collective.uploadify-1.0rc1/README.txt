Introduction
============

**Makes Plone File Uploads easy**

Multifileupload for Plone using uploadify_

.. _uploadify: http://www.uploadify.com

Usage
*****

After insall, go to http://your-plone-site/@@upload

NOTE
****

collective.uploadify contains **no** GenericSetup Profile, thus, it won't
appear in the quickinstaller tool.

If you want to smoothly integrate the upload funtionality to your site,
consider to add the following lines to your policy product in the
profiles/default/actions.xml::

    <?xml version="1.0"?>
    <object name="portal_actions" meta_type="Plone Actions Tool"
       xmlns:i18n="http://xml.zope.org/namespaces/i18n">

     <!-- *** OBJECT *** -->
     <object name="object" meta_type="CMF Action Category">
      <property name="title"></property>

      <!-- MULTI UPLOAD -->
      <object name="upload" meta_type="CMF Action" i18n:domain="wcms.skin.backend">
       <property name="title" i18n:translate="">Upload</property>
       <property name="description" i18n:translate="">Batch upload files.</property>
       <property name="url_expr">string:${object_url}/@@upload</property>
       <property name="icon_expr"></property>
       <property name="available_expr">
         python:portal.portal_workflow.getInfoFor(context, "review_state", default="") == "published" and plone_context_state.is_folderish()
       </property>
       <property name="permissions">
        <element value="Modify portal content"/>
       </property>
       <property name="visible">True</property>
      </object>
     </object>
    </object>

or simply go to the Zope Management Interface -> portal_actions -> object and
add a new CMF Action Category from the dropdown and configure it with the
following lines:

    - URL (Expression):
        string:${object_url}/@@upload

    - Condition (Expression):
        python:portal.portal_workflow.getInfoFor(context, "review_state", default="") == "published" and plone_context_state.is_folderish()


Configuration
*************

The following settings can be done in the site_properties.
(please use string properties):

  - ul_auto_upload -- true/false (default: false)

    *Set to true if you would like the files to be uploaded when they are
    selected.*

  - ul_allow_multi -- true/false (default: true)

    *Set to true if you want to allow multiple file uploads.*

  - ul_sim_upload_limit -- number 1-n (default: 4)

    *A limit to the number of simultaneous uploads you would like to allow.*

  - ul_queue_size_limit -- number 1-n (default: 999)

    *A limit to the number of files you can select to upload in one go.*

  - ul_size_limit -- size in bytes (default: empty)

    *A number representing the limit in bytes for each upload.*

  - ul_file_description -- text (default: empty)

    *The text that will appear in the file type drop down at the bottom of the
    browse dialog box.*

  - ul_file_extensions -- list of extensions (default: \*.\*;)

    *A list of file extensions you would like to allow for upload.  Format like
    \*.ext1;\*.ext2;\*.ext3. FileDesc is required when using this option.*

  - ul_button_text -- text (default: BROWSE)

    *The text you would like to appear on the default button.*

  - ul_button_image -- path to image (default: empty)

    *The path to the image you will be using for the browse button.
    NOTE: If you are using a **different sized button image** you have to set
    ul_height and ul_width otherwise your ul_button_image will be stretched to
    the defaults (110x30)*

  - ul_hide_button -- true/false (default: false)

    *Set to true if you want to hide the button image.*

  - ul_script_access -- always/sameDomain (default: sameDomain)

    *The access mode for scripts in the flash file.  If you are testing locally, set to `always`.*

  - ul_width -- number (default: 110)

    *The ul_width value which should be set when using a different sized
    ul_button_image*

  - ul_height -- number (default: 30)

    *The ul_height value which should be set when using a different sized
    ul_button_image*


Customization for specific BrowserLayer
***************************************

If you have your own skin installed which is based on it's own BrowserLayer
(by default IThemeSpecific) and want to customize the look and feel of
collective.uploadify's you could override the upload view and/or the upload
initialize callback view

 - Customize view template::

     <configure
         xmlns="http://namespaces.zope.org/zope"
         xmlns:browser="http://namespaces.zope.org/browser">

         ...

         <!-- Customize collective.uploadify upload template -->
         <browser:page
             for="collective.uploadify.browser.interfaces.IUploadingCapable"
             name="upload"
             template="templates/upload.pt"
             permission="cmf.ModifyPortalContent"
             layer=".interfaces.IThemeSpecific"
             />

     </configure>

 - Customize initialize template::

    from zope.i18n import translate
    from zope.component import getMultiAdapter
    from collective.uploadify.browser.upload import UploadInitalize
    from my.product import MyMessageFactory as _


    class MyCustomUploadInitalize(UploadInitalize):
        """ Initialize uploadify js
        """

        def upload_settings(self):

            portal_state = getMultiAdapter(
                (self.context, self.request), name="plone_portal_state")

            settings = super(MyCustomUploadInitalize, self).upload_settings()
            settings.update(dict(
                ul_height = 26,
                ul_width = 105,
                ul_button_text = translate(_('Choose images'), target_language= \
                                           self.request.get('LANGUAGE', 'de')),
                ul_button_image = portal_state.navigation_root_url() + \
                    '/button_upload.png',
            ))

            return settings

   Don't forget to register the new upload initialize view for your
   themespecific browserlayer by using::

     <configure
          xmlns="http://namespaces.zope.org/zope"
          xmlns:browser="http://namespaces.zope.org/browser">

        ...

         <browser:page
             for="*"
             name="upload_initialize"
             class=".uploadify.MyCustomUploadInitalize"
             permission="cmf.ModifyPortalContent"
             layer=".interfaces.IThemeSpecific"
             />

     </configure>
