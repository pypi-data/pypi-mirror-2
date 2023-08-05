# pylint: disable-msg=W0622,C0103
"""apycotbot packaging information"""

distname = "apycotbot"
modname = "apycotbot"
license = 'GPL'

numversion = (1, 9, 0)
version = '.'.join(str(num) for num in numversion)

author = "Logilab"
author_email = "contact@logilab.fr"
description = "Apycot bot client dedicated to launch test suites"
web = 'http://www.logilab.org/project/apycot'

install_requires = ['cubicweb-apycot >= %s' % version,
                    'logilab-common >= 0.50.0',
                    'logilab-devtools',
                    ]


from os.path import join
scripts = (join('bin', 'apycotbot'),
           join('bin', 'apycotclient'))
