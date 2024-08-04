from django.core.management.base import BaseCommand
from django.utils.text import slugify
from app.models import BlogPost  # Ensure this matches the actual app name
from django.db.models import Count

class Command(BaseCommand):
    help = 'Resolve duplicate slugs in BlogPost model'

    def handle(self, *args, **kwargs):
        # Check for duplicate slugs
        duplicates = BlogPost.objects.values('slug').annotate(slug_count=Count('slug')).filter(slug_count__gt=1)
        for duplicate in duplicates:
            print(f"Duplicate slug found: {duplicate['slug']}")

        # Resolve duplicate slugs
        for post in BlogPost.objects.all():
            original_slug = post.slug
            if BlogPost.objects.filter(slug=original_slug).count() > 1:
                new_slug = slugify(f"{original_slug}-{post.id}")
                post.slug = new_slug
                post.save()
                self.stdout.write(self.style.SUCCESS(f"Updated slug for post {post.id}: {new_slug}"))

        self.stdout.write(self.style.SUCCESS('Successfully resolved duplicate slugs'))
