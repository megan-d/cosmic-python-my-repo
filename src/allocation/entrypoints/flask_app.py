from flask import Flask

app = Flask(__name__)

@app.route('/data', methods=['GET', 'POST'])
def getData(): # execute function when this endpoint queried.
  return "Some Data"

app.run(host='<host>', port='<port>')
