from zope.interface import Interface
from wc.pageturner import mf as _
from zope import schema

class Layer(Interface):
    """
    layer class
    """
    
class IPageTurnerSettings(Interface):
    
    
    width = schema.Int(
        title=_(u'label_width_title_pageturner', default=u"Width"),
        description=_(u"label_width_description_pageturn", 
            default=u"The fixed width of the Page Viewer."),
        default=650,
        required=True
    )
    
    height = schema.Int(
        title=_(u'label_height_title_pageturner', default=u"Height"),
        description=_(u"label_height_description_pageturner", 
            default=u"The fixed height of the Page Viewer."),
        default=500,
        required=True
    )
    
    progressive_loading = schema.Bool(
        title=_(u'label_progressive_loading_pageturner', default=u'Progressive Loading'),
        description=_(u'label_progressive_loading_description_pageturner',
            default=u'Progressively load the PDF. Essential for very large PDF files.'),
        default=True
    )

    print_enabled = schema.Bool(
        title=_(u'label_print_enabled_pageturner', default=u'Print Enabled'),
        description=_(u'label_print_enabled_description_pageturner',
            default=u'Printer button enabled.'),
        default=True
    )
    
    full_screen_visible = schema.Bool(
        title=_(u'label_full_screen_visible_pageturner', default=u'Full Screen Visible'),
        description=_(u'label_full_screen_visible_description_pageturner',
            default=u'Full screen button visible.'),
        default=True
    )

    search_tools_visible = schema.Bool(
        title=_(u'label_search_tools_visible_pageturner', default=u'Search Tools Visible'),
        description=_(u'label_search_tools_visible_description_pageturner',
            default=u'Search tools button visible.'),
        default=True
    )
    
    cursor_tools_visible = schema.Bool(
        title=_(u'label_cursor_tools_visible_pageturner', default=u'Cursor Tools Visible'),
        description=_(u'label_cursor_tools_visible_description_pageturner',
            default=u'Cursor tools button visible.'),
        default=True
    )
    
    command_line_options = schema.TextLine(
        title=_(u'label_command_line_options_pageturner', default=u'Command Line Options'),
        description=_(u'description_command_line_options_pageturner', 
            default=u'It is possible that you need to provide extra options if there are errors while converting the PDF. '
                    u'This should be a comma seperated list of values(example "bitmap,bitmapfonts").'
                    u"""Some known helpful options are "poly2bitmap" for bitmap errors and "bitmapfonts" """
                    u"""for bitmap font errors."""
        ),
        default=u'',
        required=False
    )
    
class IUtils(Interface):
    
    def enabled():
        """
        return true is page turner is enabled for the object
        """