-*- encoding: utf-8 -*-

Copyright 2009-2011 Institute for the Study of the Ancient World, New York
University

Introduction
============

This package provides modules for transliteration of names from Greek and Latin
writing systems into our modern Roman writing system following conventions of
the Classical Atlas Project.

Validators return list of invalid characters for the writing system, otherwise empty list

Transliterators return a UTF-8 string generated according to the transliteration rules
for that writing system. Characters that don't match the rules are replaced with a 
question mark(?). 

Requests to validate or transliterate unsupported writing systems will raise as 
ValueError: Unsupported writing system

Examples:

  >>> from pleiades.transliteration import transliterate_name
  >>> from pleiades.transliteration.ws_grek import validate as grek_v
  >>> from pleiades.transliteration.ws_latn import validate as latn_v
  >>> from pleiades.transliteration.ws_en import validate as en_v
  >>> from pleiades.transliteration.ws_tr import validate as tr_v
  >>> from pleiades.transliteration.ws_copt import validate as copt_v
    
Roma in Latin 
    
  >>> name = 'Roma'.decode('utf-8')
  >>> latn_v(name, 'all')
  []
  >>> transliterate_name('la', 'Roma')
  'Roma'
    
Strophades in Greek with Latin transliteration
    
  >>> transliterate_name('grc-latn', 'Strophades')
  'Strophades'
    
Aphrodisias in Greek
    
  >>> name = 'Ἀφροδισιάς'.decode('utf-8')
  >>> grek_v(name, 'all')
  []
  >>> transliterate_name('grc', name)
  'Aphrodisias'
  
all characters in English

  >>> name = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'.decode('utf-8')
  >>> en_v(name, 'all')
  []
  >>> transliterate_name('en', name)
  'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
  
all characters in Turkish
  >>> name = 'Yedi Taşlar'.decode('utf-8')
  >>> tr_v(name, 'all')
  []
  >>> transliterate_name('tr', name)
  'Yedi Taslar'
  
all characters in Coptic
  >>> name = u'\u03E2\u03E3\u03E4\u03E5\u03E6\u03E7\u03E8\u03E9\u03EA\u03EB\u03EC\u03ED\u03EE\u03EF\u2C80\u2C82\u2C84\u2C86\u2C88\u2C8C\u2C8E\u2C90\u2C92\u2C94\u2C96\u2C98\u2C9A\u2C9C\u2C9E\u2CA0\u2CA2\u2CA4\u2CA6\u2CAA\u2CAC\u2CAE\u2CB0\u03E2\u03E3\u03E4\u03E5\u03E6\u03E7\u03E8\u03E9\u03EA\u03EB\u03EC\u03ED\u03EE\u03EF\u2C81\u2C83\u2C85\u2C87\u2C89\u2C8D\u2C8F\u2C91\u2C93\u2C95\u2C97\u2C99\u2C9B\u2C9D\u2C9F\u2CA1\u2CA3\u2CA5\u2CA7\u2CAB\u2CAD\u2CAF\u2CB1\u2CEF\u2CF0\u2CF1'
  >>> transliterate_name('cop', name)
  'SHshFfKHkhHhJjQqTItiABGDEZETHIKLMNXOPRSTPHCHPSOSHshFfKHkhHhJjQqTItiabgdezethiklmnxoprstphchpso'

  >>> name = 'ⲙⲛⲧⲣⲙⲛⲕⲏⲙⲉ'.decode('utf-8')
  >>> copt_v(name, 'all')
  []
  >>> transliterate_name('cop', name)
  'mntrmnkeme'

Zeugma in Greek

  >>> name = 'Ζεῦγμα'.decode('utf-8')
  >>> grek_v(name, 'all')
  []
  >>> transliterate_name('grc', name)
  'Zeugma'
  
Zeugma in Latin

  >>> name = u'Zeugma'
  >>> transliterate_name('la', name)
  'Zeugma'

Invalid script

  >>> transliterate_name('tlh', 'kitten') # doctest: +ELLIPSIS
  Traceback (most recent call last):
  ...
  ValueError: Unsupported writing system (tlh)
    
Editorial characters that should be permitted

  >>> transliterate_name('la', '(...)sinsensium')
  '(...)sinsensium'

Out-of-range characters that shouldn't be there if the validator was used 
first. Aphrodisias in Greek but mis-languaged as latin
    
  >>> name = u'\u1f08\u03c6\u03c1\u03bf\u03b4\u03b9\u03c3\u03b9\u1f71\u03c2'
  >>> transliterate_name('la', name.encode('utf-8'))
  '??????????'
    
