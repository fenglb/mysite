from schedule.models import Instrument
from django.shortcuts import render, get_object_or_404

# Create your views here.
def home( request ):
    
    return render( request, 'homepages/index.html' )

def about( request ):

    return render( request, 'homepages/about.html' )

def labs( request ):
    
    return render( request, 'homepages/labs.html' )

def insts( request ):
    
    return render( request, 'homepages/insts.html' )

def service( request ):
    
    return render( request, 'homepages/service.html' )

def contact( request ):
    
    return render( request, 'homepages/contact.html' )

def appoint( request ):
    instruments = Instrument.objects.all()
    return render( request, 'homepages/appoint.html', {'instruments': instruments,} )
