# Python script to track application name on click 

Python script that will run on the operating system startup and keep a record of which application you click on in a text (.txt) file format. Also the script will send an email with the record.txt file to a specified email address every 2 minutes.


### Configuration
Open the tracker.py file and adjust the following variable
 ```
 1. BASE_DIR
 2. FILE_NAME
 3. SENDER_EMAIL
 4. RECEIVER_EMAIL
 5. PASSWORD
 6. INTERVAL
 ```

### Run in background
To run the script in OS startup, specially for windows, you need to follow the below steps
 ```
 1. Convert the script to executable exe file
 2. Put the exe file into windows startup directory
 3. On OS start the executable script will automatically run in background
 ```