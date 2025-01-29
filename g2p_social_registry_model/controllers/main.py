import logging
from odoo import http
from odoo.http import request
from odoo.addons.g2p_registration_portal_base.controllers.main import G2PregistrationPortalBase

_logger = logging.getLogger(__name__)

class G2PSocialRegistryModel(G2PregistrationPortalBase):
    @http.route(
    ["/portal/registration/individual/create/submit"],
    type="http",
    auth="user",
    website=True,
    csrf=False,
    )
    def individual_create_submit(self, **kw):
        try:
            user = request.env.user
            name = ""
            if kw.get("family_name"):
                name += kw.get("family_name") + ", "
            if kw.get("given_name"):
                name += kw.get("given_name") + " "
            if kw.get("addl_name"):
                name += kw.get("addl_name") + " "
            if kw.get("birthdate") == "":
                birthdate = False
            else:
                birthdate = kw.get("birthdate")
            
            data = {
                "given_name": kw.get("given_name"),
                "addl_name": kw.get("addl_name"),
                "family_name": kw.get("family_name"),
                "name": name.strip(),
                "birthdate": birthdate,
                "gender": kw.get("gender"),
                "email": kw.get("email"),
                "user_id": user.id,
                "is_registrant": True,
                "is_group": False,
                
                # Additional fields
                "address": kw.get("address"),
                "occupation": kw.get("occupation"),
                "income": float(kw.get("income", 0.0)),
                "education_level": kw.get("education_level"),
                "employment_status": kw.get("employment_status"),
                "marital_status": kw.get("marital_status"),
                
            }

            request.env["res.partner"].sudo().create(data)

            return request.redirect("/portal/registration/individual")

        except Exception as e:
            _logger.exception("Error while submitting individual registration: %s", str(e))
            return request.redirect("/portal/registration/individual")


    @http.route(
        "/portal/registration/individual/update/submit",
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def update_individual_submit(self, **kw):
        try:
            member = request.env["res.partner"].sudo().browse(int(kw.get("group_id")))
            if member:
                name = ""
                if kw.get("family_name"):
                    name += kw.get("family_name") + ", "
                if kw.get("given_name"):
                    name += kw.get("given_name") + " "
                if kw.get("addl_name"):
                    name += kw.get("addl_name") + " "
                if kw.get("birthdate") == "":
                    birthdate = False
                else:
                    birthdate = kw.get("birthdate")

                member.sudo().write(
                    {
                        "given_name": kw.get("given_name"),
                        "addl_name": kw.get("addl_name"),
                        "family_name": kw.get("family_name"),
                        "name": name,
                        "birthdate": birthdate,
                        "gender": kw.get("gender"),
                        "email": kw.get("email"),
                        "address": kw.get("address"),
                        "occupation": kw.get("occupation"),
                        "income": float(kw.get("income", 0.0)),

                        # Household Details
                        "education_level": kw.get("education_level"),
                        "employment_status": kw.get("employment_status"),
                        "marital_status": kw.get("marital_status"),

                    }
                )
            return request.redirect("/portal/registration/individual")

        except Exception as e:
            _logger.error("Error occurred%s" % e)
            return request.render(
                "g2p_registration_portal_base.error_template",
                {"error_message": "An error occurred. Please try again later."},
            )
    
    @http.route(
        ["/portal/registration/group/create/submit"],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def group_create_submit(self, **kw):
        try:
            head_name = kw.get("name")
            beneficiary_id = None
            
            if kw.get("group_id"):
                beneficiary_id = request.env["res.partner"].sudo().browse(int(kw.get("group_id"))).id
            else:
                if head_name:
                    user = request.env.user

                    data = {
                        "name": head_name,
                        "is_registrant": True,
                        "is_group": True,
                        "birthdate": kw.get("dob"),
                        "gender": kw.get("gender"),
                        "user_id": user.id,

                        # Social Status Information
                        "num_preg_lact_women": int(kw.get("num_preg_lact_women", 0)),
                        "num_malnourished_children": int(kw.get("num_malnourished_children", 0)),
                        "num_disabled": int(kw.get("num_disabled", 0)),
                        "type_of_disability": kw.get("type_of_disability"),

                        # Economic Status Information
                        "caste_ethnic_group": kw.get("caste_ethnic_group"),
                        "belong_to_protected_groups": kw.get("belong_to_protected_groups"),
                        "other_vulnerable_status": kw.get("other_vulnerable_status"),
                        "income_sources": kw.get("income_sources"),
                        "annual_income": float(kw.get("annual_income", 0.0)),
                        "owns_two_wheeler": kw.get("owns_two_wheeler"),
                        "owns_three_wheeler": kw.get("owns_three_wheeler"),
                        "owns_four_wheeler": kw.get("owns_four_wheeler"),
                        "owns_cart": kw.get("owns_cart"),
                        "land_ownership": kw.get("land_ownership"),
                        "type_of_land_owned": kw.get("type_of_land_owned"),
                        "land_size": float(kw.get("land_size", 0.0)),
                        "owns_house": kw.get("owns_house"),
                        "owns_livestock": kw.get("owns_livestock"),

                    }

                    beneficiary_obj = request.env["res.partner"].sudo().create(data)

                    beneficiary_id = beneficiary_obj.id
            beneficiary = request.env["res.partner"].sudo().browse(beneficiary_id)

            if not beneficiary:
                return request.render(
                    "g2p_registration_portal_base.error_template",
                    {"error_message": "Beneficiary not found."},
                )

            for key, value in kw.items():
                if key in beneficiary:
                    beneficiary.write({key: value})
                else:
                    _logger.error(f"Ignoring invalid key: {key}")

            return request.redirect("/portal/registration/group")

        except Exception as e:
            _logger.error("Error occurred%s" % e)
            return request.render(
                "g2p_registration_portal_base.error_template",
                {"error_message": "An error occurred. Please try again later."},
            )
        



