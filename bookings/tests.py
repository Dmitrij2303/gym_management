from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from bookings.models import Booking, OneTimeVisit, Session
from clients.models import Client
from services.models import Service
from trainers.models import Trainer


class SessionModelTests(TestCase):
    def setUp(self):
        self.trainer = Trainer.objects.create(
            first_name="Петр",
            last_name="Петров",
            phone="+79990000001",
            gender=Trainer.MALE,
            specialization="Тренажерный зал",
        )
        self.service = Service.objects.create(
            name="Персональная тренировка",
            service_type=Service.INDIVIDUAL,
            default_duration_minutes=60,
            default_capacity=1,
            price=1500,
        )

    def test_session_is_created_successfully(self):
        start = timezone.now() + timedelta(days=1)
        end = start + timedelta(minutes=60)

        session = Session.objects.create(
            service=self.service,
            trainer=self.trainer,
            start_datetime=start,
            end_datetime=end,
            capacity=1,
            price=1500,
        )

        self.assertEqual(session.status, Session.PLANNED)
        self.assertEqual(session.capacity, 1)
        self.assertEqual(session.price, 1500)

    def test_session_end_datetime_must_be_greater_than_start_datetime(self):
        start = timezone.now() + timedelta(days=1)
        end = start - timedelta(minutes=30)

        session = Session(
            service=self.service,
            trainer=self.trainer,
            start_datetime=start,
            end_datetime=end,
            capacity=1,
            price=1500,
        )

        with self.assertRaises(ValidationError):
            session.full_clean()

    def test_session_cannot_overlap_with_another_session_of_same_trainer(self):
        start = timezone.now() + timedelta(days=1)
        end = start + timedelta(minutes=60)
        Session.objects.create(
            service=self.service,
            trainer=self.trainer,
            start_datetime=start,
            end_datetime=end,
            capacity=1,
            price=1500,
        )

        overlapping_session = Session(
            service=self.service,
            trainer=self.trainer,
            start_datetime=start + timedelta(minutes=30),
            end_datetime=end + timedelta(minutes=30),
            capacity=1,
            price=1500,
        )

        with self.assertRaises(ValidationError):
            overlapping_session.full_clean()


class BookingModelTests(TestCase):
    def setUp(self):
        self.client_obj = Client.objects.create(
            first_name="Иван",
            last_name="Иванов",
            phone="+79990000002",
            gender=Client.MALE,
        )
        self.trainer = Trainer.objects.create(
            first_name="Анна",
            last_name="Сидорова",
            phone="+79990000003",
            gender=Trainer.FEMALE,
            specialization="Йога",
        )
        self.service = Service.objects.create(
            name="Йога",
            service_type=Service.GROUP,
            default_duration_minutes=60,
            default_capacity=10,
            price=800,
        )

        start = timezone.now() + timedelta(days=1)
        end = start + timedelta(minutes=60)

        self.session = Session.objects.create(
            service=self.service,
            trainer=self.trainer,
            start_datetime=start,
            end_datetime=end,
            capacity=10,
            price=800,
        )

    def test_booking_is_created_successfully(self):
        booking = Booking.objects.create(
            client=self.client_obj,
            session=self.session,
            price_final=800,
        )

        self.assertEqual(booking.status, Booking.BOOKED)
        self.assertEqual(booking.client, self.client_obj)
        self.assertEqual(booking.session, self.session)

    def test_booking_must_be_unique_for_client_and_session(self):
        Booking.objects.create(
            client=self.client_obj,
            session=self.session,
            price_final=800,
        )

        with self.assertRaises(IntegrityError):
            Booking.objects.create(
                client=self.client_obj,
                session=self.session,
                price_final=800,
            )

    def test_booking_string_representation(self):
        booking = Booking.objects.create(
            client=self.client_obj,
            session=self.session,
            price_final=800,
        )

        self.assertIn(self.client_obj.full_name, str(booking))

    def test_booking_cannot_exceed_session_capacity(self):
        client_two = Client.objects.create(
            first_name="Мария",
            last_name="Петрова",
            phone="+79990000005",
            gender=Client.FEMALE,
        )
        limited_session = Session.objects.create(
            service=self.service,
            trainer=self.trainer,
            start_datetime=timezone.now() + timedelta(days=2),
            end_datetime=timezone.now() + timedelta(days=2, hours=1),
            capacity=1,
            price=800,
        )
        Booking.objects.create(
            client=self.client_obj,
            session=limited_session,
            price_final=800,
        )

        second_booking = Booking(
            client=client_two,
            session=limited_session,
            price_final=800,
        )

        with self.assertRaises(ValidationError):
            second_booking.full_clean()


class OneTimeVisitModelTests(TestCase):
    def setUp(self):
        self.client_obj = Client.objects.create(
            first_name="Мария",
            last_name="Смирнова",
            phone="+79990000004",
            gender=Client.FEMALE,
        )

    def test_one_time_visit_is_created_successfully(self):
        visit = OneTimeVisit.objects.create(
            client=self.client_obj,
            visit_date=timezone.localdate(),
            price=500,
        )

        self.assertEqual(visit.status, OneTimeVisit.PAID)
        self.assertEqual(visit.price, 500)
        self.assertEqual(visit.client, self.client_obj)
