from django.db import models


class PrayerList(models.Model):
    """
    List of prayers
    """
    name = models.CharField(max_length=250, blank=True, null=True)
    time_of_prayer = models.CharField(max_length=250, blank=True, null=True)
    details = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        verbose_name = "Prayer"
        verbose_name_plural = "Prayers"

    def __str__(self):
        return self.name


class ReligiousFiles(models.Model):
    """
    Media or other file related to religion
    """
    title = models.CharField(max_length=250, blank=True, null=True)
    document = models.FileField(upload_to="media/", blank=True, null=True)
    text_contains = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Islamic Contain"
        verbose_name_plural = "Islamic Contains"

    def __str__(self):
        return self.title
