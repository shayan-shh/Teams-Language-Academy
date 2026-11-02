from django.contrib import admin
from . import models
from django.contrib.auth.models import User

# Register your models
admin.site.register(models.Category)
admin.site.register(models.Course)

# Create a custom inline for the Profile model
class ProfileInline(admin.StackedInline):
    model = models.Profile
    can_delete = False
    verbose_name_plural = 'Profile'

# Customize the User admin
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    inlines = [ProfileInline]  # Inline Profile model

# Unregister the default User model admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register Profile model separately if you want to see it independently in the admin
admin.site.register(models.Profile)
