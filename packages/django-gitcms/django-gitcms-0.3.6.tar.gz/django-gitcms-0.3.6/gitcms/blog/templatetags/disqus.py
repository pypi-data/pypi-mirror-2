from django import template
from django.template import Template, Context, Node, Variable
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
import settings

register = template.Library()

if hasattr(settings,'DISQUS_SHORTNAME'):
    @register.inclusion_tag('blog/disqus.html')
    def disqus_thread(post):
        return {
            'disqus_shortname' : settings.DISQUS_SHORTNAME,
            'unique_identifier' : post.slug,
        }
else:
    @register.simple_tag
    def disqus_thread(_):
        return ''
            
    
