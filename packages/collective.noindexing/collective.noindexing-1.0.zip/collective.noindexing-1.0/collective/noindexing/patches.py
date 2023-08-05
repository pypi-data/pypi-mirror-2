import logging
from Products.CMFCore.CMFCatalogAware import CMFCatalogAware
from Products.Archetypes.CatalogMultiplex import CatalogMultiplex

logger = logging.getLogger(__name__)


def indexObject(self, *args, **kwargs):
    logger.info("Ignoring indexObject call.")


def unindexObject(self, *args, **kwargs):
    logger.info("Ignoring unindexObject call.")


def reindexObject(self, *args, **kwargs):
    logger.info("Ignoring reindexObject call.")

catalogMultiplexMethods = {}
catalogAwareMethods = {}


def apply():
    # Hook up the new methods.
    for module, container in ((CMFCatalogAware, catalogAwareMethods),
                              (CatalogMultiplex, catalogMultiplexMethods)):
        if not container:
            container.update({
                'index': module.indexObject,
                'reindex': module.reindexObject,
                'unindex': module.unindexObject,
            })
            module.indexObject = indexObject
            module.reindexObject = reindexObject
            module.unindexObject = unindexObject
            logger.info('patched %s', str(module.indexObject))
            logger.info('patched %s', str(module.reindexObject))
            logger.info('patched %s', str(module.unindexObject))


def unapply():
    # Hook up the old methods.
    for module, container in ((CMFCatalogAware, catalogAwareMethods),
                              (CatalogMultiplex, catalogMultiplexMethods)):
        if not container:
            continue
        module.indexObject = container['index']
        module.reindexObject = container['reindex']
        module.unindexObject = container['unindex']
        logger.info('unpatched %s', str(module.indexObject))
        logger.info('unpatched %s', str(module.reindexObject))
        logger.info('unpatched %s', str(module.unindexObject))
