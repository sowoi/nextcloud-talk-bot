import gettext

_ = gettext.gettext

TRANSLATIONS = {
    "activities": {
        "en": {
            "ACT.EVENT": _("event"),
            "ACT.TODO": _("to-do"),
            "ACT.SHARED": _("Shared"),
            "ACT.FILES": {_("deleted"), _("created"), _("changed")},
        },
        "de": {
            "ACT.EVENT": _("Termin"),
            "ACT.TODO": _("Aufgabe"),
        },
    }
}
