import json
import re
import math

printblog = []
coldArticlesData = []

wordFlu = 'flu'
wordCold = 'cold'
wordSnow = 'snow'
countFluArticle = 0
countSnowArticles = 0
countColdArticles = 0
fileNumber = 0
number = 50

def clean_text(cleantext):
    cleantext = re.sub(r'http\S+', ' ', cleantext)
    cleantext = re.sub(r"\W+|_", ' ',cleantext)
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               "]+", flags=re.UNICODE)
    cleantext = emoji_pattern.sub(r'', cleantext)

    return cleantext

while fileNumber < number:
    coldarticles = {}
    fileNumber=fileNumber+1
    file="tweet"+str(fileNumber)+".json"
    # Opening JSON file
    f = open(file,)
    data = json.load(f)
    flagforflu = 0
    flagforcold = 0
    flagforsnow = 0
    totalWords = 0
    #stroring number of fetched tweets in the list
    for i in data['Tweet_data']:
        text = i['Text']
        text = clean_text(text)
        text=text.lower()
        words = text.split(" ")
        totalWords = totalWords + len(words)
        for word in words:
            if word == 'flu':
                flagforflu = 1
            elif word == 'snow':
                flagforsnow=1
            elif word == 'cold':
                flagforcold = flagforcold+1;

    if flagforflu == 1:
        countFluArticle = countFluArticle+1

    if flagforcold > 0:
        countColdArticles = countColdArticles + 1
        ArticleName = "tweet"+str(fileNumber)+".json"
        coldarticles[ArticleName] = flagforcold
        coldarticles["OtherWords"]= totalWords
        coldArticlesData.append(coldarticles)

    if flagforsnow == 1:
        countSnowArticles = countSnowArticles + 1

flulog = math.log10(number/countFluArticle)
coldlog = math.log10(number/countColdArticles)
snowlog = math.log10(number/countSnowArticles)
print("+-------------------------------+")
print("| ""word" + "\t"+"DF" + "\t"+"N/DF" + "\t"+"log10(N/DF)"+" |\t")
print("+-------------------------------+")
print("| ""flue" + "\t"+str(countFluArticle) + "\t"+str(number)+"/"+str(countFluArticle) + "\t"+str(round(flulog,3)) + "\t\t|")
print("| ""snow" + "\t"+str(countSnowArticles) + "\t"+str(number)+"/"+str(countSnowArticles) + "\t"+str(round(snowlog,3)) + "\t\t|\t")
print("| ""cold" + "\t"+str(countColdArticles) + "\t"+str(number)+"/"+str(countColdArticles) + "\t"+str(round(coldlog,3)) + " \t\t|\t")
print("+-------------------------------+")
print("Term : Cold")
print("Cold appeared in ",len(coldArticlesData),"documents")
print("+-------------------------------------------------------------------+")
print("|  Article" + "\t\t"+"Total Words" + "\t\t"+" Frequency " + "\t\t"+" Relative Frequency "+"|\t")
print("+-------------------------------------------------------------------+")
for word in coldArticlesData:
    for key in word.keys():
        print("| "+key + "\t\t" + str(word["OtherWords"]) + "\t\t\t" + str(word[key]) + "\t\t\t\t" + str(round(word[key]/word["OtherWords"],5)) + "\t\t\t|\t")
        break
print("+-------------------------------------------------------------------+")