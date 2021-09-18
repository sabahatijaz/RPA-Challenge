# Importing required modules
import PyPDF2
import os

for subdir, dirs, files in os.walk(r'C:\Users\User\Downloads\sabahat_ijaz_2\sabahat_ijaz\output'):
    for file in files:
        #print os.path.join(subdir, file)
        filepath = subdir + os.sep + file

        if filepath.endswith(".pdf"):
            print (filepath)
            # Creating a pdf file object
            pdfFileObj = open(r'C:\Users\User\Downloads\sabahat_ijaz\sabahat_ijaz\output\005-000000018.pdf', 'rb')
            # Creating a pdf reader object
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            pageObj = pdfReader.getPage(0)
            text = pageObj.extractText().split("  ")
            result = text[3].find('Name of this Investment')
            txt1=text[3].split("Name of this Investment")
            result=result+22
            # print(result)

            txt2=text[3].find('Unique Investment Identifier (UII):')

            # print(txt2)
            print(text[3][result+5:txt2-4])
            txt2=txt2+33
            print(text[3][txt2+5:txt2+18])

            # for i in range(len(text)):
            #     # Printing the line
            #     # Lines are seprated using "\n"
            #     print(i)
            #     print(text[i], end="\n\n")

