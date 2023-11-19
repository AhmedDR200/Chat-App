from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.shortcuts import get_object_or_404


def category_icon(instance, filename):
     return f"category/{instance.id}/category_icon/{filename}"


class Category(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    icon = models.FileField(upload_to=category_icon, null=True, blank=True)

    def save(self, *args, **kwargs):
         if self.id:
              existing = get_object_or_404(Category, id=self.id)
              if existing.icon != self.icon:
                   # delete old image file
                   existing.icon.delete(save=False)
         super(Category, self).save(*args, **kwargs)


    @receiver(models.signals.pre_delete, sender="server.Category")
    def auto_delete_file_on_delete(sender, instance, **kwargs):
         for field in instance._meta.fields:
              if field.name == "icon":
                   file = getattr(instance, field.name)
                   if file:
                        file.delete(save=False)
        
         
    def __str__(self):
        return self.name


class Server(models.Model):
    name = models.CharField(max_length=150)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="server_owner")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="server_category")
    description = models.CharField(max_length=250, null=True)
    member = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return f"{self.name} - {self.id}"


class Channel(models.Model):
    name = models.CharField(max_length=130)
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='channel_server')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="channel_owner")
    topic = models.CharField(max_length=256, blank=True, null=True)

    def save(self, *args, **kwargs):
         self.name = self.name.lower()
         super(Channel, self).save(*args, **kwargs)

    def __str__(self):
            return self.name