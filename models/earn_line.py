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


from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class EarnLine(models.Model):
    _name = "l10n_co_hr_payroll.earn.line"
    _description = "Earn details"
    _order = "payslip_id, sequence"

    name = fields.Char(string="Description", required=True)
    payslip_id = fields.Many2one(
        "hr.payslip", string="Pay Slip", required=True, ondelete="cascade", index=True
    )
    sequence = fields.Integer(required=True, index=True, default=10)
    code = fields.Char(
        help="The code that can be used in the salary rules",
        compute="_compute_rule",
        store=True,
    )
    amount = fields.Float("Amount")

    date_start = fields.Date("Start date")
    date_end = fields.Date("End date")
    time_start = fields.Float("Start hour")
    time_end = fields.Float("End hour")
    quantity = fields.Float(
        "Quantity", default=1, compute="_compute_quantity", store=True
    )
    total = fields.Float("Total", compute="_compute_total", store=True)
    rule_input_id = fields.Many2one(
        "hr.rule.input",
        string="Rule input",
        copy=True,
        required=True,
        domain=[("input_id.type_concept", "=", "earn")],
    )
    category = fields.Selection(
        [
            ("basic", "Basic"),
            ("vacation_common", "Vacation common"),
            ("vacation_compensated", "Vacation compensated"),
            ("primas", "Primas"),
            ("primas_non_salary", "Primas non salary"),
            ("layoffs", "Layoffs"),
            ("layoffs_interest", "Layoffs interest"),
            (
                "licensings_maternity_or_paternity_leaves",
                "Licensings maternity or paternity leaves",
            ),
            (
                "licensings_permit_or_paid_licenses",
                "Licensings permit or paid licenses",
            ),
            (
                "licensings_suspension_or_unpaid_leaves",
                "Licensings suspension or unpaid leaves",
            ),
            ("endowment", "Endowment"),
            ("sustainment_support", "Sustainment support"),
            ("telecommuting", "Telecommuting"),
            ("company_withdrawal_bonus", "Company withdrawal bonus"),
            ("compensation", "Compensation"),
            ("refund", "Refund"),
            ("transports_assistance", "Transports assistance"),
            ("transports_viatic", "Transports viatic"),
            ("transports_non_salary_viatic", "Transports non salary viatic"),
            ("daily_overtime", "Daily overtime"),
            ("overtime_night_hours", "Overtime night hours"),
            ("hours_night_surcharge", "Hours night surcharge"),
            ("sunday_holiday_daily_overtime", "Sunday and Holiday daily overtime"),
            (
                "daily_surcharge_hours_sundays_holidays",
                "Daily surcharge hours on sundays and holidays",
            ),
            ("sunday_night_overtime_holidays", "Sunday night overtime and holidays"),
            (
                "sunday_holidays_night_surcharge_hours",
                "Sunday and holidays night surcharge hours",
            ),
            ("incapacities_common", "Incapacities common"),
            ("incapacities_professional", "Incapacities professional"),
            ("incapacities_working", "Incapacities working"),
            ("bonuses", "Bonuses"),
            ("bonuses_non_salary", "Non salary bonuses"),
            ("assistances", "Assistances"),
            ("assistances_non_salary", "Non salary assistances"),
            ("legal_strikes", "Legal strikes"),
            ("other_concepts", "Other concepts"),
            ("other_concepts_non_salary", "Non salary other concepts"),
            ("compensations_ordinary", "Compensations ordinary"),
            ("compensations_extraordinary", "Compensations extraordinary"),
            ("vouchers", "Vouchers"),
            ("vouchers_non_salary", "Vouchers non salary"),
            ("vouchers_salary_food", "Vouchers salary food"),
            ("vouchers_non_salary_food", "Vouchers non salary food"),
            ("commissions", "Commissions"),
            ("third_party_payments", "Third party payments"),
            ("advances", "Advances"),
        ],
        string="Category",
        compute="_compute_rule",
        store=True,
    )

    @api.depends("rule_input_id")
    def _compute_rule(self):
        """
        Compute the rule for each record in the self object.

        This function is decorated with `@api.depends("rule_input_id")`
        and is called when the `rule_input_id` field is changed.
        It iterates over each record in the self object and updates
        the `name`, `code`, and `category` fields based on
        the values of `rule_input_id`.

        Parameters:
            self (models.Model): The current recordset.
        """
        for rec in self:
            rec.name = rec.rule_input_id.name
            rec.code = rec.rule_input_id.code
            rec.category = rec.rule_input_id.input_id.earn_category

    @api.depends("quantity", "amount")
    def _compute_total(self):
        for rec in self:
            rec.total = rec.quantity * rec.amount

    @api.depends("date_start", "date_end", "time_start", "time_end")
    def _compute_quantity(self):
        """
        Compute the quantity for each record in the self object.

        This function is decorated with 
        `@api.depends("date_start", "date_end", "time_start", "time_end")`
        and is called when any of the mentioned fields are changed.
        It iterates over each record in the self object and updates
        the `quantity` field based on the 
        values of `date_start`, `date_end`, `time_start`, and `time_end`.

        Parameters:
            self (models.Model): The current recordset.
        """
        for rec in self:
            # Categories with days of absence
            if rec.category in (
                "vacation_common",
                "licensings_maternity_or_paternity_leaves",
                "licensings_permit_or_paid_licenses",
                "licensings_suspension_or_unpaid_leaves",
                "incapacities_common",
                "incapacities_professional",
                "incapacities_working",
                "legal_strikes",
            ):
                # Calculate quantity as the number of days between date_start and date_end
                if rec.date_end and rec.date_start:
                    rec.quantity = (rec.date_end - rec.date_start).days + 1
                else:
                    rec.quantity = 0

            # Categories with hours of overtime
            elif rec.category in (
                "daily_overtime",
                "overtime_night_hours",
                "hours_night_surcharge",
                "sunday_holiday_daily_overtime",
                "daily_surcharge_hours_sundays_holidays",
                "sunday_night_overtime_holidays",
                "sunday_holidays_night_surcharge_hours",
            ):
                # Calculate quantity as the sum of days multiplied by 24 and hours of overtime
                if rec.date_end and rec.date_start and rec.time_end and rec.time_start:
                    days = (rec.date_end - rec.date_start).days
                    rec.quantity = 24 * days + rec.time_end - rec.time_start
                else:
                    rec.quantity = 0

            # Default quantity is 1
            else:
                rec.quantity = 1

    @api.constrains("time_start")
    def _check_time_start(self):
        """
        Validate the time_start field.

        It raises a ValidationError if the time_start
        is less than 0 or greater than or equal to 24.
        """
        # Iterate over each record in the self object
        for rec in self:
            # Check if the time_start is invalid
            if rec.time_start < 0 or rec.time_start >= 24:
                # Raise a ValidationError with a formatted message
                raise ValidationError(_("Invalid start time: %s") % rec.time_start)

    @api.constrains("time_end")
    def _check_time_end(self):
        """
        Validate the time_end field.

        This function checks if the time_end is valid.
        It raises a ValidationError if the time_end is less than 0 or
        greater than or equal to 24.
        """
        # Iterate over each record in the self object
        for rec in self:
            # Check if the time_end is invalid
            if rec.time_end < 0 or rec.time_end >= 24:
                # Raise a ValidationError with a formatted message
                raise ValidationError(_("Invalid end time: %s") % rec.time_end)

    @api.constrains("date_start", "date_end")
    def _check_date_start_end(self):
        """
        Validate that the start date is before the end date.

        This function is decorated with `@api.constrains("date_start", "date_end")`
        and is called when either `date_start` or `date_end` fields are changed.
        It raises a ValidationError if the end date is less than
        the start date.

        Parameters:
            self (models.Model): The current recordset.
        """
        # Iterate over each record in the self object
        for rec in self:
            # Check if the end date is less than the start date
            if rec.date_end < rec.date_start:
                # Raise a ValidationError with a formatted message
                raise ValidationError(
                    _("The end date must always be greater than the start date for: %s")
                    % rec.name
                )

    @api.constrains("amount")
    def _check_amount(self):
        """
        Validate the amount field.

        This function checks if the amount is valid.
        It raises a ValidationError if the amount is less than or equal to 0.

        Parameters:
            self (models.Model): The current recordset.
        """
        # Iterate over each record in the self object
        for rec in self:
            # Check if the amount is invalid
            if rec.amount <= 0:
                # Raise a ValidationError with a formatted message
                raise ValidationError(
                    _("The earn amount must always be greater than 0 for: %s")
                    % rec.name
                )
