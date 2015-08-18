#!flask/bin/python
# andrew borgman
# flask app to handle incoming DET POST requests and lauch R util to merge data request

from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
import pyRserve


# template of r script we want run each time API is hit
sync_template = '''

# log all of the changes to a log file...
sink(file = file('/home/ubuntu/det-logs/sync-log.txt', 'a'), append = TRUE, type = 'message')

sqlite <- dbDriver("SQLite")
dbname <- "/home/ubuntu/dbs/barcode.db"
db_con <- dbConnect(sqlite, dbname)

uri <- readRDS('~/.redcap/ecmo/uri.rds')
gtok <- readRDS('~/.labguru/token.rds')

message("about to init object.....")
s <- SyncHandler$new(project_id = {project_id[0]}, instrument = '{instrument[0]}', redcap_id = {record[0]},
                   redcap_token = tok, guru_token = gtok, redcap_url = uri)

message("about to sync.....")
s$sync_data(db_con = db_con)

'''


# define our app and our handled routes
app = Flask(__name__)


@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello!</h1>"

@app.route('/det/api/v1.0/', methods=['POST'])
def det_syncer():

    # only have to sync if changes were made to our two inventory forms
    if request.form['instrument'] == 'pbmc' or request.form['instrument'] == 'cytokine':

        # connect to our Rserve instance
        conn = pyRserve.connect()

        # set our REDCap token appropriately
        if request.form['project_id'] == '65':
            conn.eval("tok <- readRDS('~/.redcap/controls/token.rds')")
        elif request.form['project_id'] == '52':
            conn.eval("tok <- readRDS('~/.redcap/ecmo/token.rds')")
        else:
            print 'No token for this project id...'
            print str(request.form)
            return make_response(jsonify({'result': 'failed'}), 400)


        print 'Syncing the following data:'
        print str(request.form)
        print '----------'


        # fill in our script & run it
        to_run = sync_template.format(**request.form)
        conn.eval(to_run)

    else:
        print 'Nothing to sync...'
        print str(request.form)
        print '----------'

    return make_response(jsonify({'result': 'success'}), 201)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)



