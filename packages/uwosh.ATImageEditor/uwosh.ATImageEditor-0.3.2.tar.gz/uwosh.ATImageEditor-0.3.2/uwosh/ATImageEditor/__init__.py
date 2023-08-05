from Products.CMFCore.utils import getToolByName

def uninstall(context):
    if not context.readDataFile('uwosh.ATImageEditor.txt'):
        return
    
    
    portal = context.getSite()
    catalog = getToolByName(portal, 'portal_catalog')

    images = catalog.searchResults(portal_type=["Image"])

    for image in images:
        image = image.getObject()

        if hasattr(image, 'unredostack'):
            delattr(image, 'unredostack')

        image._p_changed = 1
