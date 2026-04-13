from django.core.exceptions import ValidationError
from django.db import models

from services.models import MembershipPlan


class Client(models.Model):
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
    is_active = models.BooleanField("Активен", default=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ["last_name", "first_name"]
        indexes = [
            models.Index(fields=["last_name", "first_name"], name="idx_clients_last_first"),
        ]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return self.full_name


class ClientMembership(models.Model):
    ACTIVE = "active"
    EXPIRED = "expired"
    FROZEN = "frozen"
    USED_UP = "used_up"

    STATUS_CHOICES = [
        (ACTIVE, "Активен"),
        (EXPIRED, "Истек"),
        (FROZEN, "Заморожен"),
        (USED_UP, "Израсходован"),
    ]

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="memberships",
        verbose_name="Клиент",
    )
    membership_plan = models.ForeignKey(
        MembershipPlan,
        on_delete=models.PROTECT,
        related_name="client_memberships",
        verbose_name="План абонемента",
    )
    start_date = models.DateField("Дата начала")
    end_date = models.DateField("Дата окончания")
    remaining_visits = models.PositiveIntegerField(
        "Осталось посещений",
        blank=True,
        null=True,
    )
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=STATUS_CHOICES,
        default=ACTIVE,
    )
    created_at = models.DateTimeField("Создан", auto_now_add=True)

    class Meta:
        verbose_name = "Абонемент клиента"
        verbose_name_plural = "Абонементы клиентов"
        ordering = ["-start_date"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(end_date__gte=models.F("start_date")),
                name="chk_client_memberships_dates",
            ),
        ]

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("Дата окончания не может быть раньше даты начала.")

    def __str__(self):
        return f"{self.client.full_name} — {self.membership_plan.name}"
