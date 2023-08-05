from AccessControl import allow_module
from Products.CMFCore.utils import ToolInit

from Products.qPloneDropDownMenu.DropDownMenuTool import DropDownMenuTool
from Products.qPloneDropDownMenu.config import PROJECT_NAME

allow_module('Products.qPloneDropDownMenu.utils')

tools = (DropDownMenuTool,)
 
def initialize(context):
    ToolInit(PROJECT_NAME,
             tools=tools,
             icon='tool.gif').initialize(context)