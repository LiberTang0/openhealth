# -*- coding: utf-8 -*-
#
# 	*** Product
# 
# Created: 			    Nov 2016
# Last updated: 	 19 Feb 2017

from openerp import models, fields, api
from datetime import datetime



from . import prodvars



class Product(models.Model):
	#_name = 'openhealth.service'
	_inherit = 'product.template'




	#'base': fields.selection(

	#	[('list_price', 'Public Price'), ('standard_price', 'Cost'), ('pricelist', 'Other Pricelist')], 

	#	string="Based on", 
	#	required=True,
	#	help='Base price for computation. \n Public Price: The base price will be the Sale/public Price. \n Cost Price : The base price will be the cost price. \n Other Pricelist : Computation of the base price based on another Pricelist.'
	#),






	uom = fields.Many2one(
			'product.uom',
			required=False, 
		)




	# Origin
	x_origin = fields.Selection(
		[
			('legacy', 'Legacy'),
			('test', 'Test'), 
			('production', 'Production'),
		],
	)




	# Only Products 
	x_brand = fields.Char(
			string="Marca", 
		)





	# Canonical 

	x_family = fields.Selection(
			selection=prodvars._family_list,
		)	

	x_treatment = fields.Selection(
			selection=prodvars._treatment_list,
		)	
	
	x_zone = fields.Selection(
			selection=prodvars._zone_list,
		)	
	
	x_pathology = fields.Selection(
			selection=prodvars._pathology_list,
		)

	x_sessions = fields.Char(
			default="",
		)





	x_time = fields.Char(
			selection=prodvars._time_list,
		)





	x_name_short = fields.Char(
		)







	# Before 
	x_date_updated = fields.Date(
			)

	x_date_created = fields.Date(
			)

	x_price_vip = fields.Float(
			#string = 'Precio VIP - nex',
		)



