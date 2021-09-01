import json
import re
import csv

row = []
heading = ["Tweet","PositiveWord","NegativeWords","TotalPostive","TotalNegative","Polarity"]
storeInCSV = []
countedWordperTweet = []
fileNumber=0
number=50

def clean_text(cleantext):
    cleantext = re.sub(r'http\S+', ' ', cleantext)
    cleantext = re.sub(r"\W+|_", ' ',cleantext)
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               "]+", flags=re.UNICODE)
    cleantext = emoji_pattern.sub(r'', cleantext)

    return cleantext

def count_Word_frequency(text):
    wordfrequency = {}
    wordsInTweet = text.split(" ")
    for word in wordsInTweet:
        if word in wordfrequency.keys():
            wordfrequency[word] = wordfrequency[word]+1
        else:
            wordfrequency[word] = 1
    return wordfrequency


def getpositivewors():
    with open("positiveWords.txt") as file1:
        positive = file1.read()
    return positive.split()

def getnegativewords():
    with open("negativeWords.txt") as file2:
        negative = file2.read()
    return negative.split()

positivewordList = getpositivewors()
negativewordList = getnegativewords()
storeInCSV.append(heading)
while fileNumber < number:
    fileNumber=fileNumber+1
    file="tweet"+str(fileNumber)+".json"
    # Opening JSON file
    f = open(file,)
    data = json.load(f)
    #stroring number of fetched tweets in the list
    for i in data['Tweet_data']:
        text = i['Text']
        text = clean_text(text)
        text=text.lower()
        row.append(text)

        wordfrequency = count_Word_frequency(text.lower())
        countedWordperTweet.append(wordfrequency)

i = 0
for words in countedWordperTweet:
    positiveWord = []
    negativeWords = []
    rowData = []
    rowData.append(row[i])
    i = i + 1
    for key in words.keys():
       if key in positivewordList:
          positiveWord.append(key)
       elif key in negativewordList:
           negativeWords.append(key)

    if len(positiveWord) > len(negativeWords):
        rowData.append(positiveWord)
        rowData.append("nan")
        rowData.append(len(positiveWord))
        rowData.append(0)
        rowData.append("Positive")
    elif len(positiveWord) < len(negativeWords):
        rowData.append("nan")
        rowData.append(negativeWords)
        rowData.append(0)
        rowData.append(len(negativeWords))
        rowData.append("Negative")
    elif len(positiveWord) == len(negativeWords):
         rowData.append("nan")
         rowData.append("nan")
         rowData.append(len(positiveWord))
         rowData.append(len(negativeWords))
         rowData.append("neutral")

    storeInCSV.append(rowData)

with open("resultOfPart2.csv","w",encoding="utf-8") as output:
    writer = csv.writer(output)
    for words in storeInCSV:
        writer.writerow(words)
