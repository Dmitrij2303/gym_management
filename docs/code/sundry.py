# trainers -> models

# def clean(self):
#     if self.end_datetime <= self.start_datetime:
#         raise ValidationError(
#             {"end_datetime": "Время окончания должно быть больше времени начала."}
#         )

#     if not all([self.trainer_id, self.start_datetime, self.end_datetime]):
#         return

#     overlapping_slots = TrainerWorkSlot.objects.filter(
#         trainer_id=self.trainer_id,
#         start_datetime__lt=self.end_datetime,
#         end_datetime__gt=self.start_datetime,
#     )
#     if self.pk:
#         overlapping_slots = overlapping_slots.exclude(pk=self.pk)

#     if overlapping_slots.exists():
#         raise ValidationError(
#             "У тренера уже есть пересекающийся рабочий слот на это время."
#         )


# Имя пользователя: super_user
# Адрес электронной почты: acquatinta@mail.ru
# Password: qwerty12345


# from django.db import connection
# from django.utils.text import smart_split, unescape_string_literal


# class UnicodeInsensitiveSearchAdminMixin:
#     """
#     Django admin uses icontains by default, but SQLite applies it
#     case-insensitively only for ASCII. This mixin keeps the default
#     search and augments it with a Unicode-aware fallback.
#     """

#     supported_lookups = {
#         "exact",
#         "iexact",
#         "contains",
#         "icontains",
#         "startswith",
#         "istartswith",
#     }

#     def get_search_results(self, request, queryset, search_term):
#         base_queryset = queryset
#         queryset, may_have_duplicates = super().get_search_results(
#             request,
#             queryset,
#             search_term,
#         )

#         search_fields = self.get_search_fields(request)
#         if connection.vendor != "sqlite" or not search_term or not search_fields:
#             return queryset, may_have_duplicates

#         matched_pks = set(queryset.values_list("pk", flat=True))
#         search_queryset = base_queryset
#         related_fields = self._get_related_search_fields(search_fields)
#         if related_fields:
#             search_queryset = search_queryset.select_related(*related_fields)

#         for obj in search_queryset:
#             if obj.pk in matched_pks:
#                 continue
#             if self._matches_search_term(obj, search_fields, search_term):
#                 matched_pks.add(obj.pk)

#         if not matched_pks:
#             return queryset, may_have_duplicates

#         return base_queryset.filter(pk__in=matched_pks), may_have_duplicates

#     def _matches_search_term(self, obj, search_fields, search_term):
#         search_bits = []
#         for bit in smart_split(search_term):
#             if bit.startswith(('"', "'")) and bit[0] == bit[-1]:
#                 bit = unescape_string_literal(bit)
#             search_bits.append(bit.casefold())

#         return all(
#             any(self._matches_field(obj, field_name, bit) for field_name in search_fields)
#             for bit in search_bits
#         )

#     def _matches_field(self, obj, field_name, bit):
#         field_name, lookup = self._normalize_search_field(str(field_name))
#         value = self._resolve_field_value(obj, field_name)
#         if value is None:
#             return False

#         text = str(value).casefold()
#         if lookup in {"exact", "iexact"}:
#             return text == bit
#         if lookup in {"startswith", "istartswith"}:
#             return text.startswith(bit)
#         return bit in text

#     def _normalize_search_field(self, field_name):
#         if field_name.startswith(("^", "=", "@")):
#             prefix = field_name[0]
#             field_name = field_name[1:]
#             if prefix == "^":
#                 return field_name, "istartswith"
#             if prefix == "=":
#                 return field_name, "iexact"
#             return field_name, "icontains"

#         parts = field_name.split("__")
#         if parts[-1] in self.supported_lookups:
#             return "__".join(parts[:-1]), parts[-1]
#         return field_name, "icontains"

#     def _resolve_field_value(self, obj, field_name):
#         value = obj
#         for part in field_name.split("__"):
#             value = getattr(value, part, None)
#             if value is None:
#                 return None
#         return value

#     def _get_related_search_fields(self, search_fields):
#         related_fields = set()
#         for field_name in search_fields:
#             normalized_field, _ = self._normalize_search_field(str(field_name))
#             parts = normalized_field.split("__")
#             if len(parts) > 1:
#                 related_fields.add("__".join(parts[:-1]))
#         return tuple(sorted(related_fields))
