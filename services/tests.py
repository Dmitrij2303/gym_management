from django.db import IntegrityError
from django.test import TestCase

from services.models import MembershipPlan, Service


class ServiceModelTests(TestCase):
    def test_service_is_created_successfully(self):
        service = Service.objects.create(
            name="Йога",
            service_type=Service.GROUP,
            default_duration_minutes=60,
            default_capacity=12,
            price=900,
        )

        self.assertEqual(service.name, "Йога")
        self.assertEqual(service.service_type, Service.GROUP)
        self.assertEqual(service.default_duration_minutes, 60)
        self.assertEqual(service.default_capacity, 12)
        self.assertEqual(service.price, 900)
        self.assertTrue(service.is_active)

    def test_service_str_returns_name(self):
        service = Service.objects.create(
            name="Персональная тренировка",
            service_type=Service.INDIVIDUAL,
            default_duration_minutes=60,
            default_capacity=1,
            price=1500,
        )

        self.assertEqual(str(service), "Персональная тренировка")

    def test_service_default_duration_minutes_must_be_greater_than_zero(self):
        with self.assertRaises(IntegrityError):
            Service.objects.create(
                name="Неверная длительность",
                service_type=Service.GROUP,
                default_duration_minutes=0,
                default_capacity=10,
                price=500,
            )

    def test_service_default_capacity_must_be_greater_than_zero(self):
        with self.assertRaises(IntegrityError):
            Service.objects.create(
                name="Неверная вместимость",
                service_type=Service.GROUP,
                default_duration_minutes=60,
                default_capacity=0,
                price=500,
            )


class MembershipPlanModelTests(TestCase):
    def test_membership_plan_is_created_successfully(self):
        plan = MembershipPlan.objects.create(
            name="Месяц безлимит",
            price=3500,
            duration_days=30,
            visit_limit=None,
        )

        self.assertEqual(plan.name, "Месяц безлимит")
        self.assertEqual(plan.price, 3500)
        self.assertEqual(plan.duration_days, 30)
        self.assertIsNone(plan.visit_limit)
        self.assertTrue(plan.is_active)

    def test_membership_plan_str_returns_name(self):
        plan = MembershipPlan.objects.create(
            name="8 посещений",
            price=2500,
            duration_days=30,
            visit_limit=8,
        )

        self.assertEqual(str(plan), "8 посещений")

    def test_membership_plan_duration_days_must_be_greater_than_zero(self):
        with self.assertRaises(IntegrityError):
            MembershipPlan.objects.create(
                name="Неверный срок",
                price=2500,
                duration_days=0,
                visit_limit=8,
            )

    def test_membership_plan_visit_limit_must_be_null_or_greater_than_zero(self):
        with self.assertRaises(IntegrityError):
            MembershipPlan.objects.create(
                name="Неверный лимит",
                price=2500,
                duration_days=30,
                visit_limit=0,
            )
