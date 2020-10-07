#!/usr/bin/python

import sys, getopt, xml.etree.ElementTree as ET, datetime


def main(argv):
    # parsing arguments
    input_file = ''
    channel_id = ''
    channel_ids = []
    separation = ''
    lang = ''
    try:
        opts, args = getopt.getopt(argv, "hc:i:s:l:", ["ifile=", "channelid=", "separation="])
    except getopt.GetoptError:
        print('XMLTVExportParser.py -i <inputFile> -c <channelId> -s <max separation seconds>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('XMLTVExportParser.py -i <inputFile> -c <channelId> -s <max separation seconds>')
            sys.exit()
        if opt in '-l':
            lang = arg
        elif opt in ("-i", "--ifile", "--inputfile", "--inputFile"):
            input_file = arg
        elif opt in ("-c", "--channelId", "--channelId"):
            channel_id = arg
        elif opt in ("-s", "--separation"):
            separation = int(arg)
        else:
            print("unhandled option")
            sys.exit(2)
    print("---    arguments    ---")
    print("inputFile:", input_file)
    print("channelId:", channel_id)
    print("separation:", separation)
    print("lang:", lang)
    print("--- start analyzing ---")

    if lang == '':
        lang = 'fi'  # defaults to fi

    # parse xml root and get programmes for selected channel, and sort to make sure those are in correct order
    xml_root = ET.parse(input_file).getroot()
    if channel_id == '':
        for channel in xml_root.findall("channel"):
            channel_ids.append(int(channel.attrib['id']))
    else:
        channel_ids.append(channel_id)

    for channelIdToAnalyze in channel_ids:
        analyze_channel_id(xml_root, channelIdToAnalyze, separation, lang)


def analyze_channel_id(xmlRoot, channelId, separation, lang):
    programmes = xmlRoot.findall("programme[@channel='%s']" % channelId)
    start_times = []
    for program in programmes:
        start_time = program.attrib['start']
        start_times.append((start_time, program))
    # assumes there are no duplicate start times
    start_times.sort()
    programmes[:] = [item[-1] for item in start_times]

    for i, j in enumerate(programmes[:-1]):
        # i is current index and j is current element in loop
        try:
            current_start = datetime.datetime.strptime(j.attrib['start'], '%Y%m%d%H%M%S')
            current_stop = datetime.datetime.strptime(j.attrib['stop'], '%Y%m%d%H%M%S')
            current_title = (j.find("title"), j.find("title[@lang='%s']" % lang))[
                j.find("title[@lang='%s']" % lang) is not None].text
        except AttributeError:
            print("channelId:", channelId, 'Current analyzed program missing necessary information:', ET.tostring(j))
            continue
        try:
            next_program = programmes[i + 1]
            next_start = datetime.datetime.strptime(next_program.attrib['start'], '%Y%m%d%H%M%S')
            next_stop = datetime.datetime.strptime(next_program.attrib['stop'], '%Y%m%d%H%M%S')
            next_title = (next_program.find("title"), next_program.find("title[@lang='%s']" % lang))[
                next_program.find("title[@lang='%s']" % lang) is not None].text
        except AttributeError:
            print("channelId:", channelId, 'Next analyzed program missing necessary information:', ET.tostring(next_program))
            continue

        current_max_stop = current_stop + datetime.timedelta(0, separation)
        if current_max_stop < next_start:
            print('channelId:', channelId,
                  '| separation:', next_start - current_stop,
                  '| Program:', current_title, '(', current_start, '-', current_stop, ')',
                  '| Next program:', next_title, '(', next_start, '-', next_stop, ')')


if __name__ == "__main__":
    main(sys.argv[1:])
