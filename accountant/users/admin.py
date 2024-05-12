from django.contrib import admin
from .models import Profile, Token, PasswordResetCode

admin.site.register(Profile)
admin.site.register(Token)
admin.site.register(PasswordResetCode)

