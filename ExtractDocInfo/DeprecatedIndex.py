from bs4 import  BeautifulSoup
import re

class DeprecatedInfo:
    def __init__(self, phtml, factfolder):
        self.soup = BeautifulSoup(phtml)
        self.factfolder = factfolder
        self.ExtractDeprecateInfo()

        print("Deprecated")


    def ExtractDeprecateInfo(self):
        contentData=self.soup.find('div',{'class':'contentContainer'})
        fout=open(self.factfolder+'/deprecated.txt','a')
        deperectedList = contentData.find_all("tr")
        for depE in deperectedList:
            if (len(depE.find_all('td')) > 0):
                methodrow = depE.find_all('td')
                line= (depE.find_all('td')[0].find('a').text.replace('.','_') +' has been deprecated').replace('\n',' ').replace('\xa0','_').replace('  ',' ')
                if(depE.find_all('td')[0].find('div',{'class':'block'}) is not None):
                    splitteddesc=[ i.strip() for i in depE.find_all('td')[0].find('div',{'class':'block'}).text.split('\n') ]
                    newsentence=' '.join(splitteddesc)
                    #line=line+','+' '.join(newsentence.replace(',','').split(' ')[0:2])+','+newsentence.replace(',','')
                    newsentence=newsentence.replace('no replacement', 'with no replacement')#.replace('.', '_')
                    #newsentence=re.sub('\_ ','. ',newsentence)
                    line=line+' '+newsentence+'.'
                else:
                    line = line + '.'
                    pass
                #print(line)
                fout.write(line+'\n')
                #minfo = MethodInfo.MethodDetails(methodrow, 'summary', self.packagename + '.' + self.currenTypeName)
                #self.MethodDict[minfo.methodNameKey] = minfo

        fout.close()
        print('Deprecated Info Written ')