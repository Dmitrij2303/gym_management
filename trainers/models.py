from django.db import models


class Trainer(models.Model):
    MALE = "male"
    FEMALE = "female"

    GENDER_CHOICES = [
        (MALE, "Мужской"),
        (FEMALE, "Женский"),
    ]

    first_name = models.CharField("Имя", max_length=255)
    last_name = models.CharField("Фамилия", max_length=255)
    phone = models.CharField("Телефон", max_length=20, unique=True)
    gender = models.CharField("Пол", max_length=10, choices=GENDER_CHOICES)
    birth_date = models.DateField("Дата рождения", blank=True, null=True)
    specialization = models.CharField("Специализация", max_length=255, blank=True)
    is_active = models.BooleanField("Активен", default=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)

    class Meta:
        verbose_name = "Тренер"
        verbose_name_plural = "Тренеры"
        ordering = ["last_name", "first_name"]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return self.full_name
