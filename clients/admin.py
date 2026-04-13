from django.contrib import admin

from .models import Client, ClientMembership


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "last_name",
        "first_name",
        "phone",
        "gender",
        "birth_date",
        "is_active",
        "created_at",
    ]
    search_fields = ("first_name", "last_name", "phone")
    list_filter = ("gender", "is_active", "created_at")
    ordering = ("last_name", "first_name")
    readonly_fields = ("created_at",)
    list_per_page = 20


@admin.register(ClientMembership)
class ClientMembershipAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "client",
        "membership_plan",
        "start_date",
        "end_date",
        "remaining_visits",
        "status",
        "created_at",
    )
    search_fields = (
        "client__first_name",
        "client__last_name",
        "membership_plan__name",
    )
    list_filter = ("status", "start_date", "end_date", "created_at")
    autocomplete_fields = ("client", "membership_plan")
    ordering = ("-start_date",)
    readonly_fields = ("created_at",)
    list_select_related = ("client", "membership_plan")
    list_per_page = 20
