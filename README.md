# ExtractDocInfo
A set Python Scripts to Convert Java API Documentation into a more readable Natural Language Format. These related to w.r.t _Domain Adapation_ Component 
w.r.t Paper ["APIBot: Question Answering Bot for API Documentation"](https://dl.acm.org/citation.cfm?id=3155585)


# Usage

### Download the whole project and then
1. Delete the _.keep_ files in all subdirectories of folder [Data](https://github.com/abhishek9sharma/apibot/Data/).
2. Download the Java SE Documentaion from the official [link](https://download.oracle.com/otn-pub/java/jdk/8u161-b12/2f38c3b165be4555a1fa6e98c45e0808/jdk-8u161-docs-all.zip)
or [here](http://www.oracle.com/technetwork/java/javase/documentation/jdk8-doc-downloads-2133158.html).
3. Unzip the .zip file extracted in previous step to folder [Data](https://github.com/abhishek9sharma/apibot/Data/). You should see a _docs_ folder.
4.  Go the the folder  [ExtractDocInfo](https://github.com/abhishek9sharma/apibot/ExtractDocInfo/) and run [IterateOverAPIDocs.py](https://github.com/abhishek9sharma/apibot/ExtractDocInfo/IterateOverAPIDocs.py).
5. You should see the converted documents in the folder [FACTS](https://github.com/abhishek9sharma/apibot/Data/FACTS). This corpus can be plugged in to [Sirius](http://sirius.clarity-lab.org/sirius/).

####Misc:
*   In case you delete the folder in  [Data](https://github.com/abhishek9sharma/apibot/Data) you may run the .\setups.sh file present in the same folder.




# References
* ["APIBot: Question Answering Bot for API Documentation"](https://dl.acm.org/citation.cfm?id=3155585)

## Bibtex Citation 
```
@inproceedings{
  tian2017apibot,
  title={APIBot: Question answering bot for API documentation},
  author={Tian, Yuan and Thung, Ferdian and Sharma, Abhishek and Lo, David},
  booktitle={Automated Software Engineering (ASE), 2017 32nd IEEE/ACM International Conference on},
  pages={153--158},
  year={2017},
  organization={IEEE}
}
```
