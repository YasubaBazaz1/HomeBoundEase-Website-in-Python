from flask import Flask, render_template, request, redirect, url_for, session,flash
import mysql.connector
# import MySQLdb.cursors
import re

# database connection 
app = Flask(__name__)
app.secret_key = 'your secret key'

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Yasubabazaz06!",
  database = "mysql"
)

mycursor = mydb.cursor()

# mycursor.execute("SELECT * FROM userProfile")
# myresult = mycursor.fetchall()
# for x in myresult:
#   print(x)

@app.route('/login', methods=['GET', 'POST'])

def login():
    msg = ''  # Initialize the error message variable
    if request.method == 'POST' and 'userEmail' in request.form and 'password' in request.form:
        userEmail = request.form['userEmail']
        password = request.form['password']

        mycursor.execute("SELECT * FROM userProfile WHERE email = %s AND password = %s", (userEmail, password,))
        account = mycursor.fetchall()

        if account:
            fullName = account[0][1]
            session['logged_in'] = True
            session['username'] = fullName
            session['email'] = userEmail
            session['currentid'] = account[0]

            if userEmail == 'admin@gmail.com':
                return redirect(url_for('admin'))

            return redirect(url_for('userDashboard'))
        else:
            print("Authentication failed")
            msg = 'Incorrect username/password!'

            # Check if the email exists in the database
            mycursor.execute("SELECT * FROM userProfile WHERE email = %s", (userEmail,))
            if mycursor.fetchone() is None:
                msg = 'Email does not exist. Please register.'

    return render_template('userLoginPage.html', msg=msg)


@app.route('/userSignUp', methods=['GET', 'POST'])
def userSignUp():
    if request.method == 'POST' and 'userFullName' in request.form and 'userPhoneNum' in request.form and 'userGender' in request.form and 'userEmail' in request.form and 'userPassword' in request.form:
        userFullName = request.form['userFullName']
        userPhoneNum = request.form['userPhoneNum']
        userEmail = request.form['userEmail']
        userGender = request.form['userGender']
        password = request.form['userPassword']

        print(userFullName,userPhoneNum,userEmail,userGender,password)

        mycursor.execute("INSERT INTO userProfile (fullName, phoneNumber, gender, email, password) VALUES (%s, %s, %s, %s, %s)" , (userFullName, userPhoneNum, userGender, userEmail, password,))
        mydb.commit()
        return redirect(url_for('userAccCreated'))

    return render_template('userSignUp.html')

@app.route('/admin')
def admin():
    # Fetch user profile data from the database
    mycursor.execute("SELECT * FROM userProfile")
    userProfiles = mycursor.fetchall()

    # Fetch service provider data from the database
    mycursor.execute("SELECT * FROM serviceProviderProfile")
    serviceProviderProfiles = mycursor.fetchall()

    # Pass data to the template
    return render_template('adminDashboard.html', userProfile=userProfiles, serviceProviderProfile=serviceProviderProfiles )

@app.route('/spLoginPage', methods=['GET', 'POST'])
def spLoginPage():
    msg = ''
    if request.method == 'POST' and 'spEmail' in request.form and 'spPassword' in request.form:
        spEmail = request.form['spEmail']
        spPassword = request.form['spPassword']

        mycursor.execute("SELECT * FROM serviceProviderProfile WHERE businessEmail = %s AND password = %s" , (spEmail, spPassword,))
        spaccount = mycursor.fetchall()

        if spaccount:
            session['logged_in'] = True
            businessName = spaccount[0][1]
            session['businessName'] = businessName
            spID = spaccount[0][0]
            session['sp_id'] = spID
            return redirect(url_for('spDashboard'))
        else:
            print("Authentication failed")
            msg = 'Incorrect username/password!'

            # Check if the email exists in the database
            mycursor.execute("SELECT * FROM serviceProviderProfile WHERE businessEmail = %s", (spEmail,))
            if mycursor.fetchone() is None:
                msg = 'Email does not exist. Please register.'

    return render_template('spLoginPage.html', msg=msg)


@app.route('/spSignUp', methods=['GET', 'POST'])
def spSignUp():
    if request.method == 'POST' and 'spName' in request.form and 'spUENnumber' in request.form and 'spEmail' in request.form and 'spPhoneNum' in request.form and 'spPassword' in request.form:
        spName = request.form['spName']
        spUENnumber = request.form['spUENnumber']
        spEmail = request.form['spEmail']
        spPhoneNum = request.form['spPhoneNum']
        spPassword = request.form['spPassword']

        print(spName,spUENnumber,spPhoneNum,spEmail,spPassword)

        mycursor.execute("INSERT INTO serviceProviderProfile (businessName, UENnumber, businessEmail,businessPhoneNumber, password) VALUES (%s, %s, %s, %s, %s)" , (spName, spUENnumber, spEmail,spPhoneNum, spPassword,))
        mydb.commit()
        return redirect(url_for('spAccCreated'))

    return render_template('spSignUp.html')


@app.route('/userForgotPassword', methods=['GET', 'POST'])
def userForgotPassword():

    if request.method == 'POST' and 'userEmail' in request.form and 'newPassword' in request.form:
        # Get email and new password from the form
        user_email = request.form['userEmail']
        new_password = request.form['newPassword']
        print(user_email,new_password)

        # Check if email exists in the database
        mycursor.execute("SELECT * FROM userProfile WHERE email = %s", (user_email,))
        account = mycursor.fetchall()
        print(account)

        if account:
            # Update password for the user
            mycursor.execute("SET SQL_SAFE_UPDATES = 0;")
            mycursor.execute("UPDATE userProfile SET password = %s WHERE email = %s", (new_password, user_email))
            mydb.commit()
            print('successfully changed')

            # Redirect to login page or any other page
            return redirect(url_for('login'))
 
    return render_template('userForgotPassword.html')

@app.route('/spForgotPassword', methods=['GET', 'POST'])
def spForgotPassword():
    if request.method == 'POST' and 'spEmail' in request.form and 'newPassword' in request.form:
        spEmail = request.form['spEmail']
        new_password = request.form['newPassword']
        print(spEmail,new_password)

         # Check if email exists in the database
        mycursor.execute("SELECT * FROM serviceProviderProfile WHERE businessEmail = %s", (spEmail,))
        account = mycursor.fetchall()
        print(account)
        if account:
            # Update password for the user
            mycursor.execute("SET SQL_SAFE_UPDATES = 0;")
            mycursor.execute("UPDATE serviceProviderProfile SET password = %s WHERE businessEmail = %s", (new_password, spEmail))
            mydb.commit()
            print('successfully changed')

            # Redirect to login page or any other page
            return render_template('spPassChanged.html')
        
    return render_template('spForgotPassword.html')

@app.route('/userAccCreated')
def userAccCreated():
    return render_template('userAccountCreated.html')

@app.route('/spAccCreated', methods=['GET', 'POST'])
def spAccCreated():

    return render_template('spAccountCreated.html')

@app.route('/userContactUsPage', methods=['GET', 'POST'])   
def userContactUsPage():
    if request.method == 'POST' and 'Name' in request.form and 'Email' in request.form and 'Query' in request.form: 
            spName = request.form['Name']
            spEmail = request.form['Email']
            Query = request.form['Query']
 
            mycursor.execute("INSERT INTO userContactUs (name,email,query) VALUES (%s,%s, %s)", (spName,spEmail,Query,))
            mydb.commit()
            return render_template('userContactFormSent.html') 
        
    return render_template('userContactUsPage.html')

@app.route('/spContactUsPage', methods=['GET', 'POST'])
def spContactUsPage():
    if request.method == 'POST' and 'Name' in request.form and 'Email' in request.form and 'Query' in request.form: 
            spName = request.form['Name']
            spEmail = request.form['Email']
            Query = request.form['Query']
 
            mycursor.execute("INSERT INTO spContactUs (name,email,query) VALUES (%s,%s, %s)", (spName,spEmail,Query,))
            mydb.commit()
            return render_template('spContactFormSent.html') 
        
    return render_template('spContactUsPage.html')

@app.route('/spMyProfile', methods=['GET', 'POST'])
def spMyProfile():
        spID = session['sp_id']
        mycursor.execute("SELECT * FROM serviceProviderProfile WHERE spID = %s", (spID,))
        serviceProviderProfile = mycursor.fetchone()
        return render_template('spMyProfile.html',  serviceProviderProfile= serviceProviderProfile)

@app.route('/spUpdateMyProfile' , methods=['GET', 'POST'])
def spUpdateMyProfile():

     if request.method == 'POST' and 'businessPhone' in request.form and 'businessEmail' in request.form and 'password' in request.form:
        phone = request.form['businessPhone']
        businessEmail = request.form['businessEmail']
        password = request.form['password']

        #print(email,phone, businessEmail,)
        # Update password for the user
        mycursor.execute("SET SQL_SAFE_UPDATES = 0;")
        mycursor.execute("UPDATE serviceProviderProfile SET businessPhoneNumber = %s , password = %s WHERE businessEmail = %s", (phone, password, businessEmail, ))
        mydb.commit()
        return redirect(url_for('spMyProfile'))
        print('successfully changed')

      # Fetch user profile data from the database
        mycursor.execute("SELECT * FROM userProfile WHERE email = %s", (email,))
        userProfile = mycursor.fetchone()
        print(userProfile)
        return render_template('userUpdateMyProfile.html', userProfile=userProfile)

     else :
            #email = session['email']
            spID = session['sp_id']
            mycursor.execute('SELECT * FROM serviceProviderProfile WHERE spID = %s',(spID,))
            serviceProviderProfile = mycursor.fetchone()
            print('not working')
            return render_template('spUpdateMyProfile.html', serviceProviderProfile = serviceProviderProfile)

@app.route('/userMyProfile',  methods=['GET', 'POST'])
def userMyProfile():
    email = session['email']
    print(email)
      # Fetch user profile data from the database
    mycursor.execute("SELECT * FROM userProfile WHERE email = %s", (email,))
    userProfile = mycursor.fetchone()
    session['currentid'] = userProfile[0]
    currentid = session['currentid']
    print(currentid, "current id")


    print(userProfile[1])

    # Pass data to the template
    return render_template('userMyProfile.html', userProfile=userProfile)

@app.route('/userHealthRecords', methods=['GET', 'POST'])
def userHealthRecords():
    currentid = session['currentid']
    print(currentid)
    email = session['email']
    print(email)
      # Fetch user profile data from the database
    mycursor.execute("SELECT * FROM userHealthRecords WHERE hrUserID = %s", (currentid,))
    userHealthRecords = mycursor.fetchone()
    return render_template('userHealthRecords.html', userHealthRecords = userHealthRecords)

@app.route('/userUpdateHealthRecords', methods=['GET', 'POST'])
def userUpdateHealthRecords():
     if request.method == 'POST' and 'Age' in request.form and 'Height' in request.form and 'Weight' in request.form and 'knownillnesses' in request.form and 'medicationList' in request.form and 'drugAllergy' in request.form:
        age = request.form['Age']
        height = request.form['Height']
        weight = request.form['Weight']
        knownillnesses = request.form['knownillnesses']
        medicationList = request.form['medicationList']
        drugAllergy = request.form['drugAllergy']
        currentid = session['currentid']
        # Update password for the user
        print(age)
        mycursor.execute("SET SQL_SAFE_UPDATES = 0;")
        mycursor.execute("UPDATE userHealthRecords SET age = %s, height = %s, weight = %s , knownillnesses = %s , medicationList = %s, drugAllergy = %s  WHERE hrUserID = %s", (age, height, weight, knownillnesses, medicationList,  drugAllergy, currentid,))
        mydb.commit()
        return redirect(url_for('userHealthRecords'))
        print('successfully changed')

      # Fetch user profile data from the database
        mycursor.execute("SELECT * FROM userProfile WHERE email = %s", (email,))
        userProfile = mycursor.fetchone()
        print(userProfile)
        return render_template('userUpdateMyProfile.html', userProfile=userProfile)

     else :
            currentid = session['currentid']
            mycursor.execute('SELECT * FROM userHealthRecords WHERE hrUserID = %s',(currentid,))
            userHealthRecords = mycursor.fetchone()
            print('not working')

     return render_template('userUpdateHealthRecords.html', userHealthRecords=userHealthRecords)

@app.route('/userUpdateMyProfile',  methods=['GET', 'POST'])
def userUpdateMyProfile():
     if request.method == 'POST' and 'phone' in request.form and 'email' in request.form:
        phone = request.form['phone']
        email = request.form['email']
        email1 = session['email']
        password = request.form['password']

        print(email,phone, email1,)
        # Update password for the user
        mycursor.execute("SET SQL_SAFE_UPDATES = 0;")
        mycursor.execute("UPDATE userProfile SET phoneNumber = %s , password = %s WHERE email = %s", (phone, password, email, ))
        mydb.commit()
        return redirect(url_for('userMyProfile'))
        print('successfully changed')

      # Fetch user profile data from the database
        mycursor.execute("SELECT * FROM userProfile WHERE email = %s", (email,))
        userProfile = mycursor.fetchone()
        print(userProfile)
        return render_template('userUpdateMyProfile.html', userProfile=userProfile)

     else :
            email = session['email']
            mycursor.execute('SELECT * FROM userProfile WHERE email = %s',(email,))
            userProfile = mycursor.fetchone()
            print('not working')
     return render_template('userUpdateMyProfile.html', userProfile=userProfile)



def get_services():
    try:
        query = """
            SELECT services.*, serviceProviderProfile.businessName, serviceProviderProfile.businessPhoneNumber
            FROM services
            INNER JOIN serviceProviderProfile ON services.spServiceID = serviceProviderProfile.spID
        """
        mycursor.execute(query)
        services = mycursor.fetchall()
        print(services, "get_services area")
        return services
    except mysql.connector.Error as err:
        print("Error fetching services:", err)
        return None
    

def get_spServices():
    try:
        spID = session['sp_id']
        query = """
            SELECT serviceID, serviceName, serviceDescription, serviceTags,servicePrice
            FROM services
            WHERE spServiceID = %s
        """
        mycursor.execute(query, (spID,))
        SPservices = mycursor.fetchall()
        print(SPservices, "get_services area")
        return SPservices
    except mysql.connector.Error as err:
        print("Error fetching services:", err)
        return None

@app.route('/userDashboard')
def userDashboard():
    if 'logged_in' in session:
        serviceList = get_services()
        if serviceList is None:
            # Handle case where serviceList is None
            return "Error: Unable to fetch services"
        else:
            # Pass the service list to the template
            return render_template('userDashboard.html', serviceList=serviceList)
    else:
        # Redirect to login if not logged in
        return redirect(url_for('login'))


        

@app.route('/spDashboard')
def spDashboard():
     if 'logged_in' in session:
        spID = session['sp_id'] 
        spServiceList = get_spServices()
        print('spdashboard ' , spID)
        if spServiceList is None:
            # Handle case where serviceList is None
            return render_template('spDashboard.html')
        else:
            # Pass the service list to the template
            return render_template('spDashboard.html', spServiceList=spServiceList)
     else:
        # Redirect to login if not logged in
        return redirect(url_for('spLoginPage'))
     
      

@app.route('/addServices', methods=['GET', 'POST'])
def addServices():
     if 'logged_in' in session:
        if request.method == 'POST' and 'serviceName' in request.form and 'serviceDesc' in request.form and 'serviceTags' in request.form and 'servicePrice' in request.form: 
            serviceName = request.form['serviceName']
            serviceDesc = request.form['serviceDesc']
            servicePrice = request.form['servicePrice']
            spId = session['sp_id']
            print('add services' , spId)

        # Retrieve service tag input from the form data
        service_tags_input = request.form.get('serviceTags', '')
        
        # Parse the input to extract individual service tags
        serviceTags = [tag.strip() for tag in service_tags_input.split(',') if tag.strip()]
        
        # Insert service tags into the database
        for x in serviceTags:
            mycursor.execute("INSERT INTO services (spServiceID, serviceName, serviceDescription, serviceTags, servicePrice) VALUES (%s,%s, %s, %s, %s)", (spId,serviceName,serviceDesc, x, servicePrice))
            mydb.commit()
            return render_template('spServiceAddedpage.html') 
        
        return render_template('spAddServices.html') 
    
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('logged_in', None)
   session.pop('id', None)
   session.pop('username', None)
   session.pop('email', None)
   # Redirect to login page
   return redirect(url_for('login'))


