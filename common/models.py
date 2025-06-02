from django.db import models
from django.contrib.auth.models import User

class PCBuild(models.Model):
    # Основная информация
    name = models.CharField(max_length=100)  # Название сборки
    description = models.TextField()  # Описание сборки
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена сборки

    # Характеристики сборки
    processor = models.CharField(max_length=100)
    video_card = models.CharField(max_length=100)
    ram = models.CharField(max_length=100)  # Например: 32GB DDR4
    storage = models.CharField(max_length=100)  # Например: 1TB SSD + 2TB HDD
    motherboard = models.CharField(max_length=100)
    power_supply = models.CharField(max_length=100)
    case = models.CharField(max_length=100)
    cooling = models.CharField(max_length=100, blank=True, null=True)
    operating_system = models.CharField(max_length=100, blank=True, null=True)

    # Производитель / бренд
    brand = models.CharField(max_length=100, blank=True, null=True)
    availability = models.BooleanField(default=True)  # В наличии ли

    def __str__(self):
        return self.name

class PCBuildPhoto(models.Model):
    pc_build = models.ForeignKey(PCBuild, on_delete=models.CASCADE, related_name='photos')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Фото для сборки {self.pc_build.name}"

class Order(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Заказ #{self.id} - {self.name}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    pc_build = models.ForeignKey(PCBuild, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

