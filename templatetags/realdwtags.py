from django import template
from utils.enroll_rate import enroll_rate
register = template.Library()

@register.simple_tag
def enroll_r(enroll):
    return enroll_rate(enroll)