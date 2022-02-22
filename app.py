from pandas import read_csv,DataFrame
import numpy as np

from flask import Flask, request, render_template,make_response
from verifier import Verifier
import asyncio
async def email_verify(email):
            v = Verifier(source_addr='user@example.com')
            l = v.verify(email)
            valid = l.get('valid_format')
            deliverable= l.get('deliverable')
            full_inbox= l.get('full_inbox')
            host_exists= l.get('host_exists')
            catch_all=l.get('catch_all')
            message= l.get('message')

            return valid,deliverable,full_inbox,host_exists,catch_all,message
async def main(df):
            df[['valid','deliverable','full_inbox','host_exists','catch_all','message']]=await asyncio.gather(*[email_verify(v) for v in df['Email']])
            return df

app = Flask(__name__)
        
@app.route('/', methods=['GET', 'POST'])
def home():
        return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def file_upload():
    if request.method == 'GET'or request.method == 'POST':
        df = read_csv(request.files.get('file'),encoding='ISO-8859-1',)
        df = DataFrame(df)
        df = df.drop_duplicates()
        asyncio.run(main(df))
                
        resp = make_response(df.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename=Verified.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp

    return render_template('index.html')

# @app.route('/error', methods=['GET', 'POST'])
# def error():
#     mu=upload.var
#     mu = make_response(mu.to_csv())
#     mu.headers["Content-Disposition"] = "attachment; filename=error.csv"
#     mu.headers["Content-Type"] = "text/csv"  
#     return mu   


if __name__ == '__main__':
    app.run(debug=True)