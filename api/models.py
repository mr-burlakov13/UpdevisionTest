import secrets
from datetime import timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Profile(models.Model):
    ID_TYPE_CHOICES = (
        ('phone', 'Phone'),
        ('email', 'Email'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    id_type = models.CharField(max_length=10, choices=ID_TYPE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.id_type})"


class Token(models.Model):
    key = models.CharField(max_length=64, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens')
    created = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return self.key

    @classmethod
    def generate_token(cls, user):
        key = secrets.token_hex(32)
        now = timezone.now()
        lifetime = getattr(settings, 'TOKEN_LIFETIME', timedelta(minutes=5))
        token = cls.objects.create(
            key=key,
            user=user,
            expires_at=now + lifetime
        )
        return token

    def extend_expiration(self):
        from django.conf import settings
        lifetime = getattr(settings, 'TOKEN_LIFETIME', timedelta(minutes=5))
        self.expires_at = timezone.now() + lifetime
        self.save(update_fields=['expires_at'])
