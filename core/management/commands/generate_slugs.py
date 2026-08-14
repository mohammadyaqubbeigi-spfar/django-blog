from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import Post
from django.db.models import Q

class Command(BaseCommand):
    help = "Generate slugs for posts that do not have one"

    def handle(self, *args, **kwargs):
        posts = Post.objects.filter(Q(slug__isnull=True) | Q(slug = ""))

        count = 0

        for post in posts:
            post.slug = slugify(post.title)
            post.save()
            count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Generated slugs for {count} posts.")
        )