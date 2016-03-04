from schedule.models import Instrument
from blogs.models import BlogPost
from blogs.views import exclude_posts
from django.shortcuts import render, get_object_or_404

# Create your views here.
def home( request ):
    lastest_blogs = BlogPost.objects.exclude(title__in=exclude_posts).order_by('-pub_date')[:5] 
    return render( request, 'homepages/index.html', {'lastest_blogs': lastest_blogs} )

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
