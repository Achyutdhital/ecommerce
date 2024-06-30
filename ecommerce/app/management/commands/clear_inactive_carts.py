from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from app.models import Cart

class Command(BaseCommand):
    help = 'Clears inactive carts older than 10 days'

    def handle(self, *args, **kwargs):
        ten_days_ago = datetime.now() - timedelta(days=10)
        inactive_carts = Cart.objects.filter(updated_at__lt=ten_days_ago)
        inactive_carts.delete()
        self.stdout.write(self.style.SUCCESS('Cleared inactive carts'))