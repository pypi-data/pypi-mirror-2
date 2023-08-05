from logging import getLogger

from zope.component import adapts, queryUtility

from Products.CMFCore.Expression import Expression

from Products.GenericSetup.interfaces import ISetupEnviron
from Products.GenericSetup.utils import exportObjects
from Products.GenericSetup.utils import importObjects
from Products.GenericSetup.utils import XMLAdapterBase

from collective.jqganalytics.interfaces import IGoogleAnalyticsConfiguration



log = getLogger('collective.jqganalytics')

class GoogleAnalyticsConfigXMLAdapter(XMLAdapterBase):
    
    adapts(IGoogleAnalyticsConfiguration, ISetupEnviron)
    
    _LOGGER_ID = 'collective.jqganalytics'
    
    name = 'jqganalytics'
    
    __parameter_types = ['default','forced']
    
    def _exportNode(self):
        """ export the object as a DOM node """
        node = self._doc.createElement('configuration')
        node.setAttribute('account_id',str(self.context.account_id))
        self._exportVariables(node)
        self._logger.info('settings exported.')
        return node

    def _importNode(self, node):
        """ import the object from the DOM node """
        if self.environ.shouldPurge():
            self._purgeProperties()
        
        if node.hasAttribute('account_id'):
            self.context.account_id = node.getAttribute('account_id')
        
        self._importVariables(node)
        self._logger.info('settings imported.')
    
    def _purgeProperties(self):
        self.context.__init__()
    
    def _exportVariables(self, node):
        for variable in self.context.custom_variables:
            child = self._doc.createElement('variable')
            child.setAttribute('identifier',variable.id)
            child.setAttribute('enabled', str(variable.enabled))
            child.setAttribute('expression', variable.expression.text)
            child.setAttribute('name', variable.name.text)
            child.setAttribute('value', variable.value.text)
            child.setAttribute('scope', str(variable.scope))
            child.setAttribute('slot', str(variable.slot))
            node.appendChild(child)
    
    def _importVariables(self, node):
        log.info('importing variables')
        from collective.jqganalytics.variable import GoogleAnalyticsCustomVariable
        
        for child in node.childNodes:
            if child.nodeName != 'variable' or not child.getAttribute('identifier'):
                continue
            
            variable = None
            identifier = child.getAttribute('identifier')
            
            for v in self.context.custom_variables:
                if v.id == identifier:
                    variable = v
                    log.info('Variable %s found in context' % (str(identifier),))
                    break
            
            if child.getAttribute('remove').lower() in ('true','1','yes',):
                if not variable:
                    log.info('Remove of a non-existant variable')
                    continue
                self.context.custom_variables.remove(variable)
                log.info('Removing variable: %s' % (str(variable),))
                continue
            
            if not variable:
                log.info('Creating a new variable')
                variable = GoogleAnalyticsCustomVariable()
                variable.id = identifier
                self.context.custom_variables.append(variable)
            
            variable.enabled = child.getAttribute('enabled').lower() in ('true','1','yes',)
            variable.expression = Expression(child.getAttribute('expression'))
            variable.name = Expression(child.getAttribute('name'))
            variable.value = Expression(child.getAttribute('value'))
            try:
                variable.scope = int(child.getAttribute('scope'))
            except:
                variable.scope = 1
            
            try:
                variable.slot = int(child.getAttribute('slot'))
            except:
                variable.slot = 1
            
            

def importAnalyticsSettings(context):
    """ import settings for jQuery Google Analytics from an XML file """
    site = context.getSite()
    utility = queryUtility(IGoogleAnalyticsConfiguration, context=site)
    if utility is None:
        logger = context.getLogger('collective.jqganalytics')
        logger.info('Nothing to import.')
        return
    importObjects(utility, '', context)

def exportAnalyticsSettings(context):
    """ export settings for Query Google Analytics as an XML file """
    site = context.getSite()
    utility = queryUtility(IGoogleAnalyticsConfiguration, context=site)
    if utility is None:
        logger = context.getLogger('collective.jqganalytics')
        logger.info('Nothing to export.')
        return
    exportObjects(utility, '', context)