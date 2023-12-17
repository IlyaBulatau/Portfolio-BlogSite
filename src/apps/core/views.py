from django.views import generic
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from apps.posts.models import Post


class HomePageView(generic.ListView):
    """
    View for main page site with set of all posts
    """

    model = Post
    queryset = (
        Post.objects.filter(is_show=True)
        .select_related("tag")
        .prefetch_related("views")
    )
    template_name = "core/index.html"
    paginate_by = 5
    context_object_name = "posts"
    ordering = ("-created_on",)


class ContactPageView(generic.TemplateView):
    """
    View for contacts page it contans informations
    about website author; him contacts, locations, and name
    """

    template_name = "core/contacts.html"
    extra_context = {
        "name": _("Ilya Bulatau"),
        "about": _(
            """
            Hi, I'm a Python developer with 2 years of experience. 
            I designed this site as my portfolio. 
            On this site you can write and publish your articles, 
            read articles written by other people. 
            You can also update your profile. 
            On this page you will find information on how to contact me.
            """
        ),
        "CV": settings.RESUME_PATH,
        "socials": [
            {
                "link": "https://t.me/ilbltv",
                "image": "https://img.shields.io/badge/Telegram--blue?labelColor=green",
            },
            {
                "link": "https://www.linkedin.com/in/ilya-bulatau-585133253",
                "image": "https://img.shields.io/badge/LinkedIn--blue?labelColor=green",
            },
            {
                "link": "https://github.com/IlyaBulatau",
                "image": "https://img.shields.io/badge/GitHub--blue?labelColor=green",
            },
        ],
        "apiKey": settings.YANDEX_API_KEY,
    }
