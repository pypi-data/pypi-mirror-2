from django import template

register = template.Library()

INSERTER_VARNAME = 'INSERT_BLOCKS_CONTENT_LIST-%s'

ERR_MSG = (
    "You must use the 'render_insert_blocks' tag with '%(varname)s' as "
    "argument before you can use the 'insertblock' tag with '%(varname)s' as "
    "argument."
)

class InsertedContentList(list):
    def append(self, content):
        if not content in self:
            super(InsertedContentList, self).append(content)
    
    def render(self, delimiter='\n'):
        return delimiter.join([unicode(bit) for bit in self])


class RenderInsertBlocksNode(template.Node):
    def __init__(self, nodelist, name):
        self.nodelist = nodelist
        self.name = name
        
    def render(self, context):
        varname = INSERTER_VARNAME % self.name
        context[varname] = InsertedContentList()
        rendered_content = self.nodelist.render(context)
        rendered_insertion = context[varname].render()
        return ''.join([rendered_insertion, rendered_content])
    
@register.tag
def render_insert_blocks(parser, token):
    bits = token.split_contents()
    if len(bits) not in (1, 2):
        raise template.TemplateSyntaxError("render_insert_blocks requires one or no argument")
    bits.append('')
    name = bits[1]
    nodelist = parser.parse()
    return RenderInsertBlocksNode(nodelist, name)


class InsertBlockNode(template.Node):
    def __init__(self, nodelist, name):
        self.nodelist = nodelist
        self.name = name
        
    def render(self, context):
        varname = INSERTER_VARNAME % self.name
        assert varname in context, ERR_MSG % {'varname': varname}
        content = self.nodelist.render(context)
        context[varname].append(content)
        return ''

@register.tag
def insertblock(parser, token):
    bits = token.split_contents()
    if len(bits) not in (1, 2):
        raise template.TemplateSyntaxError("insertblocks requires one or no argument")
    bits.append('')
    name = bits[1]
    nodelist = parser.parse(('endinsertblock', 'endinsertblock %s' % name))
    parser.delete_first_token()
    return InsertBlockNode(nodelist, name)