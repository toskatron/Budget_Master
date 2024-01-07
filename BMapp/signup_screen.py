import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
sys.path.append('BMdata')
sys.path.append('BMmain')
from database import close_connection,create_connection,create_users_table,insert_user

# when this page is initialized add an info window witht his info:
# To succesfully create an acoount pleae provide all the inforamtion requested


Builder.load_string('''
<SignUpScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        canvas.before:
            Color:
                rgba: 199/255, 233/255, 176/255, 1
            Rectangle:
                pos: self.pos
                size: self.size

        BoxLayout:
            size_hint: 1, 0.1
            height: 200
            AnchorLayout:
                anchor_x: 'center'
                anchor_y: 'top'
                Image:
                    source: '../BMassets/mylogo.png'  
                    size_hint: 1, 1
                    size: 250, 250
                    pos_hint: {'center_x': 0.5, 'top': 1}  # Adjusted position with 'top' anchor

        BoxLayout:
            orientation:'horizontal'
            size_hint_y: None
            height:30

            Label:
                text:'Full Name:'
                size_hint_x:0.2
                color: 0, 0, 0, 1 
            BoxLayout:
                size_hint_x:0.3
                TextInput:
                    id: name_input

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: 30

            Label:
                text: 'Email: '
                size_hint_x: 0.2
                color: 0, 0, 0, 1 

            BoxLayout:
                size_hint_x: 0.3
                TextInput:
                    id: email_input

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: 30

            Label:
                text: 'Income: '
                size_hint_x: 0.2
                color: 0, 0, 0, 1 

            BoxLayout:
                size_hint_x: 0.3
                TextInput:
                    id: income_input

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: 30

            Label:
                text: 'Username: '
                size_hint_x: 0.2
                color: 0, 0, 0, 1 

            BoxLayout:
                size_hint_x: 0.3
                TextInput:
                    id: username_input

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: 30

            Label:
                text: 'Password: '
                size_hint_x: 0.2
                color: 0, 0, 0, 1 

            BoxLayout:
                size_hint_x: 0.3
                TextInput:
                    id: password_input
                    password: True


        BoxLayout:
            size_hint: 1,None
            height: 50
            spacing: 30  # Added spacing between buttons

            Button:
                text: 'Back'
                background_normal: '../BMassets/button2.png'
                background_down: '../BMassets/button1.png'
                on_release: root.manager.current = 'menu_screen'
            Button:
                text: 'Sign up'
                background_normal: '../BMassets/button2.png'
                background_down: '../BMassets/button1.png'
                on_release: root.signup()
''')


class SignUpScreen(Screen):
    def on_pre_enter(self):
        self.show_popup('To succesfully create an acoount please \nprovide all the inforamtion requested')
        conn = create_connection()
        if conn is not None:
            # Attempt to create the 'users' table
            create_users_table(conn)
            # Close the database connection when done
            close_connection(conn)
        else:
            print("Failed to connect to the database")
    
    def show_popup(self, message):
        popup = Popup(title='Info', content=Label(text=message), size_hint=(None, None), size=(300, 100))
        popup.open()

    def signup(self):
        username = self.ids.username_input.text
        password = self.ids.password_input.text

        if not self.validate_credentials(username, password):
            print("Invalid Credentials")
            return

        self.create_user(username, password)
        self.manager.current = 'login_screen'

    def validate_credentials(self, username, password):
        if len(username) < 3:
            print("Username must be at least 3 characters long")
            return False

        if len(password) < 4:
            print("Password must be at least 4 characters long")
            return False
        return True


    def create_user(self, username, password):
        name = self.ids.name_input.text
        income = self.ids.income_input.text
        email = self.ids.email_input.text
        connection = create_connection()
        if connection is not None:
            insert_user(connection, name, income, username, email, password)
            connection.close()
        else:
            print("Error connecting to the database")
        print(f"New user created: Username: {username}, Password: {password}")
        message = "Welcome {name} we're glad to have you on our app.\nYour log in credentials are as follows:\n Username-{username}\n Password-{password}"
        self.send_email(email,message)

    def send_email(self,email,message):
        # Email configuration
        sender_email = 'tdusan2002@gmail.com'
        sender_password = 'fmtt ivvi rtqg vtyf'
        receiver_email = email
        subject = 'Budget Master App'

        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Connect to the SMTP server and send the email
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            server.quit()
            print('Email sent successfully!')
        except Exception as e:
            print(f'Error sending email: {str(e)}')    
    
   