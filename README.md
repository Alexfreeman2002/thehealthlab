# The Health Lab
## Introduction
_**The Health Lab**_ is a health guide and goal tracker web application that provides multiple functions, for example, 
searching diseases, BMI calculator, etc. to meet the daily health needs of the majority of contemporary individuals. 
It aims to encourage a wide range of people to pay attention to their health and help people who want to improve their 
health conditions.

## Dependencies and Usage
The link below will direct you to the group's repository for the application.  The repository includes all the required 
files to run the application.  The files include python files for back-end code, html files containing front-end code
text files used to log user actions, database connections and test files.

https://github.com/newcastleuniversity-computing/CSC2033_Team9_22-23

The SQLite database is initialised by using the following code in the python console.

from app import db

from models import initdb

init_db()

By doing this allows the database to be created and contain a field for the admin in the users table.


Requirements.txt file contains a list of libraries used to create and run the application.  To install these packages 
the user can use the following command in the python console.

'pip install **library package**'

'**library package**' will be changed with the name of the package stated in the requirements.txt file, 'Flask' for example.



## Target Audience
The **target audience** of this web application can be broadly categorized into the following four groups:
1. People who want to explore more knowledge of health.
2. People who want to learn more about their disease to eliminate fear and get help.
3. People who used to live in an unhealthy lifestyle, but is seeking a way to make changes.
4. Fitness enthusiasts who are looking for an app with clean UI, efficient search functionality, and accurate calculation.

## Technologies
Solution: Web Application compatible with desktop and mobile (responsive website).
##### Front End:
- CSS
- HTML5
- JavaScript
##### Back End:
- Python Flask 
##### Database:
- SQLite 


### Register

#### Inputs

* Email- must match email format
* Username- can’t contain special character
* Password- must contain a number, special character, lowercase and uppercase character and be between 6-12 characters long
* Confirm Password- must match password field
* Submit Button- takes data entered to check if it's correct, can also be used by pressing ‘enter’ key on keyboard
#### Outputs

* Pop-Up message- appears next to a field which hasn't been given any data
* Error Message- appears when invalid data has been entered in a field
* Login Page- sends user to login page when valid information has been entered
#### Database
After register, data is stored in the database, this includes:
* The current users ID, this is their account number
* Their email, username, password(salted), role, pinkey, registered on date, current login and last login

### Login
#### Inputs

* Email- must match email format
* Password- any string can be entered
* Pin- any integer can be entered
* Recaptcha-complete recaptcha ‘I’m not a robot test’ questions
* Submit Button- takes data entered to check if it's correct, can also be used by pressing ‘enter’ key on keyboard 

#### Outputs
* Pop-Up message- appears next to a field which hasn’t been given any data
* Error Message- appears when invalid data has been entered
* Account Page- sends user to account page when valid information has been entered, and they are a user
* Admin Page- sends user to admin page when valid information has been entered, and they are an admin


### Body Mass Index Calculator
#### Inputs
Upon loading the BMI calculator there will be four input boxes:
* Height: enter the numeric value for your height, measured  in either feet or centimetres
* Measurement: enter 'cm' or  'feet', to specify which measurement your height is in
* Weight: enter the numeric value for your weight, measured  in either feet or centimetres
* Measurement: enter 'kg' or 'lbs', to specify which measurement your weight is in
<p>After inputting this data correctly use the 'calculate' button to have your bmi calculated</p>

#### Outputs
If all the data in the fields are inputted correctly and the button is pressed the user will be taken to another webpage
* This webpage will display the users BMI 
* Guidance will be given below to what the BMI means for their health
* Information about the accuracy of Body Mass Indexes will also be given

#### Database
After calculating the BMI, data is stored in the database, this includes:
* The current users ID, this is their account number
* Their height, weight and resulting BMI

### Calorie Calculator
#### Inputs
Upon loading the calorie calculator there will be three input boxes:
* Carbohydrates: enter your daily goal of carbohydrates in grams
* Protein: enter your daily goal of protein in grams
* Fat: enter your daily goal of protein in grams
<p>After inputting this data correctly use the 'calculate' button to have your daily calories calculated</p>

#### Outputs
If all the data in the fields are inputted correctly and the button is pressed the user will be taken to another webpage
* This webpage will display the users calorie goals, calculated form their inputs
* Information will be given about recommended calorie intake for men and women

#### Database
After calculating the calorie goal, data is stored in the database, this includes:
* The current users ID, this is their account number
* Their calorie goal

### Calorie Counter
#### Inputs
Upon loading the calorie counter there will be two input boxes:
* Date: enter the date you wish to either add to or create an entry for
* Calories: enter the calories you wish to add for the date given above

#### Outputs
If the entry already exists, and you choose to create a new entry an error page will be displayed.
* If the entry already exists, and you choose to add to it, a success page will be displayed.
* If the entry doesn't exist, and you choose to create a new entry a success page will be shown.
* If the entry doesn't exist, and you choose to add to it, an error page will be shown.
* If you choose to view an existing entry and there isn't any, an error page will be shown.
* If you choose to view an existing entry, and it does exist, then you will be shown the entries.

#### Database
If the user creates an entry successfully, data is stored in the database, this includes:
* The current users ID, this is their account number
* The entry date
* The calories
* If the user successfully chooses to add to an entry then the calories column is changed to the new total calories for that entry

### Period Tracker
#### Inputs
Upon loading the Period Tracker there will be four input boxes:
* Start date: enter the last start date of user's period
* End date: enter the last end date of user's period
* Period duration: enter the integer value for user's duration of period
* Period cycle: enter the integer value for user's cycle of period
<p>After inputting this data correctly use the 'track' button to have user's period tracked</p>

#### Outputs
If all the data in the fields are inputted correctly and the button is pressed the user will be taken to another webpage
* This webpage will display the prediction of user's next start date of period
* This webpage will display the prediction of user's next end date of period
* This webpage will display the prediction of user's ovulation date 
* The tip with human care will display below the results

#### Database
After tracking the next period, data is stored in the database, this includes:
* The current users ID, this is their account number
* Their start date, end date, period duration, period cycle, next start date, next end date, and date of ovulation