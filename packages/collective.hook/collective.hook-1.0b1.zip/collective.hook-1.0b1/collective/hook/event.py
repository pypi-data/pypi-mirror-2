from zope import event as zevent
from zope import interface
from zope import schema

class IHookEvent(interface.Interface):
    """HookEvent is the event triggerd by the hook.
    
    This event is triggered two times.
    
    First one is triggered before the call/code hooked.
    Next one is triggered after the call/code hooked.
    
    So you can place a handler and check before/after boolean attribute of
    the HookEvent instance
    """
    before = schema.Bool()
    after = schema.Bool()

class HookEvent(object):
    interface.implements(IHookEvent)

    def __init__(self):
        self.__before = True
        self.__after = False
        self.returned_value = None
        self.hooked_args = ()
        self.hooked_kwargs = {}
    
    def set_before(self, value):
        self.__before = bool(value)
        self.__after = not bool(value)

    def set_after(self, value):
        self.set_before(not bool(value))

    def get_after(self):
        return self.__after
    
    def get_before(self):
        return self.__before
    
    before = property(get_before, set_before)
    after = property(get_after, set_after)
    
