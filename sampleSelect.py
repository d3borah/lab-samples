"""
Python script to select one replacement sample for each of the patients
who have been "reset" for sequencing
"""

import sys
from collections import defaultdict

filename = "samples.csv"

#read the file lines, skipping the header
with open(filename) as f:
    content = f.readlines()[1:] 

#create empty list because split returns a list
data = []


#split each line in a list
for line in content: 
    data.append(line.strip().split(','))

#print data[0]

#slice the list into new list in a list comprehension
patient_ids = [x[7] for x in data_list]
len(patient_ids)
unique_patient_ids = set(patient_ids)
len(unique_patient_ids)

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
        
len(chosenPatients)

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


import operator
chosenSampList.sort(key=operator.itemgetter(8))

f = open('sample_outputfile_backup.csv', 'w')

#emit results
for s in chosenSampList:       
    f.write(', '.join(s) )
    f.write("\n")


