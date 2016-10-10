from openerp import models, fields, api
from datetime import datetime

import jxvars



	

class Product(models.Model):
	#_name = 'openhealth.service'
	_inherit = 'product.template'









	_treatment_list = [
		('laser_co2',		'laser_co2'),
		('laser_excilite',	'laser_excilite'),
		('laser_ipl',		'laser_ipl'),
		('laser_ndyag',		'laser_ndyag'),
		]
	
	x_treatment = fields.Selection(
		selection=_treatment_list,
	)	
	
	
	


	_zone_list = [ 

		('areolas',		'areolas'), 
		('armpits',		'armpits'), 
		('arms',		'arms'), 

		('back',		'back'), 
		('belly',		'belly'), 
		('body_local',	'body_local'), 
		('breast',		'breast'), 

		('cheekbones',	'cheekbones'), 

		('face',		'face'),
		('face_all',	'face_all'), 
		('face_hands',	'face_hands'), 
		('face_local',	'face_local'), 
		('face_neck',	'face_neck'), 
		('face_neck_hands',	'face_neck_hands'),   
		('feet',		'feet'), 

		('gluteus',		'gluteus'), 

		('hands',		'hands'), 
		
		('legs',		'legs'), 
		('neck',		'neck'), 
		
		('package',		'package'), 

		('shoulders',	'shoulders'), 

		('vagina',		'vagina'), 
	]
	
	
	
	x_zone = fields.Selection(
		selection=_zone_list,
	)	
	
	
	
	_pathology_list = [ 
		
		('acne_active',			'acne_active'),
		('acne_sequels',	'acne_sequels'),
		('acne_sequels_1',	'acne_sequels_1'),
		('acne_sequels_2',	'acne_sequels_2'),
		('acne_sequels_3',	'acne_sequels_3'),
		('alopecia',			'alopecia'),

		('cyst',		'cyst'),

		('depilation',			'depilation'),

		('emangiomas',		'emangiomas'),

		('keratosis',	'keratosis'),
		('keratosis_1',	'keratosis_1'),
		('keratosis_2',	'keratosis_2'),
		('keratosis_3',	'keratosis_3'),

		('polyp',		'polyp'), 
		('ruby_point',	'ruby_point'),

		('mole_1',		'mole_1'),
		('mole_2',		'mole_2o'),
		('mole_3',		'mole_3'),
		('monalisa_touch',	'monalisa_touch'),

		('psoriasis',			'psoriasis'),
		
		('rejuvenation_face_1',	'rejuvenation_face_1'),
		('rejuvenation_face_2',	'rejuvenation_face_2'),
		('rejuvenation_face_3',	'rejuvenation_face_3'),
		('rejuvenation_face_hands',			'rejuvenation_face_hands'),
		('rejuvenation_face_neck',	'rejuvenation_face_neck'),
		('rejuvenation_face_neck_hands',	'rejuvenation_face_neck_hands'),
		('rejuvenation_facial',	'rejuvenation_facial'),
		('rejuvenation_hands',	'rejuvenation_hands'),
		('rejuvenation_neck',	'rejuvenation_neck'),
		('rosacea',			'rosacea'),
		('ruby_points',		'ruby_points'),
				
		('scar',		'scar'),
		('scar_1',		'scar_1'),
		('scar_2',		'scar_2'),
		('scar_3',		'scar_3'),
		('stains',		'stains'),
		('stains_1',	'stains_1'),
		('stains_2',	'stains_2'),
		('stains_3',	'stains_3'),

		('telangiectasia',	'telangiectasia'),
		
		('varices',			'varices'),
		('vitiligo',			'vitiligo'),

		('wart',		'wart'), 

	]
	
	
	x_pathology = fields.Selection(
		selection=_pathology_list,
	)
	