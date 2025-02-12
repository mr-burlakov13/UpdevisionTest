from django.contrib import admin
from .models import Profile, Token


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'id_type')
    search_fields = ('user__username', 'id_type')


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'created', 'expires_at')
    search_fields = ('user__username', 'key')
