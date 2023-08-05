def _ugly_utf8_string_hack(item):
    """hands back a unicoded string"""
    # this is backward compat for handling non-utf8 filenames 
    # and content inside packages. :(
    # content that xml can cope with but isn't really kosher

    # if we're anything obvious - do them first
    if item is None:
        return ''
    elif isinstance(item, unicode):    
        return item
    
    # this handles any bogon formats we see
    du = False
    try:
        x = unicode(item, 'ascii')
        du = True
    except UnicodeError:
        encodings = ['utf-8', 'iso-8859-1', 'iso-8859-15', 'iso-8859-2']
        for enc in encodings:
            try:
                x = unicode(item, enc)
            except UnicodeError:
                pass
                
            else:
                if x.encode(enc) == item:
                    if enc != 'utf-8':
                        print '\n%s encoding on %s\n' % (enc, item)
                    return x.encode('utf-8')
    
    
    # Kill bytes (or libxml will die) not in the small byte portion of:
    #  http://www.w3.org/TR/REC-xml/#NT-Char
    # we allow high bytes, if it passed the utf8 check above. Eg.
    # good chars = #x9 | #xA | #xD | [#x20-...]
    newitem = ''
    bad_small_bytes = range(0, 8) + [11, 12] + range(14, 32)
    for char in item:
        if ord(char) in bad_small_bytes:
            pass # Just ignore these bytes...
        elif not du and ord(char) > 127:
            newitem = newitem + '?' # byte by byte equiv of escape
        else:
            newitem = newitem + char
    return newitem

def to_xml(item, attrib=False):
    import xml.sax.saxutils
    item = _ugly_utf8_string_hack(item)
    item = to_utf8(item)
    item = item.rstrip()
    if attrib:
        item = xml.sax.saxutils.escape(item, entities={'"':"&quot;"})
    else:
        item = xml.sax.saxutils.escape(item)
    return item
