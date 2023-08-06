from django import template

register = template.Library()

@register.inclusion_tag('gallery/inclusion_tags/gallery_listing.html')
def gallery_listing(object_list):
    return {'object_list': object_list}

@register.inclusion_tag('gallery/inclusion_tags/gallery_detail.html')
def gallery_detail(obj):
    return {'object': obj}
