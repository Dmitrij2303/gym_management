from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from trainers.models import Trainer, TrainerWorkSlot


class TrainerModelTests(TestCase):
    def test_trainer_full_name_returns_first_name_and_last_name(self):
        trainer = Trainer.objects.create(
            first_name="Петр",
            last_name="Иванов",
            phone="+79990000020",
            gender=Trainer.MALE,
            specialization="Йога",
        )

        self.assertEqual(trainer.full_name, "Петр Иванов")

    def test_trainer_str_returns_full_name(self):
        trainer = Trainer.objects.create(
            first_name="Анна",
            last_name="Смирнова",
            phone="+79990000021",
            gender=Trainer.FEMALE,
            specialization="Пилатес",
        )

        self.assertEqual(str(trainer), "Анна Смирнова")

    def test_trainer_is_active_by_default(self):
        trainer = Trainer.objects.create(
            first_name="Мария",
            last_name="Петрова",
            phone="+79990000022",
            gender=Trainer.FEMALE,
        )

        self.assertTrue(trainer.is_active)


class TrainerWorkSlotModelTests(TestCase):
    def setUp(self):
        self.trainer = Trainer.objects.create(
            first_name="Олег",
            last_name="Сидоров",
            phone="+79990000023",
            gender=Trainer.MALE,
            specialization="Тренажерный зал",
        )

    def test_trainer_work_slot_is_created_successfully(self):
        start = timezone.now() + timedelta(days=1)
        end = start + timedelta(hours=2)

        slot = TrainerWorkSlot.objects.create(
            trainer=self.trainer,
            start_datetime=start,
            end_datetime=end,
            is_available=True,
            comment="Утренний слот",
        )

        self.assertEqual(slot.trainer, self.trainer)
        self.assertTrue(slot.is_available)
        self.assertEqual(slot.comment, "Утренний слот")

    def test_trainer_work_slot_end_datetime_must_be_greater_than_start_datetime(self):
        start = timezone.now() + timedelta(days=1)
        end = start - timedelta(minutes=30)

        slot = TrainerWorkSlot(
            trainer=self.trainer,
            start_datetime=start,
            end_datetime=end,
            is_available=True,
        )

        with self.assertRaises(ValidationError):
            slot.full_clean()

    def test_trainer_work_slot_str_contains_trainer_name(self):
        start = timezone.now() + timedelta(days=1)
        end = start + timedelta(hours=1)

        slot = TrainerWorkSlot.objects.create(
            trainer=self.trainer,
            start_datetime=start,
            end_datetime=end,
        )

        self.assertIn(self.trainer.full_name, str(slot))
