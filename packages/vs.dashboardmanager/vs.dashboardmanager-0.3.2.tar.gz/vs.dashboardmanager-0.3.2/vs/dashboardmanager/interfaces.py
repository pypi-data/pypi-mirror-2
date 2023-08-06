################################################################
# vs.dashboardmanager
# (C) 2010, Veit Schiele & Andreas Jung
# Published under the GNU Public Licence V 2 (GPL 2)
################################################################

from plone.app.portlets.interfaces import IDashboard
from plone.portlets.interfaces import IPortletManager
from zope.interface import Interface

class IPortletPageColumn(IDashboard):
    """Marker interface describing columns on a portlet page.
    """
class IDashboardManager(Interface):
    """Marker interface describing dashboardmanager object.
    """