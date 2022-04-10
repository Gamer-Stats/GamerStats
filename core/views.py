from django.shortcuts import render
from core.models import SetupSettings, Wiki


def index(request):
    ss = SetupSettings.objects.all()[:9]
    wikis = Wiki.objects.all()[:3]
    template_name = "index.html"
    context = {"ss": ss, "wikis": wikis}
    return render(request, template_name, context)
