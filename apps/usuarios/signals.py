from django.db.models.signals import post_save
from django.dispatch import receiver
from usuarios.models import User, Fiscal, Address


@receiver(post_save, sender=User)
def create_fiscal_after_user(sender, instance, created, **kwargs):
    try:
        if created:
            fiscal_cls = Fiscal.create(instance)
            Address.create(fiscal_cls)
    except Exception as e:
        print(e)