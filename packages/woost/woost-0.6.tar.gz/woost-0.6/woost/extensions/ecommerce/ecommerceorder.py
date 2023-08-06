#-*- coding: utf-8 -*-
"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			September 2009
"""
from decimal import Decimal
from cocktail.translations import get_language, translations
from cocktail import schema
from woost.models import (
    Item,
    Site,
    User,
    get_current_user
)
from woost.extensions.locations.location import Location
from woost.extensions.ecommerce.ecommercebillingconcept \
    import ECommerceBillingConcept

def _translate_amount(amount, language = None, **kwargs):
    if amount is None:
        return "" 
    else:
        return translations(
            amount.quantize(Decimal("1.00")),
            language,
            **kwargs
        )


class ECommerceOrder(Item):

    members_order = [
        "customer",
        "address",
        "town",
        "region",
        "country",
        "postal_code",
        "language",
        "status",
        "purchases",
        "total_price",
        "pricing",
        "total_shipping_costs",
        "shipping_costs",
        "total_taxes",
        "taxes",
        "total"
    ]

    customer = schema.Reference(
        type = User,
        related_end = schema.Collection(),
        required = True,
        default = schema.DynamicDefault(get_current_user)
    )

    address = schema.String(
        member_group = "shipping_info",
        required = True,
        listed_by_default = False
    )

    town = schema.String(
        member_group = "shipping_info",
        required = True,
        listed_by_default = False
    )

    region = schema.String(
        member_group = "shipping_info",
        required = True,
        listed_by_default = False
    )

    country = schema.Reference(        
        member_group = "shipping_info",
        type = Location,
        relation_constraints = [Location.location_type.equal("country")],
        default_order = "location_name",
        related_end = schema.Collection(),
        required = True,
        listed_by_default = False,
        user_filter = "cocktail.controllers.userfilter.MultipleChoiceFilter"
    )

    postal_code = schema.String(
        member_group = "shipping_info",
        required = True,
        listed_by_default = False
    )

    language = schema.String(
        required = True,
        format = "^[a-z]{2}$",
        editable = False,
        default = schema.DynamicDefault(get_language),
        text_search = False,
        translate_value = lambda value, language = None, **kwargs:
            u"" if not value else translations(value, language, **kwargs)
    )

    status = schema.String(
        required = True,
        indexed = True,
        enumeration = [
            "shopping",
            "payment_pending",
            "accepted",
            "failed",
            "refund"
        ],
        default = "shopping",
        text_search = False,
        translate_value = lambda value, language = None, **kwargs:
            u"" if not value else translations(
                "ECommerceOrder.status-" + value,
                language,
                **kwargs
            )
    )
    
    purchases = schema.Collection(
        items = "woost.extensions.ecommerce.ecommercepurchase."
                "ECommercePurchase",
        integral = True,
        bidirectional = True,
        min = 1
    )

    total_price = schema.Decimal(
        member_group = "billing",
        editable = False,
        listed_by_default = False,
        translate_value = _translate_amount
    )

    pricing = schema.Collection(
        member_group = "billing",
        items = schema.Reference(type = ECommerceBillingConcept),
        related_end = schema.Collection(
            block_delete = True
        ),
        editable = False
    )

    total_shipping_costs = schema.Decimal(
        member_group = "billing",
        editable = False,
        listed_by_default = False,
        translate_value = _translate_amount
    )

    shipping_costs = schema.Collection(
        member_group = "billing",
        items = schema.Reference(type = ECommerceBillingConcept),
        related_end = schema.Collection(
            block_delete = True
        ),
        editable = False
    )
    
    total_taxes = schema.Decimal(
        member_group = "billing",
        editable = False,
        listed_by_default = False,
        translate_value = _translate_amount
    )

    taxes = schema.Collection(
        member_group = "billing",
        items = schema.Reference(type = ECommerceBillingConcept),
        related_end = schema.Collection(
            block_delete = True
        ),
        editable = False
    )
    
    total = schema.Decimal(
        member_group = "billing",
        editable = False,
        translate_value = _translate_amount
    )

    def calculate_cost(self, 
        apply_pricing = True,
        apply_shipping_costs = True, 
        apply_taxes = True
    ):
        """Calculates the costs for the order.
        :rtype: dict
        """
        from woost.extensions.ecommerce import ECommerceExtension
        extension = ECommerceExtension.instance

        order_costs = {
            "price": {
                "cost": Decimal("0.00"),
                "percentage": Decimal("0.00"),
                "concepts": []
            },
            "shipping_costs": {
                "cost": Decimal("0.00"),
                "percentage": Decimal("0.00"),
                "concepts": []
            },
            "taxes": {
                "cost": Decimal("0.00"),
                "percentage": Decimal("0.00"),
                "concepts": []
            },
            "purchases": {}
        }
        
        # Per purchase costs:
        for purchase in self.purchases:
            purchase_costs = purchase.calculate_costs(
                apply_pricing = apply_pricing,
                apply_shipping_costs = apply_shipping_costs,
                apply_taxes = apply_taxes
            )
            order_costs["purchases"][purchase] = purchase_costs

            order_costs["price"]["cost"] += purchase_costs["price"]["total"]
            order_costs["shipping_costs"]["cost"] += \
                purchase_costs["shipping_costs"]["total"]
            order_costs["taxes"]["cost"] += purchase_costs["taxes"]["total"]

        # Order price
        order_price = order_costs["price"]

        if apply_pricing:
            for pricing in extension.pricing:
                if pricing.applies_to(self):
                    pricing.apply(self, order_price)

        order_price["cost"] += \
            order_price["cost"] * order_price["percentage"] / 100

        order_price["total"] = order_price["cost"]

        # Order shipping costs
        order_shipping_costs = order_costs["shipping_costs"]

        if apply_shipping_costs:
            for shipping_cost in extension.shipping_costs:
                if shipping_cost.applies_to(self):
                    shipping_cost.apply(self, order_shipping_costs)

        order_shipping_costs["total"] = (
            order_shipping_costs["cost"]
            + order_price["total"] * order_shipping_costs["percentage"] / 100
        )

        # Order taxes
        order_taxes = order_costs["taxes"]

        if apply_taxes:
            for tax in extension.taxes:
                if tax.applies_to(self):
                    tax.apply(self, order_taxes)

        order_taxes["total"] = (
            order_taxes["cost"]
            + order_price["total"] * order_taxes["percentage"] / 100
        )

        # Total
        order_costs["total"] = (
            order_price["total"]
          + order_shipping_costs["total"]
          + order_taxes["total"]
        )

        return order_costs

    def update_cost(self,
        apply_pricing = True,
        apply_shipping_costs = True, 
        apply_taxes = True
    ):
        costs = self.calculate_cost(
            apply_pricing = apply_pricing,
            apply_shipping_costs = apply_shipping_costs,
            apply_taxes = apply_taxes
        )
        
        self.total_price = costs["price"]["total"]
        self.pricing = list(costs["price"]["concepts"])

        self.total_shipping_costs = costs["shipping_costs"]["total"]
        self.shipping_costs = list(costs["shipping_costs"]["concepts"])

        self.total_taxes = costs["taxes"]["total"]
        self.taxes = list(costs["taxes"]["concepts"])

        self.total = costs["total"]

        for purchase, purchase_costs in costs["purchases"].iteritems():
            purchase.total_price = purchase_costs["price"]["total"]
            purchase.pricing = list(purchase_costs["price"]["concepts"])
            self.pricing.extend(purchase.pricing)

            purchase.total_shipping_costs = \
                purchase_costs["shipping_costs"]["total"]
            purchase.shipping_costs = \
                list(purchase_costs["shipping_costs"]["concepts"])
            self.shipping_costs.extend(purchase.shipping_costs)

            purchase.total_taxes = purchase_costs["taxes"]["total"]
            purchase.taxes = list(purchase_costs["taxes"]["concepts"])
            self.taxes.extend(purchase.taxes)

            purchase.total = purchase_costs["total"]

    def count_units(self):
        return sum(purchase.quantity for purchase in self.purchases)

    def get_weight(self):
        return sum(purchase.get_weight() for purchase in self.purchases)

    def add_purchase(self, purchase):
        for order_purchase in self.purchases:
            if order_purchase.__class__ is purchase.__class__ \
            and all(
                order_purchase.get(option) == purchase.get(option)
                for option in purchase.get_options()
                if option.name != "quantity"
            ):
                order_purchase.quantity += purchase.quantity                
                purchase.product = None
                if purchase.is_inserted:
                    purchase.delete()
                break
        else:
            self.purchases.append(purchase)

