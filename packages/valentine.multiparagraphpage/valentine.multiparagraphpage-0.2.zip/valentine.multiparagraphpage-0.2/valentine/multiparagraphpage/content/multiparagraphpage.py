"""Definition of the MultiParagraphPage content type
"""

from zope.interface import implements, directlyProvides

from Products.CMFPlone.interfaces import INonStructuralFolder
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import newsitem
from Products.ATContentTypes.content import schemata

from valentine.multiparagraphpage import multiparagraphpageMessageFactory as _
from valentine.multiparagraphpage.interfaces import IMultiParagraphPage
from valentine.multiparagraphpage.config import PROJECTNAME

from valentine.multiparagraphfield import MultiParagraphField, MultiParagraphWidget

MultiParagraphPageSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
   MultiParagraphField(
       name='text',
       widget=MultiParagraphWidget(
           label='Text',
           label_msgid='multiparagraph_text_label',
           description_msgid='multiparagraph_text_description',
           i18n_domain='valentine.multiparagraphpage',
       ),
       searchable=True,
       default_output_type = 'text/x-html-safe',
   ),

))

MultiParagraphPageSchema.addField(schemata.relatedItemsField.copy())

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

MultiParagraphPageSchema['title'].storage = atapi.AnnotationStorage()
MultiParagraphPageSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    MultiParagraphPageSchema,
    folderish=False,
    moveDiscussion=False
)

class MultiParagraphPage(folder.ATFolder):
    """Page with a list of manageable paragraphs"""
    implements(IMultiParagraphPage, INonStructuralFolder)

    meta_type = "MultiParagraphPage"
    schema = MultiParagraphPageSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    
    def getContentType(self,fieldname=None):
        return 'text/x-html-safe'
    
atapi.registerType(MultiParagraphPage, PROJECTNAME)
