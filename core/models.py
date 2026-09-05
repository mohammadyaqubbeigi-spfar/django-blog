from django.contrib import admin
from django.db import models
from django.utils.text import slugify

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True , blank=True , null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Mets:
        ordering = ["-created_at","title"]

    @admin.display(description="Word count")
    def word_count(self):
        return len(self.content.split())

    def __str__(self):
        return self.title

    def save(self, *args , **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Post.objects.filter(slug=slug).exclude(pk = self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args , **kwargs)
