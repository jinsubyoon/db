from flask import Flask, render_template, request
import pymysql

# from flask_mysqldb import MySQL

app = Flask(__name__)

'''
app.config['MYSQL_USER'] = 'dba'
app.config['MYSQL_PASSWORD'] = 'qwer1234'
app.config['MYSQL_HOST'] = '3.35.133.232'
app.config['MYSQL_DB'] = 'DBPJ'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
'''

@app.route('/send', method=['GET', 'POST'])
def send():
    if request.method == 'POST':
        word = request.form['word']
        
        return render_template('receive.html', word=word)

    return render_template('search.html')

def main_page():
    #cur = mysql.connection.cursor()
    #cur.execute('''CREATE TABLE example (id INTEGER, name VARCHAR(20))''')
    #mysqlconnect()
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    mysqlconnect()

def mysqlconnect():
    # To connect MySQL database
    conn = pymysql.connect(
        host='3.35.133.232',
        user='dba',
        password = "qwer1234",
        db='DBPJ',
        charset="utf8"
        )

    cur = conn.cursor()
    cur.execute("select writer from papers where paper_id=660")
    output = cur.fetchall()
    print(output)

    # To close the connection
    conn.close()

