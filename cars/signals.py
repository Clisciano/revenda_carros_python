
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
# definir função para somar valores Sum
from django.db.models import Sum
from .models import Car, CarInventory

# criar função para para controlar o estoque de carros
def car_inventory_update():
    cars_count = Car.objects.all().count()
    cars_value = Car.objects.aggregate(total_value=Sum('value'))['total_value']

    # criar registro em CarInventory
    CarInventory.objects.create(cars_count=cars_count, cars_value=cars_value)

# decoradores para conectar sinais a funções
@receiver(pre_save, sender=Car)
def car_pre_save(sender, instance, **kwargs):
    if not instance.bio:
        instance.bio = 'Sem descrição'

@receiver(post_save, sender=Car)
def car_post_save(sender, instance, **kwargs):
    car_inventory_update()

@receiver(post_delete, sender=Car)
def car_post_delete(sender, instance, **kwargs):
    car_inventory_update()