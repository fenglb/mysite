from django.shortcuts import render, get_object_or_404
from staffList import Staff

# Create your views here.
def home( request ):
    
    return render( request, 'homepages/index.html' )

def about( request ):

    return render( request, 'homepages/about.html', {'Staff': Staff} )

def labs( request ):
    
    return render( request, 'homepages/labs.html' )

def insts( request ):
    
    return render( request, 'homepages/insts.html' )

def service( request ):
    
    return render( request, 'homepages/service.html' )

def contact( request ):
    
    return render( request, 'homepages/contact.html' )

def appoint( request ):
    
    return render( request, 'homepages/appoint.html' )
