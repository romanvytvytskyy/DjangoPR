# -*- coding: utf-8
from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    category = models.CharField(u'Category',
                                max_length=250, help_text=u'Max 250 symbols'
                                )
    slug = models.SlugField(u'Slug')

    class Meta:
        verbose_name = u'Category for publication'
        verbose_name_plural = u'Category for publication'

    def __str__(self):
        return self.category


class Article(models.Model):
    title = models.CharField(u'Title', max_length=250,
                             help_text=u'Max 250 symbols')
    description = models.TextField(blank=True, verbose_name=u'Description')
    pub_date = models.DateTimeField(
        u'Publication date and time', default=timezone.now)
    slug = models.SlugField(u'Slug', unique_for_date='pub_date')
    main_page = models.BooleanField(
        u'Show on main page', default=False, help_text=u'Show on main page')
    category = models.ForeignKey(
        Category, related_name='articles',
        blank=True,
        null=True,
        verbose_name=u'Category',
        on_delete=models.CASCADE
    )
    object = models.Manager()

    class Meta:
        ordering = ['-pub_date']
        verbose_name = u'Article'
        verbose_name_plural = u'Articles'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        try:
            url = reverse('news-detail', kwargs={
                'year': self.pub_date.strftime('%Y'),
                'month': self.pub_date.strftime('%m'),
                'day': self.pub_date.strftime('%d'),
                'slug': self.slug, })
        except:
            url = '/'
        return url


class ArticleImage(models.Model):
    article = models.ForeignKey(
        Article,
        verbose_name=u'Article',
        related_name='images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(u'Photo', upload_to="photos")
    title = models.CharField(u'Title', max_length=250,
                             blank=True, help_text=u'Max 250 symbols')

    class Meta:
        verbose_name = u'Article image'
        verbose_name_plural = u'Article images'

    def __str__(self):
        return self.title

    @property
    def filename(self):
        return self.image.name.rsplit('/', 1)[-1]
