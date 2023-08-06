#-*- coding: utf-8 -*-
u"""An extension that improves the integration with Facebook of documents
published with Woost.

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.events import event_handler
from cocktail.translations import translations
from cocktail import schema
from cocktail.html import templates
from cocktail.persistence import datastore
from woost.models import Extension, File


translations.define("OpenGraphExtension",
    ca = u"OpenGraph",
    es = u"OpenGraph",
    en = u"OpenGraph"
)

translations.define("OpenGraphExtension-plural",
    ca = u"OpenGraph",
    es = u"OpenGraph",
    en = u"OpenGraph"
)

translations.define("OpenGraphExtension.open_graph",
    ca = u"Integració amb OpenGraph/Facebook",
    es = u"Integración con OpenGraph/Facebook",
    en = u"OpenGraph/Facebook integration"
)

translations.define("OpenGraphExtension.site_name",
    ca = u"Nom del lloc web",
    es = u"Nombre del sitio web",
    en = u"Website name"
)

translations.define("OpenGraphExtension.site_image",
    ca = u"Imatge del lloc web",
    es = u"Imagen del sitio web",
    en = u"Website image"
)

translations.define("OpenGraphExtension.facebook_administrators",
    ca = u"Comptes de Facebook dels administradors",
    es = u"Cuentas de Facebook de los administradores",
    en = u"Facebook administrator accounts"
)

translations.define("OpenGraphExtension.facebook_applications",
    ca = u"Comptes d'aplicació de Facebook",
    es = u"Cuentas de aplicación de Facebook",
    en = u"Facebook application accounts"
)

translations.define("OpenGraphExtension.email",
    ca = u"Correu electrònic",
    es = u"Correo electrónico",
    en = u"Email address"
)

translations.define("OpenGraphExtension.phone_number",
    ca = u"Número de telèfon",
    es = u"Número de teléfono",
    en = u"Phone number"
)

translations.define("OpenGraphExtension.fax_number",
    ca = u"Número de fax",
    es = u"Número de fax",
    en = u"Fax number"
)


class OpenGraphExtension(Extension):

    members_order = [
        "site_name",
        "site_image",
        "email",
        "phone_number",
        "fax_number",
        "facebook_administrators",
        "facebook_applications"
    ]

    site_name = schema.String(
        required = True,
        member_group = "open_graph"
    )

    site_image = schema.Reference(
        required = True,
        type = File,
        related_end = schema.Collection(),
        member_group = "open_graph"
    )

    email = schema.String(
        member_group = "open_graph"        
    )

    phone_number = schema.String(
        member_group = "open_graph"
    )

    fax_number = schema.String(
        member_group = "open_graph"
    )

    facebook_administrators = schema.String(
        listed_by_default = False,
        searchable = False,
        member_group = "open_graph"
    )

    facebook_applications = schema.String(
        listed_by_default = False,
        searchable = False,
        member_group = "open_graph"
    )

    def __init__(self, **values):
        Extension.__init__(self, **values)
        self.extension_author = u"Whads/Accent SL"
        self.set("description",
            u"""Millora la integració dels documents del lloc web amb Facebook
            i altres serveis que implementin el protocol OpenGraph""",
            "ca"
        )
        self.set("description",            
            u"""Mejora la integración de los documentos del sitio web con
            Facebook y otros servicios que utilicen el protocolo OpenGraph""",
            "es"
        )
        self.set("description",
            u"""Improves the integration of the site's documents with Facebook
            and any other service that makes use of the OpenGraph protocol""",
            "en"
        )

    @event_handler
    def handle_loading(cls, event):

        from woost.extensions.opengraph import (
            strings, 
            publishable,
            opengraphtype,
            opengraphcategory
        )

        OpenGraphExtension.add_member(
            schema.Collection("categories",
                items = schema.Reference(
                    type = opengraphcategory.OpenGraphCategory
                ),
                related_end = schema.Collection(),
                member_group = "open_graph"
            )
        )

        # Install an overlay to BaseView to automatically add OpenGraph
        # metadata to HTML documents
        templates.get_class("woost.extensions.opengraph.BaseViewOverlay")

        if not event.source.installed:
            event.source.create_default_categories(verbose = True)

    def create_default_categories(self, verbose = False):
        
        from woost.extensions.opengraph.opengraphtype import OpenGraphType
        from woost.extensions.opengraph.opengraphcategory \
            import OpenGraphCategory

        for category_id, type_ids in (
            ("activities", (
                "activity",
                "sport"
            )),
            ("businesses", (
                "bar",
                "company",
                "cafe",
                "hotel",
                "restaurant"
            )),
            ("groups", (
                "cause",
                "sports_league",
                "sports_team"
            )),
            ("organizations", (
                "band",
                "government",
                "non_profit",
                "school",
                "university"
            )),
            ("people", (
                "actor",
                "athlete",
                "author",
                "director",
                "musician",
                "politician",
                "profile",
                "public_figure"
            )),
            ("places", (
                "city",
                "country",
                "landmark",
                "state_province"
            )),
            ("products_and_entertainment", (
                "album",
                "book",
                "drink",
                "food",
                "game",
                "movie",
                "product",
                "song",
                "tv_show"
            )),
            ("websites", (
                "article",
                "blog",
                "website"
            ))
        ):
            # Create the category
            og_category = OpenGraphCategory.get_instance(code = category_id)

            if og_category is None:
                
                if verbose:
                    print "Creating OpenGraph category '%s'" % category_id

                og_category = OpenGraphCategory()
                og_category.code = category_id
                og_category.insert()
                
                key = "opengraph.categories." + category_id
                
                for language in translations:
                    label = translations(key, language)
                    if label:
                        og_category.set("title", label, language)

            # Create all types in the category
            types = []

            for type_id in type_ids:
                og_type = OpenGraphType.get_instance(code = type_id)

                if og_type is None:
                    
                    if verbose:
                        print "Creating OpenGraph type '%s.%s'" % (
                            category_id,
                            type_id
                        )

                    og_type = OpenGraphType()
                    og_type.code = type_id
                    og_type.insert()
                    
                    key = "opengraph.types." + type_id

                    for language in translations:
                        label = translations(key, language)
                        if label:
                            og_type.set("title", label, language)

                types.append(og_type)

            og_category.types = types

    def get_global_properties(self):

        properties = {
            "og:site_name": self.site_name
        }

        if self.site_image:
            properties["og:image"] = self.site_image.get_uri(host = ".")

        if self.email:
            properties["og:email"] = self.email

        if self.phone_number:
            properties["og:phone_number"] = self.phone_number

        if self.fax_number:
            properties["og:fax_number"] = self.fax_number

        if self.facebook_administrators:
            properties["fb:admins"] = self.facebook_administrators

        if self.facebook_applications:
            properties["fb:app_id"] = self.facebook_applications

        return properties

    def get_properties(self, publishable):
        properties = self.get_global_properties()
        properties.update(publishable.get_open_graph_properties())
        return properties

