import ws_grek
import ws_latn

def transliterate_name(lang, name_utf8):
    """Transliterate Greek or Latin into modern Roman."""
    wsystem = lang.lower()
    if isinstance(name_utf8, unicode):
        name = name_utf8[:]
    else:
        name = unicode(name_utf8, 'utf-8')
    if wsystem == 'grc' or wsystem == 'la-grek':
        transliteration = ws_grek.transliterate(name)
    elif wsystem == 'la' or wsystem == 'grc-latn':
        transliteration = ws_latn.transliterate(name)
    else:
        raise ValueError, 'Unsupported writing system (%s)' % lang
    return transliteration
    