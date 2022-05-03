from django.shortcuts import render


def home_view(request):
    title = "Homepage"
    message = "Welcome"

    return render(request, 'home/home.html', locals())
