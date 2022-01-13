# Copyright 2020 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade

_column_renames = {
    "intrastat_product_declaration": [("year", None),("month", None),("type", "declaration_type")],
    "intrastat_product_computation_line": [("invoice_line_id", None)],
}


@openupgrade.migrate()
def migrate(cr, version):
    if not version:
        return

    openupgrade.rename_columns(env.cr, _column_renames)

    #cr.execute(
    #    'ALTER TABLE "intrastat_product_declaration" RENAME "type" '
    #    'TO "declaration_type"'
    #)
