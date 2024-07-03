from django.contrib import admin
from .models import Post,Category,Tag,Comment,Contact

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_published','view_count')
    list_display_links = ['name']
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')


admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)
admin.site.register(Contact)
# Register your models here.
