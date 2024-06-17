from odoo import models, fields, api

class Pembelian(models.Model):
    try:
        _name = 'hmcoffee.pembelian'
        _description = 'Pembelian'

        supplier_id = fields.Many2one(comodel_name='hmcoffee.supplier', string="Supplier")  # id
        tgl_pembelian = fields.Date(string='Tanggal Pembelian', default=fields.Datetime.now())
        detail_pembelian = fields.One2many(
            comodel_name='hmcoffee.detail.pembelian',
            inverse_name='pembelian_id', 
            string="Detail Pembelian"
        )  # list

        @api.model
        def unlink(self):
            if self.detail_pembelian:
                for data in self.detail_pembelian:
                    data.bahan.stok -= data.qty
            return super(Pembelian, self).unlink()

        def write(self, vals):
            a=[]
            for rec in self:
                a=self.env['hmcoffee.detail.pembelian'].search([("pembelian_id",'=',rec.id)])
                for data in a:
                    if data:
                        data.bahan.stok -=data.qty
            
            record = super(Pembelian,self).write(vals)
            for recc in self:
                b = self.env['hmcoffee.detail.pembelian'].search([('pembelian_id','=',recc.id)])
                for databaru in b:
                    if databaru in a:
                        databaru.bahan.stok += databaru.qty
            return record
    except Exception as e:
        raise Exception("Error at Pembelian Model ",e)


class DetailPembelian(models.Model):
    try:
        _name = 'hmcoffee.detail.pembelian'
        _description = 'Detail Pembelian'

        pembelian_id = fields.Many2one(comodel_name='hmcoffee.pembelian', string="Pembelian")  # id
        bahan = fields.Many2one(comodel_name='hmcoffee.produk.bahan', string='Bahan')
        qty = fields.Integer(string='Quantity')
        total_pembelian = fields.Integer(compute='_compute_total_pembelian', string='Total Pembelian')
        
                    
        @api.depends('bahan', 'qty')
        def _compute_total_pembelian(self):
            for data in self:
                data.total_pembelian = data.bahan.harga * data.qty

        @api.model
        def create(self,vals):
            try:
                # print("<<<<<<<<<<<<<<<<",vals)
                record = super(DetailPembelian,self).create(vals)
                if record.qty:
                    stok_update = record.bahan.stok+record.qty
                    self.env['hmcoadfasdfffee.produk.bahan'].search([('id','=',record.bahan.id)]).write({'stok':stok_update})
                return record

            except Exception as e:
                raise Exception("Error in create detail pembelian")
    except Exception as e:
        raise Exception("Error in DetailPembelian model ",e)
    