from django.template import Library, Node, TemplateSyntaxError
from django.contrib.contenttypes.models import ContentType


register = Library()


class LoadObjectNode(Node):

    def __init__(self, app_label, model, pk, name, nodelist):
        self.app_label = app_label
        self.model = model
        self.pk = pk
        self.name = name
        self.nodelist = nodelist

    def __repr__(self):
        return "<LoadObjectNode>"

    def render(self, context):
        app_label = self.app_label.resolve(context)
        model = self.model.resolve(context)
        pk = self.pk.resolve(context)
        try:
            content_type = ContentType.objects.get(
                app_label=app_label, model=model)
        except ContentType.DoesNotExist:
            return ''
        else:
            klass = content_type.model_class()
            try:
                val = klass._default_manager.get(pk=pk)
            except (klass.DoesNotExist, klass.MultipleObjectsReturned):
                return ''
            else:
                context.push()
                context[self.name] = val
                output = self.nodelist.render(context)
                context.pop()
                return output


def do_load_object(parser, token):
    """
    Used get an object by content type app_name and model
    attributes and object primary key and inject it into context.
    
    Usage:
    {% load_object app_label model pk as name %}
    {{ varname }}
    {% endload_object %}
    
    Exceptionally usful in conjunction with render_object template tag
    http://www.djangosnippets.org/snippets/1745/
    """
    bits = list(token.split_contents())
    if len(bits) != 6 or bits[-2] != 'as':
        raise TemplateSyntaxError(
            "%r expected format is 'load_object app_label model pk as name'" %
            bits[0])
    app_label = parser.compile_filter(bits[1])
    model = parser.compile_filter(bits[2])
    pk = parser.compile_filter(bits[3])
    name = bits[5]
    nodelist = parser.parse(('endload_object', ))
    parser.delete_first_token()
    return LoadObjectNode(app_label, model, pk, name, nodelist)

do_load_object = register.tag('load_object', do_load_object)
