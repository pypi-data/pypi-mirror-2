from zope.component import getUtility
from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

# TODO: If you define any fields for the portlet configuration schema below
# do not forget to uncomment the following import
from zope import schema
from zope.formlib import form

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# TODO: If you require i18n translation for any of your schema fields below,
# uncomment the following to import your package MessageFactory
from fhkrems.portlet.youtubeplayer import YouTubePlayerPortletMessageFactory as _

from plone.i18n.normalizer.interfaces import IIDNormalizer


class IYouTubePlayerPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    # TODO: Add any zope.schema fields here to capture portlet configuration
    # information. Alternatively, if there are no settings, leave this as an
    # empty interface - see also notes around the add form and edit form
    # below.

    # some_field = schema.TextLine(title=_(u"Some field"),
    #                              description=_(u"A field to use"),
    #                              required=True)
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    # TODO: Add any zope.schema fields here to capture portlet configuration
    # information. Alternatively, if there are no settings, leave this as an
    # empty interface - see also notes around the add form and edit form
    # below.

    # some_field = schema.TextLine(title=_(u"Some field"),
    #                              description=_(u"A field to use"),
    #                              required=True)

    header = schema.TextLine(title=_(u"youtubeplayerportlet_header_label", default=u"Portlet header"),
                             description=_(u"youtubeplayerportlet_header_description", default=u"Title of the rendered portlet"),
                             required=True)





    url = schema.TextLine(title=_(u"youtubeplayerportlet_url_label", default=u"YouTube VideoID"),
                          description=_(u"youtubeplayerportlet_url_description", default=u"ID of the youtube video"),
                          required=True)

    width = schema.TextLine(title=_(u"youtubeplayerportlet_width_label", default=u"Width"),
                            description=_(u"youtubeplayerportlet_width_description", default=u"Set width of Player"),
                            required=True)

    height = schema.TextLine(title=_(u"youtubeplayerportlet_height_label", default=u"Height"),
                            description=_(u"youtubeplayerportlet_height_description", default=u"Set height of Player incl. 25px of controls"),
                             required=True)

    hl = schema.TextLine(title=_(u"youtubeplayerportlet_hl_label", default=u"Language"),
                         description=_(u"youtubeplayerportlet_hl_description", default=u"For more Information look here: http://code.google.com/apis/youtube/2.0/reference.html#Localized_Category_Lists"),
                         required=True)

    rel = schema.Bool(title=_(u"youtubeplayerportlet_rel_label", default=u"Relational Videos"),
                      description=_(u"youtubeplayerportlet_rel_description", default=u"Sets whether the player should load related videos once playback of the initial video starts."),
                      required=False,
                      default=False)

    fs = schema.Bool(title=_(u"youtubeplayerportlet_fs_label", default=u"Fullscreen"),
                     description=_(u"youtubeplayerportlet_fs_description", default=u"Setting to True enables the fullscreen button."),
                     required=False,
                     default=True)

    hd = schema.Bool(title=_(u"youtubeplayerportlet_hd_label", default=u"Enable HD-Video playback button"),
                           description=_(u"youtubeplayerportlet_hd_description", default=u"Enable the HD playback button. This button only has an effect if an HD version of the video os available."),
                           required=False,
                           default=True)

    autoplay = schema.Bool(title=_(u"youtubeplayerportlet_autoplay_label", default=u"Autoplay"),
                           description=_(u"youtubeplayerportlet_autoplay_description", default=u"Sets whether or not the initial video will autoplay when the player loads."),
                           required=False,
                           default=False)

    loop = schema.Bool(title=_(u"youtubeplayerportlet_loop_label", default=u"Loop"),
                           description=_(u"youtubeplayerportlet_loop_description", default=u"If the player is loading a single video, play the video again and again."),
                           required=False,
                           default=False)

    disablekb = schema.Bool(title=_(u"youtubeplayerportlet_disablekb_label", default=u"Disable Keyboard Controls"),
                           description=_(u"youtubeplayerportlet_disablekb_description", default=u"Disable player Keyboard controls"),
                           required=False,
                           default=False)

    showinfo = schema.Bool(title=_(u"youtubeplayerportlet_showinfo_label", default=u"Show Information"),
                           description=_(u"youtubeplayerportlet_showinfo_description", default=u"Setting to True causes the player to not display information like the video title and rating before the video starts playing."),
                           required=False,
                           default=True)








    footer = schema.TextLine(title=_(u"youtubeplayerportlet_footer_label", default=u"Portlet footer"),
                             description=_(u"youtubeplayerportlet_footer_description", default=u"Text to be shown in the footer"),
                             required=False)

    more_url = schema.ASCIILine(title=_(u"youtubeplayerportlet_moreurl_label", default=u"Details link"),
                                description=_(u"youtubeplayerportlet_moreurl_description", default=u"If given, the header and footer will link to this URL."),
                                required=False)

    omit_border = schema.Bool(title=_(u"youtubeplayerportlet_omitborder_label", default=u"Omit portlet border"),
                              description=_(u"youtubeplayerportlet_omitborder_description", default=u"Tick this box if you want to render the text above without the standard header, border or footer."),
                              required=True,
                              default=False)

    hide = schema.Bool(title=_(u"youtubeplayerportlet_hide_label", default=u"Hide portlet"),
                       description=_(u"youtubeplayerportlet_hide_description", default=u"Tick this box if you want to temporarily hide the portlet without losing your text."),
                       required=True,
                       default=False)

class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IYouTubePlayerPortlet)

    # TODO: Set default values for the configurable parameters here

    # some_field = u""

    # TODO: Add keyword parameters for configurable parameters here
    # def __init__(self, some_field=u""):
    #    self.some_field = some_field

    header = _(u"youtubeplayerportlet_title", default=u"YouTube Player Portlet")
    footer = u""
    more_url = ""
    url = u""
    hl = u""
    height = u""
    width = u""
    rel = False
    fs = False
    hd = True
    autoplay = False
    loop = False
    disablekb = False
    showinfo = False
    omit_border = False
    hide = False

    def __init__(self, header=u"", url=u"", hl=u"", height=u"", width=u"", rel=False, fs=False, hd=True,
                       omit_border=False, autoplay=False, loop=False, disablekb=False, showinfo=False, footer=u"", more_url='', hide=False):
        self.header = header
        self.url = url
        self.width = width
        self.height = height
        self.hl = hl
        self.rel = rel
        self.fs = fs
        self.hd = hd
        self.autoplay = autoplay
        self.loop = loop
        self.disablekb = disablekb
        self.showinfo = showinfo
        self.footer = footer
        self.more_url = more_url
        self.omit_border = omit_border
        self.hide = hide

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "YouTube Player Portlet"


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('youtubeplayerportlet.pt')

    @property
    def available(self):
        return not self.data.hide

    def css_class(self):
        """Generate a CSS class from the portlet header
        """
        header = self.data.header
        normalizer = getUtility(IIDNormalizer)
        return "portlet-googlemaps-%s" % normalizer.normalize(header)

    def has_link(self):
        return bool(self.data.more_url)

    def has_footer(self):
        return bool(self.data.footer)

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IYouTubePlayerPortlet)

    def create(self, data):
        return Assignment(**data)


# NOTE: If this portlet does not have any configurable parameters, you
# can use the next AddForm implementation instead of the previous.

# class AddForm(base.NullAddForm):
#     """Portlet add form.
#     """
#     def create(self):
#         return Assignment()


# NOTE: If this portlet does not have any configurable parameters, you
# can remove the EditForm class definition and delete the editview
# attribute from the <plone:portlet /> registration in configure.zcml


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IYouTubePlayerPortlet)
    label = _(u"title_edit_youtubeplayer_portlet", default=u"Edit YouTube Player portlet")
    description = _(u"description_youtubeplayer_portlet", default=u"A portlet which can display a simple YouTube Player.")
