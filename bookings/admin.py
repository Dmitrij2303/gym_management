from django.contrib import admin

from .models import Session, Booking, OneTimeVisit


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "service",
        "trainer",
        "start_datetime",
        "end_datetime",
        "capacity",
        "price",
        "status",
        "created_at",
    )
    search_fields = (
        "service__name",
        "trainer__first_name",
        "trainer__last_name",
    )
    list_filter = ("status", "start_datetime", "created_at")
    autocomplete_fields = ("service", "trainer")
    ordering = ("start_datetime",)
    readonly_fields = ("created_at",)
    list_select_related = ("service", "trainer")
    list_per_page = 20


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "client",
        "session",
        "status",
        "price_final",
        "created_at",
    )
    search_fields = (
        "client__first_name",
        "client__last_name",
        "session__service__name",
    )
    list_filter = ("status", "created_at")
    autocomplete_fields = ("client", "session")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
    list_select_related = ("client", "session", "session__service")
    list_per_page = 20


@admin.register(OneTimeVisit)
class OneTimeVisitAdmin(UnicodeInsensitiveSearchAdminMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "client",
        "visit_date",
        "price",
        "status",
        "created_at",
    )
    search_fields = ("client__first_name", "client__last_name")
    list_filter = ("status", "visit_date", "created_at")
    autocomplete_fields = ("client",)
    ordering = ("-visit_date", "-created_at")
    readonly_fields = ("created_at",)
    list_select_related = ("client",)
    list_per_page = 20
