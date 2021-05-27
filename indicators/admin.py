from django.contrib import admin
from indicators.models import *


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('date_joined',)
    list_display = ('email', 'first_name')


class AdminDateModel(admin.ModelAdmin):
    readonly_fields = ('date',)


class LesProjets(admin.ModelAdmin):
    list_display = ('code', 'nom')


admin.site.register(User, UserAdmin)
admin.site.register(Projet, LesProjets)
