from django.db import models


class Phone(models.Model):
    name = models.CharField(max_length=255, unique=True)
    release_date = models.DateField(null=True,blank=True,)
    display_size = models.CharField(max_length=100,blank=True,)
    display_type = models.CharField(max_length=255,blank=True,)
    processor = models.CharField(max_length=255,blank=True,)
    ram = models.CharField(max_length=100,blank=True,)
    storage = models.CharField(max_length=255,blank=True,)
    battery = models.CharField(max_length=100,blank=True,)
    main_camera = models.CharField(max_length=255,blank=True,)
    selfie_camera = models.CharField(max_length=255,blank=True,)
    operating_system = models.CharField(max_length=255,blank=True,)
    source_url = models.URLField(max_length=500,unique=True,)
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True,)

    def __str__(self):
        return self.name