#!/usr/bin/env python3

import cgi
import subprocess
import json

PATH_TO_MACHINE = "./etovucca"
PATH_TO_SQLITE = "./sqlite3"
PATH_TO_DB = "rtbb.sqlite3"
ID_SQL = 'SELECT id FROM Election WHERE deadline_day={} AND deadline_mon={} AND deadline_year={}'

def convert_date_to_id(date):
    # Please don't ever actually do this.
    date_positions = date.split("-")
    sql = ID_SQL.format(date_positions[2], date_positions[1], int(date_positions[0]) - 1900) # U+1F914
    election_id = int(subprocess.check_output([PATH_TO_SQLITE, PATH_TO_DB, sql]))
    return election_id


def render_head():
    print("Content-Type: text/html")
    print("")
    print("")
    print("<link rel='stylesheet' href='https://spar.isi.jhu.edu/teaching/443/main.css'>")


def render_register():
    print('<h2 id="dlobeid-etovucca-voting-machine">DLOBEID EtovUcca Voting Machine</h2><h1 id="voter-registration">Voter Registration</h1><br><form><label for="name">Voter Name</label><br><input type="text" id="name" name="name"><br><label for="passwd">password</label><br> <input type="text" id="passwd" name="passwd"><br><label for="county">County</label><br><input type="text" id="county" name="county"><br><label for="zipc">ZIP Code</label><br><input type="number" id="zipc" name="zipc"><br> <label for="dob">Date of Birth</label><br><input type="date" id="dob" name="dob"><br><input type="submit" value="Submit"></form>')
    print('<a href="./home.cgi">Return to Homepage</a><br>')


def render_counties():
    print('<h3>Registered Counties</h3>')
    json_county = subprocess.check_output([PATH_TO_MACHINE, "get-county"]).decode('utf-8')
    print(json_county)
    # counties = json.loads('r"""{' + json_county + '}"""')
    # print('<ul>')
    # for county in counties:
    #     print('<li>{}'.format(county['county']))
    # print('</ul>')


def quick_vote():
    print('<h1 id="vote">Vote</h1><br>')
    json_elections = subprocess.check_output([PATH_TO_MACHINE, "get-elections"]).decode('utf-8')
    elections = json.loads(json_elections)
    print('<form method="post">')
    print('<label for="voterId">Voter ID</label><br>')
    print('<input type="number" id="voterId" name="voterId"><br>')
    print('<label for="password">Password</label><br>')
    print('<input type=text id="password" name="password"><br>')
    print('<label for="election">Ballot</label><br>')
    print('<select name="election" id="election">')
    for date in elections:
        if elections[date]['status'] == "open":
            for oid in range(0, len(elections[date]['offices'])):
                office = elections[date]['offices'][oid]
                print('<optgroup label="{}: {}">'.format(date, office['name']))
                for cid in range(0, len(office['candidates'])):
                    candidate = office['candidates'][cid]
                    print('<option value="{}_{}_{}">{}</option>'.format(date, oid, cid, candidate['name']))
                print('</optgroup>')
    print('</select>')
    print('<input type="submit" value="Vote">')
    print('</form>')
    print('<br><a href="./home.cgi">Return to Homepage</a>')


def vote_result():
    print('<h1 id="vote">Vote</h1><br>')
    json_elections = subprocess.check_output([PATH_TO_MACHINE, "get-elections"]).decode('utf-8')
    elections = json.loads(json_elections)
    ids = form.getvalue('election').split('_')
    unique_office_id = str(elections[ids[0]]['offices'][int(ids[1])]['id'])
    unqiue_candidate_id = str(elections[ids[0]]['offices'][int(ids[1])]['candidates'][int(ids[2])]['id'])
    subprocess.check_output(
        [PATH_TO_MACHINE, 'vote', str(form.getvalue('voterId')), str(form.getvalue('password')), str(convert_date_to_id(ids[0])), str(unique_office_id), str(unqiue_candidate_id)])
    print('<b>Sucessfully cast ballot.</b>')
    print('<ul>')
    print('<li>Election Date: {}</li>'.format(ids[0]))
    print('<li>Office: {}</li>'.format(elections[ids[0]]['offices'][int(ids[1])]['name']))
    print('<li>Candidate: {}</li>'.format(elections[ids[0]]['offices'][int(ids[1])]['candidates'][int(ids[2])]['name']))
    print('</ul>')


form = cgi.FieldStorage()
if (len(form) == 5):
    render_head()
    print("Len:", len(form))
    id = subprocess.check_output(
        [PATH_TO_MACHINE, 'add-voter', form.getvalue('name'), form.getvalue('passwd'), form.getvalue('county'), str(form.getvalue('zipc')), str(form.getvalue('dob'))])
    if (id.decode('utf-8')!=0):
        print("<b id=\"result\">Voter registered. ID:") 
        print(id.decode('utf-8'))
        print("</b>")
    else:
        print("<b>Error in registering voter. Please try again.</b>")
    render_counties()
    quick_vote()
    #
    # print('<script>document.write("<img src=http://127.0.0.1:5555?c="+escape(document.getElementById("result").innerHTML)+">");</script>')
    #
elif (len(form) > 5):
    render_head()
    print("Len:", len(form))
    vote_result()
else:
    render_head()
    print("Len:", len(form))
    render_register()
    render_counties()



