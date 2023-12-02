from django.http import HttpRequest, HttpResponse
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet


from .models import Post, IPView
from .forms import PostUpdateForm
from apps.users.mixins import UpdatePermissionMixin


class PostCreateView(generic.CreateView):
    ...


class PostUserListView(generic.ListView):
    model = Post
    template_name = "core/index.html"
    paginate_by = 5
    context_object_name = "posts"
    ordering = ["-created_on"]

    def get_queryset(self) -> QuerySet:
        if self.request.method == "GET":
            user_slug: str = self.kwargs.get("slug")
            queryset: QuerySet = self.model.objects.filter(author__slug=user_slug).all()

            # if user is not current
            if self.request.user.slug != user_slug:
                queryset: QuerySet = queryset.filter(is_show=True)
        
        return queryset



class PostDetailView(generic.DetailView):
    model = Post
    context_object_name = "post"
    template_name = "posts/post_detail.html"

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        client_ip_adress: str = self._get_client_ip_address(request)

        ipview_obj: IPView = IPView.objects.get_or_create(address=client_ip_adress)[0]
        post_obj: Post = self.get_object()

        ipview_obj.posts.add(post_obj)

        return super().get(request, *args, **kwargs)

    def _get_client_ip_address(self, request: HttpRequest) -> str:
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip_adress = x_forwarded_for.split(",")[-1].strip()
        else:
            ip_adress = request.META.get("REMOTE_ADDR")
        return ip_adress


class PostUpdateView(LoginRequiredMixin, UpdatePermissionMixin, generic.UpdateView):
    model = Post
    context_object_name = "post"
    form_class = PostUpdateForm
    template_name = "posts/post_update.html"

    def get_success_url(self) -> str:
        post: Post = self.object
        return reverse_lazy("posts:post_detail_view", args=(post.slug,))


class PostDeleteView(generic.DeleteView):
    ...
