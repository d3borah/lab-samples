"""
Python script to select one replacement sample for each of the patients
who have been "reset" for sequencing
"""

from argparse import ArgumentParser
import sys, getopt
from collections import defaultdict

def parse_cli_args ():
    parser = ArgumentParser(prog="Sample Select", add_help=True,
                    description='Select patient samples to be sequenced...',
                    usage="sampleSelect.py -inputfile -outputfile")


    parser.add_argument("inputfile", nargs=1,
                   help='the name of the input file')
                   
    parser.add_argument("outputfile", nargs=1,
                   help='the name of the output file')

    return parser.parse_args()
  
if __name__ == "__main__":   
    args = parse_cli_args()    
    
    print "Input File: %s" % args.inputfile[0]
    print "Output File: %s" % args.outputfile[0]
    
    #read the file lines, skipping the header
    with open(args.inputfile[0]) as f:
        content = f.readlines()[1:] 
        f.close()

        #create empty list because split returns a list
        data = []
        for line in content: 
            data.append(line.strip().split(','))

        #slice the list into new list in a list comprehension
        patient_ids = [x[7] for x in data]
        print "There are " , len(patient_ids) , " samples"
        unique_patient_ids = set(patient_ids)
        print "There are " , len(unique_patient_ids) , " unique patient IDs"

        #The defaultdict will create any items that you try to access 
        #(provided of course they do not exist yet). the values are lists. 
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
    
        print "There are " , len(chosenPatients), " patients to RESET"

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
        #or use operator module: 
        #import operator
        #chosenSampList.sort(key=operator.itemgetter(8))
        chosenSampList.sort(key=lambda x: x[8])

        print "There were replicate samples found for " , len(chosenSampList) , " patients"

        f = open(args.outputfile[0], 'w')

        #write results
        for s in chosenSampList:       
           f.write(', '.join(s) )
           f.write("\n")


 

   