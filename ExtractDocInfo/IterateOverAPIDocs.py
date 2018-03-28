import os
import shutil
import html2text
import re
from bs4 import BeautifulSoup
import pprint
'''
from ExtractDocInfo import  ClassUseInfo
from ExtractDocInfo import  ClassInterFaceInfo
from ExtractDocInfo import DeprecatedIndex
from ExtractDocInfo import CheckTags
'''

from ClassUseInfo import ClassUse
from ClassInterFaceInfo import ClassInterfaceInfo
from DeprecatedIndex import DeprecatedInfo
from  CheckTags import  CheckTags

class IteratteOverAPI:
    def __init__(self,apifolder,factfolder):
        self.APIFolder=apifolder
        self.factfolder=factfolder
        self.httotext = html2text.HTML2Text()
        self.APIFileList=os.listdir(factfolder)
        self.mode=None
        #UNCOMMENT BELOW TO JUST GET THE text from HTML
        #self.mode='html'

        if not self.APIFileList:
            self.APIFileList=self.LoadFileList()
        if(self.mode!='html'):
            self.WriteEnt()



    def WriteEnt(self):
        #EntList=ClassInterFaceInfo.ClassInterfaceInfo.entityDict
        EntList = ClassInterfaceInfo.entityDict

        #EntList=ClassInterFaceInfo.entityDict
        for e in EntList:
            f=open(self.factfolder.replace('FACTS','LIST')+EntList[e].EntType+'.lst','a')
            f.write(EntList[e].name+'\n')
            f.close()

    '''
    def WriteTag(self):
        TagDict=ClassInterFaceInfo.ClassInterfaceInfo.tagDict
        for t in TagDict :
            f=open(self.factfolder.replace('FACTS','TAGDICT')+'Tags.txt','a')
            f.write(TagDict[t]+'\n')
            f.close()
    '''


    def LoadFileList(self):
        folderlist=os.walk(self.APIFolder)
        count=0
        for f in folderlist:
            #print(f)
            count += 1
            cntfile = 0
            if(count<20000):
                for fs in f[2]:
                    cntfile += 1
                    #print(str(count) +':'+str(cntfile)+':'+str(f[0])+str(fs))
                    if (f[0].split('/')[-1] in{'class-use','doc-files'}):
                        #print
                        '''
                        type='class-use'
                        print(f[0].split('/')[-1])
                        apistart=str(f[0]).replace(self.APIFolder,'').replace('/','_',)
                        newname=str(count)+'_'+apistart+'_'+fs
                        orgfilehtml=self.ReadFileHTML(f[0] + '/' + fs)
                        if('.html' in fs):
                            factdata=self.GetTextFromHTML(orgfilehtml)
                            fout=open(str('FACTS2//'+newname).replace('.html','.txt'),'w')
                            fout.write(factdata)
                            fout.close()
                            print(str(count) +':'+newname)
                        print
                        '''
                    else:
                        if('serialized-form' not in str(fs) and 'overview-tree' not in str(fs) and 'index' not in str(fs) and 'package' not in str(fs) and '-frame' not in str(fs) and '-noframe' not in str(fs) and '-summary' not in str(fs) and '-values' not in str(fs) and 'help-doc' not in str(fs)):
                            orgfilehtml = self.ReadFileHTML(f[0] + '/' + fs)
                            if ('deprecated-list' in str(fs)):
                                print("Starting Processing for " + str(cntfile) + ":" + str(f[0] + '/' + fs))
                                self.GetFactsFromHTML(orgfilehtml,"deprecated")
                            elif ('.html' in fs):
                                #pass
                                print( "Starting Processing for " +str(cntfile) + ":" + str(f[0] + '/' + fs))
                                if(self.mode!='html'):
                                    self.GetFactsFromHTML(orgfilehtml,"mainfolder")
                                else:
                                    pagetext=self.GetTextFromHTML(orgfilehtml)
                                    fname=fs.replace('.html','.txt').replace('.','_')
                                    fopen=open(self.factfolder+fname,'a')
                                    fopen.write(pagetext)
                                    fopen.close()
                            #print(str(cntfile)+":"+str(f[0])+fs)
                            else:
                                pass
                            print('Finished Processing #################################################\n')

        return  folderlist

    def ReadFileHTML(self,file):
        orgfile = open(file,'r',errors='ignore')
        print(file)
        if(file=='docs/api/java/awt/AWTKeyStroke.html'):
            print("Debug")

        orgfilehtml = orgfile.read()
        orgfile.close()
        return  orgfilehtml


    def GetTextFromHTML(self,html):
        '''
        soup = BeautifulSoup(html)
        for script in soup(["script", "style"]):
            script.extract()    # rip it out
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        pagetext = ' '.join(chunk for chunk in chunks if chunk)
        return pagetext
        '''
        self.httotext.ignore_links = True
        pagetext = self.httotext.handle(html)

        # soup = BeautifulSoup(html, 'html.parser')
        # texts = soup.findAll(text=True)
        # pagetext= filter(self.visible, texts)

        return pagetext


    def GetFactsFromHTML(self, html,type):
        if type=='class-use':
            #factstext=ClassUseInfo.ClassUse(html)
            factstext=ClassUse(html)
        elif(type=='deprecated'):
            #factstext=DeprecatedIndex.DeprecatedInfo(html,self.factfolder)
            factstext=DeprecatedInfo(html,self.factfolder)
        else:
            #factstext=ClassInterFaceInfo.ClassInterfaceInfo(html,self.factfolder)
            factstext = ClassInterfaceInfo(html, self.factfolder)

        return factstext
    

    
#
ap=IteratteOverAPI('../Data/docs/api/java/','../Data/FACTS/')



