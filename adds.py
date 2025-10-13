import os
from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='profiles/')

    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)


@receiver(models.signals.pre_save, sender=Profile)
def auto_delete_old_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return  # skip new objects
    try:
        old_file = Profile.objects.get(pk=instance.pk).image
    except Profile.DoesNotExist:
        return
    new_file = instance.image
    if old_file and old_file != new_file:
        old_file.delete(save=False)
