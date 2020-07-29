from flask import Flask, render_template, request

import requests, bs4, json

def parse(contestId):
    response = requests.get('https://codeforces.com/ratings/organization/125')
    html = bs4.BeautifulSoup(response.text, 'html.parser')

    lines = html.select('td > .rated-user')
    lines = lines[20:]

    handles = []
    for line in lines:
        handles.append(line.getText())

    handles = ';'.join(handles)

    url = 'https://codeforces.com/api/contest.standings'
    params = {"contestId" : int(contestId), "handles" : handles, "showUnofficial" : True}

    response = requests.get(url = url, params = params)

    parsed_json = json.loads(response.text)

    cur = parsed_json["result"]["rows"]

    info = []
    
    serial = 1

    for i in range(len(cur)):
        cur_info = {}
        cnt = 0
        for p in cur[i]["problemResults"]:
            if(p["points"] > 0.0):
                cnt = cnt + 1
        # print(cur[i]["party"]["members"][0]["handle"], cur[i]["rank"], int(cur[i]["points"]), cnt)
        if cur[i]["rank"] == 0:
            cur[i]["rank"] = "UPSOLVER"
        cur_info = {'serial': serial, 'handle' : cur[i]["party"]["members"][0]["handle"], 'rank': cur[i]["rank"], 'points': int(cur[i]["points"]), 'cnt': cnt}
        info.append(cur_info)
        serial = serial + 1

    return info


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    cur = {}
    if(request.method == 'POST'):
        cur = parse(request.form.get('contestid'))
    return render_template('home.html', data = cur, id = request.form.get('contestid'))
if __name__ == '__main__':
    app.run()
