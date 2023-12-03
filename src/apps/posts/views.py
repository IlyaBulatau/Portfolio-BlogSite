from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy
from django.db.models import QuerySet

from .models import Post, IPView, Tag
from .forms import PostUpdateForm, PostCreateForm
from apps.users.mixins import UpdatePermissionMixin, LoginPermissionMixin
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
    ordering = ["-created_on"]

    def get_queryset(self) -> QuerySet:
        if self.request.method == "GET":
            # get slug for url path
            user_slug: str = self.kwargs.get("slug")

            # get all posts by the slug
            queryset: QuerySet = self.model.objects.filter(author__slug=user_slug).all()

            # if user is not current
            # show only posts with is_show mark
            if self.request.user.slug != user_slug:
                queryset: QuerySet = queryset.filter(is_show=True)

        return queryset


class PostDetailView(generic.DetailView):
    model = Post
    context_object_name = "post"
    template_name = "posts/post_detail.html"

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Add counting views of post
        """
        client_ip_adress: str = self._get_client_ip_address(request)

        # add new ip address if not exists
        ipview_obj: IPView = IPView.objects.get_or_create(address=client_ip_adress)[0]
        post_obj: Post = self.get_object()

        # connect posts with ip address in database
        ipview_obj.posts.add(post_obj)

        return super().get(request, *args, **kwargs)

    def _get_client_ip_address(self, request: HttpRequest) -> str:
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip_adress = x_forwarded_for.split(",")[-1].strip()
        else:
            ip_adress = request.META.get("REMOTE_ADDR")
        return ip_adress


class PostUpdateView(LoginPermissionMixin, UpdatePermissionMixin, generic.UpdateView):
    model = Post
    context_object_name = "post"
    form_class = PostUpdateForm
    template_name = "posts/post_update.html"

    def get_success_url(self) -> str:
        post: Post = self.object
        return reverse_lazy("posts:post_detail_view", args=(post.slug,))


class PostDeleteView(generic.DeleteView):
    ...
