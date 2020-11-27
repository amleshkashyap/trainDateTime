import csv
import json
import re
import sys
import math
import random


trainingData = list()
randomDelimiters = [", "]                   #, "  ", " blah ", " some text ", " "]
randomChoiceList = list()
for index in range(len(randomDelimiters)):
    randomChoiceList.append(index)


# There are multiple types of loops to create arrays - need to abstract them out - examples/codes below main
# Type 1 - range based, join using delimiters, single output array - Inputs -
#   delimiter array
#   pre-delimiter array
#   post-delimiter array
#   range size = length of pre-delimiter array
#   array to append in
def delimitedRangeSingleOutputArrays(begIndex, arrStart, arrDelims, arrFinal):
    endIndex = len(arrStart)
    for index in range(endIndex):
        for count in range(index+1, endIndex):
            for delim in arrDelims:
                tempStr = arrStart[index] + delim + arrStart[count]
                arrFinal.append(tempStr)

def delimitedRangeSingleOutputForMonthsArrays(begIndex, arrStart, arrDelims, arrFinal):
    endIndex = len(arrStart)
    for index in range(0, endIndex, 4):
        for count in range(index+1, endIndex, 4):
            for delim in arrDelims:
                tempStr = arrStart[index] + delim + arrStart[count]
                arrFinal.append(tempStr)

# End Type 1

# Type 2 -

# End Type 2


# Type 3 - append 2 arrays, single output - Inputs -
#   input array 1
#   input array 2
#   output array
def appendTwoSingleOutputArrays(arrStart, arrEnd, arrOut):
    for start in arrStart:
        for end in arrEnd:
            tempStr = start + end
            arrOut.append(tempStr)

# End Type 3


# Type 4 - append element at both sides, multiple outputs - Inputs -
#   element
#   array to append
#   delimiter
#   output array for - appended at start
#   output array for - appended at end
#   output array for - combined appended
def appendBothSidesMultipleOutputs(element, arrayInput, delimiter, arrStartOut, arrEndOut, arrCombOut):
    for entity in arrayInput:
        tempStr = entity + delimiter + element
        arrStartOut.append(tempStr)
        # arrCombOut.append(tempStr)
        tempStr = element + delimiter + entity
        arrEndOut.append(tempStr)
        # arrCombOut.append(tempStr)

# End Type 4


# Type 5 - append two arrays via delimiter, single output - Inputs -
#   start element array
#   end element array
#   delimiters array
#   output array
def appendTwoDelimiterSingleOutputArrays(arrStart, arrEnd, arrDelims, arrFinal):
    for start in arrStart:
        for end in arrEnd:
            for delim in arrDelims:
                tempStr = start + delim + end
                arrFinal.append(tempStr)

# End Type 5


# Type 6 - Write two arrays to file - Inputs -
#   array
#   output filename
def writeArrayToFile(arrayInp, outFile):
    with open(outFile, 'a', encoding='utf-8') as csvoutfile:
        spamwriter = csv.writer(csvoutfile)
        lengthArr = math.floor(len(arrayInp)/10)
        for index in range(10):
            tempArray = []
            for count in range((index)*lengthArr, (index+1) * (lengthArr)):
                tempArray.append(arrayInp[count])
            spamwriter.writerow([tempArray])
    csvoutfile.close()


def writeCompleteArrayToFile(arrayInp, outFile):
    with open(outFile, 'a', encoding='utf-8') as csvoutfile:
        spamwriter = csv.writer(csvoutfile)
        for element in arrayInp:
            spamwriter.writerow([element])
    csvoutfile.close()


def writeThreeArrayLinesToFile(arrayInp, outFile):
    with open(outFile, 'a', encoding='utf-8') as csvoutfile:
        spamwriter = csv.writer(csvoutfile)
        if(len(arrayInp) > 1000000):
            lengthArr = math.floor(len(arrayInp)/5000)
        else:
            lengthArr = math.floor(len(arrayInp)/1000)
        for index in range(0, 200, 103):
            tempArray = []
            for count in range((index)*lengthArr, (index+1) * (lengthArr)):
                tempArray.append(arrayInp[count])
            spamwriter.writerow([tempArray])
    csvoutfile.close()

# End Type 6


# Type 7 - Recursive function for Date followed by Time scenario - Inputs -
# time string
# day array
# output array
def dateBeforeTimeData(time, arrDate, arrFinal):
    for day in arrDate:
        element = dict()
        randomIndex = 0         # random.choice(randomChoiceList)
        delimLength = len(randomDelimiters[randomIndex])
        tempStr = day + randomDelimiters[randomIndex] + time
        dayLength = len(day)
        dateEntity = [0, dayLength, "DATE"]
        timeEntity = [dayLength + delimLength, len(tempStr), "TIME"]  # Take space and comma into account
        element['content'] = tempStr
        element['entities'] = [dateEntity, timeEntity]
        arrFinal.append(element)
        trainingData.append(element)

# End Type 7


# Type 8 - Time followed by Date - Inputs -
#   time string
#   day array
#   output array
def timeBeforeDateData(time, arrDate, arrFinal):
    for day in arrDate:
        element = dict()
        randomIndex = 0         # random.choice(randomChoiceList)
        delimLength = len(randomDelimiters[randomIndex])
        tempStr = time + randomDelimiters[randomIndex] + day
        timeLength = len(time)
        timeEntity = [0, timeLength, "TIME"]
        dateEntity = [timeLength + delimLength, len(tempStr), "DATE"]  # Take space and comma into account
        element['content'] = tempStr
        element['entities'] = [timeEntity, dateEntity]
        arrFinal.append(element)
        trainingData.append(element)

# End Type 8


# Type 9 - time within time - Inputs -
#   content string
#   array of entities
#   input array for time
#   output array
def timePeriodsArray(content, arrEnt, arrInput, arrFinal):
    if(len(arrEnt) == 2):
        # print(content, arrEnt)
        return
    for hour in arrInput:
        element = dict()
        if(hour in content):
            continue
        timeLength = len(hour)
        if(len(content) > 1):
            randomIndex = 0  # random.choice(randomChoiceList)
            delimLength = len(randomDelimiters[randomIndex])
            contentNew = content + randomDelimiters[randomIndex] + hour
            timeEntity = [len(content) + delimLength, len(contentNew), "TIME"]
            arrEnt.append(timeEntity)
            element['content'] = contentNew
            element['entities'] = arrEnt
            arrFinal.append(element)
            trainingData.append(element)
            timePeriodsArray(contentNew, arrEnt, arrInput, arrFinal)
            arrEnt.pop()
        else:
            contentNew = hour
            timeEntity = [0, timeLength, "TIME"]
            arrEnt.append(timeEntity)
            timePeriodsArray(contentNew, arrEnt, arrInput, arrFinal)
            arrEnt.pop()
    return

# End Type 9


# Basic Data
# All month types
monthsSmallLowerArr = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
monthsSmallUpperArr = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
monthsLargeLowerArr = ["january", "february", "march", "april", "may", "june", "july", "august", "september",
                       "october", "november", "december"]
monthsLargeUpperArr = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                       "October", "November", "December"]

# All day types
daysSmallLowerArr = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
daysSmallUpperArr = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
daysLargeLowerArr = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
daysLargeUpperArr = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Exceptions for days
daysLargeLowerSArr = ["mondays", "tuesdays", "wednesdays", "thursdays", "fridays", "saturdays", "sundays"]
daysLargeUpperSArr = ["Mondays", "Tuesdays", "Wednesdays", "Thursdays", "Fridays", "Saturdays", "Sundays"]
dailyArr = ["daily", "Daily", "every day"]      # "everyday", "Everyday", "Every Day"]

delimsArr = ["-"]                             # "to", "To", "TO" are commented out, "–" handled while parsing

# All hour types
morningHoursArr = ["3", "11"]                       # Must be sorted
afternoonHoursArr = ["23"]                    # Must be sorted?
hoursSectionArr = ["5"]                       # Must be sorted

# All section types
morningArr = ["", "am", "AM"]               # "a.m", "am.", "AM.", "A.M", "AM.", "A.M." are commented out
afternoonArr = ["", "pm", "PM"]             # "p.m", "pm.", "P.M", "PM.", "P.M." are commented out

timeCutArr = [":", "."]

minutesArr = ["15"]                     # Must be sorted


#   Cases For Final Training Data
#   a.Day + Time Period Array
#     1. Day Small + Time Hours
#     2. Day Small + Time Sections
#     3. Day Large + Time Hours
#     4. Day Large + Time Sections

#   b.Time Period Array + Day
#     1. Time Hours + Day Small
#     2. Time Sections + Day Small
#     3. Time Hours + Day Large
#     4. Time Sections + Day Large

#   c.Day Type + Time Period Array
#     1. Day Type + Time Hours
#     2. Day Type + Time Sections

#   d.Day Period + Time Period Array
#     1. Day Period Small + Time Hours
#     2. Day Period Small + Time Sections
#     3. Day Period Large + Time Hours
#     4. Day Period Large + Time Sections

#   e.Time Period Array + Day Period
#     1. Time Hours + Day Period Small
#     2. Time Sections + Day Period Small
#     3. Time Hours + Day Period Large
#     4. Time Sections + Day Period Large

#   f.Month Period + Time Period Array
#     1. Month Period Small + Time Hours
#     2. Month Period Small + Time Sections
#     3. Month Period Large + Time Hours
#     4. Month Period Large + Time Sections

#   g. Time Periods Array
#     1. Time Period 1
#     2. Time Period 1 + Time Period 2
#     3. Time Period 1 + Time Period 2 + Time Period 3


# Required Arrays - 2 + 2 + 2 + 2 + 1 = 9
# a. Day - Small Length Days + Large Length Days - won't have large + small in the same page
# b. Day Period - Small Length Days + Large Length Days - - won't have large + small in the same page
# c. Time Period - 2 arrays - Hours Only and Sections Only - since same page won't use 2 different
#    formats at least - within a format, there are possible variations
# d. Month Period - Restrictions - Small Length Months + Large Length Months
# e. Day Type - Restrictions - None
# Large and Small - Specifies length of string
# Upper and Lower - Specifies case of first letter of the string

# Main Arrays - Based on above specifications
allDaysSmall = []
allDaysLarge = []
allDayPeriodsSmall = []
allDayPeriodsLarge = []
allTimesHours = []
allTimesSections = []
allMonthPeriodsSmall = []
allMonthPeriodsLarge = []
allDayTypes = []


def createTrainData(outFile):
    print("Tested")
    # Create Only Time Data
    allDelimsArray = []             # "-", " - ", "- ", " -"    # Others like to, To, etc.
    allMinutesArr = []              # (:,.)(0-59) types
    allMinutesMorningArr = []       # (:,.)(0-59) AM/am types
    allMinutesAfternoonArr = []     # (:,.)(0-59) PM/pm types
    allHoursMorning = []            # eg, 00:00, 8:15, 09:25, 10.30, 11, etc        # Must be sorted
    allHoursAfternoon = []          # eg, 12:15, 13:25, 17.30, 23, etc              # Must be sorted
    allHoursMorningSection = []     # eg, 12:01 AM, 7.10a.m, 9.15 a.m., 11 AM, etc  # Must be sorted
    allHoursAfternoonSection = []   # eg, 12:30pm., 1.25 P.M., 3 PM., etc           # Must be sorted

    # Generate all delimiters
    for delim in delimsArr:
        allDelimsArray.append(delim)
        # allDelimsArray.append(" " + delim)
        # allDelimsArray.append(delim + " ")
        allDelimsArray.append(" " + delim + " ")
    print("Delimiters ", str(len(allDelimsArray)))

    # Generate all minutes - morning, afternoon, hours based - optimized for time
    for timeCut in timeCutArr:
        for minutes in minutesArr:
            tempStr = timeCut + minutes
            allMinutesArr.append(tempStr)
            for section in morningArr:
                tempStr = timeCut + minutes + section
                allMinutesMorningArr.append(tempStr)
            for section in afternoonArr:
                tempStr = timeCut + minutes + section
                allMinutesAfternoonArr.append(tempStr)

    # Generate all Hours only
    # Generate all hours based morning hours
    appendTwoSingleOutputArrays(morningHoursArr, allMinutesArr, allHoursMorning)

    # Generate all hours based afternoon hours
    appendTwoSingleOutputArrays(afternoonHoursArr, allMinutesArr, allHoursAfternoon)

    # Generate all section based morning hours
    appendTwoSingleOutputArrays(hoursSectionArr, allMinutesMorningArr, allHoursMorningSection)

    # Generate all section based afternoon hours
    appendTwoSingleOutputArrays(hoursSectionArr, allMinutesAfternoonArr, allHoursAfternoonSection)

    # Generate Time Periods - Hours Based
    # Generate all morning to morning type - Hours
    delimitedRangeSingleOutputArrays(0, allHoursMorning, allDelimsArray, allTimesHours)

    # Generate all morning to afternoon type - Hours
    appendTwoDelimiterSingleOutputArrays(allHoursMorning, allHoursAfternoon, allDelimsArray, allTimesHours)

    # Generate all afternoon to afternoon type - Hours
    delimitedRangeSingleOutputArrays(0, allHoursAfternoon, allDelimsArray, allTimesHours)

    # Generate Time Periods - Sections Based
    # Generate all morning to morning type - Sections
    delimitedRangeSingleOutputArrays(0, allHoursMorningSection, allDelimsArray, allTimesSections)

    # Generate all morning to afternoon type - Sections
    appendTwoDelimiterSingleOutputArrays(allHoursMorningSection, allHoursAfternoonSection, allDelimsArray,
                                         allTimesSections)

    # Generate all afternoon to afternoon type - Sections
    delimitedRangeSingleOutputArrays(0, allHoursAfternoonSection, allDelimsArray, allTimesSections)

#    writeArrayToFile(allTimesHours, outFile)
#    writeArrayToFile(allTimesSections, outFile)
    print("All Time Hours ", str(len(allTimesHours)))
    print("All Time Sections ", str(len(allTimesSections)))

    # Create Only Days, Day Types and Day Periods Data
    # Generate all day types
    for day in daysLargeLowerSArr:
        allDayTypes.append(day)
    for day in daysLargeUpperSArr:
        allDayTypes.append(day)
    for day in dailyArr:
        allDayTypes.append(day)
    print("Day Types ", str(len(allDayTypes)))

    # Generate all days only - Small
    for index in range(len(daysSmallLowerArr)):
        allDaysSmall.append(daysSmallLowerArr[index])
        allDaysSmall.append(daysSmallUpperArr[index])

    # Generate all day periods only - Small
    delimitedRangeSingleOutputArrays(0, daysSmallLowerArr, allDelimsArray, allDayPeriodsSmall)
    delimitedRangeSingleOutputArrays(0, daysSmallUpperArr, allDelimsArray, allDayPeriodsSmall)

    # Generate all days only - Large
    for index in range(len(daysLargeLowerArr)):
        allDaysLarge.append(daysLargeLowerArr[index])
        allDaysLarge.append(daysLargeUpperArr[index])

    # Generate all day periods only - Large
    delimitedRangeSingleOutputArrays(0, daysLargeLowerArr, allDelimsArray, allDayPeriodsLarge)
    delimitedRangeSingleOutputArrays(0, daysLargeUpperArr, allDelimsArray, allDayPeriodsLarge)

#    writeArrayToFile(allDaysSmall, outFile)
#    writeArrayToFile(allDaysLarge, outFile)
#    writeArrayToFile(allDayPeriodsSmall, outFile)
#    writeArrayToFile(allDayPeriodsLarge, outFile)
    print("All Days Small ", str(len(allDaysSmall)))
    print("All Days Large ", str(len(allDaysLarge)))
    print("All Day Periods Small ", str(len(allDayPeriodsSmall)))
    print("All Day Periods Large ", str(len(allDayPeriodsLarge)))

    # Create Only Months Data
    allMonthsSmallLowerBeg = []         # month date
    allMonthsSmallUpperBeg = []         # month date
    allMonthsLargeLowerBeg = []         # month date
    allMonthsLargeUpperBeg = []         # month date
    allMonthsSmallLowerEnd = []         # date month
    allMonthsSmallUpperEnd = []         # date month
    allMonthsLargeLowerEnd = []         # date month
    allMonthsLargeUpperEnd = []         # date month

    for hours in hoursSectionArr:
        appendBothSidesMultipleOutputs(hours, monthsSmallLowerArr, " ", allMonthsSmallLowerBeg,
                                       allMonthsSmallLowerEnd, allMonthPeriodsSmall)        # 11 sep, nov 5
        appendBothSidesMultipleOutputs(hours, monthsSmallUpperArr, " ", allMonthsSmallUpperBeg,
                                       allMonthsSmallUpperEnd, allMonthPeriodsSmall)        # 11 Sep, Nov 5
        appendBothSidesMultipleOutputs(hours, monthsLargeLowerArr, " ", allMonthsLargeLowerBeg,
                                       allMonthsLargeLowerEnd, allMonthPeriodsLarge)        # 11 september, november 5
        appendBothSidesMultipleOutputs(hours, monthsLargeUpperArr, " ", allMonthsLargeUpperBeg,
                                       allMonthsLargeUpperEnd, allMonthPeriodsLarge)        # 11 September, November 5

    allMonthArrayTypes = [allMonthsSmallLowerBeg, allMonthsSmallLowerEnd, allMonthsSmallUpperBeg, allMonthsSmallUpperEnd,
                          allMonthsLargeLowerBeg, allMonthsLargeLowerEnd, allMonthsLargeUpperBeg, allMonthsLargeUpperEnd]

    count = 0
    for monthType in allMonthArrayTypes:
        if(count < 4):
            delimitedRangeSingleOutputForMonthsArrays(0, monthType, allDelimsArray, allMonthPeriodsSmall)
        else:
            delimitedRangeSingleOutputForMonthsArrays(0, monthType, allDelimsArray, allMonthPeriodsLarge)
        count = count + 1

#    writeArrayToFile(allMonthPeriodsSmall, outFile)
#    writeArrayToFile(allMonthPeriodsLarge, outFile)
    print("All Month Periods Small ", str(len(allMonthPeriodsSmall)))
    print("All Month Periods Large ", str(len(allMonthPeriodsLarge)))

#   Spacy Training Sample
#   {"content":"1 November to 12 December, 10:30 AM - 12:30 PM","entities":[[0,25,"DATE"], [27,46,"TIME"]]}

    trainingDataCaseA = list()
    trainingDataCaseB = list()
    trainingDataCaseC = list()
    trainingDataCaseD = list()
    trainingDataCaseE = list()
    trainingDataCaseF = list()
    trainingDataCaseG = list()

    allDayArrayTypes = [allDaysSmall, allDaysLarge, allDayPeriodsSmall, allDayPeriodsLarge]
    allDayTrainingData = [trainingDataCaseA, trainingDataCaseB, trainingDataCaseD, trainingDataCaseE]

    print("Creating Day Training Data")

    for hour in allTimesHours:
        count = 0
        for dayTypeArray in allDayArrayTypes:
            if(count < 2):
                dateBeforeTimeData(hour, dayTypeArray, allDayTrainingData[0])    # [int(count/2)])
                timeBeforeDateData(hour, dayTypeArray, allDayTrainingData[1])    # [int(count/2)+1])
            else:
                dateBeforeTimeData(hour, dayTypeArray, allDayTrainingData[2])    # int(count/2)+1])
                timeBeforeDateData(hour, dayTypeArray, allDayTrainingData[3])    # int(count/2)+2])
            count = count + 1
        # Case (c).(1)
        dateBeforeTimeData(hour, allDayTypes, trainingDataCaseC)
        # Case (f).(1)
        dateBeforeTimeData(hour, allMonthPeriodsSmall, trainingDataCaseF)
        # Case (f).(3)
        dateBeforeTimeData(hour, allMonthPeriodsLarge, trainingDataCaseF)

    print("Training Data Case F Before Sections : ", str(len(trainingDataCaseF)))

    print("Created Day Training Data Hours")

    for hour in allTimesSections:
        count = 0
        for dayTypeArray in allDayArrayTypes:
            if(count < 2):
                dateBeforeTimeData(hour, dayTypeArray, allDayTrainingData[0])   # [int(count/2)])
                timeBeforeDateData(hour, dayTypeArray, allDayTrainingData[1])   # [int(count/2)+1])
            else:
                dateBeforeTimeData(hour, dayTypeArray, allDayTrainingData[2])   # [int(count/2)+1])
                timeBeforeDateData(hour, dayTypeArray, allDayTrainingData[3])   # [int(count/2)+2])
            count = count + 1
        # Case (c).(2)
        dateBeforeTimeData(hour, allDayTypes, trainingDataCaseC)
        # Case (f).(2)
        dateBeforeTimeData(hour, allMonthPeriodsSmall, trainingDataCaseF)
        # Case (f).(4)
        dateBeforeTimeData(hour, allMonthPeriodsLarge, trainingDataCaseF)

    print("Created Day Training Data Sections, Writing To File")

    '''
    writeThreeArrayLinesToFile(trainingDataCaseA, outFile)
    writeThreeArrayLinesToFile(trainingDataCaseB, outFile)
    writeThreeArrayLinesToFile(trainingDataCaseC, outFile)
    writeThreeArrayLinesToFile(trainingDataCaseD, outFile)
    writeThreeArrayLinesToFile(trainingDataCaseE, outFile)
    writeThreeArrayLinesToFile(trainingDataCaseF, outFile)
    '''

    print("Training Data Case A : ", str(len(trainingDataCaseA)))
    print("Training Data Case B : ", str(len(trainingDataCaseB)))
    print("Training Data Case C : ", str(len(trainingDataCaseC)))
    print("Training Data Case D : ", str(len(trainingDataCaseD)))
    print("Training Data Case E : ", str(len(trainingDataCaseE)))
    print("Training Data Case F : ", str(len(trainingDataCaseF)))

    print("Training Data Before Time Period ", str(len(trainingData)))

    print("Written to File, Creating Time Data")

    # timePeriodsArray("", [], allTimesHours, trainingDataCaseG)

    print("Completed Hours Time Periods")

    # timePeriodsArray("", [], allTimesSections, trainingDataCaseG)

    print("Completed Sections Time Periods, Writing To File")

    # print(trainingData)
    writeCompleteArrayToFile(trainingData, outFile)
    print("Training Data ", str(len(trainingData)))


if __name__ == "__main__":
    print("Testing")
    outFile = sys.argv[1]
    createTrainData(outFile)

'''
For DATE
from day month to day month
from month day to month day
from day to day
day to day
day - short/long
daily/everyday

For Time
from hours to hours
from hours section to hours section
from hours to hours section
hours to hours
hours section to hours
hours to hours section

from 1 november to 31 march 10.30 - 16.30 (Ticket Office 10.30 AM - 4.00 PM
1.30-5.30pm Mon, 9.30am-5.30pm Tuesday-Sat, 9.30am-1.30pm Sun
'''

# Examples for Array Types -
# Type 1 -
''' Example
# Generate all afternoon to afternoon type - Hours
for index in range(0, len(allHoursAfternoon) - 1):
    for count in range(index + 1, (len(allHoursAfternoon) - 1)):
        for delim in allDelimsArray:
            tempStr = allHoursAfternoon[index] + delim + allHoursAfternoon[count]
            print(tempStr)
            allTimesHours.append(tempStr)
'''
# End Type 1

# Type 2
''' Example
for timeCut in timeCutArr:
    for minutes in minutesArr:
        tempStr = timeCut + minutes
        allMinutesArr.append(tempStr)
        for section in morningArr:
            tempStr = timeCut + minutes + section
            allMinutesMorningArr.append(tempStr)
'''
# End Type 2

# Type 3
''' Example
for hours in afternoonHoursArr:
    for minutes in allMinutesArr:
        tempStr = hours + minutes
        allHoursAfternoon.append(tempStr)
'''
# End Type 3

# Type 4
''' Example
for hours in hoursSectionArr:
    # 11 sep, Nov 5
    for months in monthsSmallLowerArr:
        tempStr = months + " " + hours
        allMonthsSmallLowerBeg.append(tempStr)
        # Generate all month periods - Small
        allMonthPeriodsSmall.append(tempStr)
        tempStr = hours + " " + months
        allMonthsSmallLowerEnd.append(tempStr)
        # Generate all month periods - Small
        allMonthPeriodsSmall.append(tempStr)
'''
# End Type 4

# Type 5
''' Example
for index in range(0, len(allHoursMorning) - 1):
    for count in range(0, (len(allHoursAfternoon) - 1)):
        for delim in allDelimsArray:
            tempStr = allHoursMorning[index] + delim + allHoursAfternoon[count]
            print(tempStr)
            allTimesHours.append(tempStr)
'''
# End Type 5

# Type 6
''' Example
with open(outFile, 'w', encoding='utf-8') as csvoutfile:
    spamwriter = csv.writer(csvoutfile)
    lengthArr = math.floor(len(allTimesHours)/10)
    print(len(allTimesHours))
    print(lengthArr)
    for index in range(10):
        tempArray = []
        for count in range((index)*lengthArr, (index+1) * (lengthArr)):
            tempArray.append(allTimesHours[count])
        spamwriter.writerow([tempArray])
    lengthArr = math.floor((len(allTimesSections)/10))
csvoutfile.close()
'''
# End Type 6

# Type 7
''' Example
# Case (d).(3)
for day in allDayPeriodsLarge:
    tempStr = day + ", " + hour
    dayLength = len(day)
    dateEntity = [0, dayLength, "DATE"]
    timeEntity = [dayLength + 2, len(tempStr), "TIME"]  # Take space and comma into account
    element['content'] = tempStr
    element['entities'] = [dateEntity, timeEntity]
    trainingDataCaseD.append(element)
'''
# End Type 7

# Type 8
''' Example
# Case (e).(1)
for day in allDayPeriodsSmall:
    tempStr = hour + ", " + day
    hourLength = len(hour)
    timeEntity = [0, hourLength, "TIME"]
    dateEntity = [hourLength + 2, len(tempStr), "DATE"]  # Take space and comma into account
    element['content'] = tempStr
    element['entities'] = [timeEntity, dateEntity]
    trainingDataCaseE.append(element)
'''
# End Type 8

# Type 9
''' Example    
for hour in allTimesHours:
    element = dict()
    timeLength = len(hour)
    element['content'] = hour
    timeEntityOne = [0, timeLength, "TIME"]
    element['entities'] = [timeEntityOne]
    trainingDataCaseG.append(element)
    trainingData.append(element)
    for hourTwo in allTimesHours:
        if(hourTwo == hour):
            continue
        randomIndexTwo = random.choice(randomChoiceList)
        delimLengthTwo = len(randomDelimiters[randomIndexTwo])
        contentTwo = hour + randomDelimiters[randomIndexTwo] + hourTwo
        element['content'] = contentTwo
        timeEntityTwo = [timeLength + delimLengthTwo, len(contentTwo), "TIME"]
        element['entities'] = [timeEntityOne, timeEntityTwo]
        trainingDataCaseG.append(element)
        trainingData.append(element)
        for hourThree in allTimesHours:
            if ( (hourThree == hour) or (hourThree == hourTwo) ):
                continue
            randomIndexThree = random.choice(randomChoiceList)
            delimLengthThree = len(randomDelimiters[randomIndexThree])
            contentThree = contentTwo + randomDelimiters[randomIndexThree] + hourThree
            element['content'] = contentThree
            timeEntityThree = [len(contentTwo) + delimLengthThree, len(contentThree), "TIME"]
            element['entities'] = [timeEntityOne, timeEntityTwo, timeEntityThree]
            trainingDataCaseG.append(element)
'''
# End Type 9


# Residual Codes

    # Generate all hours based morning hours
#    for hours in morningHoursArr:
#        for minutes in allMinutesArr:
#            tempStr = hours + minutes
#            allHoursMorning.append(tempStr)

    # Generate all hours based afternoon hours
#    for hours in afternoonHoursArr:
#        for minutes in allMinutesArr:
#            tempStr = hours + minutes
#            allHoursAfternoon.append(tempStr)

    # Generate all section based morning and afternoon hours - Optimized for time
#    for hours in hoursSectionArr:
#        for minutes in allMinutesMorningArr:
#            tempStr = hours + minutes
#            allHoursMorningSection.append(tempStr)

    # Generate all section based morning and afternoon hours - Optimized for time
#    for hours in hoursSectionArr:
#        for minutes in allMinutesAfternoonArr:
#            tempStr = hours + minutes
#            allHoursAfternoonSection.append(tempStr)

        # 11 sep, nov 5
#        for months in monthsSmallLowerArr:
#            tempStr = months + " " + hours
#            allMonthsSmallLowerBeg.append(tempStr)
            # Generate all month periods - Small
#            allMonthPeriodsSmall.append(tempStr)
#            tempStr = hours + " " + months
#            allMonthsSmallLowerEnd.append(tempStr)
            # Generate all month periods - Small
#            allMonthPeriodsSmall.append(tempStr)

        # 11 Sep, Nov 5
#        for months in monthsSmallUpperArr:
#            tempStr = months + " " + hours
#            allMonthsSmallUpperBeg.append(tempStr)
            # Generate all month periods - Small
#            allMonthPeriodsSmall.append(tempStr)
#            tempStr = hours + " " + months
#            allMonthsSmallUpperEnd.append(tempStr)
            # Generate all month periods - Small
#            allMonthPeriodsSmall.append(tempStr)

        # 11 september, november 5
#        for months in monthsLargeLowerArr:
#            tempStr = months + " " + hours
#            allMonthsLargeLowerBeg.append(tempStr)
            # Generate all month periods - Large
#            allMonthPeriodsLarge.append(tempStr)
#            tempStr = hours + " " + months
#            allMonthsLargeLowerEnd.append(tempStr)
            # Generate all month periods - Large
#            allMonthPeriodsLarge.append(tempStr)

        # 11 September, November 5
#        for months in monthsLargeUpperArr:
#            tempStr = months + " " + hours
#            allMonthsLargeUpperBeg.append(tempStr)
            # Generate all month periods - Large
#            allMonthPeriodsLarge.append(tempStr)
#            tempStr = hours + " " + months
#            allMonthsLargeUpperEnd.append(tempStr)
            # Generate all month periods - Large
#            allMonthPeriodsLarge.append(tempStr)

    # Generate all morning to morning type - Hours
#    for index in range(0, len(allHoursMorning) - 1):
#        for count in range(index + 1, (len(allHoursMorning) - 1)):
#            for delim in allDelimsArray:
#                tempStr = allHoursMorning[index] + delim + allHoursMorning[count]
                # print(tempStr)
#                allTimesHours.append(tempStr)

    # Generate all morning to afternoon type - Hours
#    for index in range(0, len(allHoursMorning) - 1):
#        for count in range(0, (len(allHoursAfternoon) - 1)):
#            for delim in allDelimsArray:
#                tempStr = allHoursMorning[index] + delim + allHoursAfternoon[count]
                # print(tempStr)
#                allTimesHours.append(tempStr)

    # Generate all afternoon to afternoon type - Hours
#    for index in range(0, len(allHoursAfternoon) - 1):
#        for count in range(index + 1, (len(allHoursAfternoon) - 1)):
#            for delim in allDelimsArray:
#                tempStr = allHoursAfternoon[index] + delim + allHoursAfternoon[count]
                # print(tempStr)
#                allTimesHours.append(tempStr)

    # Generate all morning to morning type - Sections
#    for index in range(0, len(allHoursMorningSection) - 1):
#        for count in range(index + 1, (len(allHoursMorningSection) - 1)):
#            for delim in allDelimsArray:
#                tempStr = allHoursMorningSection[index] + delim + allHoursMorningSection[count]
                # print(tempStr)
#                allTimesSections.append(tempStr)

    # Generate all morning to afternoon type - Sections
#    for index in range(0, len(allHoursMorningSection) - 1):
#        for count in range(0, (len(allHoursAfternoonSection) - 1)):
#            for delim in allDelimsArray:
#                tempStr = allHoursMorningSection[index] + delim + allHoursAfternoonSection[count]
                # print(tempStr)
#                allTimesSections.append(tempStr)

    # Generate all afternoon to afternoon type - Sections
#    for index in range(0, len(allHoursAfternoonSection) - 1):
#        for count in range(index + 1, (len(allHoursAfternoonSection) - 1)):
#            for delim in allDelimsArray:
#                tempStr = allHoursAfternoonSection[index] + delim + allHoursAfternoonSection[count]
                # print(tempStr)
#                allTimesSections.append(tempStr)

#    for index in range(len(daysSmallLowerArr) - 1):
#        for count in range(index+1, (len(daysSmallLowerArr)-1)):
#            for delim in allDelimsArray:
#                tempStr = daysSmallLowerArr[index] + delim + daysSmallLowerArr[count]
#                allDays.append(tempStr)
                # Generate all day periods only - Small
#                allDayPeriodsSmall.append(tempStr)
#                tempStr = daysSmallUpperArr[index] + delim + daysSmallUpperArr[count]
#                allDays.append(tempStr)
                # Generate all day periods only - Small
#                allDayPeriodsSmall.append(tempStr)

#    for index in range(len(daysLargeLowerArr) - 1):
#        for count in range(index+1, (len(daysLargeLowerArr)-1)):
#            for delim in allDelimsArray:
#                tempStr = daysLargeLowerArr[index] + delim + daysLargeLowerArr[count]
#                allDays.append(tempStr)
                # Generate all day periods only - Large
#                allDayPeriodsLarge.append(tempStr)
#                tempStr = daysLargeUpperArr[index] + delim + daysLargeUpperArr[count]
#                allDays.append(tempStr)
                # Generate all day periods only - Large
#                allDayPeriodsLarge.append(tempStr)

# Months in Small
# Months in Small - lower + beg
'''
delimitedRangeSingleOutputArrays(0, allMonthsSmallLowerBeg, allDelimsArray, allMonthPeriodsSmall)

# Months in Small - upper + beg
delimitedRangeSingleOutputArrays(0, allMonthsSmallUpperBeg, allDelimsArray, allMonthPeriodsSmall)

# Months in Small - lower + end
delimitedRangeSingleOutputArrays(0, allMonthsSmallLowerEnd, allDelimsArray, allMonthPeriodsSmall)

# Months in Small - upper + end
delimitedRangeSingleOutputArrays(0, allMonthsSmallUpperEnd, allDelimsArray, allMonthPeriodsSmall)

# Months in Large
# Months in Large - lower + beg
delimitedRangeSingleOutputArrays(0, allMonthsLargeLowerBeg, allDelimsArray, allMonthPeriodsLarge)

# Months in Large - upper + beg
delimitedRangeSingleOutputArrays(0, allMonthsLargeUpperBeg, allDelimsArray, allMonthPeriodsLarge)

# Months in Large - lower + end
delimitedRangeSingleOutputArrays(0, allMonthsLargeLowerEnd, allDelimsArray, allMonthPeriodsLarge)

# Months in Large - upper + end
delimitedRangeSingleOutputArrays(0, allMonthsLargeUpperEnd, allDelimsArray, allMonthPeriodsLarge)
'''

# Months in Small - lower + beg
#    for index in range(len(allMonthsSmallLowerBeg)-1):
#        for count in range(index + 1, (len(allMonthsSmallLowerBeg) - 1)):
#            for delim in allDelimsArray:
#                tempStr = allMonthsSmallLowerBeg[index] + delim + allMonthsSmallLowerBeg[count]
#                allMonths.append(tempStr)
                # Month Periods in Small
#                allMonthPeriodsSmall.append(tempStr)

    # Months in Small - upper + beg
#    for index in range(len(allMonthsSmallUpperBeg)-1):
#        for count in range(index + 1, (len(allMonthsSmallUpperBeg) - 1)):
#            for delim in allDelimsArray:
#                tempStr = allMonthsSmallUpperBeg[index] + delim + allMonthsSmallUpperBeg[count]
#                allMonths.append(tempStr)
                # Month Periods in Small
#                allMonthPeriodsSmall.append(tempStr)

    # Months in Small - lower + end
#    for index in range(len(allMonthsSmallLowerEnd) - 1):
#        for count in range(index + 1, (len(allMonthsSmallLowerEnd) - 1)):
#            for delim in allDelimsArray:
#                tempStr = allMonthsSmallLowerEnd[index] + delim + allMonthsSmallLowerEnd[count]
#                allMonths.append(tempStr)
                # Month Periods in Small
#                allMonthPeriodsSmall.append(tempStr)

    # Months in Small - upper + end
#    for index in range(len(allMonthsSmallUpperEnd) - 1):
#        for count in range(index + 1, (len(allMonthsSmallUpperEnd) - 1)):
#            for delim in allDelimsArray:
#                tempStr = allMonthsSmallUpperEnd[index] + delim + allMonthsSmallUpperEnd[count]
#                allMonths.append(tempStr)
                # Month Periods in Small
#                allMonthPeriodsSmall.append(tempStr)

    # Months in Large - lower + beg
#    for index in range(len(allMonthsLargeLowerBeg) - 1):
#        for count in range(index + 1, (len(allMonthsLargeLowerBeg) - 1)):
#            for delim in allDelimsArray:
#                tempStr = allMonthsLargeLowerBeg[index] + delim + allMonthsLargeLowerBeg[count]
#                allMonths.append(tempStr)
                # Month Periods in Large
#                allMonthPeriodsLarge.append(tempStr)

    # Months in Large - upper + beg
#    for index in range(len(allMonthsLargeUpperBeg) - 1):
#        for count in range(index + 1, (len(allMonthsLargeUpperBeg) - 1)):
#            for delim in allDelimsArray:
#                tempStr = allMonthsLargeUpperBeg[index] + delim + allMonthsLargeUpperBeg[count]
#                allMonths.append(tempStr)
                # Month Periods in Large
#                allMonthPeriodsLarge.append(tempStr)

    # Months in Large - lower + end
#    for index in range(len(allMonthsLargeLowerEnd) - 1):
#        for count in range(index + 1, (len(allMonthsLargeLowerEnd) - 1)):
#            for delim in allDelimsArray:
#                tempStr = allMonthsLargeLowerEnd[index] + delim + allMonthsLargeLowerEnd[count]
#                allMonths.append(tempStr)
                # Month Periods in Large
#                allMonthPeriodsLarge.append(tempStr)

    # Months in Large - upper + end
#    for index in range(len(allMonthsLargeUpperEnd) - 1):
#        for count in range(index + 1, (len(allMonthsLargeUpperEnd) - 1)):
#            for delim in allDelimsArray:
#                tempStr = allMonthsLargeUpperEnd[index] + delim + allMonthsLargeUpperEnd[count]
#                allMonths.append(tempStr)
                # Month Periods in Large
#                allMonthPeriodsLarge.append(tempStr)

'''            
for hour in allTimesHours:
    # Case (a).(1)
    dateBeforeTimeData(hour, allDaysSmall, trainingDataCaseA)
    # Case (a).(3)
    dateBeforeTimeData(hour, allDaysLarge, trainingDataCaseA)
    # Case (b).(1)
    timeBeforeDateData(hour, allDaysSmall, trainingDataCaseB)
    # Case (b).(3)
    timeBeforeDateData(hour, allDaysLarge, trainingDataCaseB)
    # Case (c).(1)
    dateBeforeTimeData(hour, allDayTypes, trainingDataCaseC)
    # Case (d).(1)
    dateBeforeTimeData(hour, allDayPeriodsSmall, trainingDataCaseD)
    # Case (d).(3)
    dateBeforeTimeData(hour, allDayPeriodsLarge, trainingDataCaseD)
    # Case (e).(1)
    timeBeforeDateData(hour, allDayPeriodsSmall, trainingDataCaseE)
    # Case (e).(3)
    timeBeforeDateData(hour, allDayPeriodsLarge, trainingDataCaseE)
    # Case (f).(1)
    dateBeforeTimeData(hour, allMonthPeriodsSmall, trainingDataCaseF)
    # Case (f).(3)
    dateBeforeTimeData(hour, allMonthPeriodsLarge, trainingDataCaseF)
'''

'''            
for hour in allTimesSections:
    # Case (a).(2)
    dateBeforeTimeData(hour, allDaysSmall, trainingDataCaseA)
    # Case (a).(4)
    dateBeforeTimeData(hour, allDaysLarge, trainingDataCaseA)
    # Case (b).(2)
    timeBeforeDateData(hour, allDaysSmall, trainingDataCaseB)
    # Case (b).(4)
    timeBeforeDateData(hour, allDaysLarge, trainingDataCaseB)
    # Case (c).(2)
    dateBeforeTimeData(hour, allDayTypes, trainingDataCaseC)
    # Case (d).(2)
    dateBeforeTimeData(hour, allDayPeriodsSmall, trainingDataCaseD)
    # Case (d).(4)
    dateBeforeTimeData(hour, allDayPeriodsLarge, trainingDataCaseD)
    # Case (e).(2)
    timeBeforeDateData(hour, allDayPeriodsSmall, trainingDataCaseE)
    # Case (e).(4)
    timeBeforeDateData(hour, allDayPeriodsLarge, trainingDataCaseE)
    # Case (f).(2)
    dateBeforeTimeData(hour, allMonthPeriodsSmall, trainingDataCaseF)
    # Case (f).(4)
    dateBeforeTimeData(hour, allMonthPeriodsLarge, trainingDataCaseF)
'''

'''    
for hour in allTimesHours:
    element = dict()
    timeLength = len(hour)
    element['content'] = hour
    timeEntityOne = [0, timeLength, "TIME"]
    element['entities'] = [timeEntityOne]
    trainingDataCaseG.append(element)
    trainingData.append(element)
    for hourTwo in allTimesHours:
        if(hourTwo == hour):
            continue
        randomIndexTwo = random.choice(randomChoiceList)
        delimLengthTwo = len(randomDelimiters[randomIndexTwo])
        contentTwo = hour + randomDelimiters[randomIndexTwo] + hourTwo
        element['content'] = contentTwo
        timeEntityTwo = [timeLength + delimLengthTwo, len(contentTwo), "TIME"]
        element['entities'] = [timeEntityOne, timeEntityTwo]
        trainingDataCaseG.append(element)
        trainingData.append(element)
        for hourThree in allTimesHours:
            if ( (hourThree == hour) or (hourThree == hourTwo) ):
                continue
            randomIndexThree = random.choice(randomChoiceList)
            delimLengthThree = len(randomDelimiters[randomIndexThree])
            contentThree = contentTwo + randomDelimiters[randomIndexThree] + hourThree
            element['content'] = contentThree
            timeEntityThree = [len(contentTwo) + delimLengthThree, len(contentThree), "TIME"]
            element['entities'] = [timeEntityOne, timeEntityTwo, timeEntityThree]
            trainingDataCaseG.append(element)
'''
