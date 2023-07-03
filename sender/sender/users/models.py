from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for sender.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class Contacts(models.Model):
    from_who = models.CharField(max_length=250)
    to = models.CharField(max_length=250)
    text = models.TextField()
    already_used = models.BooleanField(default=False)
    failed = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Contacts'

    def __str__(self) -> str:
        return self.from_who

class Tokens(models.Model):
    title = models.CharField(max_length=250)
    token = models.CharField(max_length=250, blank=True)
    secret = models.CharField(max_length=250, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.token
