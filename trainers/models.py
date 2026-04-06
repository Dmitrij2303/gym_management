from django.core.exceptions import ValidationError
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
    specialization = models.CharField(
        "Специализация", max_length=255, blank=True, default=""
    )
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


class TrainerWorkSlot(models.Model):
    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE,
        related_name="work_slots",
        verbose_name="Тренер",
    )
    start_datetime = models.DateTimeField("Начало")
    end_datetime = models.DateTimeField("Окончание")
    is_available = models.BooleanField("Доступен для записи", default=True)
    comment = models.CharField("Комментарий", max_length=255, blank=True, null=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)

    class Meta:
        verbose_name = "Рабочий слот тренера"
        verbose_name_plural = "Рабочие слоты тренеров"
        ordering = ["start_datetime"]

    def clean(self):
        if self.end_datetime <= self.start_datetime:
            raise ValidationError("Время окончания должно быть больше времени начала.")

    def __str__(self):
        return f"{self.trainer.full_name}: {self.start_datetime:%d.%m.%Y %H:%M} - {self.end_datetime:%H:%M}"
