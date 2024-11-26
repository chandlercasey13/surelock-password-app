from django.db import models

# Import the User
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

# Import signals
from django.db.models.signals import post_save
from django.dispatch import receiver

class Login(models.Model):
    appname = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    note = models.TextField(max_length=250, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    my_datetime = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        # Hashes the password before saving.
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        # # Verifies if a given password matches the hashed password.
        return check_password(raw_password, self.password)

    def get_plaintext_password(self, user_authenticated):
        # # Retrieve the plaintext password only if the user is authenticated and authorized.
        # Check that the user is authenticated before revealing the password.
        if user_authenticated:
            # Implement retrieval logic here (e.g., stored in a secure temporary storage).
            # For example, decrypt it if using an encrypted storage or retrieve from secure memory.
            return self._retrieve_plaintext_password()
        else:
            return "Unauthorized Access"

    def _retrieve_plaintext_password(self):
        # # A private method to securely retrieve the password. This is a placeholder.
        # Implement logic here if using an encryption/decryption system for storage
        pass

    def save(self, *args, **kwargs):
        # Check if the instance already exists in the database
        if self.pk:
            # Retrieve the existing password from the database
            existing_password = Login.objects.get(pk=self.pk).password
            # Hash password only if it has changed
            if self.password != existing_password:
                self.password = make_password(self.password)
        else:
            # New instance, so hash the password
            self.password = make_password(self.password)

        # Capitalize the app name
        self.appname = self.appname.capitalize()
        super().save(*args, **kwargs)

    @property
    def most_recent(self):
        # Return the latest date between creation and update timestamps
        return self.date_updated or self.my_datetime

    def __str__(self):
        return self.appname

class Profile(models.Model):
    # Profile model to store additional user info, including timezone
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = models.CharField(max_length=100, default='UTC')  # Default to UTC if not set

    def __str__(self):
        return f"{self.user.username}'s profile"

# Signal to automatically create or update a Profile whenever a User is saved
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()