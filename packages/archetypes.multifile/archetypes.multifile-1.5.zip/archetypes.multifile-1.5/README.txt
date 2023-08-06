Introduction
============
archetypes.multifile is a Plone Archetype Field which allows to upload multiple files.

Usage
=====
1. Install package by adding the egg into your buildout cfg::
    
    [instance]
    ...
    eggs =
    	archetypes.multifile
    zcml = 
        archetypes.multifile
        
2. Rerun buildout and start the instance

3. Install via quickinstaller

4. Use it in your custom Archetypes content type::
 
    from archetypes.multifile.MultiFileField import MultiFileField
    from archetypes.multifile.MultiFileWidget import MultiFileWidget

    MultiFileField('file',
               primary=True,
               languageIndependent=True,
               storage = AnnotationStorage(migrate=True),
               widget = MultiFileWidget(
                         description = "Select the file to be added by clicking the 'Browse' button.",
                         label= "File Some Text",
                         show_content_type = False,)),


TODO
====
Add tests

KNOWN BUGS
==========
* Passes required validation even if no file is attached

Credits
=======
This package was built upon a MultiFile product by

Partecs Participatory Technologies
http://www.partecs.com

Eggified by
Matous Hora
http://dms4u.cz

Indexation feature by
Quadra Informatique - Jonathan Riboux
http://www.quadra-informatique.fr

