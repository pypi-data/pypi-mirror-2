from zope import interface, schema
from zope.formlib import form
from Products.Five.formlib import formbase
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from Products.CMFCore import utils as cmfutils
from Products.Five.browser import pagetemplatefile
#from Products.Five.browser import absoluteurl


from collective.plone.gsxml.context import TarballExportContext
from collective.plone.gsxml.content import XMLContentFSExporter


from jw.tustep import tustepMessageFactory as _

from zope.component import getMultiAdapter 
import urllib
import xml.dom.minidom as dom
import os
import shutil
import re
import webbrowser
import xmlrpclib 

class ITustepFormSchema(interface.Interface):
    # -*- extra stuff goes here -*-

    @interface.invariant
    def invariant_url(input):
        pass
	# Check input values example:
	# if input.name != 'value':
        #    raise interface.Invalid(_(u"Some error occurred !"))

class TustepForm(formbase.PageForm):
    form_fields = form.FormFields(ITustepFormSchema)
    label = _(u'TUSTEP Ausgabe')
    description = _(u'Es wird ein PDF-Dokument mithilfe von TUSTEP erzeugt.')
    result_template = pagetemplatefile.ZopeTwoPageTemplateFile('ergebnis.pt')
    #link = absoluteurl('http://germa61.uni-trier.de/tustep_pdf/buri.pdf')

    @form.action('pdf')
    def actionpdf(self, action, data):
        pass
        # Put the action handler code here 
        
       
        #-Jonas-Wagner------------------------------------------------------
        #Kontext-Prüfung
        #-------------------------------------------------------------------
        pfad = '/home/wagner/'          

        pstate = getMultiAdapter((self.context, self.request), name='plone_context_state')
        url = pstate.current_base_url()
        url = re.sub('/tustepform','',url)        
        urltest = open('/home/wagner/urltest', "w") 
        urltest.write(url) 
        urltest.close()

        #-Export-Test
        #-------------------------------------------------------------------
        export_context = TarballExportContext()
        exporter = XMLContentFSExporter(self.context)
        exporter.export(export_context, "structure", True)


        #archive = export_context.getArchiveStream()
        #archive.seek(0)

        
        
        file = export_context.getArchiveStream()  
        name = export_context.getArchiveFilename()  
        size = export_context.getArchiveSize()

        ausgabe = open(pfad + 'archiv', "w") 
        ausgabe.write(file.getvalue()) 
        ausgabe.close()
        
        shutil.rmtree(pfad + 'structure')
        os.system('tar xf ' + pfad + 'archiv --directory=' + pfad)
        
        #Ab hier Aufbereitung der Archiv-Daten
        #--------------------------------------------------------------
        eigenname = re.sub(".*/", "", url)
        string_text = ""
        
        
        xml_datei = open(pfad + 'structure/' + eigenname + r'.xml', "r")
        xml_text = ""
        for line in xml_datei: 
            xml_text += line
        
        baum = dom.parseString(xml_text)
        
        eintraege = ["shorttitle", "histdatum", "stddatum", "histort"]
        divs = baum.lastChild.getElementsByTagName("field")
        for di in divs:
            for eintrag in eintraege:
                if di.getAttribute("name") == eintrag:
                     
                    str_eintrag = "<" + eintrag + ">" + str(di.firstChild.data) + "</" + eintrag + ">" + '\n'
                    str_eintrag = re.sub("\n", "", str_eintrag)
                    str_eintrag = re.sub("\r|\t", "", str_eintrag)
                    str_eintrag = re.sub("\A\s*", "", str_eintrag)
                    str_eintrag = re.sub("\s*\Z", "", str_eintrag)
                    string_text += str(str_eintrag)
                    


        


        texttypen = ["untertitel", "fabstract", "description", "regest", "fundort", "druckort", "fachartikeltext", "originaltext", "text", "erlauterung", "uebetragung", "aboutauthors"]
        for i in texttypen:
            #Versuch des Oeffnens der Dateien 
            text_name =  eigenname + r"." + i + r".data"
            try:
                datei = open(pfad + 'structure/' + text_name, "r")
                
                org_text = ""
                for line in datei: 
                    #line = line.strip()
                    org_text += str(line)
                text = str(org_text)
                

                if re.search("\w", text):
                    text = re.sub("<!-- start content -->", "", text)
                    text = re.sub("\A\W*?<p>", "", text)
                    text = re.sub("</p>\W*?\Z", "", text)
                    text = re.sub("&nbsp;", " ", text)
                    text = re.sub("<script.*?", "", text)

                    loe = ["\n", "\r", "<a.*?>"]
                    for j in loe:
                        text = re.sub(i, "", text, re.DOTALL)
        
                    text = re.sub("&hellip;", "<...>", text)
                    text = re.sub("&mdash;", "-", text)
                    

                    string_text += '\n' + "<" + i + ">" + '\n'
                    
                    string_text += text
                    
                    string_text += '\n' + "</" + i + ">" + '\n'
                text.close()
            except:
                pass
            
        
        string_text = "<bttitel>" + str(pstate.object_title()) + "</bttitel>" + "\n" + string_text
         
        #Auslesen des Quelltextes
        #-------------------------------------------------------------------
        urllib.urlretrieve(url, '/home/wagner/Quelltext.xml')

        # Aufbereitung des Quelltextes in einen DOM-Baum
        #-------------------------------------------------------------------
        baum = dom.parse('/home/wagner/Quelltext.xml')
        divs = baum.lastChild.getElementsByTagName("div")

        # Hier werden die nicht benoetigten Divisionen getilgt
        #------------------------------------------------------------------- 
        rausschmiss = ["documentActions", "visualClear", "relatedItems", "customized"]
        for divpruef in divs:
            if divpruef.getAttribute("class") in rausschmiss:
                print 'LOESCHEN: '
                print divpruef
        
                divpruef.parentNode.removeChild(divpruef)
                #divpruef.unlink()

        # Hier wird die Content-Division in den Ausgabestring geladen
        #-------------------------------------------------------------------
        ausgabestring = "Wenn man dies sieht, ist etwas schief gegangen!"
        for divpruef in divs:
            if divpruef.getAttribute("id") == "content":
                #print len(divs)
                ausgabestring = divpruef.toxml(encoding = 'UTF-8')
                #print ausgabestring

        # Ausgabe in die Datei 'ymir.xml'   
        #-------------------------------------------------------------------    
        ausgabe = open('/home/wagner/ymir.xml', "w") 
        ausgabe.write(string_text)
        #ausgabe.write(ausgabestring) 
        ausgabe.close()
        
        # Aufruf von Tustep / PDF-Erzeugung und Übergabe
        #-------------------------------------------------------------------
        os.system('tcsh -c "tustep 1"')
        os.system('ps2pdf /home/wagner/buri.ps /home/wagner/buri.pdf')
        shutil.copy ('/home/wagner/buri.pdf', '/var/www/tustep_pdf/buri.pdf')
        #webbrowser.open_new("http://germa61.uni-trier.de/tustep_pdf/buri.pdf")
        
        pstate = getMultiAdapter((self.context, self.request), name='plone_context_state')
        obj = pstate.object_title()
        self.ergebnisse = obj
        return self.result_template()
 



    @form.action('einstellungen')
    def actioneinstellungen(self, action, data):
        # Put the action handler code here 
        pstate = getMultiAdapter((self.context, self.request), name='plone_context_state')
        url = pstate.current_base_url()
        url = re.sub('/tustepform','',url)
        obj = pstate.object_title()
        self.ergebnisse = obj
        return self.result_template()
        #return ("http://germa61.uni-trier.de/tustep_pdf/buri.pdf")




