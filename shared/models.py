from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AboutUs(BaseModel):
    name = models.CharField(max_length=128)
    profession = models.CharField(max_length=64)
    info = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'abouts'
        verbose_name = 'about'
        verbose_name_plural = 'abouts'


class Contact(BaseModel):
    full_name = models.CharField(max_length=128)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    is_read = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'contacts'
        verbose_name = 'contact'
        verbose_name_plural = 'contacts'
