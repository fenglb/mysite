from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from eguard.models import Entrance, EntranceAppointment

# Create your views here.

@login_required
def dealAppoint(request):
    if request.method == 'POST':
        appointment = get_object_or_404(EntranceAppointment, id=request.POST['entrance'])
        appointment.feedback = request.POST['feedback']
        appointment.has_approved = request.POST['check']
        appointment.save()

    return redirect( reverse("accounts:profile") )
