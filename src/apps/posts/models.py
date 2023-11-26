from django.db import models
from django.core.validators import MinLengthValidator

from apps.users.models import User
from . import constants as cons
from .choices import TAGS_CHOISE


class IPView(models.Model):
    """
    IP adress of the who user viewed certain post
    """
    address = models.GenericIPAddressField(
        db_index=True,
        unique=True,
        blank=False,
        null=False,
        )
    
    class Meta:
        db_table = "ip_views"
        verbose_name = "ip_view"
        verbose_name_plural = "ip_views"
        
    
    def _str__(self):
        return f"IP_ID: {self.pk}, ADDRESS: {self.address}"


class Tag(models.Model):
    """
    Tag of posts
    """
    name = models.CharField(choices=TAGS_CHOISE, unique=True)
    description = models.CharField(max_length=cons.TAG_LENGTH_MAX, blank=True, null=False)
    slug = models.SlugField(unique=True, db_index=True)

    class Meta:
        db_table = "tags"
        verbose_name = "tag"
        verbose_name_plural = "tags"
        default_permissions = ("delete", "change")
    
    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Posts
    """
    title = models.CharField(
        unique=True,
        null=False,
        blank=False,
        max_length=cons.TITLE_LENGTH_MAX,
        validators=[MinLengthValidator(cons.TITLE_LENGTH_MIN)],
        )
    content = models.TextField(
        blank=False,
        null=False,
        validators=[MinLengthValidator(cons.CONTENT_LENGTH_MIN)],
        )
    slug = models.SlugField(
        max_length=cons.SLUG_LENGTH_MAX,
        unique=True,
        blank=False,
        null=False,
        db_index=True
        )
    image = models.ImageField(upload_to="posts/", blank=True, null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now=True)

    tag = models.ForeignKey(
        Tag,
        related_name="posts",
        related_query_name="tag",
        on_delete=models.PROTECT,
        db_index=True
        )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="posts",
        related_query_name="author",
        db_index=True
        )
    views = models.ManyToManyField(
        IPView,
        db_table="post_view",
        related_name="posts",
        related_query_name="views",
        blank=False,
        default=0,
        db_index=True
        )

    class Meta:
        db_table = "posts"
        verbose_name = "post"
        verbose_name_plural = "posts"


    def __str__(self):
        return f"Post ID: {self.pk}, Author: {self.author.pk}, Tag: {self.tag.name}"


class Comment(models.Model):
    """
    Comment of certain post
    """
    content = models.CharField(
        max_length=cons.COMMENT_LENGTH_MAX,
        null=False,
        blank=False,
        )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="comments",
        related_query_name="author",
        )
    post = models.ForeignKey(
        Post,
        on_delete=models.PROTECT,
        db_index=True,
        related_name="comments",
        related_query_name="post"
        )   
    
    class Meta:
        db_table = "comments"
        verbose_name = "comment"
        verbose_name_plural = "comments"

    def __str__(self):
        return self.pk


class Like(models.Model):
    """
    Like of certain post
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="likes",
        related_query_name="author",
        )
    post = models.ForeignKey(
        Post,
        on_delete=models.PROTECT,
        db_index=True,
        related_name="likes",
        related_query_name="post"
        )

    class Meta:
        db_table = "likes"
        verbose_name = "like"
        verbose_name_plural = "likes"
