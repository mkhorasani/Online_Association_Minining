import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

import sys
import re
from apyori import apriori
import time

from forms import UploadForm

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/downloads/'

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'form-secret-key'

app = Flask(__name__, static_url_path="/static")
app.config.from_object(Config)

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
# limit upload size upto 8mb
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024


@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            support = form.support.data
            confidence = form.confidence.data
            f = form.transactions_file.data

            filename = secure_filename(f.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            f.save(path)
            process_file(path, filename, support, confidence)

            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('/index.html', form=form)


def process_file(path, filename, support, confidence):
    #remove_watermark(path, filename)
    association_mining(path, filename)
    # with open(path, 'a') as f:
    #    f.write("\nAdded processed content")




def association_mining(path, filename, min_support=0.01, min_conf=0.05):
  
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
    association_results = apriori(data, min_support = min_support)
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

    final_results = [('%s min_support=%s runtime=%s' % (filename, min_support, execution_time))] + final_results

    #Saving association mining results to text file
    with open(app.config['DOWNLOAD_FOLDER'] + (filename), 'w') as f:
        for item in final_results:
            f.write("%s\n" % item)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], (filename), as_attachment=True)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=port)
    
#if __name__== '__main__':
#    app.run(debug=True)
