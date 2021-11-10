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
   Details to be added...


4. Phishing Page (Completed)  
   Details to be added...


5. Integer Overflow (Completed)  
   Details to be added...


6. *Modification on Control Flow (Not implemented)

**Readme ENDS here.**
