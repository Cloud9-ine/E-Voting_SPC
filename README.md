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

2. Run this command to initialization the database, you can always use this to flush the content and rebuild the database.

       $ make initdb

3. Switch to the CGI folder, like ".../etovucca/cgi-bin/", change the file permission for every CGI file inside this folder. For example,  
       
       $ cd cgi-bin
       $ chmod 755 home.cgi

4. Switch to the root folder again. Run this command to compile the backend program and the frontend, and your frontend will start at localhost:8000.    

       $ cd ..        
       $ make

   Stop the program in terminal by using Ctrl+C.  


5. Run these commands to change the file permission of the following.  

       $ chmod 755 database_helper.py
       $ chmod 755 etovucca

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
   Details to be added...


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
