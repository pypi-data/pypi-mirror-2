from Products.Five import BrowserView
from rt.vuvuzela import vuvuzelaMessageFactory as _
from zope.interface import implements, Interface

class IvuvuzelaView(Interface):
    """
    vuvuzela view interface
    """

    def play():
        """ test method"""


class vuvuzelaView(BrowserView):
    """
    vuvuzela browser view
    """
    implements(IvuvuzelaView)

    def play(self):
        """
        Play vuvuzela
        """
        return _(u'I play vuvuzela')
