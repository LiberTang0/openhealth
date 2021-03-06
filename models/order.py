# -*- coding: utf-8 -*-
#
#
# 	Order 
# 
# Created: 				26 Aug 2016
# Last updated: 	 	29 Sep 2017




from openerp import models, fields, api
import datetime

#from . import jxvars
from . import app_vars
from . import ord_vars
from . import appfuncs
from . import cosvars
from . import treatment_vars


class sale_order(models.Model):
	
	#_name = 'openhealth.order'
	_inherit='sale.order'
	



	x_my_company = fields.Many2one(

			'res.partner',
			string = "Mi compañía", 	


			domain = [
						('company_type', '=', 'company'),
					],


			compute="_compute_x_my_company",
		)

	@api.multi
	#@api.depends('partner_id')

	def _compute_x_my_company(self):
		for record in self:

				com = self.env['res.partner'].search([
															#('name', '=', 'Clinica Chavarri'),
															('x_my_company', '=', True),
													],
													order='date desc',
													limit=1,
					)
			
				#print 'jx'
				#print com 
				#print 
				record.x_my_company = com 													





	x_type = fields.Selection(

			[	('receipt', 			'Boleta'),
				('invoice', 			'Factura'),
				('advertisement', 		'Canje Publicidad'),
				('sale_note', 			'Canje NV'),
				('ticket_receipt', 		'Ticket Boleta'),
				('ticket_invoice', 		'Ticket Factura'),	], 
			

			string='Tipo', 

			#required=True, 
			required=False, 

			compute="_compute_x_type",
		)

	@api.multi
	#@api.depends('partner_id')

	def _compute_x_type(self):
		for record in self:

			name = record.name
			pre = name.split('-')[0]


			if pre == 'BO' or  pre == 'BOL':
				record.x_type = 'receipt'

			elif pre == 'FA':
				record.x_type = 'invoice'

			elif pre == 'CP':
				record.x_type = 'advertisement'

			elif pre == 'CN':
				record.x_type = 'sale_note'
			
			elif pre == 'TKB':
				record.x_type = 'ticket_receipt'
			
			elif pre == 'TKF':
				record.x_type = 'ticket_invoice'

			#else:
			#	print 'jx'
			#	print 'This should not happen'
			#	print pre 
			#	print 






	#order_day = fields.Char(	
	#		'Day', 
	#		default = lambda *a: str(date_order.strftime('%d')),
	#	)








#'task_date_from':fields.function(lambda *a,**k:{}, method=True, type='date',string="Task date from"),
#'task_date_to':fields.function(lambda *a,**k:{}, method=True, type='date',string="Task date to"),

	#task_date_from = fields.Date(
	#	default = lambda *a,#**k:{}, 
		#method=True, 
		#type='date', 
	#	string="Task date from", 
	#)

	#task_date_to = fields.Date(
	#	default=lambda *a,#**k:{}, 
		#method=True, 
	#	string="Task date to"
	#)




	# Doctor 
	x_doctor = fields.Many2one(
			'oeh.medical.physician',
			string = "Médico", 	
		)





	# Type (product or service)
	#x_cancel_reason = fields.Char(
	x_cancel_reason = fields.Selection(
			selection=ord_vars._owner_type_list, 
			#string='Motivo de anulación', 
			string='Tipo', 
		)


	# Product Odoo 
	x_cancel_owner = fields.Char(
			#string='Quién anula', 
			string='Producto', 
		)



	# Categ
	categ = fields.Char(

			'Categoria', 

			compute="_compute_categ",
		)

	@api.multi
	#@api.depends('partner_id')

	def _compute_categ(self):
		for record in self:

			for line in record.order_line:

				#record.categ = line.product_id.name
				record.categ = line.product_id.categ_id.name



	# Product
	product = fields.Char(

			'Producto', 

			compute="_compute_product",
		)

	@api.multi
	#@api.depends('partner_id')

	def _compute_product(self):
		for record in self:

			for line in record.order_line:

				record.product = line.product_id.name







	# Comment 
	comment = fields.Selection(
		[
		('product', 'Product'),
		('service', 'Service'),
		], 
		string='Comment', 
		default='product', 
		readonly=True
	)






	# Deprecated ? 
	#margin = fields.Float(
	#		string="Margen"
	#	)

	validity_date = fields.Char(
			string="Fecha de expiración"
		)




#jz
	# State 
	state = fields.Selection(

			
			#selection = ord_vars._x_state_list, 
			selection = ord_vars._state_list, 
			

			string='Estado',	
			readonly=False,
			default='draft',

			#copy=False, 
			#index=True, 
			#track_visibility='onchange', 
			#compute="_compute_state",
			)








	# Consultation - DEPRECATED ? 
	consultation = fields.Many2one(
			'openhealth.consultation',
			string="Consulta",
			ondelete='cascade', 
		)



	# Ooor 
	x_age = fields.Integer(string='Age', default=52, help='Age of student')

	x_group = fields.Char(string='Group', compute='_compute_x_group', help='Group of student', store=True)

	@api.depends('x_age')
	def _compute_x_group(self):
	
		#self.x_group = 'NA'
		#if self.x_age > 5 and self.x_age <= 10:
		#	self.x_group = 'A'
		#elif self.x_age > 10 and self.x_age <= 12:
		#	self.x_group = 'B'
		#elif self.x_age > 12:
		#	self.x_group = 'C'

		for record in self:
			record.x_group = 'NA'
			if record.x_age > 5 and record.x_age <= 10:
				record.x_group = 'A'
			elif record.x_age > 10 and record.x_age <= 12:
				record.x_group = 'B'
			elif record.x_age > 12:
				record.x_group = 'C'




	# Year
	x_year = fields.Char(
			compute="_compute_x_year",

			string='Year', 

			#store=True, 

			default=False, 
		)

	#@api.multi
	@api.one
	@api.depends('date_order')
	def _compute_x_year(self):
		#print 
		#print 'Compute X Year'

		#date = datetime.datetime.strptime(self.date_order, date_format)
		#self.x_year = date.year
		#print self.x_year
		#print 
		#self.fats = self.name.fats

		for record in self:
			date_format = "%Y-%m-%d %H:%M:%S"
			date = datetime.datetime.strptime(record.date_order, date_format)
			record.x_year = date.year




	# Month 
	x_month = fields.Char(
			string='Month', 
			
			#store=True, 
			required=False, 

			compute="_compute_x_month",
		)

	#@api.multi
	@api.depends('date_order')
	def _compute_x_month(self):
		for record in self:
			#record.x_month = 'jz'

			date_format = "%Y-%m-%d %H:%M:%S"
			date = datetime.datetime.strptime(record.date_order, date_format)
			record.x_month = date.month






	note = fields.Text(
			"Nota",					
		)



	# Doctor name  
	x_doctor_name = fields.Char(
		)
	doctor_name = fields.Char(
								default = 'generic doctor',
		)






	# Consistency 

	#subtotal = fields.Float(
	#		string = 'Sub-total', 
			#required=True, 
	#	)

	#method = fields.Selection(
	#		string="Medio", 
	#		selection = ord_vars._payment_method_list, 			
	#		required=True, 
	#	)

	# Number of paymethods  
	#pm_complete = fields.Boolean(
	#							default = False, 
	#							readonly=False,
								#string="Pm Complete",
								#compute="_compute_pm_complete",
	#)






	# Print Order
	#@api.multi 
	#def print_order(self):
		#print 
		#print 'Print Order'
		#ret = self.treatment.open_myself()
		#return ret 
	# open_treatment









	# Payment Method 
	x_payment_method = fields.Many2one(
			'openhealth.payment_method',
			string="Pago", 
		)







	# Open Treatment
	@api.multi 
	def open_treatment(self):


		#print 
		#print 'Open Treatment'
		#ret = self.treatment.open_myself()



		if self.treatment.name != False:
			ret = self.treatment.open_myself()
		elif self.cosmetology.name != False:
			ret = self.cosmetology.open_myself()
		else:
			#print 'This should not happen !'
			ret = 0 


		return ret 
	# open_treatment



	# Open Cosmetology
	#@api.multi 
	#def open_cosmetology(self):

		#print 
		#print 'Open cosmetology'
	#	ret = self.cosmetology.open_myself()
	
	#	return ret 
	# open_cosmetology










	# Open Myself
	@api.multi 
	def open_myself(self):

		#print 
		#print 'Open Myself'

		order_id = self.id  

		return {

			# Mandatory 
			'type': 'ir.actions.act_window',
			'name': 'Open Order Current',


			# Window action 
			'res_model': 'sale.order',
			'res_id': order_id,


			# Views 
			"views": [[False, "form"]],
			'view_mode': 'form',
			'target': 'current',


			#'view_id': view_id,
			#"domain": [["patient", "=", self.patient.name]],
			#'auto_search': False, 

			'flags': {
					'form': {'action_buttons': True, }
					#'form': {'action_buttons': True, 'options': {'mode': 'edit'}}
			},			

			'context':   {

			}
		}
	# open_myself










	# Partner 
	partner_id = fields.Many2one(
			'res.partner',
			string = "Cliente", 	

			ondelete='cascade', 			

			required=True, 
		)



	# Family 
	x_family = fields.Selection(

			#string = "Tipo", 	
			string = "Familia", 	

			default='product',
			
			#selection = jxvars._family_list, 
			selection = treatment_vars._family_list, 


			#required=True, 
			required=False, 
		)










	



	#compute="_compute_x_doctor_name",
	#@api.multi
	#@api.depends('x_doctor')

	#def _compute_x_doctor_name(self):
	#	for record in self:
	#		record.x_doctor_name = record.x_doctor.name 




	# Doctor name  
	x_partner_name = fields.Char(
									default = 'generic partner',
									#compute="_compute_x_partner_name",
	)
	
	#@api.multi
	#@api.depends('partner_id')

	#def _compute_x_partner_name(self):
	#	for record in self:
	#		record.x_partner_name = record.partner_id.name 


























	# Number of paymethods  
	#pm_complete = fields.Boolean(
	#							default = False, 
	#							readonly=False,
								#string="Pm Complete",
								#compute="_compute_pm_complete",
	#)
	
	#@api.multi
	#@api.depends('pm_total')

	#def _compute_pm_complete(self):
	#	#print 'Compute Pm Complete'
	#	for record in self:
	#		if record.pm_total == record.x_amount_total: 
	#			#print 'Equal !'
	#			record.pm_complete = True
				#record.state = 'payment'
	#		else:
	#			#print 'Not Equal'
	#		#print record.pm_total
	#		#print record.x_amount_total
	#		#print record.pm_complete
	#		#print record.state





	# Payment Complete
	x_payment_complete = fields.Boolean(
								#default = False, 
								#readonly=False,
								#string="Pm Complete",
	)





	@api.multi 
	def x_reset(self):

		#print 
		#print 'jx'
		#print 'Reset'



		#self.procedure_ids.unlink()
		self.x_payment_method.unlink()
	


		#self.x_sale_document_type = False
		#self.x_sale_document.unlink()




		#self.x_appointment.unlink()
		#self.x_appointment = False
		#self.x_appointment.x_machine = False
#jz
		if self.x_appointment.x_machine != False:
			self.x_appointment.x_machine = False




		#self.pre_state = 'draft'
		self.state = 'draft'			# This works. 
		self.x_confirmed = False

		#print 
		#print 
		#print 

	# x_reset







	x_confirmed = fields.Boolean(
			default=False, 
		)




	# Total of Payments
	pm_total = fields.Float(
								#string="Total",
								#compute="_compute_pm_total",
	)
	
	@api.multi
	#@api.depends('x_payment_method')

	def _compute_pm_total(self):
		for record in self:
			total = 0.0
			for pm in record.x_payment_method:
				total = total + pm.subtotal
			record.pm_total = total
			record.x_payment_complete = True
	# _compute_pm_total





	# Target 
	x_target = fields.Selection(
			string="Target", 

			#selection = jxvars._target_list, 
			selection = app_vars._target_list, 

			compute='_compute_x_target', 
		)




	#@api.multi
	@api.depends('x_doctor')

	def _compute_x_target(self):
		for record in self:

			#if record.x_doctor.name != False: 
			if record.treatment.name != False: 
				record.x_target = 'doctor'

			#if record.x_therapist.name != False: 
			if record.cosmetology.name != False: 
				record.x_target = 'therapist'









	# Machine Required  
	x_machine_req = fields.Char(

			string='Sala req.',

			compute='_compute_x_machine_req', 
		)

	#@api.multi
	@api.depends('x_product')

	def _compute_x_machine_req(self):
		for record in self:

			tre = record.x_product.x_treatment

			mac = cosvars._hash_tre_mac[tre]

			record.x_machine_req = mac






	# Product
	x_product = fields.Many2one(
			'product.template',			
			string="Producto",
			
			#required=True, 
			required=False, 
			

			domain = [
						('x_treatment', '=', 'laser_co2'),						
					],


			compute='_compute_x_product', 
			)


	#@api.multi
	@api.depends('order_line')

	def _compute_x_product(self):
		for record in self:

			flag = False

			for line in record.order_line:
				if line.product_id.x_treatment == 'laser_co2':
					product = line.product_id.id
					flag = True 


			if flag: 
				record.x_product = product







	# Treatment
	x_treatment = fields.Char(
			#string="Tratamiento",
			
			#required=True, 
			required=False, 
			
			compute='_compute_x_treatment', 
			)

	#@api.multi
	@api.depends('x_product')
	def _compute_x_treatment(self):
		for record in self:
			record.x_treatment = record.x_product.x_treatment
	# _compute_x_treatment







# ----------------------------------------------------------- Relational ------------------------------------------------------

	# Appointment 
	x_appointment = fields.Many2one(
			'oeh.medical.appointment',
			
			string='Cita', 

			#required=True, 
			required=False, 

			compute='_compute_x_appointment', 
			)



	@api.multi
	#@api.depends('x_appointment')

	def _compute_x_appointment(self):
		for record in self:


			if record.x_family == 'procedure':				
				app = self.env['oeh.medical.appointment'].search([
																	('patient', '=', record.patient.name), 
																	('x_type', '=', 'procedure'),
																	('doctor', '=', record.x_doctor.name), 
																	#('x_target', '=', record.x_target),	
																],
																	order='appointment_date desc',
																	limit=1,
																)

			#elif record.x_family == 'consultation':			
			elif record.x_family == 'consultation'	or  record.x_family == 'product':			

				app = self.env['oeh.medical.appointment'].search([
																	('patient', '=', record.patient.name), 
																	('x_type', '=', 'consultation'),
																	('doctor', '=', record.x_doctor.name), 
																	#('x_target', '=', record.x_target),	
																],
																	order='appointment_date desc',
																	limit=1,
																)
			

			#if record.x_appointment != False:
			#if record.x_appointment.name != False:
			record.x_appointment = app




			#if record.x_target == 'doctor': 
			#	app = self.env['oeh.medical.appointment'].search([
			#														('patient', '=', record.patient.name), 
			#														('x_type', '=', 'procedure'),
			#														('x_target', '=', record.x_target),
			#														('doctor', '=', record.x_doctor.name), 
			#												],
			#												order='appointment_date desc',
			#												limit=1,)


			#else:		# therapist 
			#	app = self.env['oeh.medical.appointment'].search([
			#														('patient', '=', record.patient.name), 
			#														('x_type', '=', 'procedure'),
			#														('x_target', '=', record.x_target),

			#														('x_therapist', '=', record.x_therapist.name), 
			#												],
			#												order='appointment_date desc',
			#												limit=1,)

			













	# Amount total 
	x_amount_total = fields.Float(
			#string = "x Amount Total",
			string = "x Total",
			compute="_compute_x_amount_total",
		)


	@api.multi
	#@api.depends('x_payment_method')

	def _compute_x_amount_total(self):
		for record in self:
			sub = 0.0

			for line in record.order_line:
				sub = sub + line.price_subtotal 

			if sub == 0.0:
				sub = float(record.x_ruc)

			record.x_amount_total = sub







	x_partner_vip = fields.Boolean(
			'Vip', 

			#readonly=True
			
			default=False, 

			compute="_compute_partner_vip",
			)

	@api.multi

	def _compute_partner_vip(self):
		for record in self:
			#print 
			#print 'jx'
			#print 'Compute Partner Vip'
			rec_set = self.env['sale.order'].search([
															('partner_id','=', record.partner_id.id),
															('state','=', 'sale'),
														]) 
			for rec in rec_set:
				#print rec
				for line in rec.order_line:
					#print line
					#print line.name 
					if line.name == 'Tarjeta VIP':
						#print 'Gotcha !!!'
						record.x_partner_vip = True 
					
					#print 
			#print 
			#print 
			#print 





# ---------------------------------------------- Event --------------------------------------------------------

	event_ids = fields.One2many(
			'openhealth.event',
			'order',		
			string="Eventos", 
		)



	x_cancel = fields.Boolean(
			string='', 
			default = False
		)



	@api.multi 
	def cancel_order(self):

		#print 
		#print 'Cancel'
		self.x_cancel = True



		self.state = 'cancel'



		ret = self.create_event()
		#ret = order_funcs.create_event(self)

		return(ret)




	@api.multi 
	def activate_order(self):
		#print 
		#print 'Cancel'
		self.x_cancel = False
		self.state = 'draft'




	@api.multi 
	def create_event(self):
		nr_pm = self.env['openhealth.event'].search_count([('order','=', self.id),]) 
		name = 'Evento ' + str(nr_pm + 1)
		x_type = 'cancel'

		return {
				'type': 'ir.actions.act_window',
				'name': ' New PM Current', 

				'view_type': 'form',
				'view_mode': 'form',	
				'target': 'current',

				'res_model': 'openhealth.event',				
				#'res_id': receipt_id,

				'flags': 	{
								#'form': {'action_buttons': True, 'options': {'mode': 'edit'}}
								'form': {'action_buttons': True, }
							},

				'context': {
								'default_order': self.id,
								'default_name': name,
								'default_x_type': x_type,
							}
				}
	# create_event







# ----------------------------------------------------------- Number ofs ------------------------------------------------------


	# Number of saledocs  
	nr_saledocs = fields.Integer(
			string="Documentos de venta",
			compute="_compute_nr_saledocs",
	)
	@api.multi
	def _compute_nr_saledocs(self):
		for record in self:

			receipt =			self.env['openhealth.receipt'].search_count([('order','=', record.id),]) 

			invoice =			self.env['openhealth.invoice'].search_count([('order','=', record.id),]) 

			advertisement =		self.env['openhealth.advertisement'].search_count([('order','=', record.id),]) 

			sale_note =			self.env['openhealth.sale_note'].search_count([('order','=', record.id),]) 
			
			ticket_receipt =	self.env['openhealth.ticket_receipt'].search_count([('order','=', record.id),]) 
			
			ticket_invoice =	self.env['openhealth.ticket_invoice'].search_count([('order','=', record.id),]) 

			record.nr_saledocs= receipt + invoice + advertisement + sale_note + ticket_receipt + ticket_receipt








	# Number of paymethods  
	nr_pay_methods = fields.Integer(
			string="Documentos de venta",
			compute="_compute_nr_pay_methods",
	)
	@api.multi
	def _compute_nr_pay_methods(self):

		for record in self:

			pm = self.env['openhealth.payment_method'].search_count([('order','=', record.id),]) 

			record.nr_pay_methods = pm
























# ---------------------------------------------- Create PM --------------------------------------------------------

	@api.multi 
	def create_payment_method(self):

		#print 
		#print 'Create Payment Method'



		#nr_pm = self.env['openhealth.payment_method'].search_count([('order','=', self.id),]) 
		#name = 'Pago ' + str(nr_pm + 1)
		name = 'Pago'
		method = 'cash'



		#total = self.x_amount_total
		balance = self.x_amount_total - self.pm_total

		
		#print nr_pm
		#print name
		#print method
		#print 




		# Create 
		#if payment_method_id == False:
		self.x_payment_method = self.env['openhealth.payment_method'].create({
																				'order': self.id,

																				'name': name,
																			
																				'method': method,
																			
																				'subtotal': balance,
																			
																				'pm_total': self.pm_total,
																			
																				'total': self.x_amount_total,

																				'balance': balance, 

																				'partner': self.partner_id.id, 

																				'date_created': self.date_order,


																				#'saledoc': 'receipt', 
																			})
		payment_method_id = self.x_payment_method.id 



#jz
		# State - Change
		#print 'State changes'

		

		#self.state = 'sale'
		#self.state = 'payment'
		self.state = 'sent'

		

		#print self.state
		#print 




		return {
				'type': 'ir.actions.act_window',
				'name': ' New PM Current', 

				'view_type': 'form',
				'view_mode': 'form',	
				'target': 'current',


				'res_model': 'openhealth.payment_method',				
				'res_id': payment_method_id,


				'flags': 	{
							'form': {'action_buttons': True, 'options': {'mode': 'edit'}}
							#'form': {'action_buttons': True, }
							},


				'context': {
							'default_order': self.id,

							'default_name': name,
							'default_method': method,
							'default_subtotal': balance,
							'default_total': self.x_amount_total,
							'default_pm_total': self.pm_total,
							'default_partner': self.partner_id.id,
							'default_date_created': self.date_order,
			

							#'default_saledoc': 'receipt', 
							}
				}

	# create_payment_method








# ---------------------------------------------- Create Sale Document --------------------------------------------------------

	@api.multi 
	def create_sale_document(self):
		#print 
		#print 'Create Sale Document'

		# Search 
		sale_document_id = self.env['openhealth.sale_document'].search([('order','=',self.id),]).id



		# Create 
		if sale_document_id == False:

			sale_document = self.env['openhealth.sale_document'].create({
																			'order': self.id,
																			'total': self.x_amount_total, 
																			'partner': self.partner_id.id,				
																		})
			sale_document_id = sale_document.id 


		self.sale_document = sale_document_id




		# State
		#print 'State changes'
		self.state = 'proof'
		#print self.state
		#print 




		return {
				'type': 'ir.actions.act_window',
				'name': ' New sale_document Current', 

				'view_type': 'form',
				'view_mode': 'form',	
				'target': 'current',


				'res_model': 'openhealth.sale_document',				
				'res_id': sale_document_id,


				'flags': 	{
							#'form': {'action_buttons': True, 'options': {'mode': 'edit'}}
							'form': {'action_buttons': True, }
							},


				'context': {
							'default_order': self.id,
							'default_total': self.x_amount_total,
							'default_partner': self.partner_id.id,
							}
				}

	# create_sale_document












# ---------------------------------------------- Vars --------------------------------------------------------

	#x_receipt = fields.One2many(
	receipt = fields.Many2one(

		'openhealth.receipt',
		
		#'order',

		string='Boleta de venta',
		)



	#x_invoice = fields.One2many(
	x_invoice = fields.Many2one(

		'openhealth.invoice',
		
		#'order',

		string='Factura',
		)




	x_advertisement = fields.Many2one(
		'openhealth.advertisement',		
		string='Canje',
		)

	x_sale_note = fields.Many2one(
		'openhealth.sale_note',		
		string='Nota de venta',
		)

	x_ticket_receipt = fields.Many2one(
		'openhealth.ticket_receipt',		
		string='Ticket Boleta',
		)

	x_ticket_invoice = fields.Many2one(
		'openhealth.ticket_invoice',		
		string='Ticket Factura',
		)























	x_payment_method_code = fields.Char(

			string="Código", 
						
			#required=True, 
			required=False, 
		)






	x_ruc = fields.Char(

			string="RUC", 
						
			#required=True, 
			required=False, 
		)


















	# Machine 
	x_machine = fields.Selection(
			#string="Máquina", 
			string="Sala", 
			#selection = jxvars._machines_list, 
			selection = app_vars._machines_list, 
			
			compute='_compute_x_machine', 
		
			#required=True, 
			required=False, 
		)






	x_appointment_date = fields.Datetime(
			string="Fecha", 
			#readonly=True,

			compute='_compute_x_appointment_date', 
			
			#required=True, 
			required=False, 
			)


	x_duration = fields.Float(
			string="Duración (h)", 
			#readonly=True, 

			compute='_compute_x_duration', 
			
			#required=True, 		
			required=False, 
			)




	#@api.multi
	#@api.depends('x_appointment')
	#def _compute_x_doctor(self):
	#	for record in self:
	#		record.x_doctor = record.x_appointment.doctor








	#@api.multi
	@api.depends('x_appointment')

	def _compute_x_appointment_date(self):
		for record in self:
			record.x_appointment_date = record.x_appointment.appointment_date



	#@api.multi
	@api.depends('x_appointment')

	def _compute_x_duration(self):
		for record in self:
			record.x_duration = record.x_appointment.duration



	#@api.multi
	@api.depends('x_appointment')

	def _compute_x_machine(self):
		for record in self:
			record.x_machine = record.x_appointment.x_machine









	# Chief complaint 
	#x_chief_complaint = fields.Selection(
	#		string = 'Motivo de consulta', 
	#		selection = jxvars._chief_complaint_list, 
	#		)







	vspace = fields.Char(
			' ', 
			readonly=True
		)
	
	
	order_line = field_One2many=fields.One2many(
		'sale.order.line',
		'order_id',

		#string='Order',
		#compute="_compute_order_line",
	)


	#@api.multi
	#@api.depends('x_partner_vip')
	
	#def _compute_order_line(self):
	#	for record in self:
	#		#print 'compute_order_line'
	#		#print record.x_partner_vip 
	#		ret = record.update_order_lines()
	#		#print ret 







	# Nr treatments 
	nr_treatments = fields.Integer(
			default=0,

			compute='_compute_nr_treatments', 
		)

	@api.multi
	#@api.depends('order_line')
	
	def _compute_nr_treatments(self):
		for record in self:

			nr = record.env['openhealth.treatment'].search_count([
																		('physician', '=', record.x_doctor.name ), 
																	])

			record.nr_treatments = nr






	# Nr cosmetologies 
	nr_cosmetologies = fields.Integer(
			default=0,

			compute='_compute_nr_cosmetologies', 
		)


	@api.multi
	#@api.depends('order_line')
	
	def _compute_nr_cosmetologies(self):
		for record in self:

			nr = record.env['openhealth.cosmetology'].search_count([
																		('physician', '=', record.x_doctor.name ), 
																	])

			record.nr_cosmetologies = nr



# ----------------------------------------------------------- Relationals ------------------------------------------------------

	treatment = fields.Many2one(
			'openhealth.treatment',
			ondelete='cascade', 
			string="Tratamiento", 
		)




	cosmetology = fields.Many2one(
			'openhealth.cosmetology',
			ondelete='cascade', 			
			string="Cosmiatría", 
		)




	closing = fields.Many2one(
			'openhealth.closing',
			ondelete='cascade', 
			string="Cierre", 
		)















	
	patient = fields.Many2one(
		
			'oeh.medical.patient',

			string='Paciente', 
	)
	
	
	
	

	#x_copy_created = fields.Boolean(
	#	default=False,
	#)

		

	
	
	
	
	
	
	# Nr lines 
	nr_lines = fields.Integer(
			
			default=0,

			string='Nr líneas',
			
			compute='_compute_nr_lines', 

			#required=True, 
			required=False, 
			)

	@api.multi
	#@api.depends('order_line')
	
	def _compute_nr_lines(self):
		for record in self:
			#record.name = 'SE00' + str(record.id) 
			#record.nr_lines = 0
			
			ctr = 0
			for l in record.order_line:
				ctr = ctr + 1
			record.nr_lines = ctr 
			
	
	
	
	
	
	# Order lines 

	@api.multi 
	def clean_order_lines(self):
		
		if self.state == 'draft':
			ret = self.remove_order_lines()
















# ----------------------------------------------------------- Create order lines ------------------------------------------------------
	#@api.multi 
	def x_create_order_lines_target(self, target):		

		#print 
		#print 'jx'
		#print target
		#print 

		order_id = self.id

		product = self.env['product.template'].search([
														('x_name_short','=', target),

														#('x_origin','!=', 'legacy'),
														('x_origin','=', False),
												])
		
		product_id = product.id

		price_unit = product.list_price
		
		x_price_vip = product.x_price_vip
		product_uom = product.uom_id.id

		
		#print product
		#print product.id
		#print product.uom_id.id
		#print 

		ol = self.order_line.create({
										'product_id': product_id,
										'order_id': order_id,										
										'state':'draft',
										'name': target,
										'price_unit': price_unit,
										'x_price_vip': x_price_vip,
										'product_uom': product_uom, 
									})
		return self.nr_lines

	



# ----------------------------------------------------------- Button - Update Lines ------------------------------------------------------
	@api.multi 
	def update_line(self, order_id, product_id, name, list_price, uom_id, x_price_vip):
		order = self.env['sale.order'].search([
															('id', '=', order_id),
															#('name', 'like', name),
													])
		line = order.order_line.create({
											'order_id': order.id,
											'product_id': product_id,
											'name': name,
											'product_uom': uom_id, 
											'x_price_vip': x_price_vip, 
											'x_partner_vip': self.x_partner_vip
										})
		return line
	# update_line





# ----------------------------------------------------------- Button - Update Order ------------------------------------------------------
	@api.multi 
	def update_order(self):

		# Order 
		order_id = self.id

		# Appointment 
		appointment = self.env['oeh.medical.appointment'].search([ 	
																	('patient', 'like', self.patient.name),	
																	('doctor', 'like', self.x_doctor.name), 	
																	('x_type', 'like', 'procedure'), 
																], 
																	order='appointment_date desc', limit=1)
		appointment_id = appointment.id
		self.x_appointment = appointment_id




		# Lines 
		ret = self.order_line.unlink()

		# Cosmetology 
		for service in self.cosmetology.service_ids:
			#print service

			line = self.update_line(	
										order_id, 
										service.service.id, 
										service.service.x_name_short, 
										service.service.list_price, 
										service.service.uom_id.id,
										service.service.x_price_vip
									)
			#print 



		# Doctor 
		#for service in self.consultation.service_co2_ids:
		for service in self.treatment.service_co2_ids:
			#print service

			line = self.update_line(	
										order_id, 
										service.service.id, 
										service.service.x_name_short, 
										service.service.list_price, 
										service.service.uom_id.id,

										service.service.x_price_vip
									)
			#print 
		
		for service in self.consultation.service_excilite_ids:
			#print service
			line = self.update_line(	
										order_id, 
										service.service.id, 
										service.service.x_name_short, 
										service.service.list_price, 										
										service.service.uom_id.id,

										service.service.x_price_vip
									)

		for service in self.consultation.service_ipl_ids:
			#print service
			line = self.update_line(	order_id, 
										service.service.id, 
										service.service.x_name_short, 
										service.service.list_price, 
										service.service.uom_id.id,

										service.service.x_price_vip
									)

		for service in self.consultation.service_ndyag_ids:
			#print service
			line = self.update_line(	order_id, 
										service.service.id, 
										service.service.x_name_short, 
										service.service.list_price, 
										service.service.uom_id.id,

										service.service.x_price_vip
									)

		for service in self.consultation.service_medical_ids:
			#print service
			line = self.update_line(	order_id, 
										service.service.id, 
										service.service.x_name_short, 
										service.service.list_price, 
										service.service.uom_id.id,

										service.service.x_price_vip
									)

		#print 

	# update_order 




	@api.multi 
	def update_order_lines_app(self):

		#print 
		#print 'jx'
		#print 'Update Order Lines'


		for line in self.order_line:

			#print line


			product_id = line.product_id


			# If Service 
			if product_id.type == 'service':



				appointment = self.env['oeh.medical.appointment'].search([ 	
															('doctor', 'like', self.x_doctor.name), 	
															('patient', 'like', self.patient.name),		
															('x_type', 'like', 'procedure'), 
															('x_target', '=', 'doctor'), 
															#('state', 'like', 'pre_scheduled'), 
														], 
														order='appointment_date desc', limit=1)

				appointment_id = appointment.id

				
				#print self.x_doctor
				#print self.patient

				
				#print appointment  
				#print appointment_id  



				# Line  
				line.x_appointment_date = appointment.appointment_date
				line.x_doctor_name = appointment.doctor.name
				line.x_duration = appointment.duration 
				
				#line.x_machine_oldachine = appointment.x_machine
				line.x_machine = False


				# Self 
				self.x_appointment = appointment

				#self.x_doctor = appointment.doctor
				#self.x_appointment_date = appointment.appointment_date
				#self.x_duration = appointment.duration
				#self.x_machine = appointment.x_machine 
		#print 
	# update_order_lines_app	






	@api.multi 
	def action_confirm(self):

		#print 
		#print 'jx'
		#print 'Action confirm - Over ridden'
		 
		



		#Write your logic here
		if self.x_family == 'consultation'	or 	self.x_family == 'procedure': 
			self.x_appointment.state = 'Scheduled'


		res = super(sale_order, self).action_confirm()
		#Write your logic here
		



		#oid = self.id
		#order = self.env['sale.order'].search([ ('id', '=', oid), ], order='date_order desc', limit=1)
		#order_id = order.id
		#partner_id = order.partner_id
		#partner_id_id = order.partner_id.id
		#patient_name = partner_id.name 
		#print order 
		#print order_id
		#print partner_id_id



		patient_name = self.partner_id.name
		#print patient_name




		go_card = False 

		order_line = self.order_line
		for line in order_line:
			#print line
			#print line.name 
			#print line.product_id.name

			if line.name == 'Tarjeta VIP':
				go_card = True



		if go_card:




			# Partner 
			pl = self.env['product.pricelist'].search([
																('name','=', 'VIP'),
															],
															#order='appointment_date desc',
															limit=1,)

			self.partner_id.property_product_pricelist = pl

			#print 'jx'
			#print self.partner_id
			#print pl 
			#print self.partner_id.property_product_pricelist.name 




			# Card 
			card = self.env['openhealth.card'].search([ ('patient_name', '=', patient_name), ], order='date_created desc', limit=1)
			card_id = card.id
			#print card 




			if card.name == False: 

				# Card name 
				counter = self.env['openhealth.counter'].search([('name', '=', 'vip')])
				counter.increase()

				#name = '00000005'
				name = str(counter.value).rjust(8, '0')




			return {

				# Mandatory 
				'type': 'ir.actions.act_window',
				'name': 'Open Consultation Current',


				# Window action 
				'res_model': 'openhealth.card',
				'res_id': card_id,


				# Views 
				"views": [[False, "form"]],
				'view_mode': 'form',
				'target': 'current',


				#'view_id': view_id,
				#"domain": [["patient", "=", self.patient.name]],
				#'auto_search': False, 

				'flags': {
						'form': {'action_buttons': True, }
						#'form': {'action_buttons': True, 'options': {'mode': 'edit'}}
				},			


				'context':   {

					#'search_default_treatment': treatment_id,

					#'default_patient': patient_id,
					#'default_doctor': doctor_id,
					#'default_treatment_id': treatment_id,


					'default_name': name,
					'default_patient_name': patient_name,
				}
			}		
	# action_confirm	







# ----------------------------------------------------------- Buttons - Order  ------------------------------------------------------

	@api.multi
	def remove_myself(self):  
		#print 
		#print 
		#print 'Remove Myself'
		#print self.name 
		self.x_reset()
		self.unlink()

		#self.x_appointment.x_machine = 'none'
		#order_id = self.id
		#print "id: ", order_id
		# Search 
		#rec_set = self.env['sale.order'].browse([order_id])
		#print "rec_set: ", rec_set
		# Write
		#ret = rec_set.write({
		#						'state': 'draft',
								#'x_machine': 'none',
		#					})
		#print ret

		#for rec in rec_set:
		#	rec.x_reset
		# Unlink 
		#ret = rec_set.unlink()
		#print "ret: ", ret
		

		#print 
		#print 
	# remove_myself






# ----------------------------------------------------------- Nr Mac Clones  ------------------------------------------------------

	@api.multi 
	def get_nr_mc(self):
		nr_mac_clones =	self.env['oeh.medical.appointment'].search_count([
																			('appointment_date','=', self.x_appointment.appointment_date),													
																			('x_machine','=', self.x_appointment.x_machine),
																		]) 
		return nr_mac_clones




# ----------------------------------------------------------- Button - Reseve Machine  ------------------------------------------------------

	@api.multi 
	def reserve_machine(self):
		#print
		#print 
		#print 'jx'
		#print 'Reserve Machine'
		#print 
		date_format = "%Y-%m-%d %H:%M:%S"
		duration = self.x_appointment.duration 
		delta = datetime.timedelta(hours=duration)


		# Easiest first 
		#self.x_appointment.x_machine = self.x_machine_req
		#m_list = ['laser_co2_1', 'laser_co2_2', 'laser_co2_3']


		m_dic = {
					'consultation':			[], 


					'laser_co2_1': 			['laser_co2_1', 'laser_co2_2', 'laser_co2_3'], 

					'laser_excilite': 		['laser_excilite'], 
				
					'laser_m22': 			['laser_m22'], 



					'laser_triactive': 		['laser_triactive'], 
					
					'chamber_reduction': 	['chamber_reduction'], 
					
					'carboxy_diamond': 		['carboxy_diamond'], 
			}



		m_list = m_dic[self.x_machine_req]

		ad_str = self.x_appointment.appointment_date


		k = 1.
		out = False 



		while not out		and  	  k < 6: 		



			for x_machine_req in m_list: 



				if not out: 				
					self.x_appointment.appointment_date = ad_str

					self.x_appointment.x_machine = x_machine_req

					nr_mc = self.get_nr_mc()



					#print k
					#print self.x_appointment.appointment_date				
					#print nr_mc



					if nr_mc == 1:		# Success - Get out 
						out = True 



					#print out 
					#print 




			if not out: 	# Error - Change the date 
				ad = datetime.datetime.strptime(self.x_appointment.appointment_date, date_format) 
				ad_dt = delta + ad
				ad_str = ad_dt.strftime("%Y-%m-%d %H:%M:%S")

				k = k + 1.
	# reserve_machine










	#----------------------------------------------------------- Quick Button ------------------------------------------------------------

	@api.multi
	def open_line_current(self):  

		consultation_id = self.id 

		return {
				'type': 'ir.actions.act_window',
				'name': ' Edit Order Current', 
				'view_type': 'form',
				'view_mode': 'form',
				'res_model': self._name,
				'res_id': consultation_id,
				'target': 'current',
				'flags': {
						#'form': {'action_buttons': True, 'options': {'mode': 'edit'}}
						'form': {'action_buttons': True, }
						},
				'context': {}
		}








# ----------------------------------------------------------- CRUD ------------------------------------------------------

	@api.multi
	def unlink(self):

		#print 
		#print 'Order - Unlink - Override'
		#print 
		
		for invoice in self:

			if invoice.state not in ('draft', 'cancel'):
				#print 'jx - Warning'				
				#raise Warning(('You cannot delete an invoice which is not draft or cancelled. You should refund it instead. - jx'))
				tra = 1 
				
		return models.Model.unlink(self)





# Write - Deprecated ?
	@api.multi
	def write(self,vals):

		#print 
		#print 'CRUD - Order - Write'
		#print 
		#print vals
		#print 
		#print 

		#if vals['x_doctor'] != False: 
		#	print vals['x_doctor']
		#if vals['user_id'] != False: 
		#	print vals['user_id']



		#Write your logic here
		res = super(sale_order, self).write(vals)
		#Write your logic here
		#print 
		#print 

		return res

	# CRUD 





#sale_order()


