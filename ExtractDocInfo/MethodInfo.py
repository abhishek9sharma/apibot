from bs4 import BeautifulSoup
import bs4
'''
from ExtractDocInfo import ParamaterInfo
from ExtractDocInfo import  CheckTags
'''
from ParamaterInfo import ParameterDetails
from CheckTags import CheckTags

class MethodDetails:
    basicReturnTypes = ['byte', 'short', 'int', 'long', 'float', 'double', 'boolean', 'char', 'void']

    def __init__(self,methodrow,type,currtypename):
        self.curtypename=currtypename.replace('.','_')
        if(type=='summary'):
            #self.methodsumrow=methodrow
            self.returnType = self.ExtratcReturnTypeInfo(methodrow)
            self.codefromsummary=self.ExtractCodeFromSumamry(methodrow)
            self.summarydesc=self.ExtarctDescFromSummary(methodrow)
            self.parameterinfo=self.ExtractParamInfoFromSummary(methodrow)

    def ExtratcReturnTypeInfo(self, methodrow):
        if ((len(methodrow[0].text.split(' ')) > 1) and (
            methodrow[0].text.split(' ')[0] in {'protected', 'private', 'public'})):
            accesmodifier = methodrow[0].text.split(' ')[0]
            rtype = methodrow[0].text.split(' ')[1]
        elif(len(methodrow[0].text.split(' ')) > 1):
            accesmodifier = 'publicComplex'
            rtype = methodrow[0].text
        else:
            accesmodifier = 'public'
            rtype = methodrow[0].text



        if (rtype in MethodDetails.basicReturnTypes):
            retType = [rtype, 'basic', accesmodifier]
        elif(methodrow[0].find('a') is not None):
            rettypeeadvanced = methodrow[0].find('a').attrs['title']
            retType = [rtype, rettypeeadvanced, accesmodifier]
        else:
            retType = [rtype, 'complex', 'public']
        return  retType

    def ExtractCodeFromSumamry(self, methodrow):
        return methodrow[1].find('code').text.replace('\n', '').strip()

    def ExtarctDescFromSummary(self, methodrow):
        if(methodrow[1].find('div',{'class':'block'}) is not None):
            return methodrow[1].find('div',{'class':'block'}).text.replace('\n', '').strip()
        else:
            return ""


    def ExtractParamInfoFromSummary(self, methodrow):

        paramnames=self.codefromsummary.split('(')[1].replace(')','').split(', ')
        self.methodNameKey=methodrow[1].find('code').contents[0].contents[0].attrs['href'].split('#')[1]
        #print(self.methodNameKey)
        if(self.methodNameKey=='debug'):
            print('DEBUG')
        paraminfotemp=methodrow[1].find('code').contents[0].contents[0].attrs['href'].split('#')[1].split('-')
        paraminfo=[]
        self.noofparams = len(paraminfotemp) - 2
        #self.noofparams = len(paramnames)

        if (self.noofparams == len(paramnames)):
            self.noofparams = len(paramnames)
        else:
            if ((self.noofparams) == 1):
                paramnames[0] = self.codefromsummary.split('(')[1].replace(')', '')
            else:
                print("Unhandled Bug Please Fix Same in Constructor Also")
            pass
        pinfo={}
        if(paramnames[0]=='' and self.noofparams==1):
            self.noofparams=0

        for i in range(0,self.noofparams):
            if(paraminfotemp[i+1] in {'E'}):
                #pinfo.append(ParamaterInfo.ParameterDetails(i+1,"Type Parameter for " +self.curtypename,paramnames[i].split('\xa0')[1]))
                #pinfo[paramnames[i].split('\xa0')[1]]=ParamaterInfo.ParameterDetails(i+1,"Type Parameter for " +self.curtypename,paramnames[i].split('\xa0')[1])
                pinfo[paramnames[i].split('\xa0')[1]] =ParameterDetails(i + 1,"Type Parameter for " + self.curtypename,paramnames[i].split('\xa0')[1])

                #paraminfo.append([i+1,"Type Parameter for " +self.curtypename,paramnames[i].split('\xa0')[1]])
            else:
                #pinfo.append(ParamaterInfo.ParameterDetails(i+1,paraminfotemp[i+1],paramnames[i].split('\xa0')[1]))
                #pinfo[paramnames[i].split('\xa0')[1]]=ParamaterInfo.ParameterDetails(i+1,paraminfotemp[i+1],paramnames[i].split('\xa0')[1])
                pinfo[paramnames[i].split('\xa0')[1]] = ParameterDetails(i + 1, paraminfotemp[i + 1],
                                                                                       paramnames[i].split('\xa0')[1])

                #paraminfo.append([i+1,paraminfotemp[i+1],paramnames[i].split('\xa0')[1]])

        #print(self.methodNameKey+"::"+str(pinfo))
        return  pinfo


    def AddInfoFromDetails(self, methodrow):
        if( methodrow.find('div') is not  None):
            self.detaileddecrption = methodrow.find('div').text
        else:
            self.detaileddecrption=''
        self.codefromdetails = methodrow.find('pre').text.replace('\n', '').strip()
        self.codesnippet = []
        methodusefinder=self.methodNameKey.split('-')[0]
        try:
            if(methodrow.find_all('code') is not None):
                for codetext in methodrow.find_all('code'):
                    codesnippet = codetext.text.replace('\n', '').strip()
                    if((';' in codesnippet.replace('&nbsp;','')) or '...' in codesnippet or '.'+methodusefinder+'(' in codesnippet):
                        self.codesnippet.append(' An example of how to use the  method '+ self.methodNameKey.split('-')[0] +' in ' +self.curtypename +  ' is <CODESNIPPET>'+codesnippet.replace('\n','').replace('  ','')+'</CODESNIPPET>')
            else:
                pass
                #self.codesnippet=[]
        except:
            pass

        try:
            if(methodrow.find_all('pre') is not None):
                for codetext in methodrow.find_all('pre'):
                    codesnippet = codetext.text.replace('\n', '').strip()
                    if((';' in codesnippet.replace('&nbsp;','')) or '...' in codesnippet or '.'+methodusefinder+'(' in codesnippet):
                        self.codesnippet.append(' An example of how to use the  method '+ self.methodNameKey.split('-')[0] +' in ' +self.curtypename +  ' is <CODESNIPPET>'+codesnippet.replace('\n','').replace('  ','')+'</CODESNIPPET>')
            else:
                pass
                #self.codesnippet=[]
        except:
            pass



        self.Overides=self.Returns=self.Throws=self.SeeAlso=self.parametrdescdetailed=self.Specifiedby=self.ImpReq=self.Since=''
        descriptionList=methodrow.find_all("dl")
        for dl in descriptionList:
            dtList = dl.find_all("dt")
            ddList = dl.find_all("dd")
            ddcount = 0
            for dt in dtList:
                #CheckTags.CheckTags.AddKey(dt.text)
                if(dt.text=='Overrides:'):
                    self.Overides=ddList[ddcount].text
                elif (dt.text == 'Implementation Requirements:'):
                    if(self.ImpReq==''):
                        self.ImpReq = ddList[ddcount].text
                    else:
                        self.ImpReq = self.ImpReq + ddList[ddcount].text
                elif (dt.text == 'Implementation Note:'):
                    if(self.ImpReq==''):
                        self.ImpReq = ddList[ddcount].text
                    else:
                        self.ImpReq = self.ImpReq + ddList[ddcount].text
                elif(dt.text=='Returns:'):
                    if(self.Returns):
                        self.Returns = ddList[ddcount].text
                elif (dt.text == 'Specified by:'):
                    self.Specifiedby = self.Specifiedby +'|| '+ ddList[ddcount].text
                elif (dt.text=='Throws:'):
                        self.Throws = ddList[ddcount].text
                        if((ddcount)<len(ddList)-1):
                            for cntleft in range(len(ddList)-1-ddcount):
                                if ('Exception -' in ddList[ddcount+1].text):
                                    self.Throws = self.Throws + ', ' + ddList[ddcount+1].text  # PROBABLE WRONG LOGIC FIX LATER
                                    ddcount += 1
                                else:
                                    pass
                elif (dt.text=='See Also:'):
                    self.SeeAlso = ddList[ddcount].text
                elif (dt.text=='Parameters:'):
                    try:
                        for pnumber in range(0,self.noofparams):
                            pinfodetail=ddList[ddcount].text.split('-')
                            self.parameterinfo[pinfodetail[0].strip()].description=pinfodetail[1]
                            self.parametrdescdetailed =self.parametrdescdetailed+" "+ddList[ddcount].text
                            self.parametrdescdetailed=self.parametrdescdetailed.replace('\n' ,' ')
                            ddcount+=1
                    except:
                        print("Exception Occured")
                elif (dt.text == 'Since:'):
                        self.Since = ddList[ddcount].text
                else:
                    pass


                if (not(dt.text == 'Parameters:')):
                    ddcount+=1



            #print("")
