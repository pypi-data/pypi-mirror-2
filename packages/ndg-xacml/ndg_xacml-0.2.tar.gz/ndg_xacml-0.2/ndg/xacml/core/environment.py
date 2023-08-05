"""NDG Security Environment type definition

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "24/02/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id: environment.py 7100 2010-06-25 15:12:02Z pjkersha $"
from ndg.xacml.core import TargetChildBase
from ndg.xacml.core.match import EnvironmentMatch


class Environment(TargetChildBase):
    """XACML Environment Target Policy element
    
    @cvar MATCH_TYPE: Sets the type for match attributes in this 
    TargetChildBase derived class
    @type MATCH_TYPE: ndg.xacml.core.match.EnvironmentMatch
    @cvar ELEMENT_LOCAL_NAME: XML element local name
    @type ELEMENT_LOCAL_NAME: string
    """
    MATCH_TYPE = EnvironmentMatch
    ELEMENT_LOCAL_NAME = 'Environment'
    
    __slots__ = ()
    
    @property
    def environmentMatches(self):
        """Convenience wrapper to base class method
        @return: list of matches
        @rtype: ndg.xacml.utils.TypedList 
        """
        return self.matches
