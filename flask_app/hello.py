from flask import Flask, render_template, request
import re

import pymysql

app = Flask(__name__)

def tokenizer2(sent):
    result = [] # 초기화
    o = sent.split(' ') # splitting
    for i in o :
        i = re.sub('은$', '', i)
        i = re.sub('는$', '', i)
        i = re.sub('이가$', '', i)
        i = re.sub('의$', '', i)
        i = re.sub('을$', '', i)
        i = re.sub('를$', '', i)
        i = re.sub('에서$', '', i)
        i = re.sub('와$', '', i)
        i = re.sub('과$', '', i)
        i = re.sub('에$', '', i)
        result.append(i)
        #result.append(i.replace('[^a-z]+은', '').replace('는','').replace("을","").replace('를', ' ').replace('이','').replace('가','')) # 불필요한 Symbol 제거
    return result


@app.route('/send', methods=['GET', 'POST'])
def main_page():
    
    if request.method == 'POST':

        word = request.form['word']

        # 검색어로  들어온게 문장형식이기 때문에 단어들로 토큰화 하고 각각 sql 날려서 merge 하는 알고리즘 구현해야함
        s = tokenizer2(word)
        
        print(s)

        conn = pymysql.connect(
                host='3.35.133.232',
                user='dba',
                password = "qwer1234",
                db='DBPJ',
                charset="utf8"
                )
        cur = conn.cursor()
        


        qry_str = "select paper_id, sum(tf_idf) from (select * from (select paper_id, tf_idf from PAPERS_ORIG P JOIN (select * from TF_IDF T where term='{}') T on (P.paper_id = T.doc_id) order by tf_idf desc) a ".format(s[0])
        
        for i in range(1,len(s)):
            qry_str += "UNION ALL SELECT * FROM (select paper_id, tf_idf from PAPERS_ORIG P JOIN (select * from TF_IDF T where term='{}') T on (P.paper_id = T.doc_id) order by tf_idf desc) a ".format(s[i]) 

        qry_str += ") a GROUP BY paper_id order by sum(tf_idf) desc"

        print(qry_str)

        cur.execute("select title, body, institution, writer, fileURL from PAPERS_ORIG P JOIN ( " + qry_str + " ) T on (P.paper_id = T.paper_id)")
        
       
        output = cur.fetchall()
        
        cur.execute("select count(*) from PAPERS_ORIG P JOIN ( " + qry_str + " ) T on (P.paper_id = T.paper_id)")
        counter = cur.fetchall()


        #print(output)
        conn.commit()
        conn.close()


        return render_template('receive.html', output=output, counter=counter)
    return render_template('/search.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    # mysqlconnect()


def tokenizer2(sent):
    result = [] # 초기화
    o = sent.split(' ') # splitting
    for i in o :
        i = re.sub('은$', '', i)
        i = re.sub('는$', '', i)
        i = re.sub('이가$', '', i)
        i = re.sub('의$', '', i)
        i = re.sub('을$', '', i)
        i = re.sub('를$', '', i)
        i = re.sub('에서$', '', i)
        i = re.sub('와$', '', i)
        result.append(i)
        #result.append(i.replace('[^a-z]+은', '').replace('는','').replace("을","").replace('를', ' ').replace('이','').replace('가','')) # 불필요한 Symbol 제거
    return result











'''
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

conn.close()
'''
