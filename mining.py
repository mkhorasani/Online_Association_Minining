import re
from apyori import apriori
import time

from flask_app import app


def process_file(path, filename, support, confidence):
    #remove_watermark(path, filename)
    association_mining(path, filename, support, confidence)
    # with open(path, 'a') as f:
    #    f.write("\nAdded processed content")

def association_mining(path, filename, min_support=0.01, min_conf=0):
    start_time = time.time()

    #Importing dataset
    f = open(path,'r')
    data = f.readlines()
    #data = data[0:1000]

    #Parsing and delimiting dataset
    for i in range(0,len(data)):
        data[i] = data[i].replace('\n','')
        
    for i in range(0,len(data)):
        data[i] = re.split(';', data[i])

    #Executing association mining using the apriori toolkit
    association_results = apriori(data, min_support = min_support, min_confidence=min_conf)
    results = list(association_results)

    #Creating a list of lists of the support, itemsets
    final_results = [[0 for x in range(2)] for y in range(len(results))]

    for i in range(0,len(results)):
        final_results[i][0] = int((results[i][1])*len(data))
        final_results[i][1] = ', '.join(list(results[i][0]))

    #Sorting list of lists in descending order
    final_results.sort(reverse = True)

    end_time =  time.time()
    execution_time = (end_time - start_time)

    final_results = [('%s, min_support=%s, min_conf=%s, runtime=%s' % (filename, min_support, min_conf, execution_time))] + final_results

    #Saving association mining results to text file
    with open(app.config['DOWNLOAD_FOLDER'] + (filename), 'w') as f:
        for item in final_results:
            f.write("%s\n" % item)

