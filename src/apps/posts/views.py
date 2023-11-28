from django.http import HttpRequest, HttpResponse
from django.views import generic
from django.urls import reverse_lazy

from .models import Post, IPView
from .forms import PostUpdateForm


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
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_adress = x_forwarded_for.split(',')[-1].strip()
        else:
            ip_adress = request.META.get('REMOTE_ADDR')
        return ip_adress

class PostUpdateView(generic.UpdateView):
    model = Post
    context_object_name = "post"
    form_class = PostUpdateForm
    template_name = "posts/post_update.html"

    def get_success_url(self) -> str:
        post: Post = self.object
        return reverse_lazy("posts:post_detail_view", args=(post.slug, ))

class PostDeleteView(generic.DeleteView):
    ...

