

class FieldDetails:

    def __init__(self,fieldrow,type,currtypename):
        self.curtypename = currtypename.replace('.','_')
        if (type == 'summary'):
            self.fieldname = fieldrow[1].find('code').contents[0].contents[0].attrs['href'].split('#')[1]
            #print(self.fieldname)
            self.ExtractCodeFromSummary(fieldrow)
            self.summarydescription=self.ExtractDescFromSummary(fieldrow)
        if(type=='details'):
            self.detailedydescription = ''


    def ExtractDescFromSummary(self, fieldrow):
        if(fieldrow[1].find('div', {'class': 'block'}) is not None):
            return fieldrow[1].find('div', {'class': 'block'}).text.replace('\n', '').strip()
        else:
            return ""


    def ExtractCodeFromSummary(self, fieldrow):
         fieldmodtype=fieldrow[0].find('code').text.replace('\n', '').strip().split(' ')
         self.modifier=fieldmodtype[0]
         if(len(fieldmodtype)==2):
             self.type=fieldmodtype[1]
         elif(len(fieldmodtype)==1):
             self.type = 'public'
         else:
             "Exception Unhahndel Condition Fix the Bug for field " +self.fieldname +"  class "+ self.curtypename




    def AddInfoFromDetails(self,fielddetailrow):
        if (fielddetailrow.find('div') is not None):
            self.detaileddecrption=fielddetailrow.find('div').text
        else:
            self.detaileddecrption=''


        self.codesnippet = []
        fieldfinder=self.fieldname
        if(fielddetailrow.find_all('code') is not None):
            for codetext in fielddetailrow.find_all('code'):
                codesnippet = codetext.text.replace('\n', '').strip()
                if((';' in codesnippet.replace('&nbsp;','')) or '...' in codesnippet or '.'+fieldfinder in codesnippet):
                    self.codesnippet.append(' An example of how the  field '+ self.fieldname +' in ' +self.curtypename + ' can be used is <CODESNIPPET>'+codesnippet.replace('\n','').replace('  ','')+'</CODESNIPPET>')
        else:
            pass
            #self.codesnippet=[]


        if(fielddetailrow.find_all('pre') is not None):
            for codetext in fielddetailrow.find_all('pre'):
                codesnippet = codetext.text.replace('\n', '').strip()
                if((';' in codesnippet.replace('&nbsp;','')) or '...' in codesnippet or '.'+fieldfinder in codesnippet):
                    self.codesnippet.append(' An example of how the  field '+ self.fieldname.split('-')[0] +' in ' +self.curtypename + ' can be used is <CODESNIPPET>'+codesnippet.replace('\n','').replace('  ','')+'</CODESNIPPET>')
        else:
            pass
            #self.codesnippet=[]


        if(fielddetailrow.find('pre') is not None):
            self.syntax_fromdetailed=fielddetailrow.find('pre').text
        else:
            self.syntax_fromdetailed=''

        self.Overides = self.Returns = self.Throws = self.SeeAlso = self.parametrdescdetailed = self.Specifiedby = self.ImpReq = self.Since = ''
        descriptionList = fielddetailrow.find_all("dl")
        for dl in descriptionList:
            dtList = dl.find_all("dt")
            ddList = dl.find_all("dd")
            ddcount = 0
            for dt in dtList:
                # CheckTags.CheckTags.AddKey(dt.text)
                if (dt.text == 'Overrides:'):
                    self.Overides = ddList[ddcount].text
                elif (dt.text == 'Implementation Requirements:'):
                    if (self.ImpReq == ''):
                        self.ImpReq = ddList[ddcount].text
                    else:
                        self.ImpReq = self.ImpReq + ddList[ddcount].text
                elif (dt.text == 'Implementation Note:'):
                    if (self.ImpReq == ''):
                        self.ImpReq = ddList[ddcount].text
                    else:
                        self.ImpReq = self.ImpReq + ddList[ddcount].text
                elif (dt.text == 'Returns:'):
                    if (self.Returns):
                        self.Returns = ddList[ddcount].text
                elif (dt.text == 'Specified by:'):
                    self.Specifiedby = self.Specifiedby + '|| ' + ddList[ddcount].text
                elif (dt.text == 'Throws:'):
                    self.Throws = ddList[ddcount].text
                    if ((ddcount) < len(ddList) - 1):
                        for cntleft in range(len(ddList) - 1 - ddcount):
                            if ('Exception -' in ddList[ddcount + 1].text):
                                self.Throws = self.Throws + ', ' + ddList[
                                    ddcount + 1].text  # PROBABLE WRONG LOGIC FIX LATER
                                ddcount += 1
                            else:
                                pass
                elif (dt.text == 'See Also:'):
                    self.SeeAlso = ddList[ddcount].text
                elif (dt.text == 'Parameters:'):
                    try:
                        for pnumber in range(0, self.noofparams):
                            pinfodetail = ddList[ddcount].text.split('-')
                            self.parameterinfo[pinfodetail[0].strip()].description = pinfodetail[1]
                            self.parametrdescdetailed = self.parametrdescdetailed + " " + ddList[ddcount].text
                            self.parametrdescdetailed = self.parametrdescdetailed.replace('\n', ' ')
                            ddcount += 1
                    except:
                        print("Exception Occured")
                elif (dt.text == 'Since:'):
                    self.Since = ddList[ddcount].text
                else:
                    pass

                if (not (dt.text == 'Parameters:')):
                    ddcount += 1



