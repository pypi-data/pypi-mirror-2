""" Checkbox widget
"""
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from Products.Archetypes.public import Schema
from Products.Archetypes.public import IntegerField
from Products.Archetypes.public import BooleanField
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import IntegerWidget
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import BooleanWidget

from eea.facetednavigation.widgets.widget import CountableWidget
from eea.facetednavigation import EEAMessageFactory as _


EditSchema = Schema((
    StringField('index',
        schemata="default",
        required=True,
        vocabulary_factory='eea.faceted.vocabularies.CatalogIndexes',
        widget=SelectionWidget(
            label='Catalog index',
            label_msgid='faceted_criteria_index',
            description='Catalog index to use for search',
            description_msgid='help_faceted_criteria_index',
            i18n_domain="eea"
        )
    ),
    StringField('vocabulary',
        schemata="default",
        vocabulary_factory='eea.faceted.vocabularies.PortalVocabularies',
        widget=SelectionWidget(
            label='Vocabulary',
            label_msgid='faceted_criteria_vocabulary',
            description='Vocabulary to use to render widget items',
            description_msgid='help_faceted_criteria_vocabulary',
            i18n_domain="eea"
        )
    ),
    StringField('catalog',
        schemata="default",
        vocabulary_factory='eea.faceted.vocabularies.UseCatalog',
        widget=SelectionWidget(
            format='select',
            label='Catalog',
            label_msgid='faceted_criteria_catalog',
            description=('Get unique values from catalog as an alternative '
                         'for vocabulary'),
            description_msgid='help_faceted_criteria_catalog',
            i18n_domain="eea"
        )
    ),
    IntegerField('maxitems',
        schemata="display",
        default=0,
        widget=IntegerWidget(
            label='Maximum items',
            label_msgid='faceted_criteria_maxitems',
            description='Number of items visible in widget',
            description_msgid='help_faceted_criteria_maxitems',
            i18n_domain="eea"
        )
    ),
    BooleanField('sortreversed',
        schemata="display",
        widget=BooleanWidget(
            label='Reverse options',
            label_msgid='faceted_criteria_reverse_options',
            description='Sort options reversed',
            description_msgid='help_faceted_criteria_reverse_options',
            i18n_domain="eea"
        )
    ),
    BooleanField('count',
        schemata="countable",
        widget=BooleanWidget(
            label='Count results',
            label_msgid='faceted_criteria_count',
            description='Display number of results near each option',
            description_msgid='help_faceted_criteria_count',
            i18n_domain="eea"
        )
    ),
    BooleanField('hidezerocount',
        schemata="countable",
        widget=BooleanWidget(
            label='Hide items with zero results',
            label_msgid='faceted_criteria_emptycounthide',
            description='This option works only if "count results" is enabled',
            description_msgid='help_faceted_criteria_criteria_emptycounthide',
            i18n_domain="eea"
        )
    ),
    StringField('default',
        schemata="default",
        widget=StringWidget(
            size=25,
            label='Default value',
            label_msgid='faceted_criteria_default',
            description='Default selected item',
            description_msgid='help_faceted_criteria_radio_default',
            i18n_domain="eea"
        )
    ),
))

class Widget(CountableWidget):
    """ Widget
    """
    # Widget properties
    widget_type = 'radio'
    widget_label = _('Radio')
    view_js = '++resource++eea.facetednavigation.widgets.radio.view.js'
    edit_js = '++resource++eea.facetednavigation.widgets.radio.edit.js'
    view_css = '++resource++eea.facetednavigation.widgets.radio.view.css'

    index = ViewPageTemplateFile('widget.pt')
    edit_schema = CountableWidget.edit_schema.copy() + EditSchema

    def query(self, form):
        """ Get value from form and return a catalog dict query
        """
        query = {}
        index = self.data.get('index', '')
        index = index.encode('utf-8', 'replace')
        if not index:
            return query

        if self.hidden:
            value = self.default
        else:
            value = form.get(self.data.getId(), '')
        if not value:
            return query

        if not isinstance(value, unicode):
            value = value.decode('utf-8')

        query[index] = value.encode('utf-8')
        return query
