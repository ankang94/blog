# _*_coding:utf-8_*_
__author__ = 'ankang'
__date__ = '2018/03/31 21:12'

import json
from django.core.paginator import Paginator


# common tools for article

def parsetitles(pset, group=None):
    rlist = []
    plist = []
    raise_flag = True if group else False
    for item in pset:
        param = {'titles': [],
                 'groupid': item.groupid,
                 'comment': item.comment,
                 'parentid': item.parentid,
                 'url': '/g' + str(item.groupid)}
        if item.groupid == group:
            param['state'] = 'active'
            raise_flag = False
        plist.append(param)

    if raise_flag:
        raise ValueError

    for item in plist:
        if item.get('parentid') is None:
            rlist.append(item)

    for item in plist:
        if item in rlist:
            continue
        pitem = finditembyid(rlist, item.get('parentid').groupid)
        if pitem is not None:
            pitem['type'] = 'muilt'
            pitem['titles'].append(item)
            if item.get('state'):
                pitem['comment'] = item['comment']
                pitem['state'] = 'active'

    return rlist


def parsetabs(pset, param):
    tabs = []
    for item in pset:
        if item.groupid == int(param.get('groupid')):
            # find parent node
            tabs.append({'title': item.comment, 'url': '/g' + str(item.groupid)})
            if param.get('date'):
                datetitle = param.get('date').strftime('%Y-%m-%d')
                tabs.append({'title': datetitle, 'url': '/g' + str(item.groupid) + '?d=' + datetitle})
            if param.get('title'):
                tabs.append({'title': param.get('title')})
    return tabs


def parsesource(article, result):
    scriptlist = []
    for relas in article.script.all():
        scriptlist.append({'type': str(relas.type).upper(), 'url': relas.path})

    result['scripts'] = scriptlist

    imageret = {}
    for relas in article.image.all():
        imageret[relas.name] = relas.path.url

    result['image'] = json.dumps(imageret)


def finditembyid(targetlist, targetid):
    for item in targetlist:
        if item.get('groupid') == targetid:
            return item
    return None


def generatepage(catlogs, pid):
    catlist = []
    paginator = Paginator(catlogs, 10)
    catlogs = paginator.page(int(pid))

    pageparam = json.dumps({'current': pid, 'total': paginator.num_pages})

    for qrySet in catlogs:
        catlist.append({'title': qrySet.title,
                        'timg': qrySet.timg.url if qrySet.timg and hasattr(qrySet.timg, 'url') else None,
                        'comment': qrySet.comment,
                        'summary': qrySet.summary,
                        'date': qrySet.createdate,
                        'url': '/g' + str(qrySet.group.groupid) + '/a' + str(qrySet.articleid)})
    return {'list': catlist, 'page': pageparam}
