from django.contrib import admin

from .models import Review, User, Retailer

admin.site.register(User)
admin.site.register(Retailer)
admin.site.register(Review)

# Register your models here.
