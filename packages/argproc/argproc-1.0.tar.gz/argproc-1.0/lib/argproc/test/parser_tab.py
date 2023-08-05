
# parser_tab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = '7\xf8\x91\rGRt\xc7\x81\xbe\xd8\xb9\x0f\x85\x05\xf4'
    
_lr_action_items = {'!':([17,55,],[36,36,]),'FLOAT':([11,19,24,34,50,56,58,],[25,25,25,25,25,25,25,]),'NAME':([0,1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,24,25,32,33,34,35,36,40,41,42,43,44,45,46,47,49,50,52,54,55,56,57,58,60,62,63,],[6,-8,-45,-11,-1,-10,-7,-9,6,-5,6,6,-3,-38,-37,-36,37,-40,6,-2,-6,6,-31,-30,-32,6,-45,53,-18,-21,-22,-23,-19,-20,-14,-12,-13,6,-4,-39,37,6,-33,6,-35,-15,-34,]),'LARROW':([1,3,4,6,7,8,10,21,25,32,33,40,41,42,43,44,45,46,47,49,57,60,62,63,],[-8,15,-11,-10,-7,-9,-5,-6,-31,-30,-32,-18,-21,-22,-23,-19,-20,-14,-12,-13,-33,-35,-15,-34,]),')':([4,6,22,23,25,26,27,28,29,30,31,32,33,48,49,57,58,59,60,63,],[-11,-10,-24,-27,-31,-28,-29,-16,-25,-26,49,-30,-32,57,-13,-33,63,-17,-35,-34,]),'(':([2,6,11,19,22,24,34,40,50,56,58,],[11,-10,24,24,11,24,24,11,24,24,24,]),'*':([1,4,6,7,8,10,25,32,33,40,41,42,43,44,45,46,47,49,57,60,62,63,],[-8,-11,-10,-7,-9,21,-31,-30,-32,-18,-21,-22,-23,-19,-20,-14,-12,-13,-33,-35,-15,-34,]),',':([4,6,22,23,25,26,27,28,29,30,31,32,33,37,38,39,40,41,42,43,44,45,46,47,48,49,51,53,57,59,60,61,62,63,],[-11,-10,-24,-27,-31,-28,-29,-16,-25,-26,50,-30,-32,-43,-41,55,-18,-21,-22,-23,-19,-20,-14,56,58,-13,50,-44,-33,-17,-35,-42,-15,-34,]),'RARROW':([1,3,4,6,7,8,10,21,25,32,33,40,41,42,43,44,45,46,47,49,57,60,62,63,],[-8,14,-11,-10,-7,-9,-5,-6,-31,-30,-32,-18,-21,-22,-23,-19,-20,-14,-12,-13,-33,-35,-15,-34,]),'FIELD':([0,1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,19,20,21,24,25,32,33,34,35,40,41,42,43,44,45,46,47,49,50,52,54,56,57,58,60,62,63,],[4,-8,-45,-11,-1,-10,-7,-9,4,-5,4,4,-3,-38,-37,-36,-40,4,-2,-6,4,-31,-30,-32,4,-45,-18,-21,-22,-23,-19,-20,-14,-12,-13,4,-4,-39,4,-33,4,-35,-15,-34,]),'STRING':([11,19,24,34,50,56,58,],[33,33,33,33,33,33,33,]),'ARROW':([1,3,4,6,7,8,10,21,25,32,33,40,41,42,43,44,45,46,47,49,57,60,62,63,],[-8,16,-11,-10,-7,-9,-5,-6,-31,-30,-32,-18,-21,-22,-23,-19,-20,-14,-12,-13,-33,-35,-15,-34,]),'INTEGER':([11,19,24,34,50,56,58,],[32,32,32,32,32,32,32,]),'[':([1,3,4,6,7,8,10,11,19,21,24,25,32,33,34,35,40,41,42,43,44,45,46,47,49,50,56,57,58,60,62,63,],[-8,17,-11,-10,-7,-9,-5,34,34,-6,34,-31,-30,-32,34,17,-18,-21,-22,-23,-19,-20,-14,-12,-13,34,34,-33,34,-35,-15,-34,]),':':([4,7,],[-11,19,]),']':([4,6,22,23,25,26,27,28,29,30,32,33,37,38,39,49,51,53,57,59,60,61,63,],[-11,-10,-24,-27,-31,-28,-29,-16,-25,-26,-30,-32,-43,-41,54,-13,60,-44,-33,-17,-35,-42,-34,]),'$end':([1,3,4,5,6,7,8,9,10,13,18,20,21,25,32,33,35,40,41,42,43,44,45,46,47,49,52,54,57,60,62,63,],[-8,-45,-11,-1,-10,-7,-9,0,-5,-3,-40,-2,-6,-31,-30,-32,-45,-18,-21,-22,-23,-19,-20,-14,-12,-13,-4,-39,-33,-35,-15,-34,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'direction':([3,],[12,]),'validation':([0,9,12,],[1,1,1,]),'name':([0,9,11,12,19,24,34,50,56,58,],[2,2,22,2,40,22,22,22,40,22,]),'tags':([3,35,],[13,52,]),'fieldspec':([0,9,12,],[3,3,35,]),'tuple':([11,19,24,34,50,56,58,],[23,41,23,23,23,41,23,]),'list':([11,19,24,34,50,56,58,],[26,42,26,26,26,42,26,]),'argument':([11,24,34,50,58,],[28,28,28,59,59,]),'rule':([0,9,],[5,20,]),'field':([0,9,11,12,19,24,34,50,56,58,],[7,7,29,7,44,29,29,29,44,29,]),'literal':([11,19,24,34,50,56,58,],[30,45,30,30,30,45,30,]),'tag':([17,55,],[38,61,]),'tag_list':([17,],[39,]),'function_call':([0,9,11,12,19,24,34,50,56,58,],[8,8,27,8,43,27,27,27,43,27,]),'validator_list':([19,],[47,]),'main':([0,],[9,]),'expression':([0,9,12,],[10,10,10,]),'validator':([19,56,],[46,62,]),'empty':([3,35,],[18,18,]),'argument_list':([11,24,34,],[31,48,51,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> main","S'",1,None,None,None),
  ('main -> rule','main',1,'p_main','/home/geertj/Projects/argproc/lib/argproc/parser.py',264),
  ('main -> main rule','main',2,'p_main','/home/geertj/Projects/argproc/lib/argproc/parser.py',265),
  ('rule -> fieldspec tags','rule',2,'p_rule','/home/geertj/Projects/argproc/lib/argproc/parser.py',273),
  ('rule -> fieldspec direction fieldspec tags','rule',4,'p_rule','/home/geertj/Projects/argproc/lib/argproc/parser.py',274),
  ('fieldspec -> expression','fieldspec',1,'p_fieldspec','/home/geertj/Projects/argproc/lib/argproc/parser.py',282),
  ('fieldspec -> expression *','fieldspec',2,'p_fieldspec','/home/geertj/Projects/argproc/lib/argproc/parser.py',283),
  ('expression -> field','expression',1,'p_expression','/home/geertj/Projects/argproc/lib/argproc/parser.py',288),
  ('expression -> validation','expression',1,'p_expression','/home/geertj/Projects/argproc/lib/argproc/parser.py',289),
  ('expression -> function_call','expression',1,'p_expression','/home/geertj/Projects/argproc/lib/argproc/parser.py',290),
  ('name -> NAME','name',1,'p_name','/home/geertj/Projects/argproc/lib/argproc/parser.py',295),
  ('field -> FIELD','field',1,'p_field','/home/geertj/Projects/argproc/lib/argproc/parser.py',299),
  ('validation -> field : validator_list','validation',3,'p_validation','/home/geertj/Projects/argproc/lib/argproc/parser.py',303),
  ('function_call -> name ( argument_list )','function_call',4,'p_function_call','/home/geertj/Projects/argproc/lib/argproc/parser.py',307),
  ('validator_list -> validator','validator_list',1,'p_validator_list','/home/geertj/Projects/argproc/lib/argproc/parser.py',311),
  ('validator_list -> validator_list , validator','validator_list',3,'p_validator_list','/home/geertj/Projects/argproc/lib/argproc/parser.py',312),
  ('argument_list -> argument','argument_list',1,'p_argument_list','/home/geertj/Projects/argproc/lib/argproc/parser.py',320),
  ('argument_list -> argument_list , argument','argument_list',3,'p_argument_list','/home/geertj/Projects/argproc/lib/argproc/parser.py',321),
  ('validator -> name','validator',1,'p_validator','/home/geertj/Projects/argproc/lib/argproc/parser.py',329),
  ('validator -> field','validator',1,'p_validator','/home/geertj/Projects/argproc/lib/argproc/parser.py',330),
  ('validator -> literal','validator',1,'p_validator','/home/geertj/Projects/argproc/lib/argproc/parser.py',331),
  ('validator -> tuple','validator',1,'p_validator','/home/geertj/Projects/argproc/lib/argproc/parser.py',332),
  ('validator -> list','validator',1,'p_validator','/home/geertj/Projects/argproc/lib/argproc/parser.py',333),
  ('validator -> function_call','validator',1,'p_validator','/home/geertj/Projects/argproc/lib/argproc/parser.py',334),
  ('argument -> name','argument',1,'p_argument','/home/geertj/Projects/argproc/lib/argproc/parser.py',339),
  ('argument -> field','argument',1,'p_argument','/home/geertj/Projects/argproc/lib/argproc/parser.py',340),
  ('argument -> literal','argument',1,'p_argument','/home/geertj/Projects/argproc/lib/argproc/parser.py',341),
  ('argument -> tuple','argument',1,'p_argument','/home/geertj/Projects/argproc/lib/argproc/parser.py',342),
  ('argument -> list','argument',1,'p_argument','/home/geertj/Projects/argproc/lib/argproc/parser.py',343),
  ('argument -> function_call','argument',1,'p_argument','/home/geertj/Projects/argproc/lib/argproc/parser.py',344),
  ('literal -> INTEGER','literal',1,'p_literal','/home/geertj/Projects/argproc/lib/argproc/parser.py',349),
  ('literal -> FLOAT','literal',1,'p_literal','/home/geertj/Projects/argproc/lib/argproc/parser.py',350),
  ('literal -> STRING','literal',1,'p_literal','/home/geertj/Projects/argproc/lib/argproc/parser.py',351),
  ('tuple -> ( argument_list )','tuple',3,'p_tuple','/home/geertj/Projects/argproc/lib/argproc/parser.py',356),
  ('tuple -> ( argument_list , )','tuple',4,'p_tuple','/home/geertj/Projects/argproc/lib/argproc/parser.py',357),
  ('list -> [ argument_list ]','list',3,'p_list','/home/geertj/Projects/argproc/lib/argproc/parser.py',363),
  ('direction -> ARROW','direction',1,'p_direction','/home/geertj/Projects/argproc/lib/argproc/parser.py',367),
  ('direction -> LARROW','direction',1,'p_direction','/home/geertj/Projects/argproc/lib/argproc/parser.py',368),
  ('direction -> RARROW','direction',1,'p_direction','/home/geertj/Projects/argproc/lib/argproc/parser.py',369),
  ('tags -> [ tag_list ]','tags',3,'p_tags','/home/geertj/Projects/argproc/lib/argproc/parser.py',374),
  ('tags -> empty','tags',1,'p_tags','/home/geertj/Projects/argproc/lib/argproc/parser.py',375),
  ('tag_list -> tag','tag_list',1,'p_tag_list','/home/geertj/Projects/argproc/lib/argproc/parser.py',381),
  ('tag_list -> tag_list , tag','tag_list',3,'p_tag_list','/home/geertj/Projects/argproc/lib/argproc/parser.py',382),
  ('tag -> NAME','tag',1,'p_tag','/home/geertj/Projects/argproc/lib/argproc/parser.py',389),
  ('tag -> ! NAME','tag',2,'p_tag','/home/geertj/Projects/argproc/lib/argproc/parser.py',390),
  ('empty -> <empty>','empty',0,'p_empty','/home/geertj/Projects/argproc/lib/argproc/parser.py',398),
]
