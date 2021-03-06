# -*- coding: utf-8 -*-
#
# 	*** Appointment
#

# Created: 				14 Nov 2016
# Last updated: 	 	 26 Mar 2017

from openerp import models, fields, api
#from datetime import datetime
import datetime

from . import appfuncs
from . import time_funcs
#from . import jxvars
from . import defaults
from . import app_vars
from . import eval_vars



class Appointment(models.Model):

	_inherit = 'oeh.medical.appointment'

	#_name = 'openhealth.appointment'




	name = fields.Char(

			string="Cita #", 

			#default='',

			#compute='_compute_name', 
			required=True, 
			)

	vspace = fields.Char(
			' ', 
			readonly=True
			)





# ----------------------------------------------------------- Relational  ------------------------------------------------------

	consultation = fields.Many2one('openhealth.consultation',
		string="Consulta",

		#ondelete='cascade', 			# Very important. 
	)


	procedure = fields.Many2one('openhealth.procedure',
		string="Procedimiento",

		#ondelete='cascade', 
	)

	procedure_cos = fields.Many2one('openhealth.procedure.cos',
		string="Proc. - Cos",
		#ondelete='cascade', 
	)



	session = fields.Many2one('openhealth.session',
		string="Sesión",
		#ondelete='cascade', 
	)



	control = fields.Many2one('openhealth.control',
		string="Control",		
		#ondelete='cascade', 
	)








	x_target = fields.Selection(
			string="Target", 
			selection = app_vars._target_list, 
			index=True,

			required=True, 
		)





	#@api.multi 
	#def get_x_target(self):
	#	return self.x_target


	#x_target = 'therapist'

	#x_target = get_x_target
	#x_target = self.x_target




	#@api.multi
	#def _compute_x_type(self):
	#	for record in self:
	#		record.x_type = record.x_target





	# Doctor 
	doctor = fields.Many2one(
			'oeh.medical.physician',			
			string = "Médico", 

			#default=defaults._doctor,
			
			required=True, 
			#required=False, 
			readonly = False, 
			

			#domain = [						
						#('x_type', '=', 'therapist'),
						#('x_type', '=', _compute_x_type ),
			#		],
			)







	# Number of clones  
	nr_clones = fields.Integer(
			string="nr_clones",
			compute="_compute_nr_clones",
	)
	@api.multi
	def _compute_nr_clones(self):
		for record in self:
			record.nr_clones =	self.env['oeh.medical.appointment'].search_count([
																						('appointment_date','=', record.appointment_date),
																						('doctor','=', record.doctor.name),
																					]) 
			if record.nr_clones > 1:
				record.state = 'error'






	# Number of mac_clones  
	nr_mac_clones = fields.Integer(
			string="nr_mac_clones",
			compute="_compute_nr_mac_clones",
	)
	@api.multi
	def _compute_nr_mac_clones(self):
		for record in self:

			if record.x_machine != False: 

				record.nr_mac_clones =	self.env['oeh.medical.appointment'].search_count([

																						('appointment_date','=', record.appointment_date),

																						('x_machine','=', record.x_machine),
					
																					]) 
				if record.nr_mac_clones > 1:
					record.state = 'error'

			else:
				record.nr_mac_clones = 1 









	#x_tree = fields.Boolean(
	#	)




	# Display 
	x_display = fields.Char(
			compute='_compute_x_display', 
		)


	@api.multi
	#@api.depends('x_appointment')

	def _compute_x_display(self):
		for record in self:

			#record.x_display = record.x_patient_name_short + ' - '  + record.x_doctor_code + ' - ' + record.x_type_cal 
			record.x_display = record.x_patient_name_short + ' - '  + record.x_doctor_code + ' - ' + record.x_type_cal + ' - ' + record.x_state_short
			

			#if record.x_machine != False	or 	record.x_machine_cos != False:
			if record.x_machine != False:
				record.x_display = record.x_display + ' - ' + record.x_machine_short






	# State short 
	_hash_state = {
						#False:				'', 

						'Scheduled':				'1',

						'pre_scheduled':			'2',

						'pre_scheduled_control':	'3',

						'error':					'55',
					}



	x_state_short = fields.Char(
			compute='_compute_x_state_short',
		)

	#@api.multi
	@api.depends('state')
	def _compute_x_state_short(self):
		for record in self:

			if record.state != False:
				record.x_state_short = self._hash_state[record.state]





	

	_hash_x_machine = {
							False:				'', 

							'laser_co2_1':		'C1',
							'laser_co2_2':		'C2',
							'laser_co2_3':		'C3',
							
							#'laser_co2_1':		'Co2_1',
							#'laser_co2_2':		'Co2_2',
							#'laser_co2_3':		'Co2_3',


							'laser_excilite':	'Exc',

							'laser_m22':		'M22',




							'laser_triactive':		'Tri',
							'chamber_reduction':	'Cam',
							'carboxy_diamond':		'CaDi',
						}



	x_machine_short = fields.Char(
			compute='_compute_x_machine_short',
		)




	#@api.multi
	@api.depends('x_machine')
	def _compute_x_machine_short(self):
		for record in self:
			if record.x_machine != False:
				record.x_machine_short = self._hash_x_machine[record.x_machine]










	x_machine = fields.Selection(
			string="Sala", 

			selection = app_vars._machines_list, 

			#required=True, 
		)

















	x_error = fields.Integer(			
			default = 0, 
			required=True, 
		)


	# Create procedure 
	x_create_procedure_automatic = fields.Boolean(
			
			#string="¿ Crear procedimiento de manera automática ?",
			string="¿ Crear Cita para el Procedimiento ?",

			default=True, 
			
			#required=True, 
		)






	# Chief complaint 
	x_chief_complaint = fields.Selection(			# Necessary 
			string = 'Motivo de consulta', 

			#selection = jxvars._pathology_list, 
			#selection = jxvars._chief_complaint_list, 
			selection = eval_vars._chief_complaint_list, 

			#required=True, 
			)


	#jxx
	@api.onchange('x_chief_complaint')

	def _onchange_x_chief_complaint(self):

		#print 
		#print 'On change Chief complaint'


		if self.x_chief_complaint != False:	

			#t = self.env['openhealth.treatment'].search([	
			#													('chief_complaint', 'like', self.x_chief_complaint), 
			#													('patient', 'like', self.patient.name),
			#												])

			t = self.env['openhealth.treatment'].search([
																#('chief_complaint', 'like', 'acne_active'), 
																('chief_complaint', 'like', self.x_chief_complaint), 

																#('patient', 'like', 'Revilla')], 
																('patient', 'like', self.patient.name),


																#('physician', 'like', 'Chavarri'),
																('physician', 'like', self.doctor.name),


																],
																order='start_date desc',
																limit=1,
															)


			#print t
			#if not (t == False  or  t == nil):



			#if t != False:
			if len(t) == 1:
				#print 'found'
				self.treatment = t.id



			else:
				tra = 1 
				#print 'empty'

				#self.open_treatment_current()

				#return {
				#	'warning': {
				#		'Cita': "Error: El Tratamiento no existe.",
						#'Para el paciente': self.patient.name,
				#	}}


			
			#print self.treatment 

		#print 







	APPOINTMENT_STATUS = [
			
			# jx 
			('Scheduled', 		'Confirmado'),
			('pre_scheduled', 	'No confirmado'),
			('pre_scheduled_control', 	'Pre-cita'),


			('error', 			'Error'),


			# OeHealth 
			#('Scheduled', 'Scheduled'),
			#('Completed', 'Completed'),
			#('Invoiced', 'Invoiced'),
			#('Completed', 'Completo'),
			#('Invoiced', 'Facturado'),
		]



	state = fields.Selection(

			selection = APPOINTMENT_STATUS, 
			string="Estado",
			
			default='pre_scheduled',

			readonly=False, 
			required=True, 
		)





	APPOINTMENT_STATUS_PROXY = [
									('pre_scheduled', 	'No confirmado'),
									('Scheduled', 		'Confirmado'),
								]

	x_state_proxy = fields.Selection(
			selection = APPOINTMENT_STATUS_PROXY, 
		)








	# Patient def

	patient = fields.Many2one(
			'oeh.medical.patient',
			
			string = "Paciente", 	

			#default = defaults._patient,

			ondelete='cascade', 			

			#required=True, 
			readonly = False, 
		)







	x_patient_name_short = fields.Char(
			compute='_compute_x_patient_name_short', 
		)


	#@api.multi
	@api.depends('patient')

	def _compute_x_patient_name_short(self):
		for record in self:
			patient_name = record.patient.name
			first_half = patient_name.split(' ')[0]
			record.x_patient_name_short = first_half













	# X Doctor Code 
	x_doctor_code = fields.Char(
			compute='_compute_x_doctor_code',
		)

	#@api.multi
	@api.depends('doctor')
	def _compute_x_doctor_code(self):
		for record in self:
			#record.x_doctor_code = self._hash_doctor_code[record.doctor.name]
			record.x_doctor_code = app_vars._hash_doctor_code[record.doctor.name]













	# On change - Machine

	@api.onchange('x_machine')

	def _onchange_x_machine(self):

		#print 
		#print 'On change Machine'


		if self.x_machine != False:	

			#print self.x_machine 

			#print self.doctor.name
			#print self.patient.name
			#print self.appointment_date
			#print self.x_date
			#print self.duration
			#print self.appointment_end
			#print 

			self.x_error = 0



			# Check for collisions 

			#ret, doctor_name, start, end = appfuncs.check_for_collisions(self, self.appointment_date, self.doctor.name, self.duration, self.x_machine)
			#ret, doctor_name, start, end = appfuncs.check_for_collisions(self, self.appointment_date, self.doctor.name, self.duration, self.x_machine, 'machine')
			ret, doctor_name, start, end = appfuncs.check_for_collisions(self, self.appointment_date, self.doctor.name, self.duration, self.x_machine, 'machine', self.x_type)



			if ret != 0:	# Error 

				self.x_error = 1
				self.x_machine = False

				return {
							'warning': {
									'title': "Error: Colisión !",
									'message': 'La sala ya está reservada: ' + start + ' - ' + end + '.',
						}}



			else: 			# Success 

				#print 'Success !'
				#print 
				

				# Treatment 
				self.treatment = self.env['openhealth.treatment'].search([

															('patient', 'like', self.patient.name),
															('physician', 'like', self.doctor.name),

															],
															order='start_date desc',
															limit=1,
														)

				#print self.treatment 



		#print









# ----------------------------------------------------------- On change - Doctor  ------------------------------------------------------

	@api.onchange('doctor', 'x_type')

	def _onchange_doctor(self):

		#print 
		#print 'On change Doctor'
		#print self.x_machine
		#print self.doctor.name



		if self.doctor.name != False:

			#print self.doctor.name
			#print self.patient.name
			#print self.appointment_date
			#print self.x_date
			#print self.duration
			#print self.appointment_end
			#print 

			self.x_error = 0




			# Check for collisions
			ret = 0 


			#ret, doctor_name, start, end = appfuncs.check_for_collisions(self, self.appointment_date, self.doctor.name, self.duration, False, 'doctor')
			ret, doctor_name, start, end = appfuncs.check_for_collisions(self, self.appointment_date, self.doctor.name, self.duration, False, 'doctor', self.x_type)


			#print ret 




			if ret != 0:	# Error 

				#print 'Error: Collision !'
				#print 

				self.x_error = 1
				self.doctor = False

				return {
							'warning': {
									'title': "Error: Colisión !",
									'message': 'Cita ya existente, con el ' + doctor_name + ": " + start + ' - ' + end + '.',
						}}


			else: 			# Success  
				tra = 1
				#print 'Success !'
				#print 


		#print 

	# _onchange_doctor






	# Date 
	appointment_date = fields.Datetime(
			string="Fecha", 
			readonly=False,
			#states={'Scheduled': [('readonly', False)]})
			)




	x_date = fields.Date(
			string="Fecha", 

			#default = fields.Date.today, 
			compute="_compute_x_date",
			#required=True, 
		)

	#@api.multi
	@api.depends('appointment_date')

	def _compute_x_date(self):

		date_format = "%Y-%m-%d %H:%M:%S"
		#date_format = "%Y-%m-%d"

		for record in self:
			#record.x_date = record.appointment_date
			#record.x_date = record.appointment_date.strftime("%Y-%m-%d")

			dt = datetime.datetime.strptime(record.appointment_date, date_format)


			record.x_date = dt.strftime("%Y-%m-%d")




	#x_time = fields.Date(
	#x_time = fields.Datetime(
	x_time = fields.Char(
			string="Hora", 

			compute="_compute_x_time",
		)

	#@api.multi
	@api.depends('appointment_date')

	def _compute_x_time(self):

		#print 
		#print 'compute x_time'

		date_format = "%Y-%m-%d %H:%M:%S"
		#date_format = "%H:%M:%S"

		for record in self:
			#record.x_time = record.appointment_date
			
			#record.x_time = record.appointment_date.strftime("%H:%M:%S")


			dt = datetime.datetime.strptime(record.appointment_date, date_format)
			delta = datetime.timedelta(hours=5)
			dt = dt - delta
			#print dt

			record.x_time = dt.strftime("%H:%M:%S")

			if record.state == 'pre_scheduled_control':
				record.x_time = ''


		#print 





	# Date end 
	appointment_end = fields.Datetime(
			string="Fecha fin", 		
			readonly=True, 
			)








	# Colors 
	color_patient_id = fields.Integer(
			default=2,
		)



	# Color Doctor id 
	_hash_colors_doctor = {

			'Dra. Acosta': 1,
			'Dr. Canales': 2,
			'Dr. Chavarri': 3,
			'Dr. Escudero': 4,
			'Dr. Gonzales': 5,
			'Dr. Vasquez': 6,

		}


	color_doctor_id = fields.Integer(
			default=1,
			compute='_compute_color_doctor_id', 
		)


	#@api.multi
	@api.depends('doctor')
	def _compute_color_doctor_id(self):
		for record in self:	
			record.color_doctor_id = self._hash_colors_doctor[record.doctor.name]






	# Color x_type id 
	_hash_colors_x_type = {


			'Procedimiento': 1,
			'procedure': 1,

			'Consulta': 2,
			'consultation': 2,



			'procedure_pre_scheduled': 3,
			

			'Sesion': 4,
			'session': 4,

			
			'Control': 5,
			'control': 5,
			
		}


	color_x_type_id = fields.Integer(
			default=1,
			compute='_compute_color_x_type_id', 
		)


	#@api.multi
	@api.depends('x_type')
	def _compute_color_x_type_id(self):
		for record in self:	

			if record.x_type == 'procedure'   and   record.state == 'Pre-scheduled':
				#print 'Gotcha !!!'
				record.color_x_type_id = self._hash_colors_x_type['procedure_pre_scheduled']

			else:
				record.color_x_type_id = self._hash_colors_x_type[record.x_type]








	# Duration


	_hash_duration = {
					'0.25' 	: 0.25, 

     				'0.5' 	: 0.5, 

     				#'0.75' 	: 0.75, 
     				#'1.0' 	: 1.0, 
     				#'2.0' 	: 2.0, 
				}




	_duration_list = [
        			('0.25', 	'15 min'),
        			('0.5', 	'30 min'),

					#('0.75', 	'45 min'),
        			#('1.0', 	'60 min'),
        			#('2.0', 	'120 min'),
        		]




     # Duration min 

	x_duration_min = fields.Selection(

			selection = _duration_list, 

			string="Duración (min)", 
		
			#default = '0.5',
			#default = '0.25',

			#readonly=True,
		)





	#@api.onchange('x_type')
	#def _onchange_x_type(self):
	#	if self.x_type != False:	
	#		if self.x_type == 'consultation'  or  self.x_type == 'procedure':
	#			self.x_duration_min = '0.5'
	#		elif self.x_type == 'control':
	#			self.x_duration_min = '0.25'







	#@api.onchange('x_duration_min')
	#def _onchange_x_duration_min(self):
	#	if self.x_duration_min != False:	
			#self.duration = self._hash_duration[self.x_duration_min]
	#		self.duration = self._hash_duration[self.x_duration_min]









	# Duration 

	duration = fields.Float(
			string="Duración (h)", 			
			compute='_compute_duration', 
			readonly=True, 
		)



	#@api.multi
	@api.depends('x_type')
	
	def _compute_duration(self):

		for record in self:	

			#if record.x_type == 'consultation'  or  record.x_type == 'procedure':
			if record.x_type == 'consultation'   or   record.x_type == 'procedure'   or   record.x_type == 'session':

				record.duration = 0.5

			elif record.x_type == 'control':
			#elif record.x_type == 'control'  or  record.x_type == 'session':

				record.duration = 0.25








	


	# Type 
	_type_list = [
        			('consultation', 'Consulta'),
        			#('procedure', 'Procedimiento'),
        			('procedure', 'Procedimiento'),
        			('session', 'Sesión'),
        			('control', 'Control'),

        			#('Consulta', 'Consulta'),
        			#('Procedimiento', 'Procedimiento'),
        			#('Sesion', 'Sesión'),
        			#('Control', 'Control'),
        		]



    # x_type 
	x_type = fields.Selection(
				selection = _type_list, 
				string="Tipo",
				#default="consultation",
				required=True, 
				)






	_type_cal_dic = {
        			'consultation': 	'C',
        			'procedure': 		'P',
        			'session': 			'S',
        			
        			#'control': 			'X',


        			'Consulta': 	'C',
        			'Procedimiento': 		'P',
        			'Sesion': 			'S',


        			#'X': 			'Ctl',
        			'control': 			'Ctl',
        			'Control': 			'Ctl',
        		}



	_type_cal_list = [
        			('C', 'C'),
        			('P', 'P'),
        			('S', 'S'),

        			#('X', 'Ctl'),
        			('Ctl', 'Ctl'),

        			#('consultation', 'C'),
        			#('procedure', 'P'),
        			#('session', 'S'),
        			#('control', 'X'),
        		]


	x_type_cal = fields.Selection(
				selection = _type_cal_list, 
				#string="Tipo",

				
				compute='_compute_x_type_cal', 
				)


	#@api.onchange('x_type')
	#def _onchange_x_type(self):
	#	self.x_type_cal = self._type_cal_dic[self.x_type]



	#@api.multi
	@api.depends('x_type')
	
	def _compute_x_type_cal(self):

		for record in self:	

			record.x_type_cal = self._type_cal_dic[record.x_type]








	# ----------------------------------------------------------- On Change - Patient Doctor ------------------------------------------------------

	@api.onchange('patient','doctor')
	def _onchange_patient_doctor(self):


		if self.patient != False and self.doctor != False:
			


			if self.x_target == 'doctor': 	
				
				treatment = self.env['openhealth.treatment'].search([
																				('patient', 'like', self.patient.name),
																				
																				('physician', 'like', self.doctor.name),
																			
																			],
																				order='start_date desc',
																				limit=1,
																			)
				self.treatment = treatment



			else: 

				cosmetology = self.env['openhealth.cosmetology'].search([
																				('patient', 'like', self.patient.name),
																				
																				('physician', 'like', self.doctor.name),
																			
																			],
																				order='start_date desc',
																				limit=1,
																			)
				self.cosmetology = cosmetology
			


			#print 

	# _onchange_patient_doctor















	# ----------------------------------------------------------- Indexes ------------------------------------------------------

	treatment = fields.Many2one(
			
			'openhealth.treatment',
			
			string="Tratamiento",
			
			ondelete='cascade', 
			
			required=False, 
			#required=True, 

			#compute='_compute_treatment', 
		)


	#@api.multi
	#@api.depends('patient', 'doctor')
	#def _compute_treatment(self):
	#	for record in self:
	#		print 'jz'
	#		if record.patient != False and record.doctor != False:
	#			print 'jz'
	#			tre = self.env['openhealth.treatment'].search([
	#																			('patient', '=', record.patient.name),
	#																			('doctor', '=', record.doctor.name),
	#																],
																	#order='start_date desc',
	#																limit=1,
	#																)
	#			record.treatment = tre






	#@api.multi
	#@api.depends('patient', 'doctor')
	#def _compute_treatment(self):
	#	for record in self:
	#		if record.patient != False and record.doctor != False:
				#treatment = self.env['openhealth.treatment'].search([
				#																('patient', 'like', self.patient.name),
				#																('doctor', 'like', self.doctor.name),
				#															],
				#																order='start_date desc',
				#																limit=1,
				#															)
				#record.treatment = treatment
				#record.treatment.id = 3
	#			#print 'jx'

















	#@api.multi
	#@api.depends('start_date')

	#def _compute_name(self):
	#	#print 'compute name'
	#	for record in self:
	#		idx = record.id
	#		if idx < 10:
	#			pre = 'AP000'
	#		elif idx < 100:
	#			pre = 'AP00'
	#		elif idx < 1000:
	#			pre = 'AP0'
	#		else:
	#			pre = 'AP'
	#		record.name =  pre + str(idx) 
	#	#print self.name 
	#	#print 






# ----------------------------------------------------------- Open ------------------------------------------------------

	def open_popup(self):
	#def open_current(self):

		#the best thing you can calculate the default values 
		# however you like then pass them to the context

		#print 
		#print 'open popup'
		#print 

		return {

        	'type': 'ir.actions.act_window',

        	'name': 'Import Module',

        	'view_type': 'form',

        	'view_mode': 'form',


			#'target': 'new',
			'target': 'current',


        	'res_model': 'oeh.medical.appointment',


        	#'context': {
        	#		#'default_partner_id':value, 			
        	#		#'default_other_field':othervalues        			
        	#		},

    		}
	# open_popup










# ----------------------------------------------------------- Buttons - Appointment  ------------------------------------------------------

	@api.multi
	def remove_appointment(self):  

		#print 
		#print 'Remove Appointment'

		appointment_id = self.id
		#print "id: ", appointment_id
		
		rec_set = self.env['oeh.medical.appointment'].browse([appointment_id])
		#print "rec_set: ", rec_set
		
		ret = rec_set.unlink()
		#print "ret: ", ret
		#print 






# ----------------------------------------------------------- Treatment  ------------------------------------------------------


	# Button - Treatment 
	# -------------------
	@api.multi
	def open_treatment_current(self):  

		#print 
		#print 'Open Treatment'

		patient_id = self.patient.id 
		#print patient_id


		doctor_id = self.doctor.id
		#print doctor_id 


		return {

			# Mandatory 
			'type': 'ir.actions.act_window',
			'name': 'Open Treatment Current',

			# Window action 
			'res_model': 'openhealth.treatment',

			# Views 
			"views": [[False, "form"]],
			'view_mode': 'form',


			#'target': 'current',
			#'target': 'inline'.
			'target': 'new',


			'flags': {
						'form': {'action_buttons': True, 'options': {'mode': 'edit'}}
						#'form': {'action_buttons': True, }
					},


			'context':   {
				'search_default_patient': patient_id,

				'default_patient': patient_id,

				'default_doctor': doctor_id,

			}

		}






	# Search Treatment
	@api.multi
	def search_treatment(self):

		#print 
		#print 'Search Treatment'


		treatment = self.env['openhealth.treatment'].search([

															#('patient', 'like', 'Revilla')], 
															('patient', 'like', self.patient.name),

															#('physician', 'like', 'Chavarri'),
															('physician', 'like', self.doctor.name),

															],
															order='start_date desc',
															limit=1,
														)

		self.treatment = treatment.id
		#print self.treatment  






	# Create Treatment
	@api.multi
	def create_treatment(self):

		#print 
		#print 'Create Treatment'

		patient_id = self.patient.id
		doctor_id = self.doctor.id
		start_date = self.appointment_date

		#chief_complaint = self.x_chief_complaint


		treatment = self.env['openhealth.treatment'].create(
																{
																'patient': patient_id,	

																'physician': doctor_id,

																'start_date': start_date, 

																#'chief_complaint': chief_complaint, 
																}
														)
				
		self.treatment = treatment.id

		#print self.treatment  











# ----------------------------------------------------------- CRUD ------------------------------------------------------

	@api.model
	def create(self,vals):

		#print 
		#print 'jx Create - Override'
		#print 
		#print vals
		#print 
	

		appointment_date = vals['appointment_date']
		x_type = vals['x_type']

		if 'doctor' in vals:
			doctor = vals['doctor']
			#print "doctor: ", doctor
		

		if 'patient' in vals:
			patient = vals['patient']
			#print "patient: ", patient


		if 'treatment' in vals:
			treatment = vals['treatment']
			#print "treatment: ", treatment



		# Cosmetology 
		if 'cosmetology' in vals:
			cosmetology = vals['cosmetology']
			#print "cosmetology: ", cosmetology




		x_create_procedure_automatic = vals['x_create_procedure_automatic']
		#x_chief_complaint = vals['x_chief_complaint']


		#print "appointment date: ", appointment_date
		#print "x_type: ", x_type
		

		#print "x_create_procedure_automatic: ", x_create_procedure_automatic 
		#print x_chief_complaint
		#print


		#print self.treatment





		# Create Procedure 
		if x_type == 'consultation'  and  x_create_procedure_automatic:



			# Consultation 
			date_format = "%Y-%m-%d %H:%M:%S"

			adate_con = datetime.datetime.strptime(appointment_date, date_format)

			delta_fix = datetime.timedelta(hours=1.5)
			
			adate_base = adate_con + delta_fix



			




			#app = appfuncs.create_app_procedure(self, adate_base, doctor, patient, treatment, x_create_procedure_automatic, False)
			#app = appfuncs.create_app_procedure(self, adate_base, doctor, patient, treatment, x_create_procedure_automatic)
			#app = appfuncs.create_appointment_procedure(self, adate_base, doctor, patient, treatment, x_create_procedure_automatic)
			app = appfuncs.create_appointment_procedure(self, adate_base, doctor, patient, treatment, cosmetology, x_create_procedure_automatic)
			#print app 







		# Return 
		res = super(Appointment, self).create(vals)

		return res

	# create - CRUD



# CRUD





