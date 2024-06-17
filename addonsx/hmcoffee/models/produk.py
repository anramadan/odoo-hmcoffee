from odoo import api,models,fields

class Produk(models.Model):
    try:
        _name = "hmcoffee.produk"
        _description = "model.technical.name"
        
    # Main Fields
        name = fields.Char(string="Nama Produk")
        kategori = fields.Selection(selection=[
            ("Kopi", "Kopi"),
            ("Minuman", "Minuman"),
            ("Makanan", "Makanan")],
            string="Kategori")
        harga_produk = fields.Integer(string='Harga Produk',compute='_compute_harga_produk',readonly=True)

    # Relationship Fields
        pesanan_ids = fields.One2many(comodel_name="hmcoffee.detail.pesanan",string="produk_id",inverse_name="produk_id")
        
        detail_produk_ids = fields.One2many('hmcoffee.detail.produk', 'produk_id', string='Detail Produk')

        
    # api
        @api.depends('detail_produk_ids','harga_produk')
        def _compute_harga_produk(self):
            # raise Exception("<<<<<<<<<<<<")
            try:
                for produk in self:
                    produk.harga_produk = sum((bahan.harga) for bahan in produk.detail_produk_ids) *1.2
            except:
                raise Exception("Error in produk compute harga")
    
    except Exception as e:
        raise Exception("Error in Produk Model:",e)

class DetailProduk(models.Model):
    try:
        _name="hmcoffee.detail.produk"
        _description = "model.technical.name"

        produk_id = fields.Many2one(comodel_name='hmcoffee.produk', string='Produk')
        bahan_id = fields.Many2one(comodel_name="hmcoffee.produk.bahan", string="Bahan")
        harga = fields.Integer(readonly=True, string="Harga",compute="_compute_harga")
        qty = fields.Integer(string="Quantity")

        @api.depends('qty','harga')
        def _compute_harga(self):
            try:
                for produk in self:
                    produk.harga = sum(bahan.harga * produk.qty for bahan in produk.bahan_id)
            except Exception as e:
                raise Exception("Error in detailproduk compute harga ", e)

    except Exception as e:
        raise Exception("Error in Detail Produk Model:",e)