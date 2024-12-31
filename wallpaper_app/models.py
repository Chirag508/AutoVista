from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField  # Import CloudinaryField

class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    author = models.CharField(max_length=200)
    image = CloudinaryField('image')  # Replaced ImageField with CloudinaryField
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def secure_image_url(self):
        return self.image.url.replace("http://", "https://")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Sub_category(models.Model):
    name = models.CharField(max_length=255, default="Autovista")
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Wallpaper(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = CloudinaryField('image')  # Replaced ImageField with CloudinaryField
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(Sub_category, on_delete=models.CASCADE)
    resolution = models.CharField(max_length=20)
    downloads = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Ensure image URLs always use HTTPS
    def __str__(self):
        return self.title
    @property
    def secure_image_url(self):
        return self.image.url.replace("http://", "https://")

