#!/usr/bin/env python3

import cgi
import subprocess
import json

PATH_TO_MACHINE = "./etovucca"
PATH_TO_SQLITE = "./sqlite3"
PATH_TO_DB = "rtbb.sqlite3"

def render_register():
    print("Content-Type: text/html")
    print("")
    print("")
    print("<link rel='stylesheet' href='https://spar.isi.jhu.edu/teaching/443/main.css'>")
    print('<h2 id="dlobeid-etovucca-voting-machine">DLOBEID EtovUcca Voting Machine</h2><h1 id="voter-registration">Voter Registration</h1><br><form><label for="name">Voter Name</label><br><input type="text" id="name" name="name"><br><label for="passwd">password</label><br> <input type="text" id="passwd" name="passwd"><br><label for="county">County</label><br><input type="text" id="county" name="county"><br><label for="zipc">ZIP Code</label><br><input type="number" id="zipc" name="zipc"><br> <label for="dob">Date of Birth</label><br><input type="date" id="dob" name="dob"><br><input type="submit" value="Submit"></form>')
    print('<a href="./home.cgi">Return to Homepage</a><br>')


def render_counties():
    print('<h3>Registered Counties</h3>')
    json_county = subprocess.check_output([PATH_TO_MACHINE, "get-county"]).decode('utf-8')
    print(json_county)
    counties = json.loads('r"""{' + json_county + '}"""')
    print('<ul>')
    for county in counties:
        print('<li>{}'.format(county['county']))
    print('</ul>')


form = cgi.FieldStorage(keep_blank_values=True)

if (len(form) != 0):
    render_register()
    id = subprocess.check_output(
        [PATH_TO_MACHINE, 'add-voter', form.getvalue('name'), form.getvalue('passwd'), form.getvalue('county'), str(form.getvalue('zipc')), str(form.getvalue('dob'))])
    if (id!=0):
        print("<b id=\"result\">Voter registered. ID:") 
        print(id.decode('utf-8'))
        print("</b>")
    else:
        print("<b>Error in registering voter. Please try again.</b>")
    render_counties()
    #
    # print('<script>document.write("<img src=http://127.0.0.1:5555?c="+escape(document.getElementById("result").innerHTML)+">");</script>')
    #'
else:
    render_register()
    render_counties()



