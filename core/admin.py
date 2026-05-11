from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 0


class UserWithProfileAdmin(UserAdmin):
    inlines = (ProfileInline,)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'nickname', 'rating')
    search_fields = ('user__username', 'nickname')
    list_filter = ('rating',)
    raw_id_fields = ('user',)


admin.site.unregister(User)
admin.site.register(User, UserWithProfileAdmin)
