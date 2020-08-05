from apscheduler.schedulers.blocking import BlockingScheduler

import requests, bs4

sched = BlockingScheduler()

@sched.scheduled_job('interval', max_instances=5, hours=1)
def job():
    response = requests.get('https://codeforces.com/ratings/organization/125')
    html = bs4.BeautifulSoup(response.text, 'html.parser')

    lines = html.select('td > .rated-user')
    lines = lines[20:]

    handles = []
    for line in lines:
        handles.append(line.getText())

    handles = ';'.join(handles)
    with open('users.txt', 'w') as f:
        f.write(handles)
    
    with open('users.txt', 'r') as f:
        print(f.read())

sched.start()