from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Inherit existing field and make it required
    l10n_in_pan = fields.Char(
        required=True
    )

    # Python constraint for uniqueness check
    @api.constrains('l10n_in_pan')
    def _check_pan_unique(self):
        for rec in self:
            if rec.l10n_in_pan:
                # Format the PAN
                pan = rec.l10n_in_pan.replace(' ', '').upper()

                # Check for duplicates
                duplicate = self.search([
                    ('l10n_in_pan', '=', pan),
                    ('id', '!=', rec.id)
                ], limit=1)

                if duplicate:
                    raise ValidationError('PAN Number already exists! Please enter a unique PAN number.')

    # Python constraint for PAN format validation
    @api.constrains('l10n_in_pan')
    def _check_pan_format(self):
        for rec in self:
            if rec.l10n_in_pan:
                pan = rec.l10n_in_pan.replace(' ', '').upper()

                # Check PAN length
                if len(pan) != 10:
                    raise ValidationError('PAN must be exactly 10 characters long.')

                # Check PAN format: First 5 characters should be letters
                if not pan[:5].isalpha():
                    raise ValidationError('First 5 characters of PAN must be letters.')

                # Check characters 6-9 should be digits
                if not pan[5:9].isdigit():
                    raise ValidationError('Characters 6 to 9 of PAN must be digits.')

                # Check 10th character should be a letter
                if not pan[9].isalpha():
                    raise ValidationError('Last character of PAN must be a letter.')

    # Auto-format PAN on create
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'l10n_in_pan' in vals and vals['l10n_in_pan']:
                vals['l10n_in_pan'] = vals['l10n_in_pan'].replace(' ', '').upper()
        return super(ResPartner, self).create(vals_list)

    # Auto-format PAN on write
    def write(self, vals):
        if 'l10n_in_pan' in vals and vals['l10n_in_pan']:
            vals['l10n_in_pan'] = vals['l10n_in_pan'].replace(' ', '').upper()
        return super(ResPartner, self).write(vals)
