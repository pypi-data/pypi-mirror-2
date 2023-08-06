from django.db.models.manager import Manager
from django.template import Context, Node, Variable
from django.template.loader import get_template

class BaseModelBlockNode (Node):
    def __init__(self, thing, resolved=True):
        """
        thing -- The thing (probably a model instance or a list of model 
                 instances) to be rendered as a block.
        resolved -- If True, then ``thing`` is a resolved value.  If False,
                    then thing is the name of a variable which, in context,
                    will contain the value of the thing.
        """
        self.thing = thing
        self.resolved = resolved
    
    def get_template_variable(self, thing, type_of_thing):
        """
        Return the name of the template variable that should be used to render
        the thing.  If the variable name does not resolve to a value, then a 
        default template will be used.
        """
        if isinstance(thing, (list, tuple)):
            template_variable = ''
        elif hasattr(thing, 'model') and thing:
            template_variable = '%s_%s_%s_template' % \
                (thing.model._meta.app_label, thing.model._meta.module_name, 
                 type_of_thing)
        elif hasattr(thing, '_meta') and thing:
            template_variable = '%s_%s_%s_template' % \
                (thing._meta.app_label, thing._meta.module_name, type_of_thing)
        else:
            template_variable = ''
        return template_variable
    
    def get_resolved_value(self, context):
        """
        Return a resolved version of the thing being rendered -- either a model
        instance or a list of such instances. Specifically, if the name of the
        value was passed to the node as a string, resolve the value w.r.t. the
        context. If the actual value was passed in, then just return the value. 
        """
        if not self.resolved:
            res_var = Variable(self.thing).resolve(context)
        else:
            res_var = self.thing
        return res_var
    
    def render(self, context):
        queryset = self.get_resolved_value(context)
        template_variable = self.get_template_variable(queryset, self.thing_type)
        template_name = context.get(template_variable,
                                    'model_blocks/object_%s.html' % self.thing_type)
        template = get_template(template_name)
        
        context.update(Context(self.get_context_data(queryset)))
        if 'title' not in context:
            context['title'] = None
        return template.render(context)


class ModelDetailNode (BaseModelBlockNode):
    
    thing_type = 'detail'
    
    def get_context_data(self, instance):
        """
        Calculate additional context data that will be used to render the thing.
        """
        fields = []
        for field in instance._meta.fields:
            name = field.name
            label = field.verbose_name
            value = getattr(instance, field.name)
            is_list = False
            is_direct = True
            model = instance._meta.module_name
            
            if value is not None:
                fields.append((
                    name, label, value, is_list, is_direct, model,
                ))
        
        for rel_obj, model in instance._meta.get_all_related_objects_with_model():
            name = rel_obj.get_accessor_name()
            label = name
            value = getattr(instance, name)
            is_list = isinstance(value, (list, tuple, Manager))
            is_direct = False
            
            if value is not None:
                fields.append((
                    name, label, value, is_list, is_direct, model,
                ))
        
        return {'model':instance._meta.module_name, 
                'instance':instance, 
                'fields':fields}


class ModelTeaserNode (ModelDetailNode):
    
    thing_type = 'teaser'


class ModelListNode (BaseModelBlockNode):
    
    thing_type = 'list'
    
    def get_context_data(self, queryset):
        if hasattr(queryset, 'model') and queryset.model:
            model = queryset.model._meta.module_name
        else:
            model = None
        
        return {'model':model, 'instance_list':queryset}
    

