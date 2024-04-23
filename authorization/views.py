from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authorization.forms import SignupForm


def user_registration(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse('events-list'))

    else:
        form = SignupForm()
    context = {"form": form, 'title': 'Registration', 'button': 'Register'}
    return render(request, "registration.html", context)
