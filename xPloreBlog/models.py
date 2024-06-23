from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.db.models import Avg
from datetime import datetime
from django.conf import settings
from django.utils import timezone
from django.db.models import Q

# Create your models here.


class PostManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(subtitle__icontains=query) |
                         Q(slug__icontains=query)
                         )
            # distinct() is often necessary with Q lookups
            qs = qs.filter(or_lookup).distinct()
        return qs


class Project(models.Model):
    project_id = models.CharField(max_length=20)
    project_name = models.CharField(max_length=100)
    project_about = RichTextField()
    p_background = models.CharField(max_length=200, null=True)
    p_team = models.CharField(max_length=200, null=True)
    p_core_value = models.CharField(max_length=200, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='proj_created_by')
    created_on = models.DateField(default=timezone.now)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='proj_updated_by')
    updated_on = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.project_id} {self.project_name}"

    class Meta:
        verbose_name_plural = 'Projects'

# AUTHOR MODEL


class Author(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='auth_user', null=True, blank=True)
    auth_avatar = models.ImageField(
        default='default.jpg', upload_to='profile_images', null=True, blank=True)
    email = models.EmailField(max_length=50)
    auth_role = models.IntegerField(default=0)
    auth_code = models.CharField(max_length=5)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='auth_created_by')
    created_on = models.DateField(default=timezone.now)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='auth_updated_by')
    updated_on = models.DateField(auto_now=True)

    def full_name(self):
        user_rec = User.objects.get(id=self.user.id)
        first_name = user_rec.first_name
        last_name = user_rec.last_name
        return f"{first_name} {last_name}"

    def get_absolute_url(self):
        return f"/author/{self.id}/"

    def __str__(self):
        return self.full_name()

    class Meta:
        verbose_name_plural = 'Authors'


# Tag MODEL - many (tag) to many (post) relation
class Tag(models.Model):
    entity_type = models.CharField(max_length=50)
    tag_title = models.CharField(max_length=75)
    caption = models.CharField(max_length=150, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='tag_created_by')
    created_on = models.DateField(default=timezone.now)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='tag_updated_by')
    updated_on = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.tag_title} - {self.caption}"

    class Meta:
        verbose_name_plural = 'Tags'

# Tag MODEL - many (tag) to many (post) relation


class Category(models.Model):
    entity_type = models.CharField(max_length=50, default='Blog')
    name = models.CharField(max_length=75, null=True)
    description = models.CharField(max_length=150, null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='catg_created_by')
    created_on = models.DateField(default=timezone.now)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='catg_updated_by')
    updated_on = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = 'Categories'


class Status(models.Model):
    entity_type = models.CharField(max_length=50, default='Blog')
    name = models.CharField(max_length=75, null=True)
    description = models.CharField(max_length=150, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='s_created_by')
    created_on = models.DateField(default=timezone.now)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='s_updated_by')
    updated_on = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.description}"

    class Meta:
        verbose_name_plural = 'Statuses'


# POST MODEL - one (author) to many (post) relation


class Post(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=150)
    slug = models.SlugField(default='', unique=True, db_index=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='posts', default=1)
    status = models.ForeignKey(
        Status, on_delete=models.DO_NOTHING, related_name='statuses', default=1)
    excerpt = models.CharField(max_length=400)
    content = RichTextField()
    img_url = models.CharField(
        max_length=300, default='https://images.unsplash.com/photo-1714390000391-322d3dec6147?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxlZGl0b3JpYWwtZmVlZHw1NjJ8fHxlbnwwfHx8fHw%3D')
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, related_name='categories')
    tag = models.ManyToManyField(Tag)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='post_created_by')
    created_on = models.DateField(default=timezone.now)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='post_updated_by')
    updated_on = models.DateField(auto_now=True)

    objects = PostManager()

    def avg_post_comment(self):
        return self.cposts.aggregate(avg_rating=Avg('rating')).get('avg_rating', 0)

    def get_absolute_url(self):
        return f"/posts/{self.slug}/"

    def latest_post(self):
        date_format = "%Y-%m-%d"
        current_dt = datetime.strptime(str(datetime.now().date()), date_format)
        post_creation_dt = datetime.strptime(str(self.created_on), date_format)
        diff_in_days = current_dt - post_creation_dt
        return diff_in_days

    def __str__(self):
        return f"{self.title} {self.subtitle}"

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Posts'


# Post_Comment MODEL - one (post) to many (comment) relation
class PostComment(models.Model):
    comment = RichTextField()
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='cposts')
    reader = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='cuser', null=True)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='com_created_by', null=True)
    created_on = models.DateField(default=timezone.now)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='com_updated_by', null=True)
    updated_on = models.DateField(auto_now=True)

    def average_rating(self):
        return self.comment.aggregate(Avg('rating'))

    def __str__(self):
        return f"{self.id} {self.post.title} {self.comment} {self.reader} {self.updated_on}"

    class Meta:
        verbose_name_plural = 'Comments'


class Reply(models.Model):
    r_text = RichTextField()
    r_comment = models.ForeignKey(
        PostComment, on_delete=models.CASCADE, related_name='rcomments')
    reader = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ruser', null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='rep_created_by', null=True)
    created_on = models.DateField(default=timezone.now)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='rep_updated_by', null=True)
    updated_on = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.r_comment.id} {self.r_comment.post.title} {self.reader.first_name}-{self.reader.last_name} {self.updated_on}"

    class Meta:
        verbose_name_plural = 'Replies'
