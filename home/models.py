from news.models import NewsPage
from profiles.models import GamePage, ProfilePage
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class HomePage(Page):
    body = RichTextField(blank=True)
    intro = RichTextField(blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('body', classname="full"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['news_posts'] = NewsPage.objects.live().order_by('-last_published_at')[:6]
        context['games'] = GamePage.objects.live()
        context['players'] = ProfilePage.objects.live().order_by('first_published_at')[:15]
        return context
