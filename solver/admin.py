from django.contrib import admin

from .models import Concept, Attribute, Equation

admin.site.register(Concept)
admin.site.register(Attribute) 
admin.site.register(Equation)
