from schedule.models import Instrument
from blogs.models import BlogPost
from schedule.models import Instrument
from accounts.models import CustomUser
from blogs.views import exclude_posts
from django.shortcuts import render, get_object_or_404

# Create your views here.
def home( request ):
    lastest_blogs = BlogPost.objects.exclude(title__in=exclude_posts).filter(category='nmr').order_by('-pub_date')[:5] 
    lastest_news = BlogPost.objects.exclude(title__in=exclude_posts).filter(category='news').order_by('-pub_date')[:5] 
    projects = BlogPost.objects.exclude(title__in=exclude_posts).filter(category='pr')
    instruments = Instrument.objects.all()
    hot_spots = BlogPost.objects.exclude(title__in=exclude_posts).filter(category='hot')

    staffs = CustomUser.objects.filter( is_staff=True )
    return render( request, 'homepages/index.html', {'lastest_blogs': lastest_blogs, 'lastest_news': lastest_news, 'projects': projects, 'instruments': instruments, 'staffs': staffs, 'hot_spots': hot_spots } )

def post(request, md5):
    args = {'blogpost': get_object_or_404(BlogPost, md5=md5)}
    return render(request, 'blogs/blogpost.html', args)

def about( request ):

    return render( request, 'homepages/about.html' )

def labs( request ):
    
    return render( request, 'homepages/labs.html' )

def insts( request ):
    instruments = Instrument.objects.all()
    return render( request, 'homepages/insts.html', {'instruments': instruments} )

def service( request ):
    
    return render( request, 'homepages/service.html' )

def contact( request ):
    
    return render( request, 'homepages/contact.html' )

def appoint( request ):
    instruments = Instrument.objects.all()
    return render( request, 'homepages/appoint.html', {'instruments': instruments,} )

def map(request):
    return render(request, 'homepages/map.html')
