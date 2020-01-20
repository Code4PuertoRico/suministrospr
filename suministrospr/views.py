from django.shortcuts import render


def base_layout(request):
    template = "base.html"
    return render(request, template)
