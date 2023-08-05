import logging
logger = logging.getLogger('inqbus.plone.fastmemberdata')

def initialize(context):
    """Initializer called when used as a Zope 2 product."""

    # Monkey patched ZODBMutablePropertyProvider.setMemberProperties, to fire an event on change MemberData onjects.
    from zope.event import notify
    from zope.lifecycleevent import ObjectModifiedEvent
    def patched_setPropertiesForUser(self, user, propertysheet):
        # fire a zope event to inform other components:
        notify(ObjectModifiedEvent(user))
        return self.orig_setPropertiesForUser(user, propertysheet)
    from Products.PlonePAS.plugins.property import ZODBMutablePropertyProvider
    ZODBMutablePropertyProvider.orig_setPropertiesForUser = ZODBMutablePropertyProvider.setPropertiesForUser
    ZODBMutablePropertyProvider.setPropertiesForUser = patched_setPropertiesForUser
    logger.info('Monkey patched ZODBMutablePropertyProvider.setPropertiesForUser, to fire an event on change MemberData onjects!')
