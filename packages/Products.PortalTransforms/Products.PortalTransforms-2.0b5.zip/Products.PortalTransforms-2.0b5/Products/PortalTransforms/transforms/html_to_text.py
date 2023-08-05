from Products.PortalTransforms.libtransforms.retransform import retransform

import htmlentitydefs

class html_to_text(retransform):
    inputs  = ('text/html',)
    output = 'text/plain'

def register():
    def sub_func(matchobj):
        full = matchobj.group()
        ent = matchobj.group(1)
        result = htmlentitydefs.name2codepoint.get(ent)
        if result is None:
            if ent.startswith('#'):
                return unichr(int(ent[1:])).encode('utf-8')
            else:
                return full
        else:
            return unichr(result).encode('utf-8')

    return html_to_text("html_to_text",
                       ('<script [^>]>.*</script>(?im)', ' '),
                       ('<style [^>]>.*</style>(?im)', ' '),
                       ('<head [^>]>.*</head>(?im)', ' '),
                       ('(?im)</?(font|em|i|strong|b)(?=\W)[^>]*>', ''),
                       ('<[^>]*>(?i)(?m)', ' '),
                       (r'&([a-zA-Z0-9#]*?);', sub_func),
                       )
