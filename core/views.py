from django.shortcuts import render


def home_view(request):
    context = {
        "club_name": "Фитнес-клуб",
    }
    return render(request, "core/home.html", context)
