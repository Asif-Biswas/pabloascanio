from django.contrib import admin
from .models import Role, Charge, Region, District, Sector, State, Municipality, Church, UserProfile

admin.site.register(Role)
admin.site.register(Charge)
admin.site.register(Region)
admin.site.register(District)
admin.site.register(Sector)
admin.site.register(State)
admin.site.register(Municipality)
admin.site.register(UserProfile)

class ChurchAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'district', 'sector', 'state', 'municipality', 'total_members', 'code')
    readonly_fields = ['total_members', 'category', 'code']

admin.site.register(Church, ChurchAdmin)