import os
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Place
import qrcode

# This function will be triggered after a new Place is saved
@receiver(post_save, sender=Place)
def generate_qr_code(sender, instance, created, **kwargs):
    if created:
        # Only generate QR code when a new Place is created (not updated)
        place_id = instance.id
        url = f'http://127.0.0.1:8000/ratingform/{place_id}/'  # The URL the QR code should point to
        qr_img = qrcode.make(url)

        # Define the path to save the QR code image
        qr_code_dir = os.path.join(settings.MEDIA_ROOT, 'qrcodes')
        os.makedirs(qr_code_dir, exist_ok=True)  # Ensure the directory exists

        qr_code_path = os.path.join(qr_code_dir, f'place_{place_id}.png')
        qr_img.save(qr_code_path)

