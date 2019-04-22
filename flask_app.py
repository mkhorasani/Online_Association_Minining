import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename


import sys
import re
from apyori import apriori
import time

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/downloads/'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__, static_url_path="/static")
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
# limit upload size upto 8mb
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            process_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename)
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('/index.html')


def process_file(path, filename):
    #remove_watermark(path, filename)
    association_mining(path, filename)
    # with open(path, 'a') as f:
    #    f.write("\nAdded processed content")




def association_mining(path, filename):
  
    start_time = time.time()

    #Importing dataset
    file = open(path,'r')
    data = file.readlines()
    #data = data[0:1000]

    #Parsing and delimiting dataset
    for i in range(0,len(data)):
        data[i] = data[i].replace('\n','')
        
    for i in range(0,len(data)):
        data[i] = re.split(';', data[i])

    #Executing association mining using the apriori toolkit
    min_support = 0.05
    association_results = apriori(data, min_support = 0.01)
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


    




#def remove_watermark(path, filename):
#    input_file = PdfFileReader(open(path, 'rb'))
#    output = PdfFileWriter()
#    for page_number in range(input_file.getNumPages()):
#        page = input_file.getPage(page_number)
#        page.mediaBox.lowerLeft = (page.mediaBox.getLowerLeft_x(), 20)
#        output.addPage(page)
#    output_stream = open(app.config['DOWNLOAD_FOLDER'] + filename, 'wb')
#    output.write(output_stream)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], (filename), as_attachment=True)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=port)
    
#if __name__== '__main__':
#    app.run(debug=True)
