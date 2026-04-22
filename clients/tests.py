from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from clients.models import Client, ClientMembership
from services.models import MembershipPlan


class ClientModelTests(TestCase):
    def test_client_full_name_returns_first_name_and_last_name(self):
        client = Client.objects.create(
            first_name="Олег",
            last_name="Иванов",
            phone="+79990000010",
            gender=Client.MALE,
        )

        self.assertEqual(client.full_name, "Олег Иванов")

    def test_client_str_returns_full_name(self):
        client = Client.objects.create(
            first_name="Мария",
            last_name="Смирнова",
            phone="+79990000011",
            gender=Client.FEMALE,
        )

        self.assertEqual(str(client), "Мария Смирнова")

    def test_client_is_active_by_default(self):
        client = Client.objects.create(
            first_name="Анна",
            last_name="Петрова",
            phone="+79990000012",
            gender=Client.FEMALE,
        )

        self.assertTrue(client.is_active)


class ClientMembershipModelTests(TestCase):
    def setUp(self):
        self.client_obj = Client.objects.create(
            first_name="Иван",
            last_name="Иванов",
            phone="+79990000013",
            gender=Client.MALE,
        )
        self.membership_plan = MembershipPlan.objects.create(
            name="Месяц безлимит",
            price=3000,
            duration_days=30,
            visit_limit=None,
        )

    def test_client_membership_is_created_successfully(self):
        membership = ClientMembership.objects.create(
            client=self.client_obj,
            membership_plan=self.membership_plan,
            start_date=date(2026, 4, 1),
            end_date=date(2026, 4, 30),
            remaining_visits=None,
        )

        self.assertEqual(membership.status, ClientMembership.ACTIVE)
        self.assertEqual(membership.client, self.client_obj)
        self.assertEqual(membership.membership_plan, self.membership_plan)

    def test_client_membership_end_date_cannot_be_earlier_than_start_date(self):
        membership = ClientMembership(
            client=self.client_obj,
            membership_plan=self.membership_plan,
            start_date=date(2026, 4, 10),
            end_date=date(2026, 4, 1),
            remaining_visits=None,
        )

        with self.assertRaises(ValidationError):
            membership.full_clean()

    def test_client_membership_string_representation(self):
        membership = ClientMembership.objects.create(
            client=self.client_obj,
            membership_plan=self.membership_plan,
            start_date=date(2026, 4, 1),
            end_date=date(2026, 4, 30),
        )

        self.assertIn(self.client_obj.full_name, str(membership))
        self.assertIn(self.membership_plan.name, str(membership))
