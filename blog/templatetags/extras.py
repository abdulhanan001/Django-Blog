from django import template

register = template.Library()


@register.filter(name='get_val')
# yaha per dict main replyDict ay gi or (key) main comment.sno
def get_val(dict, key):
    return dict.get(key)
