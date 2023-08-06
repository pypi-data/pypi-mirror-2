import re

from django.template import Library, Node, TemplateSyntaxError, loader
from django.conf import settings

register = Library()

class SortableInlineNode(Node):
    def __init__(self, inlines):
        self.inlines = []
        for inline in inlines:
            m = re.search("(?P<prefix>\w+)(?P<order_field>\(\w+\))?", inline)
            try:
                prefix = m.group('prefix').lower()
            except:
                raise TemplateSyntaxError("Incorrect syntax for the prefixes passed to {% sortable_inlines %}")
            try:
                order_field = m.group('order_field')[1:-1] # Strip parentheses
            except:
                order_field = None
            self.inlines.append((prefix, order_field))

    def render(self, context):
        c = {"inlines": [(prefix, order_field) for (prefix, order_field) in self.inlines], "MEDIA_URL": settings.MEDIA_URL}
        return loader.render_to_string("adminboost/sortable_inlines.html", c)


@register.tag
def sortable_inlines(parser, token):
    """
        Syntax:
        
        {% sortable_inlines "<prefix1>(<order_field1>)" "<prefix2>(<order_field2>)" "prefix3" ... %}
        
        `prefix` is the form fielf prefix for the inline. This can be found in the `id` of the inline DIV with the `inline-group` class (e.g. <div class="inline-group" id="<prefix>-group">).
        `order_field` is the field in the inline model used for ordering (typically an IntegerField).
        
        e.g.:
        
        {% sortable_inlines "image_set(ordering)" "video_set" %}
        
        If no order field is given, then "order" is used by default.
    """
    bits = token.split_contents()[1:]
    if len(bits) < 1:
        raise TemplateSyntaxError("'sortable_inlines' statement requires at least one argument")
    try:
        bits = [c[1:-1] for c in bits]
    except IndexError:
        raise TemplateSyntaxError("Incorrect syntax for the prefixes passed to {% sortable_inlines %}. Try surrounding prefixes with double quotes")
    return SortableInlineNode(bits)
