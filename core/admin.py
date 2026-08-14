from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title" , "slug" ,"word_count", "created_at" , "updated_at")
    readonly_fields = ("created_at" , "updated_at")
    search_fields = ("title", "slug")
    list_filter = ("created_at",)
    
