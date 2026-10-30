from urllib.parse import quote

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactForm
from .models import Collection, Craft, HeroSlide, Look, SiteSettings, Testimonial


def home(request):
    context = {
        "heroes": HeroSlide.objects.filter(is_active=True),
        "collections": Collection.objects.filter(is_active=True),
        "looks": Look.objects.filter(is_active=True, is_featured=True)[:4],
        "crafts": Craft.objects.filter(is_active=True),
        "testimonials": Testimonial.objects.filter(is_active=True),
    }
    return render(request, "core/home.html", context)


def collection_detail(request, slug):
    collection = get_object_or_404(Collection, slug=slug, is_active=True)
    context = {
        "collection": collection,
        "looks": collection.looks.filter(is_active=True),
        "collections": Collection.objects.filter(is_active=True),
    }
    return render(request, "core/collection.html", context)


def look_detail(request, slug):
    look = get_object_or_404(Look.objects.select_related("collection"), slug=slug, is_active=True)
    more = Look.objects.filter(is_active=True, collection=look.collection).exclude(pk=look.pk)[:3]
    return render(request, "core/look.html", {"look": look, "more": more})


def contact(request):
    initial = {}
    look_name = request.GET.get("look", "")
    if look_name:
        initial["message"] = f"I would like to enquire about the {look_name}."

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)
            enquiry.look = request.POST.get("look", "")[:120]
            enquiry.save()
            messages.success(request, "Thank you — your note is with the atelier. We reply within two working days.")
            if enquiry.look:
                return redirect(f"{request.path}?look={quote(enquiry.look)}#enquiry")
            return redirect(f"{request.path}#enquiry")
    else:
        form = ContactForm(initial=initial)

    return render(
        request,
        "core/contact.html",
        {"form": form, "look": look_name, "site": SiteSettings.load()},
    )
