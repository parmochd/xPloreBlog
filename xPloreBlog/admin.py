from django.contrib import admin
from .models import Project, Author, Tag, Post, PostComment, Reply, Category, Status

# Register your models here.


class Projectadmin(admin.ModelAdmin):
    list_display = ('project_id', 'project_name', 'created_on',)


class Authoradmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'email',)


class Tagadmin(admin.ModelAdmin):
    list_display = ('id', 'entity_type', 'tag_title', 'caption', )


class Statusadmin(admin.ModelAdmin):
    list_display = ('id', 'entity_type', 'name', 'description', )


class Categoryadmin(admin.ModelAdmin):
    list_display = ('id', 'entity_type', 'name', 'description', )


class Postadmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'subtitle', 'author', 'category',)
    prepopulated_fields = {'slug': ('title',), }
    list_filter = ('tag',)


class PostCommentadmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'reader', 'updated_on',)


class Replyadmin(admin.ModelAdmin):
    list_display = ('id', 'r_comment', 'reader', 'updated_on',)


admin.site.register(Project, Projectadmin)
admin.site.register(Author, Authoradmin)
admin.site.register(Tag, Tagadmin)
admin.site.register(Status, Statusadmin)
admin.site.register(Category, Categoryadmin)
admin.site.register(Post, Postadmin)
admin.site.register(PostComment, PostCommentadmin)
admin.site.register(Reply, Replyadmin)
