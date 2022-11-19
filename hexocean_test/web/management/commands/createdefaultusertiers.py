from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from hexocean_test.web.models import UserTier

class Command(BaseCommand):
    help = 'Creates the 3 default user tiers'

    def handle(self, *args, **options):
        basic = UserTier(name='Basic', thumbnail_sizes=[200])
        premium = UserTier(name='Premium', thumbnail_sizes=[200, 400], original_photo_access=True)
        enterprise = UserTier(name='Enterprise', thumbnail_sizes=[200, 400], original_photo_access=True, expiring_link_access=True)
        try:
            UserTier.objects.bulk_create([basic, premium, enterprise])
            print('Successfully created!')
        except IntegrityError:
            print('All default tiers or 1 of them is already created')
