# -*- coding: utf-8 -*-
from restkit.ext.wsgi_proxy import HostProxy
from saladier import Saladier
from salade import Salade
import os

def make_rewrite(global_config, **local_config):
    if 'theme' not in local_config:
        local_config['theme'] = os.path.join(os.path.dirname(__file__), 'theme.html')
    uri = local_config.get('uri')
    if 'salade' not in local_config:
        class SimpleSalade(Salade):
            uri = local_config.get('uri')
            def __call__(self):
                self.standard_rules()
                self.theme('body').append(self.content('body > *'))
                if self.uri:
                    def link_repl(link):
                        script_name = '%s/' % self.request.script_name
                        if link.startswith(self.uri):
                            return link.replace(self.uri, script_name)
                        elif link.startswith('/'):
                            return script_name.rstrip('/') + link
                        else:
                            return link
                    self.theme[0].rewrite_links(link_repl)
                self.rewrite_links()
                return self.theme
        local_config['salade'] = SimpleSalade
    app = HostProxy(uri=uri, allowed_methods=['GET', 'HEAD', 'POST'])
    return Saladier(app, **local_config)
