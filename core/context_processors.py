from core.models import SiteNav


def site_nav(request):
    obj = SiteNav.objects.get(pk=1)
    return {"site_nav": obj}
