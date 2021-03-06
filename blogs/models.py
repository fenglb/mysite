import os
import re
import hashlib
from datetime import datetime

from django.db import models
from django.utils import timezone

# for slug, get_absolute_url
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from unidecode import unidecode

# delete md_file before delete/change model
from django.db.models.signals import pre_delete
from django.dispatch import receiver

# get gfm html and store it
import requests
from django.core.files.base import ContentFile
from accounts.models import CustomUser

from datetime import datetime
# tagging
from taggit.managers import TaggableManager
from mistune.markdown_mistune import markdown2html_mistune as md

exclude_category = ("news", "pr", "hot")

upload_dir = 'BlogPost/{0}/{1}'
def get_upload_md_name(instance, filename):
    if instance.pub_date:
        year = instance.pub_date.year   # always store in pub_year folder
    else:
        year = datetime.now().year
    upload_to = upload_dir.format(year, unidecode(instance.title) + '.md')
    return upload_to

def get_html_name(instance, filename):
    if instance.pub_date:
        year = instance.pub_date.year
    else:
        year = datetime.now().year
    upload_to = upload_dir.format(year, filename)
    return upload_to

def get_upload_img_name(instance, filename):
    upload_to = upload_dir.format('images', filename)  # filename involves extension
    return upload_to

class BlogPost(models.Model):

    class Meta:
        ordering = ['-pub_date']    # ordered by pub_date descending when retriving

    CATEGORY_CHOICES = ( 
        (u'nmr', 'NMR'),
        (u'lx', 'Linux/Ubuntu'),
        (u'news', 'News'),
        (u'pr', 'Projects'),
        (u'hot', 'Hot Spot'),
        (u'pl', 'Personal'),
        (u'pg', 'Python/Programming'),
        (u'ot', 'Others' )
        )
    title = models.CharField(max_length=150)
    thumbnail = models.ImageField(upload_to=get_upload_img_name, blank=True)
    body = models.TextField(blank=True)
    md_file = models.FileField(upload_to=get_upload_md_name, blank=True)  # uploaded md file
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    last_edit_date = models.DateTimeField('last edited', auto_now=True)
    slug = models.SlugField(max_length=200, blank=True)
    html_file = models.FileField(upload_to=get_html_name, blank=True)    # generated html file
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    author = models.ManyToManyField( CustomUser )
    tags = TaggableManager() 
    md5  = models.CharField(unique=True, max_length=32, blank=True)

    def __str__(self):
        return self.title

    @property
    def filename(self):
        if self.md_file:
            return os.path.basename(self.title)
        else:
            return 'no md_file'

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.title))
        if not self.body and self.md_file:
            self.body = self.md_file.read()
        if not self.md5:
            md5_model = hashlib.md5()
            md5_str = datetime.now().isoformat() + self.slug
            md5_model.update(md5_str.encode('utf-8'))
            self.md5 = md5_model.hexdigest()
        # generate rendered html file with same name as md
        headers = {'Content-Type': 'text/plain'}

        #self.body = md(self.body) # convert the markdown to html

        if type(self.body) == bytes:  # sometimes body is str sometimes bytes...
            data = self.body
        elif type(self.body) == str:
            data = self.body.encode('utf-8')
        else:
            print("somthing is wrong")

        r = requests.post('https://api.github.com/markdown/raw', headers=headers, data=data)
        html_data = r.content
        if not self.description:
            p = re.compile(r"\<p\>(.*)\<\/p\>")
            m = p.finditer(html_data.decode('utf-8'))
            try: self.description = next(m).groups()[0]
            except StopIteration: self.description = self.body[:200]
        # avoid recursive invoke
        self.html_file.save(self.slug+'.html', ContentFile(html_data), save=False)
        self.html_file.close()

        super(BlogPost, self).save(*args, **kwargs)

    def display_html(self):
        with open(self.html_file.path, encoding='utf-8') as f:
            return f.read()

    def get_absolute_url(self):

        if self.category in exclude_category:
            return reverse('homepages:post', kwargs={'md5': self.md5})
        else:
            return reverse('blogs:blogpost', kwargs={'md5': self.md5})


@receiver(pre_delete, sender=BlogPost)
def blogpost_delete(instance, **kwargs):
    if instance.md_file:
        instance.md_file.delete(save=False)
    if instance.html_file:
        instance.html_file.delete(save=False)

class BlogPostImage(models.Model):

    blogpost = models.ForeignKey(BlogPost, related_name='images')
    image = models.ImageField(upload_to=get_upload_img_name)

