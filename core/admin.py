from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Collection,
    ContactMessage,
    Craft,
    HeroSlide,
    Look,
    LookImage,
    SiteSettings,
    Testimonial,
)


def thumb(obj, field="image", height=64):
    image = getattr(obj, field, None)
    if not image:
        return "—"
    return format_html(
        '<img src="{}" style="height:{}px;width:{}px;object-fit:cover;'
        'border-radius:4px;border:1px solid #ddd;display:block" alt="">',
        image.url,
        height,
        int(height * 0.8),
    )


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Brand",
            {
                "fields": (
                    "brand_name",
                    "logo",
                    "tagline",
                    "announcement",
                )
            },
        ),
        (
            "Atelier section",
            {
                "fields": (
                    "about_kicker",
                    "about_title",
                    "about_text",
                    "about_image",
                    "about_caption",
                )
            },
        ),
        (
            "Numbers",
            {
                "fields": (
                    ("stat_years_value", "stat_years_label"),
                    ("stat_pieces_value", "stat_pieces_label"),
                    ("stat_hands_value", "stat_hands_label"),
                )
            },
        ),
        (
            "Contact",
            {
                "fields": (
                    "contact_kicker",
                    "contact_title",
                    "contact_text",
                    "contact_email",
                    "contact_phone",
                    "contact_address",
                    "contact_hours",
                    "instagram_url",
                    "pinterest_url",
                    "whatsapp_url",
                )
            },
        ),
        ("Footer", {"fields": ("footer_note",)}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ("thumb", "title", "kicker", "order", "is_active")
    list_editable = ("order", "is_active")
    list_display_links = ("thumb", "title")
    search_fields = ("title", "kicker", "subtitle")

    @admin.display(description="Image")
    def thumb(self, obj):
        return thumb(obj)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("thumb", "name", "look_count", "order", "is_active")
    list_editable = ("order", "is_active")
    list_display_links = ("thumb", "name")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")

    @admin.display(description="Cover")
    def thumb(self, obj):
        return thumb(obj, "cover_image")

    @admin.display(description="Looks")
    def look_count(self, obj):
        return obj.looks.count()


class LookImageInline(admin.TabularInline):
    model = LookImage
    extra = 1
    fields = ("image", "caption", "order", "preview")

    readonly_fields = ("preview",)

    @admin.display(description="Preview")
    def preview(self, obj):
        return thumb(obj, height=72) if obj.pk else "—"


@admin.register(Look)
class LookAdmin(admin.ModelAdmin):
    list_display = ("thumb", "name", "collection", "price_label", "is_featured", "order", "is_active")
    list_editable = ("is_featured", "order", "is_active")
    list_display_links = ("thumb", "name")
    list_filter = ("collection", "is_featured", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "label", "description", "detail")
    inlines = [LookImageInline]

    @admin.display(description="Image")
    def thumb(self, obj):
        return thumb(obj)


@admin.register(Craft)
class CraftAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("author", "short_quote", "order", "is_active")
    list_editable = ("order", "is_active")

    @admin.display(description="Quote")
    def short_quote(self, obj):
        return (obj.quote[:70] + "…") if len(obj.quote) > 70 else obj.quote


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "look", "created_at", "is_read")
    list_editable = ("is_read",)
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "message", "look")
    date_hierarchy = "created_at"

    def has_add_permission(self, request):
        return False
