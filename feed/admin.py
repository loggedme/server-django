from django.contrib import admin

from feed.models import Post, PostImage, LikedPost, SavedPost, Comment, HashTag, HashTaggedPost


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'created_at', 'created_by')
    list_display_links = ('id', 'content', 'created_at', 'created_by')
    search_fields = ('id', 'content', 'created_at', 'created_by')
    list_filter = ('created_at', 'created_by')


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'image')
    list_display_links = ('id', 'post', 'image')
    search_fields = ('id', 'post', 'image')
    list_filter = ('post',)


@admin.register(LikedPost)
class LikedPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')
    list_display_links = ('user', 'post')
    search_fields = ('user', 'post')
    list_filter = ('user', 'post')


@admin.register(SavedPost)
class SavedPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')
    list_display_links = ('user', 'post')
    search_fields = ('user', 'post')
    list_filter = ('user', 'post')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'content', 'created_at', 'created_by')
    list_display_links = ('id', 'post', 'content', 'created_at', 'created_by')
    search_fields = ('id', 'post', 'content', 'created_at', 'created_by')
    list_filter = ('created_at', 'created_by')


@admin.register(HashTag)
class HashTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    list_filter = ('name',)


@admin.register(HashTaggedPost)
class HashTaggedPostAdmin(admin.ModelAdmin):
    list_display = ('post', 'hashtag')
    list_display_links = ('post', 'hashtag')
    search_fields = ('post', 'hashtag')
    list_filter = ('post', 'hashtag')
