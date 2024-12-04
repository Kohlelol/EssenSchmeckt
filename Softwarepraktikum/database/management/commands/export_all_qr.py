from django.core.management.base import BaseCommand
from database.models import Person
import os
from PIL import Image

class Command(BaseCommand):
    help = 'Generate and save QR codes for all persons in the static directory'
    
    def handle(self, *args, **kwargs):
        static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'qr_codes')
        os.makedirs(static_dir, exist_ok=True)

        all_qr_codes = [person.generate_QR() for person in Person.objects.all()]

        for i, qrcode in enumerate(all_qr_codes):
            qrcode_path = os.path.join(static_dir, f'{i}.png')
            qrcode.save(qrcode_path)
            self.stdout.write(self.style.SUCCESS(f'Successfully saved QR code for person {i} at {qrcode_path}'))
    