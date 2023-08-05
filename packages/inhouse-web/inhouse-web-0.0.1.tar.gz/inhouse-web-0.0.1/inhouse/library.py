# -*- coding: utf-8 -*-

import calendar
import cgi
import datetime
import decimal
import logging
import re

from django import template
from django.contrib.auth.models import User
from django.core.cache import cache
from django.forms import BaseForm, Form
from django.forms.forms import NON_FIELD_ERRORS
from django.forms.util import ErrorDict
from django.utils.html import mark_safe
from django.utils.translation import ugettext as _

from models import Account, Booking

register = template.Library()

@register.filter
def format_errors(form, non_field_msg=_(u'General errors')):
    class FormError: object
    field_msg = _(u'Field errors')
    retval = FormError()
    if not isinstance(form, BaseForm):
        return retval
    retval.non_field_errors = ErrorDict()
    retval.field_errors = ErrorDict()
    #retval[field_msg] = []
    #retval[non_field_msg] = []
    for field, errors in form.errors.iteritems():
        if field == NON_FIELD_ERRORS:
            #key = non_field_msg
            #retval[non_field_msg].append(errors)
            retval.non_field_errors[non_field_msg] = errors
        else:
            retval.field_errors[form.fields[field].label] = errors
            #key = form.fields[field].label
            #key = field_msg
            #retval[key].append([form.fields[field].label, errors])
            #retval[field_msg].append(errors)
        #retval[key].append(errors)
    return retval


@register.filter
def format_minutes_to_time(val):
    """Formates minutes as decimal to a hour string.

    :param val:

    :returns: String formatted time in MM:HH
    """
    if not val:
        return ''
    h = int(val / 60)
    m = int(val % 60)
    return u'%02i:%02i' % (h, m)


@register.filter
def nickname(user):
    """Returns either the user first and last name or the login name."""
    if user.first_name and user.last_name:
        return u'%s %s' % (user.first_name, user.last_name)
    else:
        return user.username


@register.filter
def show_booking_link(booking_id):
    """Display a booking (edit) link with a tooltip."""
    ret = cache.get('booking:%d' % booking_id)
    if ret is None:
        logging.debug("Missing cache entry for booking:%d", booking_id)
        booking = Booking.get_by_id(booking_id)
        ret = ("""<a onmouseover="JS_showInfoPopup(this, 'bookingPopupDiv', "
        'edit', '/booking_popup/')" href="/time/edit/%(id)d">%(title)s</a>"""
               % {'id': booking.id, 'title': cgi.escape(booking.get_title())})
        cache.set('booking:%d' % booking_id, ret)
    return mark_safe(ret)


@register.filter
def show_user_link(user_id):
    ret = cache.get('user:%d' % user_id)
    if ret is None:
        logging.debug('Missing cache entry for user:%d', user_id)
        user = User.objects.filter(id=user_id)[0]
        account = Account.get_account_for_user(user)
        ret = ("""<a onmouseover="JS_showInfoPopup(this, 'userPopupDiv', 'mailto', '/user_popup/')"
        href="/user/%(id)s">%(name)s</a>"""
               % {'id': user.id, 'name': cgi.escape(account.nickname)})
        cache.set('user:%d' % user_id, ret)
    return mark_safe(ret)


P_DAY_URL = re.compile(r"""^time/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d+)/$""")

@register.tag(name='get_calendar')
def do_calendar(parser, token):
    syntax_help = 'syntax should be \'get_calendar for <month> <year> as <var_name>\''
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, '%r tag requires arguments, %s' \
              % (token.contents.split()[0], syntax_help)
    m = re.search(r'as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, '%r tag had invalid arguments, %s' \
              % (tag_name, syntax_help)
    return CalendarNode(*m.groups())


class Calendar(object):

    def __init__(self, month, year):
        self.month = month
        self.year = year
        self.data = None
        self.plugins = []
        self.weekdays = []
        self.months = []
        self.years = []

    def _set_month(self, val):
        assert isinstance(val, (int, long))
        assert val > 0 and val < 13
        self._month = val

    def _get_month(self):
        return self._month

    def _set_year(self, val):
        assert isinstance(val, (int, long))
        self._year = val

    def _get_year(self):
        return self._year

    month = property(_get_month, _set_month)
    year = property(_get_year, _set_year)

    def get_previous_date(self):
        m = (self.month - 1) or 12
        y = self.year
        if m == 12:
            y -= 1
        return datetime.date(y, m, 1)

    def get_next_date(self):
        m = self.month
        y = self.year
        if m + 1 > 12:
            m = 1
            y += 1
        else:
            m += 1
        return datetime.date(y, m, 1)

    def set_data(self):
        today = datetime.date.today()
        cal = calendar.Calendar()
        first_date = today - datetime.timedelta(days=today.weekday())
        for i in range(0, 7):
            self.weekdays.append([i, first_date + datetime.timedelta(days=i)])
        for i in range(1, 13):
            self.months.append([i, datetime.date(self.year, i, 1)])
        for i in range(today.year - 5, today.year + 6):
            self.years.append([i, str(i)])
        self.data = cal.monthdatescalendar(self.year,  self.month)


class CalendarNode(template.Node):

    def __init__(self, var_name):
        self.var_name = var_name

    def render(self, context):
        today = datetime.date.today()
        request = template.Variable('request').resolve(context)
        month = int(request.session['calendar_month'])
        year = int(request.session['calendar_year'])
        context['selected_month'] = datetime.date(year, month, 1)
        cal = Calendar(month, year)
        cal.set_data()
        context[self.var_name] = cal
        selected_day = None
        m = P_DAY_URL.match(request.path[1:])
        if m:
            # Restrieve the selected day from then URL path
            year = int(m.group(1))
            month = int(m.group(2))
            day = int(m.group(3))
            selected_day = datetime.date(year, month, day)
        context['selected_day'] = selected_day
        context['next'] = cal.get_next_date()
        context['prev'] = cal.get_previous_date()
        return ''
