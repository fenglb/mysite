from collections import defaultdict
from os.path import join

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404

from .models import BlogPost

exclude_posts = ("about", "projects", "talks", )
exclude_category = ("news", "pr", "hot")


# Create your views here.
def home(request, page=''):
    args = dict()
    num = 6
    args['blogposts'] = BlogPost.objects.exclude(title__in=exclude_posts).exclude(category__in=exclude_category)
    max_page = 1.0*len(args['blogposts']) / num 
    if page and int(page) < 2:  # /0, /1 -> /
        return redirect("/blogs/")
    else:
        page = int(page) if (page and int(page) > 0) else 1
        args['page'] = page
        args['prev_page'] = page + 1 if page < max_page else None
        args['newer_page'] = page - 1 if page > 1 else None
        # as template slice filter, syntax: list|slice:"start:end"
        args['sl'] = str(num * (page - 1)) + ':' + str(num * (page - 1) + num)
        return render(request, 'blogs/index.html', args)


def blogpost(request, md5):
    args = {'blogpost': get_object_or_404(BlogPost, md5=md5)}
    return render(request, 'blogs/blogpost.html', args)

def archive(request):
    args = dict()
    blogposts = BlogPost.objects.exclude(title__in=exclude_posts)

    def get_sorted_posts(category):
        posts_by_year = defaultdict(list)
        posts_of_a_category = blogposts.filter(category=category)  # already sorted by pub_date
        for post in posts_of_a_category:
            year = post.pub_date.year
            posts_by_year[year].append(post)
        posts_by_year = sorted(posts_by_year.items(), reverse=True)  # [('2014',post_list), ('2013',post_list)]
        return posts_by_year

    args['data'] = [
        ('NMR', get_sorted_posts("nmr")),
        ('Linux/Ubuntu', get_sorted_posts("lx")),
        ('Personal', get_sorted_posts("pl")),  # no category
        ('Python/Programming', get_sorted_posts("pg")),  # no category
        ('Others', get_sorted_posts("ot")),  # no category
    ]

    return render(request, 'blogs/archive.html', args)


def about(request):
    the_about_post = get_object_or_404(BlogPost, title="about")
    args = {"about": the_about_post}
    return render(request, 'blogs/about.html', args)


def projects(request):
    # use markdown to show projects
    the_projects_post = get_object_or_404(BlogPost, title="projects")
    args = {"projects": the_projects_post}
    return render(request, 'blogs/projects.html', args)


def talks(request):
    # use markdown to show talks, could be changed if need better formatting
    the_talks_post = get_object_or_404(BlogPost, title="talks")
    args = {"talks": the_talks_post}
    return render(request, 'blogs/talks.html', args)


def article(request, freshness):
    """ redirect to article accroding to freshness, latest->oldest:freshness=1->N """
    if freshness.isdigit():
        try:
            article_url = BlogPost.objects.all()[int(freshness) - 1].get_absolute_url()
            return redirect(article_url)
        except IndexError:
            raise Http404
        except AssertionError:  # freshness=0
            raise Http404
    else:
        return redirect('/')
