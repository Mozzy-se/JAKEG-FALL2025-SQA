## COMP 5710 Project Report
 Team Name: JAKEG 	
 
 Team Members: Jake Galliher


## Activities
### Step 1 - Project Setup
- Files were downloaded from project repo and MLForensics.zip was unzipped.
- Team repo was created for this assignment with requested name formatting.
- The README.md file was required for team repo that lists team name and members.

### Step 2 - Automated Fuzz Testing
- The fuzz.py file was created and added to the team repo.
- From the provided existing Python project, 5 methods were chosen to fuzz.
- These methods include:

	- mining.giveTimeStamp
 	- mining.dumpContentIntoFile
  - mining.makeChunks
  - mining.days_between
  - py_parser.getPythonParseObject
 
The reason these functions were selected was because they were simple and effective for the fuzzing part of the project.

Upon collecting the methods of choice, here was the fuzzing strategy that was implemented:
- Geneates random strings, ints, lists, and filenames.
- Execution of each func 200 times with varying inputs.
- Uses wrapper to capture and count crashes.
- Logging output through fuzz.py summarizes results of each function.

The results of this showed a continued bug for mining.makeChunks, where crashes occurred when the generated chunk size was zero which produced a ValueError.

Screenshots showing fuzzing output:
<img width="1097" height="868" alt="image" src="https://github.com/user-attachments/assets/87b61cd6-f45f-45ab-84a0-e765e3b5e01e" />
<img width="1115" height="951" alt="image" src="https://github.com/user-attachments/assets/0bd3b455-5b9e-4b85-bf0f-4f1905147281" />

## Step 3 - Logging + Forensics Integration
- Logging was added using Python's logging module to the five methods used for fuzzing.
- The results of the forensics log was coded to be generated and contain entires as shown in the screenshot, the file can also be found in the team repo.
<img width="802" height="1298" alt="image" src="https://github.com/user-attachments/assets/f22a596b-bd29-44cc-a651-56a6b8dd2239" />

## Step 4 - Continuous Integration with Github Actions
- A GitHub actions workflow file was created.
- The workflow works to install required dependencies, execute fuzzing script, and marks the build if fuzzing crashes.
<img width="1520" height="633" alt="image" src="https://github.com/user-attachments/assets/36c5ab0a-5754-403a-aa44-ab8b4c6c85c0" />

## Step 5 - Lessons Learned
Throughout working on this project, here are the things that I learned:
- Fuzz testing helps with showing what happens when providing unpredictable inputs, which can help with finding bugs and errors in functions provided.
- Forensic logging helps with showing key parameters and errors, along with providing evidence of function behavior.
- Using Github actions for continuous integration is useful for make sure that code is correct and prevents issues with every commit. 



