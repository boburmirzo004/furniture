from django.shortcuts import render

from shared.models import AboutUs


def home_page_view(request):
    return render(request, 'shared/home.html')


def contact_page_view(request):
    return render(request, 'shared/contact.html')

def about_us_page_view(request):
    context  = {
        "abouts":AboutUs.objects.all()
    }
    return render(request, 'shared/about-us.html',context=context)
