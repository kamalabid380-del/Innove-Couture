from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.urls import reverse

from core.models import (
    Collection,
    Craft,
    HeroSlide,
    Look,
    SiteSettings,
    Testimonial,
)

DEMO = Path(settings.BASE_DIR) / "demo_assets"


class Command(BaseCommand):
    help = "Load the Innove Couture demo content and photography."

    def handle(self, *args, **options):
        if not DEMO.exists():
            self.stderr.write("demo_assets folder is missing.")
            return

        settings_obj = SiteSettings.load()
        if not settings_obj.about_image:
            self._attach(settings_obj, "about_image", "atelier.jpg")

        collections = self._seed_collections()
        self._seed_heroes(collections)
        self._seed_looks(collections)
        self._seed_crafts()
        self._seed_testimonials()

        self.stdout.write(self.style.SUCCESS("Demo content is in place. Visit /"))

    def _attach(self, instance, field_name, filename):
        content = ContentFile((DEMO / filename).read_bytes())
        getattr(instance, field_name).save(filename, content, save=True)

    def _seed_collections(self):
        data = [
            (
                "Bridal Atelier",
                "collection-bridal.jpg",
                "Heirloom embroidery, reimagined for the modern bride — ivory silks, tulle "
                "and antique gold, drawn for one person at a time.",
            ),
            (
                "Evening Edit",
                "collection-evening.jpg",
                "Sculpted silhouettes for the hours after dark — satin, organza and quiet drama.",
            ),
            (
                "Everyday Silks",
                "collection-silks.jpg",
                "Soft tailoring in washed silks and raw linen, made to be lived in.",
            ),
        ]
        collections = {}
        for index, (name, image, description) in enumerate(data, start=1):
            collection, created = Collection.objects.get_or_create(
                name=name,
                defaults={"description": description, "order": index},
            )
            if created and not collection.cover_image:
                self._attach(collection, "cover_image", image)
            collections[name] = collection
        return collections

    def _seed_heroes(self, collections):
        data = [
            {
                "image": "hero-1.jpg",
                "kicker": "The Bridal Series — 2026",
                "title": "Something borrowed from the light.",
                "subtitle": "Hand-embroidered ivory silks and antique gold, drawn for one bride at a time.",
                "cta_label": "Explore bridal",
                "cta_url": reverse("core:collection", args=[collections["Bridal Atelier"].slug]),
                "order": 1,
            },
            {
                "image": "hero-2.jpg",
                "kicker": "The Evening Edit",
                "title": "Cut for the way you move.",
                "subtitle": "Bias-cut satin, midnight weights, and an open back that does the talking.",
                "cta_label": "View the edit",
                "cta_url": reverse("core:collection", args=[collections["Evening Edit"].slug]),
                "order": 2,
            },
        ]
        for entry in data:
            if HeroSlide.objects.filter(title=entry["title"]).exists():
                continue
            slide = HeroSlide(**{key: value for key, value in entry.items() if key != "image"})
            self._attach(slide, "image", entry["image"])

    def _seed_looks(self, collections):
        data = [
            {
                "collection": "Bridal Atelier",
                "name": "The Noor Gown",
                "label": "Bridal · Ivory",
                "image": "look-noor.jpg",
                "description": "An ivory silk gown with a square neckline, worked edge to edge in "
                "antique-gold zardozi and pearl flowers. The veil is tulle, the train is twelve "
                "feet, the weight is almost nothing.",
                "detail": "Hand embroidery — 640 hours\nIvory silk, tulle, antique-gold zardozi\n"
                "Made to measure, 10–12 weeks",
                "is_featured": True,
                "order": 1,
            },
            {
                "collection": "Bridal Atelier",
                "name": "The Meher Lehenga",
                "label": "Bridal · Tulle",
                "image": "look-meher.jpg",
                "description": "Twelve panels of tulle that fall like water, bordered in gold gota "
                "and finished with a hand-worked dupatta in the same thread.",
                "detail": "Gota and dabka work\nIvory tulle, silk lining, gold borders\n"
                "Made to measure, 8–10 weeks",
                "is_featured": True,
                "order": 2,
            },
            {
                "collection": "Evening Edit",
                "name": "The Mina Dress",
                "label": "Evening · Black",
                "image": "look-mina.jpg",
                "description": "Bias-cut black satin with a sculpted, open back. Cut on a single "
                "grain so the dress moves before you do.",
                "detail": "Bias-cut satin, silk-lined\nOpen back, hidden hook-and-eye\n"
                "Made to measure, 6–8 weeks",
                "is_featured": True,
                "order": 3,
            },
            {
                "collection": "Everyday Silks",
                "name": "The Sahar Suit",
                "label": "Everyday · Sand",
                "image": "look-sahar.jpg",
                "description": "Sand linen, unlined and softened by wash, with a shoulder that "
                "sits exactly where it should. The first piece our clients live in.",
                "detail": "Washed linen, unlined\nSoft unstructured shoulder\n"
                "Made to measure, 4–6 weeks",
                "is_featured": True,
                "order": 4,
            },
        ]
        for entry in data:
            if Look.objects.filter(name=entry["name"]).exists():
                continue
            look = Look(
                collection=collections[entry["collection"]],
                name=entry["name"],
                label=entry["label"],
                description=entry["description"],
                detail=entry["detail"],
                is_featured=entry["is_featured"],
                order=entry["order"],
            )
            self._attach(look, "image", entry["image"])

    def _seed_crafts(self):
        data = [
            (
                "The Conversation",
                "We begin with tea and a sketchbook — your occasion, your comfort, the "
                "references you keep returning to.",
                1,
            ),
            (
                "The Cloth",
                "Fabrics are chosen by hand: silks from the old markets, tulle from mills we "
                "have used for years, linens washed until they soften.",
                2,
            ),
            (
                "The Hand",
                "Embroidery, fittings and finishing span six to ten weeks, carried out by six "
                "artisans in the same room where it all started.",
                3,
            ),
        ]
        for title, text, order in data:
            Craft.objects.get_or_create(title=title, defaults={"text": text, "order": order})

    def _seed_testimonials(self):
        data = [
            (
                "The fitting felt less like a dress and more like being understood.",
                "Ayesha R.",
                "Bride, 2025 — Lahore",
                1,
            ),
            (
                "Innove restyled my mother's dupatta for my nikkah — sixty years apart, the "
                "same thread.",
                "Sana M.",
                "Bride, 2024 — Lahore",
                2,
            ),
            (
                "Quiet, exact, unhurried. The only atelier I trust with a deadline.",
                "Hira K.",
                "Client — Karachi",
                3,
            ),
        ]
        for quote, author, detail, order in data:
            Testimonial.objects.get_or_create(
                author=author,
                defaults={"quote": quote, "detail": detail, "order": order},
            )
