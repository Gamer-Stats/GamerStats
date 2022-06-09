from django import template
import os
from django.utils.http import urlencode

register = template.Library()


@register.filter
def pcspecs(tag):
    tag = "/pc-specs/" + tag + "/"
    return tag


@register.filter
def game_url(tag):
    tag = "/pc-specs/games/" + tag + "/"
    return tag


@register.filter
def team_url(tag):
    tag = "/pc-specs/teams/" + tag + "/"
    return tag


@register.filter
def s_news(tag):
    tag = "/news/" + tag + "/"
    return tag


# Image urls


@register.filter
def img_url(tag):
    newimg = os.path.splitext(os.path.basename(tag))
    newimg = """
    <picture>
        <source
        media='(min-width: 586px)'
        srcset='/media/profiles/webp/200/{0}.webp, /media/profiles/webp/400/{0}.webp 2x'>
        <source
        media='(min-width: 586px)'
        srcset='/media/profiles/jpeg/200/{0}.jpeg, /media/profiles/jpeg/400/{0}.jpeg 2x'>
        <source
        media='(max-width: 585px)'
        srcset='/media/profiles/webp/156/{0}.webp, /media/profiles/webp/312/{0}.webp 2x'>
        <source
        media='(max-width: 585px)'
        srcset='/media/profiles/jpeg/156/{0}.jpeg, /media/profiles/jpeg/312/{0}.jpeg 2x'>
        <img
        class='card-image'
        src='{1}'
        alt="{0} Setup" />
    </picture>
    """.format(
        newimg[0], tag
    )
    return newimg


@register.filter
def team_img_url(tag):
    newimg = os.path.splitext(os.path.basename(tag))
    newimg = """
    <picture>
        <source
        media='(min-width: 1px)'
        srcset='/media/teams/main/webp/156/{0}.webp, /media/teams/main/webp/312/{0}.webp 2x'>
        <source
        media='(min-width: 1px)'
        srcset='/media/teams/main/png/156/{0}.png, /media/teams/main/png/312/{0}.png 2x'>
        <img
        class='card-image'
        src='{1}'
        alt="{0} Logo" />
    </picture>
    """.format(
        newimg[0], tag
    )
    return newimg


@register.filter
def game_img_url(tag):
    newimg = os.path.splitext(os.path.basename(tag))
    newimg = """
    <picture>
        <source
        media='(min-width: 1px)'
        srcset='/media/games/main/webp/208/{0}.webp, /media/games/main/webp/416/{0}.webp 2x'>
        <source
        media='(min-width: 1px)'
        srcset='/media/games/main/jpeg/156/{0}.jpeg, /media/games/main/jpeg/312/{0}.jpeg 2x'>
        <img
        class='card-image'
        src='{1}'
        alt="{0} Game Banner" />
    </picture>
    """.format(
        newimg[0], tag
    )
    return newimg


@register.filter
def img_specs_url(tag):
    newimg = os.path.splitext(os.path.basename(tag))
    newimg = """
    <picture>
        <source
        media='(min-width: 786px)'
        srcset='/media/specs/webp/180/{0}.webp, /media/specs/webp/260/{0}.webp 1.4x'>
        <source
        media='(min-width: 786px)'
        srcset='/media/specs/png/180/{0}.png, /media/specs/png/260/{0}.png 2x'>
        <source
        media='(max-width: 786px)'
        srcset='/media/specs/webp/134/{0}.webp, /media/specs/webp/260/{0}.webp 2x'>
        <source
        media='(max-width: 786px)'
        srcset='/media/specs/png/134/{0}.png, /media/specs/png/260/{0}.png 1.9x'>
        <img
        class='card-image'
        src='{1}'
        alt="{0}" />
    </picture>
    """.format(
        newimg[0], tag
    )
    return newimg


# Share URLS


@register.filter
def reddit(tag, title):
    name = os.path.basename(os.path.abspath(tag)) + " "
    tag = (
        "https://www.reddit.com/submit?"
        + urlencode({"url": tag})
        + "&"
        + urlencode({"title": name + title + "GamerStats.net"})
    )
    return tag


@register.filter
def twitter(tag, title):
    name = os.path.basename(os.path.abspath(tag)) + " "
    tag = (
        "https://twitter.com/intent/tweet?"
        + urlencode({"text": tag})
        + "&"
        + urlencode({"title": name + title + "@TheGamerStats"})
    )
    return tag


@register.filter
def fb(tag, title):
    name = os.path.basename(os.path.abspath(tag)) + " "
    tag = (
        "https://www.facebook.com/dialog/share?app_id=360275042692796"
        + "&"
        + urlencode({"href": tag})
        + "&"
        + urlencode({"quote": name + title + "@GamerStats"})
    )
    return tag


@register.filter
def vk(tag, title):
    name = os.path.basename(os.path.abspath(tag)) + " "
    tag = (
        "https://vk.com/share.php?"
        + "&"
        + urlencode({"url": tag})
        + "&"
        + urlencode({"comment": name + title + "@thegamerstats"})
    )
    return tag


@register.filter
def telegram(tag, title):
    name = os.path.basename(os.path.abspath(tag)) + " "
    tag = (
        "https://t.me/share/url?"
        + "&"
        + urlencode({"url": tag})
        + "&"
        + urlencode({"text": name + title + "- Gamer Stats"})
    )
    return tag


# New Share URLS


@register.filter
def redditNews(tag, title):
    tag = (
        "https://www.reddit.com/submit?"
        + urlencode({"url": tag})
        + "&"
        + urlencode({"title": title + " - GamerStats.net"})
    )
    return tag


@register.filter
def twitterNews(tag, title):
    tag = (
        "https://twitter.com/intent/tweet?"
        + urlencode({"text": tag})
        + "&"
        + urlencode({"title": title + " @TheGamerStats"})
    )
    return tag


@register.filter
def fbNews(tag, title):
    tag = (
        "https://www.facebook.com/dialog/share?app_id=360275042692796"
        + "&"
        + urlencode({"href": tag})
        + "&"
        + urlencode({"quote": title + " @GamerStats"})
    )
    return tag


@register.filter
def vkNews(tag, title):
    tag = (
        "https://vk.com/share.php?"
        + "&"
        + urlencode({"url": tag})
        + "&"
        + urlencode({"comment": title + " @thegamerstats"})
    )
    return tag


@register.filter
def telegramNews(tag, title):
    tag = (
        "https://t.me/share/url?"
        + "&"
        + urlencode({"url": tag})
        + "&"
        + urlencode({"text": title + " - Gamer Stats"})
    )
    return tag
