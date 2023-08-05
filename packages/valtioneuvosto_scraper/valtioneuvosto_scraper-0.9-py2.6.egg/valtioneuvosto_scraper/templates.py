
tmpl_main = """

<?xml version="1.0" encoding="UTF-8"?>
<hallitukset xmlns="http://valtioneuvosto.fi/namespaces/2010/07">
   %s
</hallitukset>

"""


tmpl_government = """

   <hallitus tunniste="%i" tyyppi="%s" kesto="%i">%s
      <aloitus>%s</aloitus>
      <lopetus>%s</lopetus>
      %s
   </hallitus>
"""


tmpl_position = """      <salkku>%s
         %s
      </salkku>"""


tmpl_minister = """

         <ministeri puolue="%s">%s
            <nimitetty>%s</nimitetty>
            <eronnut>%s</eronnut>
         </ministeri>

"""
