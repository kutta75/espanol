from django import template 
register = template.Library() 

@register.filter 
def to5c(value) : 
    value5 = value*5 
    return str(value5)

