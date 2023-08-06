from django import template
from django.db.models import Count

from sentry.helpers import get_db_engine
from sentry.plugins import GroupActionProvider

import datetime
try:
    from pygooglechart import SimpleLineChart
except ImportError:
    SimpleLineChart = None

register = template.Library()

@register.filter
def is_dict(value):
    return isinstance(value, dict)

@register.filter
def with_priority(result_list, key='score'):
    if result_list:
        if isinstance(result_list[0], dict):
            _get = lambda x, k: x[k]
        else:
            _get = lambda x, k: getattr(x, k)

        min_, max_ = min([_get(r, key) for r in result_list]), max([_get(r, key) for r in result_list])
        mid = (max_ - min_) / 4
        for result in result_list:
            val = _get(result, key)
            if val > max_ - mid:
                priority = 'veryhigh'
            elif val > max_ - mid * 2:
                priority = 'high'
            elif val > max_ - mid * 3:
                priority = 'medium'
            elif val > max_ - mid * 4:
                priority = 'low'
            else:
                priority = 'verylow'
            yield result, priority

@register.filter
def num_digits(value):
    return len(str(value))

@register.filter
def can_chart(group):
    engine = get_db_engine()
    return SimpleLineChart and not engine.startswith('sqlite')

@register.filter
def chart_url(group):
    today = datetime.datetime.now()

    chart_qs = group.message_set.all()\
                      .filter(datetime__gte=today - datetime.timedelta(hours=24))\
                      .extra(select={'hour': 'extract(hour from datetime)'}).values('hour')\
                      .annotate(num=Count('id')).values_list('hour', 'num')

    rows = dict(chart_qs)
    if rows:
        max_y = max(rows.values())
    else:
        max_y = 1

    chart = SimpleLineChart(300, 80, y_range=[0, max_y])
    chart.add_data([max_y]*30)
    chart.add_data([rows.get((today-datetime.timedelta(hours=d)).hour, 0) for d in range(0, 24)][::-1])
    chart.add_data([0]*30)
    chart.fill_solid(chart.BACKGROUND, 'eeeeee')
    chart.add_fill_range('eeeeee', 0, 1)
    chart.add_fill_range('e0ebff', 1, 2)
    chart.set_colours(['eeeeee', '999999', 'eeeeee'])
    chart.set_line_style(1, 1)
    return chart.get_url()

def sentry_version():
    from sentry import get_version
    return get_version()
register.simple_tag(sentry_version)

@register.filter
def get_actions(group, request):
    action_list = []
    for cls in GroupActionProvider.plugins.itervalues():
        inst = cls(group.pk)
        action_list = inst.actions(request, action_list, group)
    for action in action_list:
        yield action[0], action[1], request.META['PATH_INFO'] == action[1]

@register.filter
def get_panels(group, request):
    panel_list = []
    for cls in GroupActionProvider.plugins.itervalues():
        inst = cls(group.pk)
        panel_list = inst.panels(request, panel_list, group)
    for panel in panel_list:
        yield panel[0], panel[1], request.META['PATH_INFO'] == panel[1]

@register.filter
def get_widgets(group, request):
    for cls in GroupActionProvider.plugins.itervalues():
        inst = cls(group.pk)
        resp = inst.widget(request, group)
        if resp:
            yield resp

@register.filter
def get_tags(group, request):
    tag_list = []
    for cls in GroupActionProvider.plugins.itervalues():
        inst = cls(group.pk)
        tag_list = inst.tags(request, tag_list, group)
    for tag in tag_list:
        yield tag

@register.filter
def timesince(value):
    from django.template.defaultfilters import timesince
    if not value:
        return 'Never'
    if value < datetime.datetime.now() - datetime.timedelta(days=5):
        return value.date()
    value = (' '.join(timesince(value).split(' ')[0:2])).strip(',')
    if value == '0 minutes':
        return 'Just now'
    if value == '1 day':
        return 'Yesterday'
    return value + ' ago'