#!/usr/bin/python

import sys, getopt, xml.etree.ElementTree as ET, datetime

def main(argv):
    # parsing arguments
    inputFile = ''
    channelId = ''
    channelIds = []
    separation = ''
    try:
        opts, args = getopt.getopt(argv, "hc:i:s:", ["ifile=", "channelid=","separation="])
    except getopt.GetoptError:
        print('XMLTVExportParser.py -i <inputFile> -c <channelId> -s <max separation seconds>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('XMLTVExportParser.py -i <inputFile> -c <channelId> -s <max separation seconds>')
            sys.exit()
        elif opt in ("-i", "--ifile", "--inputfile", "--inputFile"):
            inputFile = arg
        elif opt in ("-c", "--channelId", "--channelId"):
            channelId = arg
        elif opt in ("-s", "--separation"):
            separation = int(arg)
        else:
            print("unhandled option")
            sys.exit(2)
    print("---    arguments    ---")
    print("inputFile:", inputFile)
    print("channelId:", channelId)
    print("separation:", separation)
    print("--- start analyzing ---")

    # parse xml root and get programmes for selected channel, and sort to make sure those are in correct order
    xmlRoot = ET.parse(inputFile).getroot()
    if channelId == '':
        for channel in xmlRoot.findall("channel"):
            channelIds.append(int(channel.attrib['id']))
    else:
        channelIds.append(channelId)

    for channelIdToAnalyze in channelIds:
        analyzeChannelId(xmlRoot, channelIdToAnalyze, separation)

def analyzeChannelId(xmlRoot, channelId, separation):
    # print("channelId:", channelId, "being analyzed")
    programmes = xmlRoot.findall("programme[@channel='%s']" % channelId)
    startTimes = []
    for program in programmes:
        startTime = program.attrib['start']
        startTimes.append((startTime, program))
    # assumes there are no duplicate start times
    startTimes.sort()
    programmes[:] = [item[-1] for item in startTimes]

    for i, j in enumerate(programmes[:-1]):
        # i is current index and j is current element in loop
        try:
            currentStart = datetime.datetime.strptime(j.attrib['start'], '%Y%m%d%H%M%S')
            currentStop = datetime.datetime.strptime(j.attrib['stop'], '%Y%m%d%H%M%S')
            currentTitle = (j.find("title"), j.find("title[@lang='fi']"))[j.find("title[@lang='fi']") != None].text
        except AttributeError:
            print("channelId:", channelId, 'Current analyzed program missing necessary information:', ET.tostring(j))
            continue
        try:
            next = programmes[i+1]
            nextStart = datetime.datetime.strptime(next.attrib['start'], '%Y%m%d%H%M%S')
            nextStop = datetime.datetime.strptime(next.attrib['stop'], '%Y%m%d%H%M%S')
            nextTitle = (next.find("title"), next.find("title[@lang='fi']"))[next.find("title[@lang='fi']") != None].text
        except AttributeError:
            print("channelId:", channelId, 'Next analyzed program missing necessary information:', ET.tostring(next))
            continue

        currentMaxStop = currentStop + datetime.timedelta(0, separation)
        if currentMaxStop < nextStart:
            print('channelId:', channelId, 'Programs', currentTitle, '[', currentStart,'-',currentStop,'] and',nextTitle,'[',nextStart,'-',nextStop,'] have too large separation (', nextStart - currentStop, ')')

    print("channelId:", channelId, "analyzed")


if __name__ == "__main__":
    main(sys.argv[1:])





