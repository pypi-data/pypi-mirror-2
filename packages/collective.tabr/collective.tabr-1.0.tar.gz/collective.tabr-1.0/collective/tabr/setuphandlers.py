from Products.CMFCore.utils import getToolByName

STYLES = (
    ('Tab', 'h2', 'content-tab'),
    ('Default Tab', 'h2', 'default-content-tab'),
    ('Pane Break', 'hr', 'pane-break'),
)

FCKTEMPLATE = """
<Style name="%s" element="%s">
  <Attribute name="class" value="%s" />
</Style>"""

def importVarious(context):
    # Only run step if a flag file is present
    log = context.getLogger('collective.tabr')
    if context.readDataFile('tabr_various.txt') is None:
        return
    
    site = context.getSite()
        
    kupu = getToolByName(site, 'kupu_library_tool', None)
    if kupu is not None:
        all_styles = kupu.getParagraphStyles()
        to_add = {}
        for title, tag, css in STYLES:
            to_add[css] = "%s|%s" % (title, tag)
        
        for style in all_styles:
            css_class = style.split('|')[-1]
            if css_class in to_add:
                del to_add[css_class]

        if to_add:
            all_styles += ['|'.join((title,tag,css)) for title, tag, css in STYLES if css in to_add]
            kupu.configure_kupu(parastyles = all_styles)
            log.info("kupu styles added")
    
    portal_props = getToolByName(site, 'portal_properties')
    fck_props = getattr(portal_props, 'fckeditor_properties', None)
    if fck_props is not None:
        all_styles = fck_props.getProperty('fck_menu_styles', None)
        for style in STYLES:
            all_styles += FCKTEMPLATE % style
        fck_props.manage_changeProperties(fck_menu_styles= all_styles)
        log.info("FCKEditor styles added")
        
    return 'Styles added'
    