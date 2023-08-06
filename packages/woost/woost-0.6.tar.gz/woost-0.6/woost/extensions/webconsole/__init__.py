#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from pkg_resources import resource_filename
import cherrypy
from cocktail import schema
from cocktail.events import event_handler
from cocktail.translations import translations
from woost.models import (
    Site,
    Extension,
    Role,
    Document,
    Controller,
    Template
)

translations.define("WebConsoleExtension",
    ca = u"Intèrpret de Python",
    es = u"Intérprete de Python",
    en = u"Python interpreter"
)

translations.define("WebConsoleExtension-plural",
    ca = u"Intèrpret de Python",
    es = u"Intérprete de Python",
    en = u"Python interpreter"
)

class WebConsoleExtension(Extension):

    def __init__(self, **values):
        Extension.__init__(self, **values)
        self.extension_author = u"Whads/Accent SL"
        self.set("description",
            u"""Proporciona accés directe a l'intèrpret de Python en que
            s'executa l'aplicació a través de la web""",
            "ca"
        )
        self.set("description",            
            u"""Proporciona acceso directo al intérprete de Python que ejecuta
            la aplicación a través de la web""",
            "es"
        )
        self.set("description",
            u"""Provides a web interface to access the Python interpreter that
            the application runs on""",
            "en"
        )

    @event_handler
    def handle_loading(cls, event):

        extension = event.source

        from woost.extensions.webconsole import strings
        from woost.controllers import CMS

        CMS.ApplicationContainer.webconsole_resources = \
            cherrypy.tools.staticdir.handler(
                section = "webconsole_resources",
                dir = resource_filename("webconsole", "resources")
            )
        
        if not extension.installed:
            
            def apply_translations(item, member):
                for lang in translations:
                    trans = translations("%s.%s" % (item.qname, member), lang)
                    if trans:
                        item.set(member, trans, lang)

            # Permissions: by default, only administrators can use the web
            # console
            from woost.extensions.webconsole.webconsolepermission \
                import WebConsolePermission

            administrators = Role.get_instance(qname = "woost.administrators")

            if administrators:
                web_console_permission = WebConsolePermission()
                web_console_permission.insert()
                administrators.permissions.append(web_console_permission)

            # Controller
            controller = Controller()
            controller.qname = "woost.extensions.webconsole.controller"
            controller.python_name = \
                "woost.extensions.webconsole.cmswebconsole.CMSWebConsole"
            apply_translations(controller, "title")
            controller.insert()

            # Template
            template = Template()
            template.qname = "woost.extensions.webconsole.template"
            template.engine = "cocktail"
            template.identifier = "webconsole.WebConsole"
            apply_translations(template, "title")
            template.insert()

            # Page
            page = Document()
            page.qname = "woost.extensions.webconsole.page"
            page.parent = Site.main.home
            page.path = "webconsole"
            page.hidden = True
            page.requires_https = True
            page.controller = controller
            page.template = template
            page.per_language_publication = False
            apply_translations(page, "title")
            page.insert()


def breakpoint(open_browser = False, stack_depth = 0):
    """Set a `~webconsole.utils.breakpoint` that is only triggered by users
    with `code execution rights <WebConsolePermission>`.
    """
    from cocktail.controllers import Location
    from webconsole.utils import breakpoint as webconsole_breakpoint
    from woost.models import get_current_user, Publishable, Site
    from woost.extensions.webconsole.webconsolepermission \
        import WebConsolePermission   

    user = get_current_user()

    if user and user.has_permission(WebConsolePermission):

        def initializer(session):
            if open_browser:
                
                # Find the web console document
                webconsole = Publishable.require_instance(
                    qname = "woost.extensions.webconsole.page"
                )
                
                # Determine the URI for the breakpoint session
                webconsole_location = Location.get_current_host()
                webconsole_location.path_info = \
                    u"/" + Site.main.get_path(webconsole)
                webconsole_location.query_string["session_id"] = session.id

                # Open a web browser tab pointing at the URI
                from webbrowser import open
                open(str(webconsole_location))
        
        return webconsole_breakpoint(
            initializer = initializer,
            stack_depth = stack_depth + 1
        )

