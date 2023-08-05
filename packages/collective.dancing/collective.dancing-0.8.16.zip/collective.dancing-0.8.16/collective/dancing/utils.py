import zope.schema.vocabulary
import z3c.form.interfaces
import Acquisition

import collective.singing.async

def get_queue():
    """Get the job queue"""
    return collective.singing.async.get_queue('collective.dancing.jobs')

def get_request_container():
    site = zope.app.component.hooks.getSite()
    return site.aq_chain[-1]

def fix_request(wrapped, skip=1):
    return aq_append(wrapped, get_request_container(), skip)

def aq_append(wrapped, item, skip=0):
    """Return wrapped with an aq chain that includes `item` at the
    end.
    
      >>> class AQ(Acquisition.Explicit):
      ...     def __init__(self, name):
      ...         self.name = name
      ...     def __repr__(self):
      ...         return '<AQ %s>' % self.name

      >>> one, two, three = AQ('one'), AQ('two'), AQ('three')
      >>> one_of_two = one.__of__(two)
      >>> one_of_two.aq_chain
      [<AQ one>, <AQ two>]
      >>> aq_append(one_of_two, three).aq_chain
      [<AQ one>, <AQ two>, <AQ three>]
      >>> aq_append(one_of_two, three, skip=1).aq_chain
      [<AQ one>, <AQ three>]
    """
    value = item
    for item in tuple(reversed(wrapped.aq_chain))[skip:]:
        value = Acquisition.aq_base(item).__of__(value)
    return value

class AttributeToDictProxy(object):
    def __init__(self, wrapped, default=z3c.form.interfaces.NOVALUE):
        super(AttributeToDictProxy, self).__setattr__('wrapped', wrapped)
        super(AttributeToDictProxy, self).__setattr__('default', default)

    def __setitem__(self, name, value):
        self.wrapped[name] = value

    __setattr__ = __setitem__

    def __getattr__(self, name):
        return self.wrapped.get(name, self.default)

class LaxVocabulary(zope.schema.vocabulary.SimpleVocabulary):
    """This vocabulary treats values the same if they're equal.
    """
    def getTerm(self, value):
        same = [t for t in self if t.value == Acquisition.aq_base(value)]
        if same:
            return same[0]
        else:
            raise LookupError(value)
