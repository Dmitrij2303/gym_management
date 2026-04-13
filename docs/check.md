| Lookup        | Значение                            | Пример                              | SQL-смысл                   |
| ------------- | ----------------------------------- | ----------------------------------- | --------------------------- |
| `exact`       | равно                               | `name__exact="Ivan"`                | `name = 'Ivan'`             |
| `iexact`      | равно без учёта регистра            | `name__iexact="ivan"`               | case-insensitive equality   |
| `gt`          | больше                              | `price__gt=100`                     | `price > 100`               |
| `gte`         | больше или равно                    | `price__gte=100`                    | `price >= 100`              |
| `lt`          | меньше                              | `price__lt=100`                     | `price < 100`               |
| `lte`         | меньше или равно                    | `price__lte=100`                    | `price <= 100`              |
| `in`          | входит в список                     | `id__in=[1, 2, 3]`                  | `id IN (...)`               |
| `range`       | в диапазоне                         | `price__range=(100, 200)`           | `BETWEEN 100 AND 200`       |
| `isnull`      | `NULL` или нет                      | `comment__isnull=True`              | `comment IS NULL`           |
| `contains`    | содержит подстроку                  | `name__contains="ol"`               | `LIKE '%ol%'`               |
| `icontains`   | содержит без учёта регистра         | `name__icontains="ol"`              | case-insensitive contains   |
| `startswith`  | начинается с                        | `name__startswith="Ol"`             | `LIKE 'Ol%'`                |
| `istartswith` | начинается с без учёта регистра     | `name__istartswith="ol"`            | case-insensitive startswith |
| `endswith`    | заканчивается на                    | `email__endswith=".com"`            | `LIKE '%.com'`              |
| `iendswith`   | заканчивается без учёта регистра    | `email__iendswith=".com"`           | case-insensitive endswith   |
| `date`        | сравнение по дате у `DateTimeField` | `created_at__date=date(2026, 4, 8)` | только дата                 |
| `year`        | год                                 | `created_at__year=2026`             | год из даты                 |
| `month`       | месяц                               | `created_at__month=4`               | месяц из даты               |
| `day`         | день месяца                         | `created_at__day=8`                 | день из даты                |
| `hour`        | час                                 | `created_at__hour=14`               | час из времени              |
| `minute`      | минута                              | `created_at__minute=30`             | минута из времени           |
| `second`      | секунда                             | `created_at__second=0`              | секунда из времени          |
| `week_day`    | день недели                         | `created_at__week_day=2`            | зависит от БД               |
| `regex`       | по regex                            | `name__regex=r"^A.*"`               | regex                       |
| `iregex`      | regex без учёта регистра            | `name__iregex=r"^a.*"`              | case-insensitive regex      |
