from django.db import models
from django.utils.text import slugify


class SiteSettings(models.Model):
    """Singleton row holding every global text block and contact detail."""

    brand_name = models.CharField(max_length=80, default="Innove Couture")
    logo = models.ImageField(
        upload_to="brand/",
        blank=True,
        help_text="Optional. If empty the brand name is shown as a wordmark.",
    )
    announcement = models.CharField(
        max_length=200,
        default="Bespoke fittings by appointment — Lahore Atelier",
        help_text="The line that scrolls across the strip under the hero.",
    )
    tagline = models.CharField(max_length=160, default="Quietly extraordinary.")

    about_kicker = models.CharField(max_length=80, default="The Atelier")
    about_title = models.CharField(max_length=160, default="Cut by hand, finished by heart.")
    about_text = models.TextField(
        default=(
            "Innove Couture is a small atelier in Lahore devoted to slow, deliberate "
            "dressing. Every piece begins as a conversation — a silhouette drawn for one "
            "person, a fabric chosen by hand, a surface worked stitch by stitch until it "
            "feels inevitable. We make few things, and we make them properly."
        )
    )
    about_image = models.ImageField(upload_to="about/", blank=True)
    about_caption = models.CharField(max_length=120, blank=True, default="Hand embroidery, studio no. 2")

    stat_years_value = models.CharField(max_length=12, default="12")
    stat_years_label = models.CharField(max_length=60, default="Years of atelier practice")
    stat_pieces_value = models.CharField(max_length=12, default="400+")
    stat_pieces_label = models.CharField(max_length=60, default="Pieces hand-finished")
    stat_hands_value = models.CharField(max_length=12, default="06")
    stat_hands_label = models.CharField(max_length=60, default="Master artisans")

    contact_kicker = models.CharField(max_length=80, default="Enquiries")
    contact_title = models.CharField(max_length=160, default="Begin with a conversation.")
    contact_text = models.TextField(
        default=(
            "Bridal consultations are booked four to six months ahead. Write to us with "
            "your date, your city, and a sentence about what you are imagining."
        )
    )
    contact_email = models.EmailField(default="hello@innovecouture.com")
    contact_phone = models.CharField(max_length=40, default="+92 300 000 0000")
    contact_address = models.CharField(max_length=200, default="Studio 12, Gulberg III, Lahore")
    contact_hours = models.CharField(max_length=120, default="Mon – Sat, 11:00 – 19:00, by appointment")
    instagram_url = models.URLField(blank=True, default="https://instagram.com/")
    pinterest_url = models.URLField(blank=True)
    whatsapp_url = models.URLField(blank=True)

    footer_note = models.CharField(
        max_length=200,
        default="© Innove Couture. Every piece made to order in Lahore.",
    )

    class Meta:
        verbose_name = "Site content"
        verbose_name_plural = "Site content"

    def __str__(self):
        return self.brand_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class HeroSlide(models.Model):
    image = models.ImageField(upload_to="hero/")
    kicker = models.CharField(max_length=80, default="The Bridal Series — 2026")
    title = models.CharField(max_length=160, default="Something borrowed from the light.")
    subtitle = models.CharField(max_length=220, blank=True)
    cta_label = models.CharField(max_length=60, blank=True, default="Explore the collections")
    cta_url = models.CharField(max_length=200, blank=True, default="/#collections")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Hero slide"
        verbose_name_plural = "Hero slides"

    def __str__(self):
        return self.title


class Collection(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=90, unique=True, blank=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to="collections/")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Collection"
        verbose_name_plural = "Collections"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Look(models.Model):
    collection = models.ForeignKey(Collection, related_name="looks", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=110, unique=True, blank=True)
    label = models.CharField(max_length=80, blank=True, help_text="e.g. Bridal · Ivory")
    description = models.TextField(blank=True)
    detail = models.TextField(blank=True, help_text="Fabric and craft notes shown beside the image.")
    image = models.ImageField(upload_to="looks/")
    price_label = models.CharField(max_length=60, blank=True, default="Made to order")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Look"
        verbose_name_plural = "Looks"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class LookImage(models.Model):
    look = models.ForeignKey(Look, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="looks/gallery/")
    caption = models.CharField(max_length=120, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Look image"
        verbose_name_plural = "Look images"

    def __str__(self):
        return self.caption or f"Image {self.pk}"


class Craft(models.Model):
    title = models.CharField(max_length=80)
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Atelier step"
        verbose_name_plural = "Atelier steps"

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=80)
    detail = models.CharField(max_length=120, blank=True, help_text="e.g. Bride, 2025 — Lahore")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.author} — {self.quote[:40]}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    message = models.TextField()
    look = models.CharField(max_length=120, blank=True, help_text="Look referenced in the enquiry, if any.")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Enquiry"
        verbose_name_plural = "Enquiries"

    def __str__(self):
        return f"{self.name} — {self.created_at:%d %b %Y}"
