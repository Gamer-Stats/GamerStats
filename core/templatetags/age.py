from django import template
import datetime

register = template.Library()


# Converts Date into Time Left
@register.filter
def article_age(tag):
    tag = tag.timestamp()
    today = datetime.datetime.today()
    epoch_today = today.timestamp()
    secs = epoch_today - tag
    mins = (epoch_today / 60) - (tag / 60)
    hours = mins / 60
    days = hours / 24
    if days >= 1:
        if days < 2:
            return "{0} day ago".format(int(days))
        else:
            return "{0} days ago".format(int(days))
    else:
        if hours >= 1 and hours < 2:
            return "{0} hour ago".format(int(hours))
        elif hours >= 2:
            return "{0} hours ago".format(int(hours))
        elif mins > 2:
            return "{0} minutes ago".format(int(mins))
        elif mins > 1:
            return "{0} minute ago".format(int(mins))
        else:
            return "{0} seconds ago".format(int(secs))
    # if mins < 60:
    #     return "{0} minutes ago".format(int(mins))
    # elif hours >= 1 and mins < 61:
    #     return "{0} hour ago".format(int(hours))
    # elif hours > 1 and hours < 2:
    #     return "{0} hour and {1} minutes ago".format(int(hours), int(mins))
    # elif hours > 2:
    #     return "{0} hours and {1} minutes ago".format(int(hours), int(mins))
