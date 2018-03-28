from bs4 import BeautifulSoup
import bs4
from lxml import html


'''
from ExtractDocInfo import MethodInfo
from ExtractDocInfo import  ConstructorInfo
from ExtractDocInfo import FieldInfo
from ExtractDocInfo import  InheritedMethodInfo
from ExtractDocInfo import  InheritedFieldInfo
from ExtractDocInfo import NEPackage
from ExtractDocInfo import NEClass
from ExtractDocInfo import NEEnum
from ExtractDocInfo import NEError
from ExtractDocInfo import NEExcp
from ExtractDocInfo import NEInterface
from ExtractDocInfo import NEParser
'''

from MethodInfo import MethodDetails
from ConstructorInfo import ContDetails
from FieldInfo import FieldDetails
from InheritedMethodInfo import InheritedMethodDetails
from InheritedFieldInfo import  InheritedFieldDetails
from NEPackage import NEntPkg
from NEClass import NEntClass
from NEEnum import NEntEnum
from NEError import NEntError
from NEExcp import NEntException
from NEInterface import NEntInterface
from NEParser import NEntParent


import re
import nltk
from nltk.tokenize import  word_tokenize as wt


class ClassInterfaceInfo:
    INTERFACECHECK="All Implemented Interfaces:"

    SUBCLASSCHECK = "Direct Known Subclasses:"
    SUBINTERFACECHECK="All Known Subinterfaces:"

    IMPLCLASSESCHECK="All Known Implementing Classes:"

    SUPINTERFACECHECK = "All Superinterfaces:"

    REFERENCEINFOCHECK=['Since:','See Also:']


    CHCKFIELDSUMMARY="field.summary"
    CHCKFIELDinheritedSUMMARY = "fields.inherited"

    CHCKMETHODSUMMARY = "method.summary"
    CHCKMETHODinheritedSUMMARY="methods.inherited"
    CHCKCONSTRUCTORUSUMMARY = "constructor.summary"
    basicReturnTypes=['byte','short','int','long','float','double','boolean','char','void']
    numtowordPos={'1':'First ','2' :'Second', '3':'Third' ,'4':'Fourth','5':'Fifth','6':'Sixth','7':'Seventh'}
    entityDict = {}
    descreplacer={'VBN'}

    def __init__(self,phtml,factfolder):
        self.factfolder=factfolder
        self.html=phtml
        self.soup = BeautifulSoup(self.html)
        self.ImplementedClasses={}
        self.ImplementedInterFaces = {}
        self.AllKnownSubInterfaces = {}
        self.AllKnownSuperInterfaces = {}
        self.AllKnownImplClasses = {}
        self.MethodDict={}
        self.InheritedMethodDict = {}
        self.ConstructorDict={}
        self.FieldDict = {}
        self.InheritedFieldDict = {}
        self.DirectSubclasses={}
        self.MainDescription={}
        self.InheritedInfo={}
        self.since=''
        self.ExtraInfo={}
        self.blocktypeDict = {
            'basicinfo.txt': ['BASICINFO_BLOCK', []],
            'inheritance.txt': ['INHERITANCE_BLOCK', []],
            #'implementedInterfacesinfo.txt': ['INHERITANCE_BLOCK', []],
            'descinfo.txt': ['MAINDESC_BLOCK', []],
            'MethodinfoSum.txt': ['METHOD_BLOCK_SUMMARY', []],
            'MethodinfoDetailed.txt': ['METHOD_BLOCK_DETAIL', []],
            'constinfoDetailed.txt': ['CONSTRUCTOR_BLOCK_DETAIL', []],
            'constinfoSum.txt': ['CONSTRUCTOR_BLOCK_SUMMARY', []],
            'FieldinfoSum.txt': ['FIELD_BLOCK_SUMMARY', []],
            'FieldinfoDetailed.txt': ['FIELD_BLOCK_DETAIL', []]
        }

        self.ExtractInfo()
        self.WriteData()
        self.WriteToFile()
        print("Extracted Information for "+ self.fullsresolvedname)

    def ExtractInfo(self):
        self.ExtractHeader()
        self.ExtractSubClassesandInfoDetails()
        self.ExtractSummary()
        self.ExtractDetails()
        self.ExtractMainDesc()
        self.ExtractInheritanceInfo()
        #print("CompletedImplementationTillHere")
        #print("DEBUG")

    def ExtractHeader(self):
        infoLine=self.soup.find("div", {"class": "header"}).find("h2", {"class": "title"}).text
        self.currenTypeName=infoLine.split(' ')[1]
        self.currenType =infoLine.split(' ')[0]
        try:
            self.packagename=self.soup.find("div", {"class": "header"}).find_all("div", {"class": "subTitle"})[1].text
        except:
            self.packagename=self.soup.find("div", {"class": "header"}).find_all("div", {"class": "subTitle"})[0].text

        self.packagename=self.packagename.replace('.','_')
        #self.fullsresolvedname = self.packagename + '.' + self.currenTypeName
        self.fullsresolvedname = self.packagename + '_' + self.currenTypeName
        self.fullsresolvedname=self.fullsresolvedname.replace('.', '_')
        self.writeFileName = self.fullsresolvedname.replace('.', '_')

        #AddCode to Extract Entities
        if(self.packagename not in ClassInterfaceInfo.entityDict):
            #ClassInterfaceInfo.entityDict[self.packagename]=NEParser.NEntParent(self.packagename,None,'Package')
            ClassInterfaceInfo.entityDict[self.packagename] = NEntParent(self.packagename, None, 'Package')

        if (self.fullsresolvedname not in ClassInterfaceInfo.entityDict):
                #ClassInterfaceInfo.entityDict[self.fullsresolvedname] = NEParser.NEntParent(self.fullsresolvedname,self.packagename,self.currenType)
                ClassInterfaceInfo.entityDict[self.fullsresolvedname] = NEntParent(self.fullsresolvedname,self.packagename, self.currenType)

    def ExtractInheritanceInfo(self):
        inheritanceList=self.soup.find_all("ul", {"class": "inheritance"})
        cnt=0
        for p in inheritanceList:
            self.InheritedInfo[cnt]=p.find('li').text
            cnt+=1

    def ExtractMainDesc(self):
        #print("\nMain Description")
        descRow=self.soup.find("div", {"class": "description"})
        self.deprecationInfo=''
        txttoreplace1=''
        txttoreplace2 = ''

        if(descRow.find('span',{'class':'deprecatedLabel'}) is not None):
            txttoreplace1=descRow.find('span',{'class':'deprecatedLabel'}).text
            self.deprecationInfo=self.fullsresolvedname +' is deprecated.'
            if(descRow.find('span',{'class':'deprecationComment'}) is not  None):
                txttoreplace2=descRow.find('span',{'class':'deprecationComment'}).text
                self.deprecationInfo =self.deprecationInfo +' '+ descRow.find('span',{'class':'deprecationComment'}).text +'. '

        descData=''
        if( self.soup.find("div", {"class": "description"}).find_all('div',{"class":"block"}) is not None):
            for ds in self.soup.find("div", {"class": "description"}).find_all('div',{"class":"block"}):
                descData =  descData+ds.text
        else:
            descData=''


        descData=descData.replace(txttoreplace1,'')
        descData=descData.replace(txttoreplace2, '')
        descData=descData.replace('\n', '')

        descCodesnippet = []
        if(descRow.find_all('code') is not None):
            for codetext in descRow.find_all('code'):
                codesnippet = codetext.text.replace('\n', '').strip()
                if((';' in codesnippet.replace('&nbsp;','')) or '...' in codesnippet):
                    descCodesnippet.append(' An example of how to use the '+self.fullsresolvedname+  ' is <CODESNIPPET>'+codesnippet.replace('\n','').replace('  ','')+'</CODESNIPPET>')

        if(len(descCodesnippet)>0):
            for cs in descCodesnippet:
                descData=descData+codesnippet +'. '


        declarationSyntax=self.soup.find("div", {"class": "description"}).find('pre').text.replace('\n',' ')

        if('Implementation Requirements:' in descData):
            print("DEBUG")

        self.MainDescription['desc']=descData +' '+self.deprecationInfo
        self.MainDescription['syntax'] = declarationSyntax

    def ExtractSubClassesandInfoDetails(self):
        descriptionList=self.soup.find("div", {"class": "description"}).find_all("dl")
        for dl in descriptionList:
            dtList=dl.find_all("dt")
            ddList = dl.find_all("dd")
            dtcount=0
            for dt in dtList:
                if(dt.contents[0] in [ClassInterfaceInfo.IMPLCLASSESCHECK,ClassInterfaceInfo.INTERFACECHECK,ClassInterfaceInfo.SUBCLASSCHECK,ClassInterfaceInfo.SUBINTERFACECHECK,ClassInterfaceInfo.SUPINTERFACECHECK]):
                    #print(dt.contents[0])
                    #print(ddList[dtcount].text)
                    lastcontent=""
                    for data in ddList[dtcount].contents:
                        if type(data)==bs4.element.Tag:
                            if(dt.contents[0]==ClassInterfaceInfo.INTERFACECHECK):
                                packageInfo=data.attrs['title'].replace("interface in","").strip()
                                self.ImplementedInterFaces[packageInfo+"."+data.text]=[data.text ,  packageInfo ]
                                lastcontent=packageInfo+"."+data.text
                            elif (dt.contents[0] == ClassInterfaceInfo.SUBCLASSCHECK):
                                packageInfo = data.attrs['title'].replace("class in", "").strip()
                                self.DirectSubclasses[packageInfo+"."+ data.text] = [data.text ,  packageInfo ]
                                lastcontent = packageInfo + "." + data.text
                            elif (dt.contents[0] == ClassInterfaceInfo.SUBINTERFACECHECK):
                                packageInfo = data.attrs['title'].replace("interface in", "").strip()
                                self.AllKnownSubInterfaces[packageInfo + "." + data.text] = [data.text,  packageInfo ]
                                lastcontent = packageInfo + "." + data.text
                            elif (dt.contents[0] == ClassInterfaceInfo.IMPLCLASSESCHECK):
                                packageInfo = data.attrs['title'].replace("class in", "").strip()
                                self.ImplementedClasses[packageInfo + "." + data.text] = [data.text,  packageInfo ]
                                lastcontent = packageInfo + "." + data.text
                            elif (dt.contents[0] == ClassInterfaceInfo.SUPINTERFACECHECK):
                                packageInfo = data.attrs['title'].replace("interface in", "").strip()
                                self.AllKnownSuperInterfaces[packageInfo + "." + data.text] = [data.text, packageInfo]
                                lastcontent = packageInfo + "." + data.text

                            else:
                                #print(dt.contents[0])
                                pass
                        else:
                            if('<E>' in data):
                                if (dt.contents[0] == ClassInterfaceInfo.INTERFACECHECK):
                                    self.ImplementedInterFaces[lastcontent][0]=self.ImplementedInterFaces[lastcontent][0]+'<E>'
                                elif(dt.contents[0] == ClassInterfaceInfo.SUBCLASSCHECK):
                                    self.DirectSubclasses[lastcontent][0] = self.DirectSubclasses[lastcontent][0] + '<E>'
                                elif (dt.contents[0] == ClassInterfaceInfo.SUBINTERFACECHECK):
                                    self.AllKnownSubInterfaces[lastcontent][0] = self.AllKnownSubInterfaces[lastcontent][
                                                                                0] + '<E>'
                                else:
                                    pass
                elif(dt.find('span') is not None and dt.find('span').contents[0] in ClassInterfaceInfo.REFERENCEINFOCHECK):
                    if(dt.find('span').contents[0]=='Since:'):
                        for data in ddList[dtcount]:
                            sentence=' The '+ self.currenType +' '+ self.fullsresolvedname + ' is present since Java '+data.replace('.','_') +'.'
                            #print(sentence)
                            if(self.fullsresolvedname in self.ExtraInfo):
                                self.ExtraInfo[self.fullsresolvedname].append(sentence)
                            else:
                                self.ExtraInfo[self.fullsresolvedname]=[sentence]
                    elif (dt.find('span').contents[0] == 'See Also:'):
                        relList=[]
                        for data in ddList[dtcount].find_all('a'):
                            relList.append('See '+data.attrs['href'].replace('../','').replace('.html','').replace('/','_').split('#')[0] +' as reference to ' +self.fullsresolvedname +'. ')
                        #sentence= ' See also '+ ', '.join(relList)+' for functionality related to  '+ self.currenType +' '+ self.fullsresolvedname  +'.'


                        if (self.fullsresolvedname in self.ExtraInfo):
                          self.ExtraInfo[self.fullsresolvedname]=self.ExtraInfo[self.fullsresolvedname] + relList
                        else:
                            self.ExtraInfo[self.fullsresolvedname] = relList
                        #print(sentence)


                    else:
                        pass
                else:
                    pass

                dtcount+=1
                #print()

    def ExtractSummary(self):
        if(self.soup.find("div", {"class": "summary"}) is None):
            pass
        else:
            summaryList = self.soup.find("div", {"class": "summary"}).find_all("ul")
            debugcount=0
            for ul in summaryList:
                    summaryField=ul.find('a').attrs['name']
                    #print(summaryField)
                    if(summaryField=="method.summary"):
                        self.ExtractInfoFromMethodSummary(ul)
                    elif ("methods.inherited.from" in summaryField):
                        inheritedfrom=summaryField.replace('methods.inherited.from.','')
                        self.ExtractInfoFromInheritedMethodSummary(ul,inheritedfrom)
                    elif ("fields.inherited.from" in summaryField):
                        inheritedfrom = summaryField.replace('fields.inherited.from.', '')
                        self.ExtractInfoFromInheritedFieldSummary(ul, inheritedfrom)
                    elif(summaryField=="constructor.summary"):
                        #print(str(debugcount))
                        self.ExtractInfoFromConstructorSummary(ul)
                    elif (summaryField == "field.summary"):
                        if(not('FIELD SUMMARY' in ul.contents[1].contents[1])):
                            self.ExtractInfoFromFieldSummary(ul)
                        else:
                            pass
                    else:
                         pass
                    debugcount+=1

    def ExtractDetails(self):
        #print("\nDetails")
        if(self.soup.find("div", {"class": "details"}) is None):
            pass
        else:
            detailList = self.soup.find("div", {"class": "details"}).find_next("ul").find_next("li").find_all('li')
            for li in detailList:
                if(li.find('a') is not None and 'name' in li.find('a').attrs):
                    detailmode=li.find('a').attrs['name']
                    if(detailmode=='field.detail'):
                        self.ExtractInfoFromFieldDetails(li)
                    elif(detailmode=='constructor.detail'):
                        self.ExtractInfoFromConstructorDetails(li)
                    elif (detailmode == 'method.detail'):
                        self.ExtractInfoFromMethodDetails(li)
                        pass
                    else:
                        pass

    def ExtractInfoFromFieldDetails(self,li):
        for ul in li.find_all('ul'):
            if(ul.find('li').find('h4') is not None):
                fieldname=ul.find('li').find('h4').text
                try:
                    if (fieldname == 'Debug'):
                        print('DEBUG')
                    self.FieldDict[fieldname].AddInfoFromDetails(ul.find('li'))
                except:
                    print(
                        "Exception Occured while trting to get detailed description for the field " + fieldname + " with infotag" + str(
                            ul))
            else:
                print("Some unhandled Condition for " +self.fullsresolvedname+" Plese fix Later")

    def ExtractInfoFromMethodDetails(self,li):
        #for ul in li.find_all('ul'):
        currmethodname = ''
        cnt=0
        for item in li.find_all():
            if(item.name=='ul' and len(item.attrs)>0):
                #print(cnt)
                ul=item
                #methodname=ul.find('li').find('h4').text
                try:
                    if(currmethodname=='debug'):
                        print("DEBUG")
                    self.MethodDict[currmethodname].AddInfoFromDetails(ul.find('li'))
                except:
                    print("Exception Occured while starting to get detailed description for the method "+currmethodname+"with infotag" +str(ul))
            elif (item.name=='a'):
                if('name' in item.attrs):
                    #print(cnt)
                    currmethodname=item.attrs['name']
                else:
                    pass
            else:
                pass
            cnt+=1

    def ExtractInfoFromConstructorDetails(self,li):
        #for ul in li.find_all('ul'):
        currconstname = ''
        cnt=0
        for item in li.find_all():
            if(item.name=='ul' and len(item.attrs)>0):
                #print(cnt)
                ul=item
                #methodname=ul.find('li').find('h4').text
                try:
                    self.ConstructorDict[currconstname].AddInfoFromDetails(ul.find('li'))
                except:
                    print("Exception Occured while starting to get detailed description for  the constructr "+currconstname+" with infotag" +str(ul))
            elif (item.name=='a'):
                if('name' in item.attrs):
                    #print(cnt)
                    currconstname=item.attrs['name']
                else:
                    pass
            else:
                pass
            cnt+=1

    def ExtractInfoFromMethodSummary(self,ul):
        for tr in ul.find_all('tr'):
            if (len(tr.find_all('td')) > 0):
                methodrow = tr.find_all('td')
                #minfo = MethodInfo.MethodDetails(methodrow, 'summary', self.packagename + '.' + self.currenTypeName)
                minfo = MethodDetails(methodrow, 'summary', self.packagename + '.' + self.currenTypeName)

                self.MethodDict[minfo.methodNameKey] = minfo

                '''
                # Extract Return TypeInfo of the method
                if ((len(methodrow[0].text.split(' ')) > 1) and (methodrow[0].text.split(' ')[0] in {'protected','private','public'})):
                    accesmodifier = methodrow[0].text.split(' ')[0]
                    rtype = methodrow[0].text.split(' ')[1]
                else:
                    accesmodifier = 'public'
                    rtype = methodrow[0].text

                if (rtype in ClassInterfaceInfo.basicReturnTypes):
                    retType = [rtype, 'basic', accesmodifier]
                elif(accesmodifier=='public'):
                    retType = [rtype, 'complex', accesmodifier]
                else:
                    rettypeeadvanced = methodrow[0].find('a').attrs['title']
                    retType = [rtype, rettypeeadvanced, accesmodifier]

                #EXTRACT PARAMATER INFO FROM METHOD SUMMARY

                methodcodekey=methodrow[1].find('code').text.replace('\n', '').strip()
                methodsumDescription=methodrow[1].find('div',{'class':'block'}).text.replace('\n', '').strip()
                methodimputparams = {}

                methodinfo = methodrow[1].text.split('\n')
                if (methodcodekey not in self.MethodDict):
                    self.MethodDict[methodcodekey] = {}
                    self.MethodDict[methodcodekey]['summarydesc'] =  methodsumDescription
                    self.MethodDict[methodcodekey]['retType'] = [retType]
                else:
                    self.MethodDict[methodcodekey]['summarydesc'] =  methodsumDescription
                    self.MethodDict[methodcodekey]['retType'] = [retType]
                #print("The method "+ methodcodekey +" in "+ self.packagename + "." + self.currenTypeName+ " "+str(self.MethodDict[methodcodekey]['summarydesc']))
                #print(tr.text)
                #print()
                '''
            else:
                pass
        #print("Extracted Information From Method Summary ")

    def ExtractInfoFromInheritedMethodSummary(self,ul,inhfrm):
        for m in ul.find('code').find_all('a'):
            #inmethodinfo=InheritedMethodInfo.InheritedMethodDetails(m,'summary',self.packagename + '.' + self.currenTypeName,inhfrm)
            inmethodinfo = InheritedMethodDetails(m, 'summary',
                                                                      self.packagename + '.' + self.currenTypeName,
                                                                      inhfrm)

            self.InheritedMethodDict[inmethodinfo.methodref] = inmethodinfo
        #print("Extracted Information From Inherited Method Summary")

    def ExtractInfoFromInheritedFieldSummary(self,ul,inhfrm):
        for f in ul.find('code').find_all('a'):
            #inFieldinfo=InheritedFieldInfo.InheritedFieldDetails(f,'summary',self.packagename + '.' + self.currenTypeName,inhfrm)
            inFieldinfo = InheritedFieldDetails(f, 'summary',
                                                                   self.packagename + '.' + self.currenTypeName, inhfrm)

            self.InheritedFieldDict[inFieldinfo.fieldref] = inFieldinfo
        #print("Extracted Information From Inherited Method Summary")

    def ExtractInfoFromConstructorSummary(self,ul):
        for table  in ul.find_all('table'):
            if('Constructor' in table.attrs['summary']):
                for tr in table.find_all('tr'):
                    if (len(tr.find_all('td')) > 0):
                        constrow = tr.find_all('td')
                        #constinfo = ConstructorInfo.ContDetails(constrow, 'summary', self.packagename + '.' + self.currenTypeName)
                        constinfo = ContDetails(constrow, 'summary',
                                                                self.packagename + '.' + self.currenTypeName)

                        self.ConstructorDict[constinfo.constNameKey]= constinfo

                    else:
                        pass
                #print("Extracted Information From Constructor Summary ")

    def ExtractInfoFromFieldSummary(self,ul):
        for tr in ul.find_all('tr'):
            if (len(tr.find_all('td')) > 0):
                fieldrow = tr.find_all('td')
                #fieldinfo = FieldInfo.FieldDetails(fieldrow, 'summary', self.packagename + '.' + self.currenTypeName)
                fieldinfo = FieldDetails(fieldrow, 'summary', self.packagename + '.' + self.currenTypeName)

                self.FieldDict[fieldinfo.fieldname]=fieldinfo

            else:
                pass
        #print("Extracted Information From Field Summary ")

    def WriteData(self):

        self.WriteMostBasicInfo()
        self.WriteInheritanceInfo()
        self.WriteSubClasses()
        self.WriteSubInterfaces()
        self.WriteImpClasses()
        self.WriteSupInterfaces()
        self.WriteImplementedInterfaces()
        self.WriteDescInfo()
        self.WriteMethodInfo()
        self.WriteConstInfo()
        self.WriteFieldInfo()
        self.WriteInhMethodInfo()
        self.WriteInhFieldInfo()


        #print("################################################################################################################################################")

    def WriteMostBasicInfo(self):
        data=self.fullsresolvedname +" is "+ self.currenType+" in " + self.packagename+'.\r\n'
        data=''
        self.WritetoBlockDict(data,self.writeFileName+'_basicinfo.txt')
        #print("_____________________________________________________________________")

    def WriteInheritanceInfo(self):
        inheritancedata=''
        treelength=len(self.InheritedInfo)

        for i in range(0,len(self.InheritedInfo)-1):
            #inheritancedata=inheritancedata+ '\n'+self.InheritedInfo[treelength-1-i] +' extends ' + self.InheritedInfo[treelength-2-i]
            #TUNING DATABASE removed the package name from Entity Information
            inheritancedata=inheritancedata+ ''+'_'.join(self.InheritedInfo[treelength-1-i].split('.')) +' extends ' +'_'.join( self.InheritedInfo[treelength-2-i].split('.')) +'. '
            i+=1
        self.WritetoBlockDict(inheritancedata, self.writeFileName + '_inheritance.txt')
        #print(inheritancedata)

    def WriteImplementedInterfaces(self):
        IList=[]
        data=''
        if(len(self.ImplementedInterFaces)>0):
            data = 'The interfaces implemented by ' + self.fullsresolvedname + ' are '+ data + ', '.join(self.ImplementedInterFaces).replace('\n', '').replace('.', '_') + '.'
            self.WritetoBlockDict(data, self.writeFileName + '_inheritance.txt')
        elif(len(self.ImplementedInterFaces)==0):
            data = 'The interfaces implemented by ' + self.fullsresolvedname + ' are zero. '
            self.WritetoBlockDict(data, self.writeFileName + '_inheritance.txt')
        else:
            pass


        '''
        for sc in self.ImplementedInterFaces:
            #print(self.currenType + " " + self.currenTypeName + " extends the interface " + self.ImplementedInterFaces[sc][0] + " in " +self.ImplementedInterFaces[sc][1])
            #data=self.currenType + " " + self.currenTypeName + " implements the interface " + self.ImplementedInterFaces[sc][1]+"."+self.ImplementedInterFaces[sc][0]
            data = self.currenTypeName + " implements the interface " + \
                   self.ImplementedInterFaces[sc][1] + "." + self.ImplementedInterFaces[sc][0]

            self.WritetoBlockDict(data, self.writeFileName + '_inheritance.txt')
            IList.append(self.ImplementedInterFaces[sc][1]+"."+self.ImplementedInterFaces[sc][0])
            #print("_____________________________________________________________________")

        if(data!=''):
            #print(data)
            data= 'The interfaces implemented by ' +self.fullsresolvedname +' are '
            data=data+ ','.join(IList).replace('\n','').replace('.','_') +'.'
            #for i in IList:
            #    data=data +' ' +str(i) +','
            #data=data+'</p>'
            #print(data)
            self.WritetoBlockDict(data, self.writeFileName + '_inheritance.txt')
        '''

    def WriteConstInfo(self):

        constdatamain = self.fullsresolvedname + ' contains ' + str(len(self.ConstructorDict)) + ' constructors'
        #constdatamain = 'The number of constructors in ' + self.fullsresolvedname + ' is ' + str(len(self.ConstructorDict)) +'.\r\n'
        constdatamain = 'The number of constructors in '+self.fullsresolvedname+' are ' + str(len(self.ConstructorDict)) + '.\r\n'

        self.WritetoBlockDict(constdatamain, self.writeFileName + '_basicinfo.txt')

        cnt = 0
        for const in self.ConstructorDict:
            constobj = self.ConstructorDict[const]
            constDatasum = ''
            constdatadetailed = ''
            constname = constobj.codefromsummary.replace(' ', '')

            # SummaryInfo
            #constDatasum = constDatasum + '\n' + constname + ' is a constructor of ' + self.currenType + ' ' + constobj.curtypename
            # CHANGE is sentence (MAJRO CHANGES)
            #constDatasum = constDatasum + '' + constname + ' is a constructor. '

            # constDatasum = constDatasum + '\n' + constname + ' in ' + constobj.curtypename + ' contains ' + str(constobj.noofparams) +' parameters '
            if (constobj.summarydesc is not None):
                #constDatasum = constDatasum + '\n' + constname + ' in ' + constobj.curtypename + ' ' + constobj.summarydesc
                constDatasum = constDatasum + ' The constructor ' + constname + ' ' + constobj.summarydesc

            constDatasum = constDatasum + ' The constructor ' + constname + ' takes in ' + str(
                len(constobj.parameterinfo)) + ' parameters. '
            prminfo = constobj.parameterinfo
            for prm in prminfo:
                # constDatasum = constDatasum + '\n' + prm +' is the ' + ClassInterfaceInfo.numtowordPos[str(prminfo[prm].position)]+' paramater in the const '+ constname + ' of ' +self.currenType +' ' + constobj.curtypename
                constDatasum = constDatasum + '' + prm + ' is the paramater ' + str(prminfo[
                                                                                               prm].position) + ' in the constructor ' + constname +'. '#' of ' + self.currenType + ' ' + constobj.curtypename
                constDatasum = constDatasum + '' + 'The type of ' + prm + ' is ' + prminfo[prm].parameterType+'. '
                if (not (prminfo[prm].description.strip() == '')):
                    constDatasum = constDatasum + '' + 'Paramater ' + prm + ' in the constructor ' + constname + ' is' + \
                                   prminfo[prm].description+'. '

            # DetailedInfo
            if(constobj.detailedesc==True):
                if(constobj.detaileddecrption is not ''):
                    constdatadetailed = constdatadetailed + 'The constructor ' + constname + ' in '+ self.fullsresolvedname +' ' + constobj.detaileddecrption.replace('\n',' ').replace('  ',' ').replace('Deprecated','has been deprecated')
                if (constobj.Overides != ''):
                    constdatadetailed = constdatadetailed + ' The constructor ' + constname + ' overides the constructor ' + constobj.Overides.replace(
                        '\n', ' ').replace('  ',' ')+'.'

                if (constobj.Throws != ''):
                    constdatadetailed = constdatadetailed + ' The constructor ' + constname  + ' throws the exception ' + constobj.Throws.replace(
                        '\n', ' ').replace('  ',' ')+'.'

                if (constobj.Returns != ''):
                    constdatadetailed = constdatadetailed + ' The constructor ' + constname + ' returns ' + constobj.Returns.replace(
                        '\n', ' ').replace('  ',' ')+'.'


                if (constobj.ImpReq!=''):
                    methoddatadetailed = constdatadetailed + ' The implementation requirements of constructor ' + constname + ' in '+ self.fullsresolvedname+' are <IMPSNIPPET>' + constobj.ImpReq.replace(
                        '\n', '  ').replace('  ', ' ') + '</IMPSNIPPET>.'

                if (constobj.Since!=''):
                    methoddatadetailed = constdatadetailed + ' The constructor ' + constname +  ' in '+ self.fullsresolvedname +' is present since Java ' + constobj.Since.replace(
                        '\n', '  ').replace('  ', ' ').replace('.', '_') + '.'

                if (constobj.SeeAlso!=''):
                    constdatadetailed = constdatadetailed + ' See ' + constobj.SeeAlso.replace(
                        '\n', '  ').replace('  ', ' ')+' as reference to ' + constname +   '.'

                if (len(constobj.codesnippet) > 0):
                    for cs in constobj.codesnippet:
                        #print(cs)
                        constdatadetailed=constdatadetailed + cs +'. '

                if (constobj.Specifiedby != ''):
                    sbList = constobj.Specifiedby.split('||')[1:]
                    constdatadetailed=constdatadetailed+'.'
                    for sb in sbList:
                        constdatadetailed = constdatadetailed + ' The constructor ' + constname + ' in ' + constobj.curtypename + ' is specified by ' + sb.replace(
                            '\n', ' ').replace('  ',' ')
            self.WritetoBlockDict(constdatadetailed, self.writeFileName + 'const_' + str(cnt) + '_constinfoDetailed.txt')
            self.WritetoBlockDict(constDatasum, self.writeFileName + 'const_' + str(cnt) + '_constinfoSum.txt')
            self.LogToFIle('METHODNAMES', 'methodList.csv', constname.split('(')[0] +  ',const\n')
            self.LogToFIle('METHODNAMES', 'methodListDetail.csv',self.fullsresolvedname+'_'+ constname.split('(')[0] +  ',const\n')

            cnt += 1
            #print(' ')

    def WriteSubClasses(self):
        if(len(self.DirectSubclasses)>0):
            datainheritance='The direct know subclasses of ' + self.fullsresolvedname +' are ' + ', '.join(self.DirectSubclasses).replace('.','_') +'.'
            self.WritetoBlockDict(datainheritance, self.writeFileName + '_inheritance.txt')
        elif (len(self.DirectSubclasses)== 0):
            datainheritance='The direct know subclasses of ' + self.fullsresolvedname +' are zero. '
            self.WritetoBlockDict(datainheritance, self.writeFileName + '_inheritance.txt')
        else:
            pass


        '''
        #for sc in self.DirectSubclasses:
            #print(self.currenType+" "+self.currenTypeName + " is the parent of class " + self.DirectSubclasses[sc][0] + " in " + self.DirectSubclasses[sc][1])
            #print(self.DirectSubclasses[sc][0]+ " in " + self.DirectSubclasses[sc][1]+ " is the direct known sub class of " + self.currenType+" "+self.currenTypeName)

            #databasic=self.currenType + " " + self.currenTypeName + " is the parent of class " + self.DirectSubclasses[sc][1]+"."+self.DirectSubclasses[sc][0]
            #datainheritance=self.DirectSubclasses[sc][1]+"."+self.DirectSubclasses[sc][0] + " is the direct known sub class of " + self.currenType +" "+self.currenTypeName
            #datainheritance = datainheritance+self.DirectSubclasses[sc][1].replace('.','_') + "_" + self.DirectSubclasses[sc][0] +', '

            #self.WritetoBlockDict(databasic, self.writeFileName + '_inheritance.txt')
        '''

            #print()
        #print("_____________________________________________________________________")

    def WriteSubInterfaces(self):
        if(len(self.AllKnownSubInterfaces)>0):
            datainheritance='The known interfaces which implement ' + self.fullsresolvedname +' are '+', '.join(self.AllKnownSubInterfaces).replace('.','_') +'.'
            self.WritetoBlockDict(datainheritance, self.writeFileName + '_inheritance.txt')
        elif(len(self.AllKnownSubInterfaces)==0):
            datainheritance='The known interfaces which implement ' + self.fullsresolvedname +' are zero.'
            self.WritetoBlockDict(datainheritance, self.writeFileName + '_inheritance.txt')
        else:
            pass

    def WriteSupInterfaces(self):
        if(len(self.AllKnownSuperInterfaces)>0):
            datainheritance='The known super interfaces of ' + self.fullsresolvedname +' are '+', '.join(self.AllKnownSuperInterfaces).replace('.','_') +'.'
            self.WritetoBlockDict(datainheritance, self.writeFileName + '_inheritance.txt')
        elif(len(self.AllKnownSuperInterfaces)==0):
            datainheritance='The known super interfaces of ' + self.fullsresolvedname +' are zero.'
            self.WritetoBlockDict(datainheritance, self.writeFileName + '_inheritance.txt')
        else:
            pass


    def WriteImpClasses(self):
        if (len(self.ImplementedClasses) > 0):
            datainheritance = 'The known classes which implement ' + self.fullsresolvedname + ' are ' + ', '.join(self.ImplementedClasses).replace('.', '_') + '.'
            self.WritetoBlockDict(datainheritance, self.writeFileName + '_inheritance.txt')
        elif (len(self.ImplementedClasses) == 0):
            datainheritance = 'The known classes which implement ' + self.fullsresolvedname + ' are zero.'
            self.WritetoBlockDict(datainheritance, self.writeFileName + '_inheritance.txt')
        else:
            pass


        '''
        for sc in self.AllKnownSubInterfaces:
            #print(self.currenType + " " + self.currenTypeName + " is the parent of interface " + self.AllKnownSubInterfaces[sc][0] + " in " + self.AllKnownSubInterfaces[sc][1])
            #print(self.AllKnownSubInterfaces[sc][0] + " in " + self.AllKnownSubInterfaces[sc][1] + " is the direct known sub class of " + self.currenType + " " + self.currenTypeName)

            #databasic=self.currenType + " " + self.currenTypeName + " is the parent of interface " +self.AllKnownSubInterfaces[sc][1]+"."+self.AllKnownSubInterfaces[sc][0]
            #datainheritance=self.AllKnownSubInterfaces[sc][1]+"."+self.AllKnownSubInterfaces[sc][0] + " is a known sub interface of " + self.currenType + " " + self.currenTypeName
            datainheritance = datainheritance+self.AllKnownSubInterfaces[sc][1] + "." + self.AllKnownSubInterfaces[sc][0] +','

            #self.WritetoBlockDict(databasic, self.writeFileName + '_inheritance_interface.txt')
        '''
        #print("_____________________________________________________________________")

    def WriteDescInfo(self):
        datadesc=''
        #datadesc=datadesc+'<p>the declaration syntax for '+self.fullsresolvedname +' is '+self.MainDescription['syntax']+'<p>'
        #datadesc =datadesc +'\n\n'+ self.fullsresolvedname +' ' + self.MainDescription['desc'].replace('\n',' ').replace(' ',' ')
        datadesc = datadesc + '\n\n' + self.MainDescription['desc'].replace('\n','  ').replace('  ', ' ')
        datadesc=self.HandleDescription(datadesc)
        if(self.fullsresolvedname in self.ExtraInfo):
            for extInf in self.ExtraInfo[self.fullsresolvedname]:
                datadesc =datadesc +extInf

        #print(datadesc)
        self.WritetoBlockDict(datadesc, self.writeFileName + '_descinfo.txt')

    def WriteMethodInfo(self):

        methodatamain =  self.fullsresolvedname+' contains '+ str(len(self.MethodDict)) +' methods'
        #methodatamain = 'The number of methods in ' + self.fullsresolvedname + ' is ' + str(len(self.MethodDict))+'.\r\n'
        methodatamain = 'The number of methods in '+self.fullsresolvedname+' are ' + str(len(self.MethodDict)+len(self.InheritedMethodDict)) + '.\r\n'

        self.WritetoBlockDict(methodatamain, self.writeFileName + '_basicinfo.txt')


        cnt=0
        for method in self.MethodDict:
            methodobj=self.MethodDict[method]
            methodatasum = ''
            methoddatadetailed = ''
            methodname=methodobj.codefromsummary.replace(' ','')

            '''
            #SummaryInfo
            methodatasum=methodatasum +'\n' +methodobj.codefromsummary + ' is a method of ' +self.currenType +' ' + methodobj.curtypename
            #methodatasum = methodatasum + '\n' + methodobj.codefromsummary + ' in ' + methodobj.curtypename + ' contains ' + str(methodobj.noofparams) +' parameters '
            methodatasum = methodatasum + '\n' + methodobj.codefromsummary + ' in ' + methodobj.curtypename + ' ' + methodobj.summarydesc
            methodatasum = methodatasum + '\n' + methodobj.codefromsummary + ' takes in  ' + str(len(methodobj.parameterinfo)) + ' parameters '
            prminfo=methodobj.parameterinfo
            for prm in prminfo:
                #methodatasum = methodatasum + '\n' + prm +' is the ' + ClassInterfaceInfo.numtowordPos[str(prminfo[prm].position)]+' paramater in the method '+ methodobj.codefromsummary + ' of ' +self.currenType +' ' + methodobj.curtypename
                methodatasum = methodatasum + '\n' + prm + ' is the ' +' paramater' +  str(prminfo[prm]) + ' in the method ' + methodobj.codefromsummary + ' of ' + self.currenType + ' ' + methodobj.curtypename
                methodatasum = methodatasum + '\n' + 'The type of '+prm + ' is  ' + prminfo[prm].parameterType
                if(not(prminfo[prm].description.strip()=='')):
                    methodatasum = methodatasum + '\n'+  'Paramater '+ prm  +' in the method '+ methodobj.codefromsummary +  ' is ' + prminfo[prm].description


            #DetailedInfo
            methoddatadetailed = methoddatadetailed + '\n' + methodobj.codefromsummary + ' in ' + methodobj.curtypename + ' ' + methodobj.detaileddecrption
            if(methodobj.Overides!=''):
                methoddatadetailed = methoddatadetailed + '\n'+methodobj.codefromsummary + ' in ' + methodobj.curtypename + ' overides the method ' + methodobj.Overides

            if (methodobj.Throws != ''):
                methoddatadetailed = methoddatadetailed + '\n' + methodobj.codefromsummary + ' in ' + methodobj.curtypename + ' throws the exception ' + methodobj.Throws

            if (methodobj.Returns != ''):
                methoddatadetailed = methoddatadetailed + '\n' + methodobj.codefromsummary + ' in ' + methodobj.curtypename + ' returns  ' + methodobj.Returns

            if (methodobj.Specifiedby != ''):
                sbList=methodobj.Specifiedby.split('||')[1:]
                for sb in sbList:
                    methoddatadetailed = methoddatadetailed + '\n' + methodobj.codefromsummary + ' in ' + methodobj.curtypename + ' is specified by ' + sb
            '''

            # SummaryInfo
            #methodatasum = methodatasum + '\n' + methodname + ' is a method of ' + self.currenType + ' ' + methodobj.curtypename

            #CHANGE is sentence (MAJRO CHANGES)
            #methodatasum = methodatasum + '' + methodname + ' is a method.'

            # methodatasum = methodatasum + '\n' + methodname +  ' contains ' + str(methodobj.noofparams) +' parameters '
            methodatasum = methodatasum + ' The method ' + methodname +  ' ' + methodobj.summarydesc.replace('Deprecated','has been deprecated')
            methodatasum = methodatasum + ' The method ' + methodname + ' takes in ' + str(len(methodobj.parameterinfo)) + ' parameters. '
            prminfo = methodobj.parameterinfo
            for prm in prminfo:
                # methodatasum = methodatasum + '\n' + prm +' is the ' + ClassInterfaceInfo.numtowordPos[str(prminfo[prm].position)]+' paramater in the method '+ methodname + ' of ' +self.currenType +' ' + methodobj.curtypename
                methodatasum = methodatasum + '' + prm + ' is the ' + 'paramater ' + str(prminfo[prm].position) + ' in the method ' + methodname +' .'#+ ' of ' + self.currenType + ' ' + methodobj.curtypename
                methodatasum = methodatasum + ' ' + 'The type of ' + prm + ' is ' + prminfo[prm].parameterType+' .'
                if (not (prminfo[prm].description.strip() == '')):
                    methodatasum = methodatasum + ' ' + 'Paramater ' + prm + ' in the method ' + methodname + ' is' + prminfo[prm].description+' .'

            # DetailedInfo
            methoddatadetailed = methoddatadetailed+'<NEWMETHOD> ' + 'The method ' + methodname +  ' in '+ self.fullsresolvedname +' '  + methodobj.detaileddecrption.replace('\n',' ').replace('  ',' ').replace('Deprecated','has been deprecated')
            if (methodobj.Overides != ''):
                methoddatadetailed = methoddatadetailed + ' The method ' + methodname +  ' overides the method ' + methodobj.Overides.replace('\n','  ').replace('  ',' ') +'.'

            if (methodobj.Throws != ''):
                methoddatadetailed = methoddatadetailed + ' The method ' + methodname +  ' throws the exception ' + methodobj.Throws.replace('\n','  ').replace('  ',' ')+'.'

            if (methodobj.Returns != ''):
                methoddatadetailed = methoddatadetailed + ' The method '   + methodname +  ' returns ' + methodobj.Returns.replace('\n','  ').replace('  ',' ')+'.'



            if (methodobj.SeeAlso != ''):
                methoddatadetailed = methoddatadetailed +' See ' + methodobj.SeeAlso.replace(
                    '\n', '  ').replace('  ', ' ')+ ' as reference to ' + methodname +  '.'

            if (methodobj.Specifiedby != ''):
                sbList = methodobj.Specifiedby.split('||')[1:]
                methoddatadetailed=methoddatadetailed+'.'
                for sb in sbList:
                    methoddatadetailed = methoddatadetailed + ' The method ' + methodname +  ' is specified by' + sb.replace('\n',' ') +'.'

            if (methodobj.ImpReq!=''):
                methoddatadetailed = methoddatadetailed + ' The implementation requirements of method ' + methodname + ' in '+ self.fullsresolvedname+ ' are <IMPSNIPPET>' + methodobj.ImpReq.replace(
                    '\n', '  ').replace('  ', ' ') + '</IMPSNIPPET>.'

            if (methodobj.Since!=''):
                methoddatadetailed = methoddatadetailed + ' The method ' + methodname + ' in '+ self.fullsresolvedname +' is present since Java ' + methodobj.Since.replace(
                    '\n', '  ').replace('  ', ' ').replace('.','_') + '.'

            if (len(methodobj.codesnippet)>0):
                for cs in methodobj.codesnippet:
                    #print(cs)
                    methoddatadetailed = methoddatadetailed + cs + '. '
                #methoddatadetailed = methoddatadetailed + ' One of the ways in which the method ' + methodname + ' can be used is as follows ' + methodobj.codesnippet.replace(
                #    '\n', '  ').replace('  ', ' ') + '.'

            methoddatadetailed=methoddatadetailed+' </NEWMETHOD>'

            self.WritetoBlockDict(methodatasum, self.writeFileName +'method_'+str(cnt)+'_MethodinfoSum.txt')
            self.WritetoBlockDict(methoddatadetailed, self.writeFileName + 'method_' + str(cnt) + '_MethodinfoDetailed.txt')
            self.LogToFIle('METHODNAMES','methodList.csv',methodname.split('(')[0]+',method\n')
            self.LogToFIle('METHODNAMES', 'methodListDetail.csv',
                           self.fullsresolvedname + '_' + methodname.split('(')[0] + ',const\n')

            cnt+=1
            #print(' ')

    def WriteFieldInfo(self):
        fieldData = ''
        fieldDatamain = self.fullsresolvedname + ' contains ' + str(len(self.FieldDict)) + ' fields'
        #fieldDatamain = 'The number of fields in ' + self.fullsresolvedname + ' is ' + str(len(self.FieldDict)) +'.\r\n'
        fieldDatamain = 'The number of fields in '+self.fullsresolvedname+' are ' + str(len(self.FieldDict)+len(self.InheritedFieldDict)) + '.\r\n'

        self.WritetoBlockDict(fieldDatamain, self.writeFileName + '_basicinfo.txt')

        cnt=0
        for field in self.FieldDict:
            fieldobj=self.FieldDict[field]
            fieldsum=''
            fieldDetails=''

            #summary
            # CHANGE is sentence (MAJRO CHANGES)
            #fieldsum = fieldsum + '' + field + ' is a field.'# of ' + self.currenType + ' ' + fieldobj.curtypename
            fieldsum = fieldsum  + ' The field ' + field + ' in '+ self.fullsresolvedname +' ' + fieldobj.summarydescription.replace('Deprecated',' has been deprecated')
            fieldsum = fieldsum + ' ' + 'The modifier of '+ field + ' is ' + fieldobj.modifier +'.'

            #Details
            fieldDetails = fieldDetails + 'The field ' + field +' '+ fieldobj.detaileddecrption.replace('\n',' ').replace('Deprecated',' has been deprecated')

            #if(fieldobj.syntax_fromdetailed!=''):
            #    fieldDetails = fieldDetails + '' + 'The declaration syntax  of ' + field +  ' is ' + fieldobj.syntax_fromdetailed.replace(' ','_').replace('\xa0','_') +'.'

            if (len(fieldobj.codesnippet)>0):
                for cs in fieldobj.codesnippet:
                    #print(cs)
                    fieldDetails = fieldDetails + cs + '. '

            if (fieldobj.SeeAlso != ''):
                fieldDetails = fieldDetails +' See ' + fieldobj.SeeAlso.replace(
                    '\n', '  ').replace('  ', ' ')+ ' as reference to ' + field +  '.'

            if (fieldobj.Specifiedby != ''):
                sbList = fieldobj.Specifiedby.split('||')[1:]
                fieldDetails = fieldDetails+'.'
                for sb in sbList:
                    fieldDetails = fieldDetails + ' The field ' + field +  ' is specified by' + sb.replace('\n',' ') +'.'


            if (fieldobj.Since!=''):
                fieldDetails = fieldDetails + ' The field ' + field + ' in '+ self.fullsresolvedname +' is present since Java ' + fieldobj.Since.replace(
                    '\n', '  ').replace('  ', ' ').replace('.','_') + '.'



            self.WritetoBlockDict(fieldsum, self.writeFileName + 'fiel_' + str(cnt) + '_FieldinfoSum.txt')
            self.WritetoBlockDict(fieldDetails, self.writeFileName + 'field_' + str(cnt) + '_FieldinfoDetailed.txt')
            self.LogToFIle('METHODNAMES', 'methodList.csv', field + ',field\n')
            self.LogToFIle('METHODNAMES', 'methodListDetail.csv',
                           self.fullsresolvedname + '_' + field.split('(')[0] + ',const\n')

            cnt+=1

    def WriteInhMethodInfo(self):
        inhmethodata=''
        for inhmethod in self.InheritedMethodDict:
            inhmethodObj=self.InheritedMethodDict[inhmethod]
            #inhmethodata=inhmethodata +'\n'+ self.fullsresolvedname +' inherits the method '+   inhmethodObj.methodname + ' from ' + inhmethodObj.inheritedfrom
            inhmethodata=inhmethodata +''+'The method '+   inhmethodObj.methodname + '() is inherited from ' + inhmethodObj.inheritedfrom.replace('.','_') +'. '


        self.WritetoBlockDict(inhmethodata, self.writeFileName + '_inheritance.txt')

    def WriteInhFieldInfo(self):
        inhfieldata = ''

        for inhfield in self.InheritedFieldDict:
            inhfieldObj=self.InheritedFieldDict[inhfield]
            #inhfieldata=inhfieldata +'\n'+ self.fullsresolvedname +' inherits the field '+   inhfieldObj.fieldname + ' from ' + inhfieldObj.inheritedfrom
            inhfieldata = inhfieldata + '' + 'The field ' + inhfieldObj.fieldname + ' is inherited from ' + inhfieldObj.inheritedfrom.replace('.','_') +'. '

        self.WritetoBlockDict(inhfieldata, self.writeFileName + '_inheritance.txt')

    def WritetoBlockDict(self,data,blockname):
        blocktype=blockname.split('_')[-1]
        self.blocktypeDict[blocktype][1].append(data)

    def WriteToFile(self):
        fout = open(self.factfolder + '/' + self.fullsresolvedname.replace('.','_')+'.txt', 'a')
        #fout = open(self.factfolder+'/test22.csv', 'a')
        #data=data.replace('[', 'SquareBracketStart').replace(']', 'SquareBracketEnd').replace('<', 'AngularBracketStart').replace('>', 'AngularBracketEnd').replace('(','ParenthesesStart').replace(')', 'ParenthesesEnd')
        #fout = open(self.factfolder + '/' + filename, 'a')
        #data='<'+ClassInterfaceInfo.blocktypeDict[blocktype] +'_START>' +data + '\n<'+ClassInterfaceInfo.blocktypeDict[blocktype] +'_END>\n\n'


        for block in self.blocktypeDict:
            fout.write('<'+self.blocktypeDict[block][0]+'>')
            for blockdata in self.blocktypeDict[block][1]:
                try:
                    #blockdata=blockdata.replace('[', 'SquareBracketStart').replace(']', 'SquareBracketEnd').replace('<', 'AngularBracketStart').replace('>', 'AngularBracketEnd').replace('(','ParenthesesStart').replace(')', 'ParenthesesEnd')
                    fout.write('\n'+blockdata.replace('  ',' ').replace('\n','').replace('..','.').replace('. .','.')+'\n')
                except:
                    print("Exception Occured while writing file " + str(self.fullsresolvedname))
            fout.write('\n</' + self.blocktypeDict[block][0] + '>\n\n\n\n')
        fout.close()


    def LogToFIle(self,foldername,filename,data):
        fout=open(self.factfolder.replace('FACTS',foldername)+'/'+filename,'a')
        fout.write(data)
        fout.close()



    def HandleDescription(self,datadesc):
        #print(datadesc)
        descrpition_all_sentences=datadesc.split('.')
        process=True
        checkFSen = descrpition_all_sentences[0]
        checkFSenTag = nltk.pos_tag(wt(checkFSen.replace('\n', '')))
        for c in checkFSen.split(' ')[0:2]:
            if str(c).replace('\n', '') in self.currenTypeName:
                process = False
        if (process):
            checkFSenNew = checkFSen.split(' ')
            if (checkFSenTag[0][1] in ['DT']):
                checkFSenNew[0] = self.fullsresolvedname + ' is '
            elif (checkFSenTag[0][1] in ['VBN', 'IN', 'JJ', 'NNP', 'NN', 'VBD', 'CD']):
                checkFSenNew[0] = self.fullsresolvedname + ' is ' + checkFSenNew[0]
            elif (checkFSenTag[0][1] in ['VBZ', 'RB', 'NNS', 'VB']):
                checkFSenNew[0] = self.fullsresolvedname + ' ' + checkFSenNew[0]
            else:
                pass
            checkFSenNew = str(checkFSenNew[0]) + ' '.join(checkFSenNew[1:])
            checkFSenNew2 = checkFSenNew.replace('\n', '') + ',' + checkFSenTag[0][0] + ',' + checkFSenTag[0][1]
            fout = open(self.factfolder.replace('FACTS','REPLACED') + '/replaced_data.csv', 'a')
            fout.write(self.fullsresolvedname.replace(',', '') + ',' + ' '.join(checkFSen.split(' ')[0:2]).replace('\n',
                                                                                                                '').replace(
                ',', '') + ',' + checkFSen.replace(',', '').replace('\n', '') + ',' + checkFSenNew2 + '\n')
        else:
            checkFSenNew = checkFSen

        desc_return=checkFSenNew+ '. '.join(descrpition_all_sentences[1:])
        return  desc_return
        fout.close()
