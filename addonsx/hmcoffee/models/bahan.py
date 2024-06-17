from odoo import api,models,fields
class Bahan(models.Model):
    try:
        _name = "hmcoffee.produk.bahan"
        _description = "model.technical.name"
        _rec_name = "name"

        name = fields.Char(string="Nama Bahan")
        harga = fields.Integer(string="Harga")
        stok = fields.Integer(string="Stock Barang")

        produk_ids = fields.One2many(
            comodel_name='hmcoffee.detail.produk', 
            string="Produk",
            inverse_name="bahan_id",
            ondelete="cascade")
        supplier_id = fields.Many2many(
            comodel_name='hmcoffee.supplier', string="Supplier"
        )
        pembelian_ids = fields.One2many(
            comodel_name="hmcoffee.detail.pembelian",
            inverse_name="bahan",
        )
    except Exception as e:
        raise Exception(f"Error in Bahan {e}")
