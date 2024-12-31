from django.contrib import admin
from .models import Blog,Category,Sub_category,Wallpaper


admin.site.site_header = "AutoVista Admin"
admin.site.site_title = "AutoVista Admin Portal"
admin.site.index_title = "Welcome to AutoVista - Premium Automotive Wallpapers Portal"

# Register your models here.

class Blogadmin(admin.ModelAdmin):
    list_display = ('title','slug','author','image','created_at','updated_at')
    list_filter = ('title','slug','author','created_at')
    search_fields = ('title','slug','author')
    list_per_page = 15
    ordering = ('created_at',)
    
    
admin.site.register(Blog,Blogadmin)
admin.site.register(Category)
admin.site.register(Sub_category)
admin.site.register(Wallpaper)