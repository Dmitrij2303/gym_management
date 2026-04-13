from django.db import models


class Service(models.Model):
    GROUP = "group"
    INDIVIDUAL = "individual"

    SERVICE_TYPE_CHOICES = [
        (GROUP, "Групповое занятие"),
        (INDIVIDUAL, "Индивидуальное занятие"),
    ]

    name = models.CharField("Название", max_length=255)
    service_type = models.CharField(
        "Тип услуги", max_length=20, choices=SERVICE_TYPE_CHOICES
    )
    default_duration_minutes = models.PositiveIntegerField(
        "Длительность по умолчанию (мин)"
    )
    default_capacity = models.PositiveIntegerField(
        "Вместимость по умолчанию", default=1
    )
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    is_active = models.BooleanField("Активна", default=True)
    created_at = models.DateTimeField("Создана", auto_now_add=True)

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ["name"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(default_duration_minutes__gt=0),
                name="chk_services_duration",
            ),
            models.CheckConstraint(
                condition=models.Q(default_capacity__gt=0),
                name="chk_services_capacity",
            ),
        ]

    def __str__(self):
        return self.name


class MembershipPlan(models.Model):
    name = models.CharField("Название", max_length=255, unique=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField("Срок действия (дни)")
    visit_limit = models.PositiveIntegerField("Лимит посещений", blank=True, null=True)
    is_active = models.BooleanField("Активен", default=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)

    class Meta:
        verbose_name = "План абонемента"
        verbose_name_plural = "Планы абонементов"
        ordering = ["name"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(duration_days__gt=0),
                name="chk_membership_plans_duration",
            ),
            models.CheckConstraint(
                condition=models.Q(visit_limit__isnull=True)
                | models.Q(visit_limit__gt=0),
                name="chk_membership_plans_visit_limit",
            ),
        ]

    def __str__(self):
        return self.name
