from odoo import fields,models,api

class Pesanan(models.Model):
    try:
        _name="hmcoffee.pesanan"
        _description="model.technical.name"

        # Main Fields
        pesanan_id = fields.Char(string="Kode Pesanan",readonly=True, default=lambda self:('New'))
        harga_pesanan = fields.Integer('Harga Pesanan',compute="_compute_harga_pesanan")
        
        # Rel Fields
        pelanggan_id = fields.Many2one('hmcoffee.pelanggan', string='pelanggan')
        detail_pesanan_ids = fields.One2many('hmcoffee.detail.pesanan', 'pesanan_id', string='detail_pesanan')
    except Exception as e:
        raise Exception("Error at pesanan ",e)

class DetailPesanan(models.Model):
    try:
        _name="hmcoffee.detail.pesanan"
        _description="model.technical.name"

        # Main Fields
        quantity=fields.Integer(string="Quantity")
        harga=fields.Integer(string="Harga",digits=2,compute="_total_harga")
        
        # Rel Fields
        pesanan_id = fields.Many2one('hmcoffee.pesanan', string='Pelanggan')
        produk_id=fields.Many2one(comodel_name="hmcoffee.produk",string="Produk")
        
        @api.depends('quantity')
        def _total_harga(self):
            for pesanan in self:
                pesanan.harga=sum(produk.harga_produk for produk in pesanan.produk)
        
        @api.model
        def create(self,vals):
            try:
                # print("<<<<<<<<<<<<<<<<",vals)
                record = super(DetailPesanan,self).create(vals)
                if record.quantity:
                    
                    produk_link = self.env['hmcoffee.produk'].search([('id','=',record.produk_id.id)]).mapped('detail_produk_ids')

                    for produk in produk_link:
                        bahan_link = self.env['hmcoffee.produk.bahan'].search([('id','=',produk.bahan_id.id)])
                        raise Exception(bahan_link,'<<<<<<<<<<<<<<<<<<')

                    self.env['hmcoffee.produk.bahan'].search([('id','=',record.bahan.id)]).write({'stok':stok_update})
                return record

            except Exception as e:
                raise Exception("Error in create detail pembelian")
    except Exception as e:
        raise Exception("Error at Detail Pesanan ",e)    