# from django.shortcuts import render
# from core.models import SetupSettings
# from django import template
# from django.db.models import Q
# from django.shortcuts import render
# from django.http import HttpResponse


# register = template.Library()


# @register.filter
# def search():
#     if HttpResponse.method == "GET":
#         query = HttpResponse.GET.get("searched")
#         ss = SetupSettings.objects.filter(Q(title__icontains=query))

#     template_name = "searched.html"
#     context = {"ss": ss}
#     return render(HttpResponse, template_name, context)
