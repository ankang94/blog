from django.shortcuts import render
from apps.article.models import Article, ArticleGroup
from django.utils.safestring import mark_safe
import datetime
from .utils import parsetitles, Cache, parsetabs, parsesource


# Create your views here.
def article(request, group, index):
    if not Cache().get('titles'):
        Cache('titles', ArticleGroup.objects.all())
    grouoplist = parsetitles(Cache().get('titles'), int(group))
    articles = Article.objects.get(articleid=int(index))

    result = {'title': articles.title,
              'comment': articles.comment,
              'article': mark_safe(articles.context),
              'groupid': articles.group.groupid,
              'date': articles.createdate}

    parsesource(articles, result)
    tabs = parsetabs(Cache().get('titles'), result)
    return render(request, 'page/container.html', {'dict': result, 'titles': grouoplist, 'tabs': tabs})


def catlog(request, qrygroup):
    qrydate = request.GET.get('d')

    catlist = []

    if not qrygroup or not qrygroup.strip():
        qrygroup = 0
    if not Cache().get('titles'):
        Cache('titles', ArticleGroup.objects.all())
    grouoplist = parsetitles(Cache().get('titles'), int(qrygroup))

    if not qrydate:
        catlogs = Article.objects.filter(group__groupid=qrygroup).all()
    else:
        try:
            qrydate = datetime.datetime.strptime(qrydate, '%Y-%m-%d')
            catlogs = Article.objects.filter(group__groupid=qrygroup,
                                             createdate__year=qrydate.year,
                                             createdate__month=qrydate.month,
                                             createdate__day=qrydate.day).all()
        except:
            catlogs = Article.objects.filter(group__comment=qrygroup).all()

    for qrySet in catlogs:
        catlist.append({'title': qrySet.title,
                        'comment': qrySet.comment,
                        'date': qrySet.createdate,
                        'url': '/g/' + str(qrygroup) + '/a/' + str(qrySet.articleid)})

    param = {'groupid': qrygroup}
    if qrydate:
        param['date'] = qrydate
    tabs = parsetabs(Cache().get('titles'), param)
    return render(request, 'page/catlog.html', {'catlog': catlist, 'titles': grouoplist, 'tabs': tabs})
