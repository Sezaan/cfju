from flask import Flask, render_template, request
import requests, bs4, json

errors = []
def parse(contestId):
    # response = requests.get('https://codeforces.com/ratings/organization/125')
    # html = bs4.BeautifulSoup(response.text, 'html.parser')

    # lines = html.select('td > .rated-user')
    # lines = lines[20:]

    # handles = []
    # for line in lines:
        # handles.append(line.getText())

    # handles = ';'.join(handles)
    handles = ""
    with open('users.txt', 'r') as f:
        handles = f.read()

    url = 'https://codeforces.com/api/contest.standings'
    params = {"contestId" : int(contestId), "handles" : handles, "showUnofficial" : True}

    response = requests.get(url = url, params = params)

    cur = {}

    parsed_json = json.loads(response.text)
    if parsed_json["status"] == "FAILED":
        errors.append("Invalid Contest ID. (Contest does not exist yet.)")
    else:
        cur = parsed_json["result"]["rows"]

    info = []
    
    serial = 1
    okay = 0

    for i in range(len(cur)):
        cur_info = {}
        cnt = 0
        for p in cur[i]["problemResults"]:
            if(p["points"] > 0.0):
                cnt = cnt + 1
        # print(cur[i]["party"]["members"][0]["handle"], cur[i]["rank"], int(cur[i]["points"]), cnt)
        if cur[i]["rank"] == 0:
            cur[i]["rank"] = "UPSOLVER"
            if(not okay):
                serial = 1
                okay = 1
        cur_info = {'serial': serial, 'handle' : cur[i]["party"]["members"][0]["handle"], 'rank': cur[i]["rank"], 'points': int(cur[i]["points"]), 'cnt': cnt}
        info.append(cur_info)
        serial = serial + 1

    return info


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    errors.clear()
    cur = []
    id = ""
    if(request.method == 'POST'):
        check = request.form.get('contestid')
        try:
            check = int(check)
        except ValueError:
            errors.append("Invalid Contest ID. (Not a integer.)")
        
        if(type(check) == str):
            errors.append("Invalid Contest ID. (Not a integer)")
        elif(check <= 0):
            errors.append("Invalid Contest ID. (ID can't be negative or 0)")

        if(len(errors) == 0):
            cur = parse(request.form.get('contestid'))
            id = request.form.get('contestid')

    return render_template('home.html', data = cur, id = id, errors = errors)

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()