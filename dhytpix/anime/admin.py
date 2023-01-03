from django.contrib import admin
from .models import Anime, User
from django.contrib.auth.admin import UserAdmin


fields = list(UserAdmin.fieldsets)
fields.append(
    ("Historic", {'fields': ('historic_animes',)})
)
UserAdmin.fieldsets = tuple(fields)


# Register your models here.
admin.site.register(Anime)
admin.site.register(User, UserAdmin)
