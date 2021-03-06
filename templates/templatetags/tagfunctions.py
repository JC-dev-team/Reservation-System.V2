from django import template
register = template.Library()


@register.filter
def index(indexable, i):
    return indexable[i]

# @register.filter
# def waitingList_Status(status,time_session):

#     if status == 'Day off' and time_session =='Lunch':
#         return '中午店休'
#     elif status == 'Day off' and time_session =='Dinner':
#         return '晚上店休'

@register.filter
def time_session_name(text):
    if text=='Lunch':
        return '午餐'

    elif text=='Dinner':
        return '晚餐'

