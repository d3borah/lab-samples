"""
Python script to select one replacement sample for each of the patients
who have been "reset" for sequencing
"""

import sys, getopt
from collections import defaultdict
import operator


def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print 'test.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print 'Input file is "', inputfile
    print 'Output file is "', outputfile
    #read the file lines, skipping the header
    with open(inputfile) as f:
        content = f.readlines()[1:] 
        f.close()

        #create empty list because split returns a list
        data = []

        #split each line in a list
        for line in content: 
            data.append(line.strip().split(','))

        #slice the list into new list in a list comprehension
        patient_ids = [x[7] for x in data]
        print "There are " , len(patient_ids) , " patient IDs"
        unique_patient_ids = set(patient_ids)
        print "There are " , len(unique_patient_ids) , " unique patient IDs"

        #The defaultdict will create any items that you try to access (provided of course they do not exist yet). the values are lists. 
        patientSamples = defaultdict(list)

        #make the per patient dictionary containing all of that patient's samples
        for patient in unique_patient_ids:
            for sample in data:
                if sample[7] == patient:
                    patientSamples[patient].append(sample)


        #for key, value in patientSamples.iteritems():
        #print key, 'corresponds to',patientSamples[key]

        #make a list to contain the patients we want to find the additional samples for
        chosenPatients = []
        for key, value in patientSamples.iteritems():
            for myvalue in patientSamples[key]:
                if myvalue[5] == "Reset":
                    chosenPatients.append(key)
    

        """
        go through the samples and select just one sample for each of the chosen patients, provided 
        the sample status is "Duplicate" or blank
        """
        chosenSamples = {}
        for patient in chosenPatients:
            if patient in chosenSamples:
                break
            else:
                for value in patientSamples.iteritems():
                    for myvalue in patientSamples[patient]:
                        if ((myvalue[5] == "") | (myvalue[5] == "Duplicate")):
                           chosenSamples[patient] = myvalue            

        chosenSampList = []
        for item in chosenSamples:
            chosenSampList.append(chosenSamples[item])
        #sort the list by one of the nested list elements - the freezer location
        chosenSampList.sort(key=operator.itemgetter(8))

        f = open(outputfile, 'w')

        #write results
        for s in chosenSampList:       
           f.write(', '.join(s) )
           f.write("\n")

if __name__ == "__main__":
   main(sys.argv[1:])

   