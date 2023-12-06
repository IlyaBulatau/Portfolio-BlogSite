from typing import Any
from django.db import models
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy
from django.db.models import QuerySet, Q, Prefetch
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    SearchHeadline,
)

from .models import Post, IPView, Tag
from .forms import PostUpdateForm, PostCreateForm
from apps.users.mixins import OwnerPermissionMixin, LoginPermissionMixin
from apps.users.models import User


class PostCreateView(LoginPermissionMixin, generic.CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = "posts/post_create.html"
    success_url = reverse_lazy("core:index_view")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        # get Post instance with data from form
        self.object: Post = form.save(commit=False)

        # set author for the post
        self.object.author: User = self.request.user

        # get tag name and create it if not exists
        # set tag for the post
        tag_choise: str = form.data.get("tag")
        self.object.tag: Tag = Tag.objects.get_or_create(name=tag_choise)[0]

        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class PostUserListView(generic.ListView):
    model = Post
    template_name = "core/index.html"
    paginate_by = 5
    context_object_name = "posts"

    def get_queryset(self) -> QuerySet:
        if self.request.method == "GET":
            # get slug for url path
            user_slug: str = self.kwargs.get("slug")
            current_user = self.request.user

            # if user is not current
            # show only posts with is_show mark
            query_filter = (
                Q(author__slug=user_slug, is_show=True)
                if current_user.slug != user_slug
                else Q(author__slug=user_slug)
            )

            # get all posts by the slug
            queryset: QuerySet = (
                self.model.objects.filter(query_filter)
                .select_related("tag")
                .prefetch_related("views")
                .order_by("-created_on")
            )

        return queryset


class PostDetailView(generic.DetailView):
    model = Post
    context_object_name = "post"
    template_name = "posts/post_detail.html"

    def get_queryset(self) -> Post:
        post_slug: str = self.kwargs.get(self.slug_field)
        self.client_address: str = self._get_client_ip_address(self.request)

        self.object: Post = (
            Post.objects.filter(slug=post_slug)
            .select_related("author")
            .prefetch_related(
                Prefetch(
                    lookup="views",
                    queryset=IPView.objects.filter(address=self.client_address),
                    to_attr="view",
                ),
            )
            .first()
        )

        return self.object

    def get_object(self, queryset: QuerySet | None = ...) -> Post:
        return self.get_queryset()

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Add counting views of post
        """
        response = super().get(request, *args, **kwargs)

        # connect posts with ip address in database
        if not self.object.view:
            ip_view = IPView.objects.get_or_create(address=self.client_address)[0]
            self.object.views.add(ip_view)
        return response

    def _get_client_ip_address(self, request: HttpRequest) -> str:
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip_adress = x_forwarded_for.split(",")[-1].strip()
        else:
            ip_adress = request.META.get("REMOTE_ADDR")
        return ip_adress


class PostUpdateView(LoginPermissionMixin, OwnerPermissionMixin, generic.UpdateView):
    model = Post
    context_object_name = "post"
    form_class = PostUpdateForm
    template_name = "posts/post_update.html"

    def get_success_url(self) -> str:
        post: Post = self.object
        return reverse_lazy("posts:post_detail_view", args=(post.slug,))


class PostSearchView(generic.ListView):
    model = Post
    template_name = "posts/post_search.html"
    paginate_by = 5
    context_object_name = "posts"
    ordering = ("-created_on",)

    def get_queryset(self) -> QuerySet:
        query = self.request.GET.get("q")

        search_vector = SearchVector("content", "title", "tag__name")
        search_query = SearchQuery(query)
        search_rank = SearchRank(search_vector, search_query)
        search_headline = SearchHeadline(
            "content", search_query, min_words=60, max_words=61, max_fragments=2
        )

        return (
            Post.objects.annotate(search=search_vector, rank=search_rank)
            .annotate(headline=search_headline)
            .filter(search=search_query, is_show=True)
            .select_related("tag")
            .prefetch_related("views")
            .order_by("-rank")
        )


class PostDeleteView(LoginPermissionMixin, OwnerPermissionMixin, generic.DeleteView):
    model = Post
    template_name = "posts/post_delete.html"

    def get_success_url(self) -> str:
        post: Post = self.object
        return reverse_lazy("posts:post_user_view", args=(post.author.slug,))

    def get_queryset(self) -> QuerySet:
        post_slug: str = self.kwargs.get(self.slug_field)
        return Post.objects.filter(slug=post_slug).select_related("author")
