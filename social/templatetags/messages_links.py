from django import template
from django.utils.html import escape
from django.utils.encoding import force_text, smart_text

register = template.Library()

@register.filter()
def generate_links(value):
    hashtags = [word for word in value.split(" ") if len(word) and word[0] == "#"]
    mentions = [mention for mention in value.split(" ") if len(mention) and mention[0] == "@"]

    value = escape(value)

    for i in hashtags:
        value = value.replace(i, "<a href='/t/" + str(i[1:]) + "'>" + str(i) + "</a>")

    for i in mentions:
        value = value.replace(i, "<a href='/u/" + str(i[1:]) + "'>" + str(i) + "</a>")

    return value
