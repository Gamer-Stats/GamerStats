from django.shortcuts import render
from core.models import News, SetupSettings, Wiki


def index(request):
    ss = SetupSettings.objects.all()[:9]
    wikis = Wiki.objects.all()[:3]
    news = News.objects.all()[:7]
    template_name = "index.html"
    context = {"ss": ss, "wikis": wikis, "news": news}
    return render(request, template_name, context)
