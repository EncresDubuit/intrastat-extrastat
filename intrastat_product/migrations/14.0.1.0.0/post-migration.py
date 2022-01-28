# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# Copyright 2021 ForgeFlow <http://www.forgeflow.com>

from openupgradelib import openupgrade  # pylint: disable=W7936

_months = [
    (1, "01"),
    (2, "02"),
    (3, "03"),
    (4, "04"),
    (5, "05"),
    (6, "06"),
    (7, "07"),
    (8, "08"),
    (9, "09"),
    (10, "10"),
    (11, "11"),
    (12, "12"),
]


def update_intrastat_product_declaration_year(env):
    openupgrade.logged_query(
        env.cr, """
        UPDATE intrastat_product_declaration
        SET year = {integer_year} || ''
        """.format(integer_year=openupgrade.get_legacy_name("year"))
    )


def map_intrastat_product_declaration_month(env):
    openupgrade.map_values(
        env.cr,
        openupgrade.get_legacy_name("month"),
        "month",
        _months,
        table="intrastat_product_declaration",
    )


def update_invoice_relation_fields(env):
    # In a Odoo project started from v13.0, these invoices tables doesn't exist!
    if openupgrade.table_exists(env.cr, "account_invoice"):
        openupgrade.logged_query(
            env.cr,
            """
            UPDATE account_move am
            SET (intrastat_transaction_id, intrastat_transport_id,
                src_dest_country_id, src_dest_region_id
                ) = (ai.intrastat_transaction_id,
                ai.intrastat_transport_id, ai.src_dest_country_id,
                ai.src_dest_region_id)
            FROM account_invoice ai
            WHERE am.id = ai.move_id""",
        )
        if openupgrade.table_exists(env.cr, "account_invoice_line"):
            openupgrade.logged_query(
                env.cr,
                """
                UPDATE intrastat_product_computation_line ipcl
                SET invoice_line_id = (SELECT id FROM account_move_line aml WHERE aml.move_id = ai.move_id AND aml.account_id = ail.account_id LIMIT 1)
                FROM account_invoice_line ail
                JOIN account_invoice ai ON ai.id = ail.invoice_id
                WHERE ipcl.%(old_line_id)s = ail.id"""
                % {"old_line_id": openupgrade.get_legacy_name("invoice_line_id")},
            )

@openupgrade.migrate()
def migrate(env, version):
    update_intrastat_product_declaration_year(env)
    map_intrastat_product_declaration_month(env)
    update_invoice_relation_fields(env)
    openupgrade.load_data(
        env.cr, "intrastat_product", "migrations/14.0.1.0.0/noupdate_changes.xml"
    )
    