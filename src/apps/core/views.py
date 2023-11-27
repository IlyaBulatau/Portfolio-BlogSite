from django.views import generic

from apps.posts.models import Post


class HomePageView(generic.ListView):
    model = Post
    template_name = "core/index.html"
    paginate_by = 2
    context_object_name = "posts"
    ordering = ("-created_on", )