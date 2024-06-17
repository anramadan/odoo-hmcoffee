from odoo import fields,models,api
import random

class Pesanan(models.Model):
    try:
        _name="hmcoffee.pesanan"
        _description="model.technical.name"
        # Main Fields
        pesanan_id = fields.Char(string="Kode Pesanan",readonly=True, default=f"PSN-{((random.randint(1,100000)))}")
        harga_pesanan = fields.Integer('Harga Pesanan',compute="_compute_harga_pesanan")
        
        # Rel Fields
        # pelanggan_id = fields.Many2one('hmcoffee.pelanggan', string='pelanggan')
        detail_pesanan_ids = fields.One2many('hmcoffee.detail.pesanan', 'pesanan_id', string='Detail Pesanan')

        @api.depends('detail_pesanan_ids')
        def _compute_harga_pesanan(self):
            for pesanan in self:
                pesanan.harga_pesanan=sum(detail.harga for detail in pesanan.detail_pesanan_ids)

        @api.model
        def unlink(self):
            if self.detail_pesanan_ids:
                for data in self.detail_pesanan_ids:
                    produk_link = self.env['hmcoffee.produk'].search([('id', '=', data.produk_id.id)]).mapped('detail_produk_ids')
                    for produk in produk_link:
                        bahan_link = self.env['hmcoffee.produk.bahan'].search([('id', '=', produk.bahan_id.id)])
                        bahan_link.stok += (data.quantity * produk.qty)
                        bahan_link.write({'stok': bahan_link.stok})
            return super(Pesanan, self).unlink()
        
        def write(self, vals):
            a=[]
            for rec in self:
                a=self.env['hmcoffee.detail.pesanan'].search([("pesanan_id",'=',rec.id)])
                for data in a:
                    if data:
                        produk_link = self.env['hmcoffee.produk'].search([('id', '=', data.produk_id.id)]).mapped('detail_produk_ids')
                        for produk in produk_link:
                            bahan_link = self.env['hmcoffee.produk.bahan'].search([('id', '=', produk.bahan_id.id)])
                            bahan_link.stok += (data.quantity * produk.qty)
                            bahan_link.write({'stok': bahan_link.stok})
            
            record = super(Pesanan,self).write(vals)
            for recc in self:
                b = self.env['hmcoffee.detail.pesanan'].search([('pesanan_id','=',recc.id)])
                for databaru in b:
                    if databaru in a:
                        produk_link = self.env['hmcoffee.produk'].search([('id', '=', databaru.produk_id.id)]).mapped('detail_produk_ids')
                        for produk in produk_link:
                            bahan_link = self.env['hmcoffee.produk.bahan'].search([('id', '=', produk.bahan_id.id)])
                            bahan_link.stok -= (databaru.quantity * produk.qty)
                            bahan_link.write({'stok': bahan_link.stok})
            return record

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
                pesanan.harga=sum(produk.harga_produk for produk in pesanan.produk_id)
        
        @api.model
        def create(self, vals):
            try:
                record = super(DetailPesanan, self).create(vals)
                if record.quantity:
                    produk_link = self.env['hmcoffee.produk'].search([('id', '=', record.produk_id.id)]).mapped('detail_produk_ids')
                    for produk in produk_link:
                        bahan_link = self.env['hmcoffee.produk.bahan'].search([('id', '=', produk.bahan_id.id)])
                        bahan_link.stok -= (record.quantity * produk.qty)
                        bahan_link.write({'stok': bahan_link.stok})

                return record

            except Exception as e:
                raise Exception("Error in create detail pembelian") from e
    except Exception as e:
        raise Exception("Error at Detail Pesanan ",e)    



