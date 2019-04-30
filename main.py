from flask import Flask, request, redirect
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)
 
app = Flask(__name__)
app.config['DEBUG'] = True





@app.route("/")
def display_signup():
    template = jinja_env.get_template("user_signup.html")
    return template.render()

@app.route("/", methods = ['POST'])
def validate_form():
    
    username = request.form['username']
    password = request.form['password']
    verify_password = request.form['verify_password']    
    email = request.form['email']
    
    username_error = ""
    password_error = ""
    verify_password_error = ""
    email_error = ""

    countcurly = email.count('@')
    countdot = email.count(".")
    
    if not username:
        username_error = "Please enter a name"
        username = ""
    
    elif len(username)>20 or len(username)<3:
        username_error = "Username must be between 3 and 20 characters"
        username = ""
    
    else:
        hasSpace = False
        for char in username:
            if char.isspace():
                hasSpace = True               
        if hasSpace:
             username_error = "Username cannot contain spaces"
             username = ""

    if not password:
        password_error = "Please enter a password"
        
    elif len(password)>20 or len(password)<3:
        password_error = "Password must be between 3 and 20 characters"
               

    else:
        hasSpace = False
        for char in password:
            if char.isspace():
                hasSpace = True            
        if hasSpace:
             password_error = "Password cannot contain spaces"
             
    if verify_password != password:
        verify_password_error = "Passwords must match"
     
      
    if email:
        if len(email)>20 or len(email)<3:
            email_error = "Email must be between 3 and 20 characters"
            email = ""
        else:
            if countcurly!=1 or countdot!=1:
                email_error = "Email must contain one @ and one ."
                email = ""
            else:
                hasSpace = False
                for char in email:
                    if char.isspace():
                        hasSpace = True
                if hasSpace:
                    email_error = "Email cannot contain spaces"
                    
    if not password_error and not username_error and not verify_password_error and not email_error:
        name = username 
        return redirect("/valid_signup?name={0}".format(name))



    else:
        template = jinja_env.get_template("user_signup.html")
        return template.render(username=username,username_error=username_error,password=password,password_error=password_error,
      verify_password=verify_password,verify_password_error=verify_password_error,email=email,email_error=email_error)    
    

@app.route("/valid_signup",methods =['GET'])
def valid_signup():
    name = request.args.get('name')
    template = jinja_env.get_template("welcome.html")
    return template.render(name=name)

app.run()