import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
sys.path.append('BMassets')
sys.path.append('BMdata')
sys.path.append('BMmain')

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import Config
from user import User
from user_manager import UserManager
from database import create_connection,close_connection
Window.size = (360, 640)
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'fullscreen', '0')


Builder.load_string('''
<LoginScreen>:
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: 199/255, 233/255, 176/255, 1
            Rectangle:
                pos: self.pos
                size: self.size
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
            height: 60
            spacing: 30  # Added spacing between buttons

            Button:
                text: 'Back'
                background_normal: '../BMassets/button2.png'
                background_down: '../BMassets/button1.png'
                on_release: root.manager.current = 'menu_screen'
            Button:
                text: 'Login'
                background_normal: '../BMassets/button2.png'
                background_down: '../BMassets/button1.png'
                on_release: root.login()

''')

class LoginScreen(Screen):

    def login(self):
        entered_username = self.ids.username_input.text
        entered_password = self.ids.password_input.text
        user = User.get_user(create_connection(), entered_username, entered_password)

        if not user:
            print("Authentication failed.")
        else:
            UserManager.set_current_user(user)  # Store the user in UserManager
            print("Authentication successful.")
            #self.send_email(user.email,"You have just logged in!")
            self.manager.current = 'home_screen'

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
    
    
