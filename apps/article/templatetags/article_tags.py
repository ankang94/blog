# _*_ coding:utf-8 _*_
__author__ = 'ankang'
__date__ = '2018/4/19 下午 3:11'

from django import template
from apps.article.models import Article, ArticleGroup, ExtSource
from myWeb.cache import Cache

register = template.Library()


def gettitle():
    if not Cache().get('titles'):
        Cache('titles', ArticleGroup.objects.all())
    return Cache().get('titles')


def gettop():
    if not Cache().get('tops'):
        Cache('tops', Article.objects.order_by('-createdate', '-articleid')[:10])
    return [{'title': item.title,
             'comment': item.comment,
             'date': item.createdate,
             'group': item.group.comment,
             'url': '/g' + str(item.group.groupid) + '/a' + str(item.articleid)} for item in Cache().get('tops')]


def getadpic():
    if not Cache().get('adpic'):
        Cache('adpic', ExtSource.objects.filter(state='A', type='RP'))
    if not Cache().get('adpic'):
        return None
    return [{'title': item.title, 'url': item.path.url} for item in Cache().get('adpic')]


@register.simple_tag
def get_carousel():
    if not Cache().get('carousel'):
        Cache('carousel', ExtSource.objects.filter(state='A', type='CP'))
    if not Cache().get('carousel'):
        return None
    return [{'name': item.title, 'url': item.path.url} for item in Cache().get('carousel')]


@register.inclusion_tag('page/right_bar.html', takes_context=True)
def get_right_bar(context):
    context.update({'top': gettop(), 'adpic': getadpic()})
    return context


@register.inclusion_tag('page/article_list.html', takes_context=True)
def get_article_list(context):
    return context


@register.inclusion_tag('page/article_tabs.html', takes_context=True)
def get_article_tabs(context):
    if 'catlog.html' in context.template.name:
        context.update({'page_type': 'C'})
    return context
