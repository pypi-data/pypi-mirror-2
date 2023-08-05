from zope import event

from collective.hook.event import HookEvent

def hook(eventclass=HookEvent):
    """Decorator to make a method or function hook(able). 
    
    You can provide an optinal eventclass. Default is HookEvent 
    """

    def hook_decorator(func):

        def hooked(*args, **kwargs):
            eventinstance = eventclass()
            eventinstance.hooked_args = args
            eventinstance.hooked_kwargs = kwargs
            event.notify(eventinstance)

            value = func(*args, **kwargs)

            eventinstance.after = True
            eventinstance.returned_value = value
            event.notify(eventinstance)

            return value

        return hooked

    return hook_decorator
