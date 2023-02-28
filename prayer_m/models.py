from django.db import models


class PrayerList(models.Model):
    """
    List of prayers
    """
    pass


class ReligiousFiles(models.Model):
    """
    Media or other file related to religion
    """
    title = models.CharField(max_length=250, blank=True, null=True)
    document = models.FileField(upload_to="/media", blank=True, null=True)
    text_contains = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Islamic Contain"
        verbose_name_plural = "Islamic Contains"
