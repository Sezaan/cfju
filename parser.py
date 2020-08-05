import requests, bs4, json

def parse():
    response = requests.get('https://codeforces.com/ratings/organization/125')
    html = bs4.BeautifulSoup(response.text, 'html.parser')

    lines = html.select('td > .rated-user')
    lines = lines[20:]

    handles = []
    for line in lines:
        handles.append(line.getText())

    handles = ';'.join(handles)

    url = 'https://codeforces.com/api/contest.standings'
    params = {"contestId" : 1384, "handles" : handles, "showUnofficial" : True}

    response = requests.get(url = url, params = params)

    parsed_json = json.loads(response.text)

    cur = parsed_json["result"]["rows"]

    info = []

    for i in range(len(cur)):
        cur_info = {}
        cnt = 0
        for p in cur[i]["problemResults"]:
            if(p["points"] > 0.0):
                cnt = cnt + 1
        # print(cur[i]["party"]["members"][0]["handle"], cur[i]["rank"], int(cur[i]["points"]), cnt)
        cur_info = {'handle' : cur[i]["party"]["members"][0]["handle"], 'rank': cur[i]["rank"], 'points': int(cur[i]["points"]), 'cnt': cnt}
        info.append(cur_info)

    return handles

if __name__ == '__main__':
    cur = parse()
    print(cur)
