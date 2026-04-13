from django.contrib import admin

from .models import Trainer, TrainerWorkSlot


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "last_name",
        "first_name",
        "phone",
        "gender",
        "specialization",
        "is_active",
        "created_at",
    )
    search_fields = ("first_name", "last_name", "phone", "specialization")
    list_filter = ("gender", "is_active")
    ordering = ("last_name", "first_name")
    readonly_fields = ("created_at",)
    list_per_page = 20


@admin.register(TrainerWorkSlot)
class TrainerWorkSlotAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "trainer",
        "start_datetime",
        "end_datetime",
        "is_available",
        "created_at",
    )
    search_fields = ("trainer__first_name", "trainer__last_name", "comment")
    list_filter = ("is_available", "start_datetime", "created_at")
    autocomplete_fields = ("trainer",)
    ordering = ("start_datetime",)
    readonly_fields = ("created_at",)
    list_select_related = ("trainer",)
    list_per_page = 20
