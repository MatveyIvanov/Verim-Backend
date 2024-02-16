import gettext


# TODO: вынести в настройки
DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = ["en", "ru"]
DOMAIN = "base"
LOCALE_DIR = "locale"
_lang = DEFAULT_LANGUAGE


def activate_translation(lang: str):
    global _lang
    _lang = DEFAULT_LANGUAGE if lang not in SUPPORTED_LANGUAGES else lang


def _(message: str) -> str:
    if _lang == DEFAULT_LANGUAGE:
        return message
    return gettext.translation(DOMAIN, localedir=LOCALE_DIR, languages=[_lang]).gettext(
        message
    )


"""
1. python utils/pygettext.py -d base -o locale/base.pot /  FIXME: почему-то нет файла pygettext, пока что используется скопированный из исходников
2. msgmerge locale/ru/LC_MESSAGES/base.po locale/base.pot -U
3. msgfmt -o locale/ru/LC_MESSAGES/base.mo locale/ru/LC_MESSAGES/base
"""
