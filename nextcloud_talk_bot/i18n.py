# i18n.py
import gettext

locale_path = "../locales"
supported_languages = ["de", "fr", "es"]
translation = gettext.translation(
    "NextcloudTalkBot",
    localedir=locale_path,
    languages=supported_languages,
    fallback=True)
_ = translation.gettext
