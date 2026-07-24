from django.shortcuts import render


from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "website/home.html"


class AboutView(TemplateView):
    template_name = "website/about.html"


class GalleryView(TemplateView):
    template_name = "website/gallery.html"


class ContactView(TemplateView):
    template_name = "website/contact.html"
