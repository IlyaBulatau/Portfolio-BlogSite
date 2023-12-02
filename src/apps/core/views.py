from django.views import generic

from apps.posts.models import Post


class HomePageView(generic.ListView):
    model = Post
    queryset = Post.objects.filter(is_show=True)
    template_name = "core/index.html"
    paginate_by = 5
    context_object_name = "posts"
    ordering = ("-created_on",)
