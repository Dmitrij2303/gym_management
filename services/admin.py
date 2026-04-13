from django.contrib import admin

from .models import Service, MembershipPlan


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "service_type",
        "default_duration_minutes",
        "default_capacity",
        "price",
        "is_active",
        "created_at",
    )
    search_fields = ("name",)
    list_filter = ("service_type", "is_active", "created_at")
    ordering = ("name",)
    readonly_fields = ("created_at",)
    list_per_page = 20


@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "duration_days",
        "visit_limit",
        "is_active",
        "created_at",
    )
    search_fields = ("name",)
    list_filter = ("is_active", "created_at")
    ordering = ("name",)
    readonly_fields = ("created_at",)
    list_per_page = 20
