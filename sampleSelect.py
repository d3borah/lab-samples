import sys
from collections import defaultdict

filename = "samples.csv"

with open(filename) as f:content = f.readlines()[1:] #skip the header
data = []

for line in content: 
    data.append(line.strip().split(',')) #split returns a list, if you want a tuple, convert it to a tuple

#print data[0]

patient_ids = [x[7] for x in data_list]#list comprehension
len(patient_ids)
unique_patient_ids = set(patient_ids)
len(unique_patient_ids)
patientSamples = defaultdict(list)

for patient in unique_patient_ids:
    for sample in data:
        if sample[7] == patient:
                patientSamples[patient].append(sample)

#for key, value in patientSamples.iteritems():
    #print key, 'corresponds to',patientSamples[key]

chosenPatients = []
for key, value in patientSamples.iteritems():
    for myvalue in patientSamples[key]:
        if myvalue[5] == "Reset":
            chosenPatients.append(key)
        
len(chosenPatients)

chosenSamples = {}
for patient in chosenPatients:
    if patient in chosenSamples:
            break
    else:
        for value in patientSamples.iteritems():
            for myvalue in patientSamples[patient]:
                if ((myvalue[5] == "") | (myvalue[5] == "Duplicate")):
                    chosenSamples[patient] = myvalue            

len(chosenSamples)

#for item in chosenSamples:
    #print chosenSamples[item][5]

f = open('sample_outputfile_backup.csv', 'w')

#emit results
for item in chosenSamples:
    f.write(', '.join(chosenSamples[item])  )
    f.write("\n")
