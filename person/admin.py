from django.contrib import admin
# from .models import Musician,Album
from .models import Country,City,State,Person,Town

# Register your models here.
admin.site.register(Country)
admin.site.register(City)
admin.site.register(State)
admin.site.register(Town)
admin.site.register(Person)
# admin.site.register(Student)
