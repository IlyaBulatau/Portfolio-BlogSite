from django.http import HttpRequest, HttpResponse
from django.views import generic

from .models import Post, IPView


class PostDetailView(generic.DetailView):
    model = Post
    context_object_name = "post"

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        client_ip_adress: str = self._get_client_ip_address(request)

        ipview_obj: IPView = IPView.objects.get_or_create(address=client_ip_adress)[0]
        post_obj: Post = self.get_object()

        print(ipview_obj.posts.add(post_obj))
        # post_obj.views.get_or_create(address=client_ip_adress)
        
        return super().get(request, *args, **kwargs)


    def _get_client_ip_address(self, request: HttpRequest) -> str:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_adress = x_forwarded_for.split(',')[-1].strip()
        else:
            ip_adress = request.META.get('REMOTE_ADDR')
        return ip_adress

class PostUpdateView(generic.UpdateView):
    ...


class PostDeleteView(generic.DeleteView):
    ...

