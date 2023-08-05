"""Product initialization.

$Id: __init__.py 115106 2010-04-12 09:15:14Z jcbrand $
"""
from Products.CMFCore import utils as CMFCoreUtils
import Products.CMFNotification.patches
import permissions

def initialize(context):
    import NotificationTool
    tools = (NotificationTool.NotificationTool, )
    CMFCoreUtils.ToolInit(NotificationTool.META_TYPE,
                          tools=tools,
                          icon='tool.gif').initialize(context)
