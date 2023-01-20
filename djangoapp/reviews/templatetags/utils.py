from django import template
from django.db import models


register = template.Library()


@register.filter
def model_type(model: models.Model) -> str:
    return type(model).__name__
