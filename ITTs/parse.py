import csv
import uuid

csvfile1 = open('output/indicators.csv', 'wb')
indicators = csv.writer(csvfile1, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
indicators.writerow(["country", "project", "subproject", "submission_date", "activity", "subactivity", "indicator_id", "indicator_level", "indicator", "classification", "unit", "baseline", "actual_to_date", "end_of_compact_target", "percent_complete_to_date", "notes"])


csvfile2 = open('output/indicator_details.csv', 'wb')
indicator_details = csv.writer(csvfile2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
indicator_details.writerow(["indicator_id", "compact_year", "timeframe", "q1", "q2", "q3", "q4", "yearly_target", "percent_complete"])


def parse(filename):

    yearly = {}

    with open(filename, 'rU') as csvfile:
        subproject = filename.split("_")[1]
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

        country = ""
        project = ""
        subproject = ""
        submission_date = ""
        activity = "All Activities"
        subactivity = "N/A"

        indicator_num = 0

        for (i, row) in enumerate(spamreader):
            #print row
            if i == 1:
                country = row[1].strip()
            if i == 2:
                project = row[1].strip()
            if i == 3:
                submission_date = row[0].split(":")[1].strip()
                #parse compact year
                for year in range(1, 6):
                    yearly[str(year)] = {}

            if i == 4:
                #parse timeframes for compact years
                for year in range(1, 6):
                    yearly[str(year)]["timeframe"] = row[4+year].strip()

            if i > 7:
                #print len(''.join(row)), row[0]
                #skip short row
                if len(''.join(row)) < 10:
                    #print "####skipping short row"
                    continue
                else:
                    if row[0].find("Sub-Activity") == 0:
                        subactivity = row[0].replace("\n", " ").strip()
                        #print subactivity
                        continue
                    elif row[0].find("Activity") == 0:
                        activity = row[0].replace("\n", " ").strip()
                        #print activity
                        continue

                    #skipping short lines (probably unneccessary)
                    if True:
                        indicator_num = indicator_num+1
                        indicator_id = country.upper()+"_"+project.upper()+"_"+str(indicator_num).zfill(4)

                        indicator_level = row[0]
                        indicator = row[1]
                        classification = row[2]
                        unit = row[3]
                        baseline = row[4]

                        actual_to_date = row[39]
                        end_of_compact_target = row[40]
                        percent_complete_to_date = row[41]
                        notes = row[42]

                        for year in range(1, 6):
                            yearly[str(year)]["q1"] = row[5+(year-1)*7]
                            yearly[str(year)]["q2"] = row[6+(year-1)*7]
                            yearly[str(year)]["q3"] = row[7+(year-1)*7]
                            yearly[str(year)]["q4"] = row[8+(year-1)*7]
                            yearly[str(year)]["yearly_target"] = row[9+(year-1)*7]
                            yearly[str(year)]["percent_complete"] = row[10+(year-1)*7]

                        #indicators.writerow(["country", "project", "subproject", "submission_date", "activity", "subactivity", "indicator_id", "indicator_level", "indicator", "classification", "unit", "baseline", "actual_to_date", "end_of_compact_target", "percent_complete_to_date", "notes"])
                        indicators.writerow([country, project, subproject, submission_date, activity, subactivity, indicator_id, indicator_level, indicator, classification, unit, baseline, actual_to_date, end_of_compact_target, percent_complete_to_date, notes])
                        #print [country, project, subproject, submission_date, activity, subactivity, indicator_id, indicator_level, indicator, classification, unit, baseline, actual_to_date, end_of_compact_target, percent_complete_to_date, notes]

                        #indicator_details.writerow(["indicator_id", "compact_year", "timeframe", "q1", "q2", "q3", "q4", "yearly_target", "percent_complete"])
                        for year in range(1, 6):
                            indicator_details.writerow([indicator_id,
                                                        year,
                                                        yearly[str(year)]["timeframe"],
                                                        yearly[str(year)]["q1"],
                                                        yearly[str(year)]["q2"],
                                                        yearly[str(year)]["q3"],
                                                        yearly[str(year)]["q4"],
                                                        yearly[str(year)]["yearly_target"],
                                                        yearly[str(year)]["percent_complete"]])

                        #print yearly
import os

#f=open("kpis.txt", "w")
#f.write("---")

os.chdir("data/")
for files in os.listdir("."):
    if files.endswith(".csv"):
        print files
        parse(files)

csvfile1.close()
csvfile2.close()
