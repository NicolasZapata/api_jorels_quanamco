# -*- coding: utf-8 -*-
#
#   l10n_co_hr_payroll
#   Copyright (C) 2022  Jorels SAS
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published
#   by the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#   email: info@jorels.com
#


from odoo import fields, models, api


class HrContract(models.Model):
    _inherit = "hr.contract"

    type_worker_id = fields.Many2one(
        comodel_name="l10n_co_edi_jorels.type_workers", string="Type worker"
    )
    subtype_worker_id = fields.Many2one(
        comodel_name="l10n_co_edi_jorels.subtype_workers", string="Subtype worker"
    )
    high_risk_pension = fields.Boolean(string="High risk pension", default=False)
    integral_salary = fields.Boolean(string="Integral salary", default=False)
    type_contract_id = fields.Many2one(
        comodel_name="l10n_co_edi_jorels.type_contracts", string="Type contract"
    )
    payroll_period_id = fields.Many2one(
        comodel_name="l10n_co_edi_jorels.payroll_periods",
        string="Payroll period",
        compute="_compute_payroll_period_id",
        # store=True,
    )

    @api.depends("schedule_pay")
    def _compute_payroll_period_id(self):
        """
        This function computes the 'payroll_period_id' field based on the
        'schedule_pay' field of each record in the self iterable.

        The function uses a dictionary to map the possible values of 'schedule_pay'
        to the corresponding 'payroll_period_id' values.

        If 'schedule_pay' is not present, 'payroll_period_id' is set to None.
        """
        # Dictionary that maps 'schedule_pay' values to 'payroll_period_id' values
        values = {
            "monthly": 5,
            "quarterly": 6,
            "semi-annually": 6,
            "annually": 6,
            "weekly": 1,
            "bi-weekly": 4,
            "bi-monthly": 6,
        }
        # Loop through each record in the self iterable
        for rec in self:
            # If 'schedule_pay' is present, set 'payroll_period_id' to the corresponding value
            if rec.schedule_pay:
                rec.payroll_period_id = values[rec.schedule_pay]
            # If 'schedule_pay' is not present, set 'payroll_period_id' to None
            else:
                rec.payroll_period_id = None
