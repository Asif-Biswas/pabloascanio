from django.contrib import admin
from .models import Role, Charge, Region, District, Sector, State, Municipality, Church


admin.site.register(Role)
admin.site.register(Charge)
admin.site.register(Region)
admin.site.register(District)
admin.site.register(Sector)
admin.site.register(State)
admin.site.register(Municipality)
admin.site.register(Church)