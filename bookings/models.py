from django.core.exceptions import ValidationError
from django.db import models

from services.models import Service
from trainers.models import Trainer
from clients.models import Client


class Session(models.Model):
    PLANNED = "planned"
    COMPLETED = "completed"
    CANCELED = "canceled"

    STATUS_CHOICES = [
        (PLANNED, "Запланировано"),
        (COMPLETED, "Проведено"),
        (CANCELED, "Отменено"),
    ]

    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name="sessions",
        verbose_name="Услуга",
    )
    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.PROTECT,
        related_name="sessions",
        verbose_name="Тренер",
    )
    start_datetime = models.DateTimeField("Дата и время начала")
    end_datetime = models.DateTimeField("Дата и время окончания")
    capacity = models.PositiveIntegerField("Количество мест", default=1)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=STATUS_CHOICES,
        default=PLANNED,
    )
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        verbose_name = "Занятие"
        verbose_name_plural = "Занятия"
        ordering = ["start_datetime"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(end_datetime__gt=models.F("start_datetime")),
                name="chk_sessions_time",
            ),
            models.CheckConstraint(
                condition=models.Q(capacity__gt=0),
                name="chk_sessions_capacity",
            ),
        ]

    def clean(self):
        if self.end_datetime <= self.start_datetime:
            raise ValidationError("Время окончания должно быть больше времени начала.")

        if not all(
            [self.trainer_id, self.start_datetime, self.end_datetime]
        ) or self.status == self.CANCELED:
            return

        overlapping_sessions = Session.objects.filter(
            trainer_id=self.trainer_id,
            start_datetime__lt=self.end_datetime,
            end_datetime__gt=self.start_datetime,
        ).exclude(status=self.CANCELED)
        if self.pk:
            overlapping_sessions = overlapping_sessions.exclude(pk=self.pk)

        if overlapping_sessions.exists():
            raise ValidationError(
                "У тренера уже есть другое занятие, которое пересекается по времени."
            )

    def __str__(self):
        return f"{self.service.name} — {self.start_datetime:%d.%m.%Y %H:%M}"


class Booking(models.Model):
    BOOKED = "booked"
    VISITED = "visited"
    CANCELED = "canceled"
    MISSED = "missed"

    STATUS_CHOICES = [
        (BOOKED, "Записан"),
        (VISITED, "Посетил"),
        (CANCELED, "Отменена"),
        (MISSED, "Не пришел"),
    ]

    CLIENT = "client"
    TRAINER = "trainer"
    ADMIN = "admin"

    CANCELED_BY_CHOICES = [
        (CLIENT, "Клиент"),
        (TRAINER, "Тренер"),
        (ADMIN, "Администратор"),
    ]

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="Клиент",
    )
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="Занятие",
    )
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=STATUS_CHOICES,
        default=BOOKED,
    )
    canceled_by = models.CharField(
        "Кто отменил",
        max_length=20,
        choices=CANCELED_BY_CHOICES,
        blank=True,
        null=True,
    )
    cancel_reason = models.CharField(
        "Причина отмены",
        max_length=255,
        blank=True,
    )
    price_final = models.DecimalField("Итоговая цена", max_digits=10, decimal_places=2)
    created_at = models.DateTimeField("Создана", auto_now_add=True)

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["client", "session"],
                name="unique_client_session_booking",
            )
        ]

    def __str__(self):
        return f"{self.client.full_name} -> {self.session}"

    def clean(self):
        if not self.session_id or self.status not in [self.BOOKED, self.VISITED]:
            return

        occupied_slots = Booking.objects.filter(
            session_id=self.session_id,
            status__in=[self.BOOKED, self.VISITED],
        )
        if self.pk:
            occupied_slots = occupied_slots.exclude(pk=self.pk)

        if occupied_slots.count() >= self.session.capacity:
            raise ValidationError(
                {"session": "Нельзя записать клиента: все места на занятии уже заняты."}
            )


class OneTimeVisit(models.Model):
    PAID = "paid"
    VISITED = "visited"
    CANCELED = "canceled"

    STATUS_CHOICES = [
        (PAID, "Оплачено"),
        (VISITED, "Посетил"),
        (CANCELED, "Отменено"),
    ]

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="one_time_visits",
        verbose_name="Клиент",
    )
    visit_date = models.DateField("Дата посещения")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=STATUS_CHOICES,
        default=PAID,
    )
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        verbose_name = "Разовое посещение"
        verbose_name_plural = "Разовые посещения"
        ordering = ["-visit_date", "-created_at"]
        indexes = [
            models.Index(fields=["visit_date"], name="idx_one_time_visits_visit_date"),
        ]

    def __str__(self):
        return f"{self.client.full_name} — {self.visit_date}"
