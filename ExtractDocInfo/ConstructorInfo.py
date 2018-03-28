from bs4 import BeautifulSoup
import bs4
'''
from ExtractDocInfo import ParamaterInfo
from ExtractDocInfo import CheckTags
'''
from  ParamaterInfo import  ParameterDetails
from CheckTags import  CheckTags


class ContDetails:
    basicReturnTypes = ['byte', 'short', 'int', 'long', 'float', 'double', 'boolean', 'char', 'void']

    def __init__(self,constrow,type,currtypename):
        self.curtypename = currtypename.replace('.','_')
        self.detailedesc=False
        if (type == 'summary'):
            self.summarydesc = self.ExtarctDescFromSummary(constrow)
            self.codefromsummary = self.ExtractCodeFromSumamry(constrow)
            self.parameterinfo = self.ExtractParamInfoFromSummary(constrow)
            self.modifiertype=''
            #print(self.paremeterinfo)
            # self.methodsumrow=methodrow
            #self.returnType = self.ExtratcReturnTypeInfo(methodrow)
            #self.paremeterinfo = self.ExtractParamInfoFromSummary(methodrow)


    def ExtarctDescFromSummary(self, constrow):
        if(len(constrow)>1):
            return ''
        else:
            if(constrow[0].find('div', {'class': 'block'}) is not None):
                return constrow[0].find('div', {'class': 'block'}).text.replace('\n', '').strip()
            else:
                pass

    def ExtractCodeFromSumamry(self, constrow):
        if (len(constrow) > 1):
            return constrow[0].text+ ' '+constrow[1].find('code').text.replace('\n', '').strip()
        else:
            return constrow[0].find('code').text.replace('\n', '').strip()

    def ExtractParamInfoFromSummary(self, constrow):
        paramnames = self.codefromsummary.split('(')[1].replace(')', '').split(', ')
        if (len(constrow) > 1):
            self.constNameKey=constrow[1].find('code').contents[0].contents[0].attrs['href'].split('#')[1]
            paraminfotemp = constrow[1].find('code').contents[0].contents[0].attrs['href'].split('#')[1].split('-')
        else:
            self.constNameKey = constrow[0].find('code').contents[0].contents[0].attrs['href'].split('#')[1]
            paraminfotemp = constrow[0].find('code').contents[0].contents[0].attrs['href'].split('#')[1].split('-')

        paraminfo = []
        self.noofparams = len(paraminfotemp) - 2
        if(self.noofparams == len(paramnames)):
            self.noofparams = len(paramnames)
        else:
            if((self.noofparams)==1):
                paramnames[0]= self.codefromsummary.split('(')[1].replace(')', '')
            else:
                print("Unhandled Bug Please Fix Same in Method Also")
            pass
        pinfo ={}
        if (paramnames[0] == '' and self.noofparams == 1):
            self.noofparams = 0
        #print(self.constNameKey)
        for i in range(0, self.noofparams):
            if (paraminfotemp[i + 1] in {'E'}):
                #pinfo.append(ParamaterInfo.ParameterDetails(i + 1, "Type Parameter for " + self.curtypename,paramnames[i].split('\xa0')[1]))
                #paraminfo.append([i+1,"Type Parameter for " +self.curtypename,paramnames[i].split('\xa0')[1]])
                #pinfo[paramnames[i].split('\xa0')[1]] = ParamaterInfo.ParameterDetails(i + 1, "Type Parameter for " + self.curtypename,paramnames[i].split('\xa0')[1])
                pinfo[paramnames[i].split('\xa0')[1]] = ParameterDetails(i + 1,"Type Parameter for " + self.curtypename,paramnames[i].split('\xa0')[1])

            else:
                #pinfo.append(ParamaterInfo.ParameterDetails(i + 1, paraminfotemp[i + 1], paramnames[i].split('\xa0')[1]))
                # paraminfo.append([i+1,paraminfotemp[i+1],paramnames[i].split('\xa0')[1]])
                #pinfo[paramnames[i].split('\xa0')[1]] = ParamaterInfo.ParameterDetails(i + 1, paraminfotemp[i + 1],paramnames[i].split('\xa0')[1])
                pinfo[paramnames[i].split('\xa0')[1]] = ParameterDetails(i + 1, paraminfotemp[i + 1],paramnames[i].split('\xa0')[1])

        # print(self.methodNameKey+"::"+str(pinfo))
        return pinfo

    def AddInfoFromDetails(self, constrow):
        self.detailedesc=True
        if(constrow.find('div') is not None):
            self.detaileddecrption = constrow.find('div').text
        else:
            self.detaileddecrption = ''

        self.codefromdetails = constrow.find('pre').text.replace('\n', '').strip()
        self.codesnippet = []
        constusefinder = self.constNameKey.split('-')[0]
        try:
            if(constrow.find_all('code') is not None):
                for codetext in constrow.find_all('code'):
                    codesnippet = codetext.text.replace('\n', '').strip()
                    if((';' in codesnippet.replace('&nbsp;','')) or '...' in codesnippet or constusefinder+'(' in codesnippet):
                        self.codesnippet.append(' An example of how to use the constructor '+ self.constNameKey.split('-')[0] +' in ' +self.curtypename + ' is <CODESNIPPET>'+codesnippet.replace('\n','').replace('  ','')+'</CODESNIPPET>')
            else:
                pass
                #self.codesnippet=[]
        except:
            pass

        try:
            if(constrow.find_all('pre') is not None):
                for codetext in constrow.find_all('pre'):
                    codesnippet = codetext.text.replace('\n', '').strip()
                    if((';' in codesnippet.replace('&nbsp;','')) or '...' in codesnippet or constusefinder+'(' in codesnippet):
                        self.codesnippet.append(' An example of how to use the constructor '+ self.constNameKey.split('-')[0] +' in ' +self.curtypename + ' is <CODESNIPPET>'+codesnippet.replace('\n','').replace('  ','')+'</CODESNIPPET>')
            else:
                pass
                #self.codesnippet=[]
        except:
            pass


        self.Overides = self.Returns = self.Throws = self.SeeAlso = self.parametrdescdetailed = self.Specifiedby =self.ImpReq=self.Since= ''

        descriptionList=constrow.find_all("dl")
        for dl in descriptionList:
            dtList = dl.find_all("dt")
            ddList = dl.find_all("dd")
            ddcount = 0
            for dt in dtList:
                #CheckTags.CheckTags.AddKey(dt.text)
                if(dt.text=='Overrides:'):
                    self.Overides=ddList[ddcount].text
                elif (dt.text == 'Since:'):
                    self.Since = ddList[ddcount].text
                elif (dt.text == 'Implementation Requirements:'):
                    if(self.ImpReq==''):
                        self.ImpReq = ddList[ddcount].text
                    else:
                        self.ImpReq = self.ImpReq+ ddList[ddcount].text
                    self.ImpReq = ddList[ddcount].text
                elif (dt.text == 'Implementation Note:'):
                    if(self.ImpReq==''):
                        self.ImpReq = ddList[ddcount].text
                    else:
                        self.ImpReq = self.ImpReq+ ddList[ddcount].text
                    self.ImpReq = ddList[ddcount].text
                elif(dt.text=='Returns:'):
                    self.Returns = ddList[ddcount].text
                elif (dt.text == 'Specified by:'):
                    self.Specifiedby = self.Specifiedby + '|| ' + ddList[ddcount].text
                elif (dt.text=='Throws:'):
                    self.Throws = ddList[ddcount].text
                elif (dt.text=='See Also:'):
                    self.SeeAlso = ddList[ddcount].text
                elif (dt.text=='Parameters:'):
                    try:
                        for pnumber in range(0,self.noofparams):
                            pinfodetail=ddList[ddcount].text.split('-')
                            self.parameterinfo[pinfodetail[0].strip()].description=pinfodetail[1]
                            self.parametrdescdetailed =self.parametrdescdetailed+" "+ddList[ddcount].text
                            self.parametrdescdetailed=self.parametrdescdetailed.replace('\n', ' ')
                            ddcount+=1
                    except:
                        print("Exception Occured")
                else:
                    pass

                if (not(dt.text == 'Parameters:')):
                    ddcount+=1
