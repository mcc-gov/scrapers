import csv

csvfile1 = open('output/compacts.csv', 'wb')
compacts = csv.writer(csvfile1, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
compacts.writerow(["country", "signed", "start", "end", "closeout", "quarter", "report", "budget"])

csvfile2 = open('output/projects.csv', 'wb')
projects = csv.writer(csvfile2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
projects.writerow(["country", "project", "objective", "benefits"])

csvfile4 = open('output/activities.csv', 'wb')
activities = csv.writer(csvfile4, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
activities.writerow(["country", "project", "activity", "outcome"])

csvfile3 = open('output/kpis.csv', 'wb')
kpis = csv.writer(csvfile3, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
kpis.writerow(["country", "project", "activity", "kpi", "baseline", "target", "actual", "percent"])

csvfile4 = open('output/notes.csv', 'wb')
notes = csv.writer(csvfile4, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
notes.writerow(["country", "mark", "note"])

comments = {}


def parse_comments(filename):

    country = ""

    comment = ""
    with open(filename, 'rU') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for (i, row) in enumerate(spamreader):
            #print row
            if i == 1:
                country = row[1]

            if i == 11:
                #print country
                pass

            if i > 11:
                #skip short row
                if len(''.join(row)) < 20:
                    #print "####skipping short row"
                    continue
                else:
                    if row[0].find("Project") == 0:
                        continue

                    if row[0].find("Transition to High") == 0:
                        pass

                    if len(row[0]) > 10:

                        comment = row[0]
                        if comment[0] == "*" or comment[0] == "[" or comment[0] == "1" or comment[0] == "2" or comment[0] == "3" or comment[0] == "4":
                            if not country in comments.keys():
                                comments[country] = {}

                            #print comment
                            if comment.find("***") == 0:
                                comment = comment[3:].strip()
                                comments[country]["***"] = comment
                            elif comment.find("**") == 0:
                                comment = comment[2:].strip()
                                comments[country]["**"] = comment
                            elif comment.find("*") == 0:
                                comment = comment[1:].strip()
                                comments[country]["*"] = comment
                            elif comment.find("[1]") == 0:
                                comment = comment[3:].strip()
                                comments[country]["[1]"] = comment
                            elif comment.find("[2]") == 0:
                                comment = comment[3:].strip()
                                comments[country]["[2]"] = comment
                            elif comment.find("[3]") == 0:
                                comment = comment[3:].strip()
                                comments[country]["[3]"] = comment
                            elif comment.find("[4]") == 0:
                                comment = comment[3:].strip()
                                comments[country]["[4]"] = comment
                            elif comment.find("[5]") == 0:
                                comment = comment[3:].strip()
                                comments[country]["[5]"] = comment

                            #print "comments: ", project
                            continue



def parse(filename):

    country = ""
    signed = ""
    start = ""
    end = ""
    closeout = ""
    quarter = ""
    report = ""
    budget = ""

    project = ""
    objective = ""
    benefits = ""
    activity = ""
    outcome = ""
    #kpi = ""
    #baseline = ""
    #target = ""
    #actuals = ""
    #percent = ""

    comments

    with open(filename, 'rU') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for (i, row) in enumerate(spamreader):
            #print row
            if i == 1:
                country = row[1]
                signed = row[6]
            if i == 2:
                start = row[6]
            if i == 3:
                end = row[6]
            if i == 4:
                closeout = row[6]
            if i == 5:
                budget = row[6]
            if i == 8:
                report = row[1]
            if i == 6:
                quarter = row[1]

            if i == 11:
                #print country
                #print signed
                #print start
                #print end
                #print closeout
                #print quarter
                #print report
                #print budget
                compacts.writerow([country, signed, start, end, closeout, quarter, report, budget])

            if i > 11:
                #skip short row
                if len(''.join(row)) < 20:
                    #print "####skipping short row"
                    continue
                else:
                    if row[0].find("Project") == 0:
                        continue

                    if row[0].find("Transition to High") == 0:
                        pass

                    if len(row[0]) > 10:
                        comment = row[0]
                        if comment[0] == "*" or comment[0] == "[" or comment[0] == "1" or comment[0] == "2" or comment[0] == "3" or comment[0] == "4":
                            continue


                        project = row[0]
                        objective = ""
                        benefits = row[1].replace("\n", " ").replace("  ", " ").strip()
                        notes = ""

                        #splitting string into project/objective
                        try:
                            project, objective = project.split("\n", 1)
                            project = project.strip()
                            objective = objective.strip()
                        except ValueError:
                            objective = ""

                        projects.writerow([country, project, objective, benefits])
                        print "project: ", [country, project, objective, benefits]

                    kpi = row[3].replace("\n", " ").replace("  ", " ").strip()
                    baseline = row[4].replace("\n", " ").replace("  ", " ").strip()
                    target = row[5].replace("\n", " ").replace("  ", " ").strip()
                    actual = row[6].replace("\n", " ").replace("  ", " ").strip()
                    percent = row[7].replace("\n", " ").replace("  ", " ").strip()


                    if len(row[2]) > 10:
                        activity = row[2]
                        outcome = ""

                        activity = activity.replace("\n", " ").replace("  ", " ").strip()
                        outcome = outcome.replace("\n", " ").replace("  ", " ").strip()
                        #print "activity: ", activity
                        try:
                            if activity.find("Outcome") > 0:
                                activity, outcome = activity.split('Outcome')
                                outcome = 'Outcome'+outcome
                            else:
                                outcome = ""
                        except ValueError:
                            outcome = ""
                        #print "outcome", outcome
                        activity = activity.replace("\n", " ").replace("  ", " ").strip()
                        outcome = outcome.replace("\n", " ").replace("  ", " ").strip()

                        activities.writerow([country, project, activity, outcome])

                        #print row
                        #notes = ""
                        #if country in comments:
                        #    for comment in comments[country]:
                        #        mark = comment
                        #        print country, mark, comments[country][comment]
                        #        print project
                        #        if kpi.find(mark) > 0:
                        #            print mark, "---", kpi
                        #            notes = notes + "\n" + mark + " " + comments[country][comment]

                        #notes = notes.strip()


                    #embedd comments field

                    kpis.writerow([country, project, activity, kpi, baseline, target, actual, percent])

    #print country
    #print signed
    #print start
    #print end
    #print closeout
    #print quarter
    #print report
    #print budget

import os

#f=open("kpis.txt", "w")
#f.write("---")

#path to your KPIs data saved as CSV
os.chdir("csv")
for files in os.listdir("."):
    if files.endswith(".csv"):
        parse_comments(files)

for country in comments:
    for note in comments[country]:
        notes.writerow([country, note, comments[country][note]])
print comments

for files in os.listdir("."):
    if files.endswith(".csv"):
        parse(files)

csvfile1.close()
csvfile2.close()
csvfile3.close()
csvfile4.close()