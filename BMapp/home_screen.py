import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.popup import Popup
from login_screen import LoginScreen
from user_manager import UserManager

sys.path.append('BMdata')
from database import create_connection, create_expenses_table, insert_expense, close_connection, get_income, update_income,get_tip



Builder.load_string('''
<HomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        padding: dp(11)
        canvas.before:
            Color:
                rgba: 199/255, 233/255, 176/255, 1
            Rectangle:
                pos: self.pos
                size: self.size
        
        BoxLayout:
            size_hint:1,0.1
            height:dp(200)
            AnchorLayout:
                anchor_x: 'center'
                anchor_y: 'top'
                Image:
                    source: '../BMassets/mylogo.png'  
                    size: 100, 100
                    

        BoxLayout:
            size_hint: 1, None
            height: dp(40)
            orientation: 'horizontal'
            canvas.before:
                Color:
                    rgba: (199/255, 233/255, 176/255, 1)
                Rectangle:
                    pos: self.pos
                    size: self.size

            Label:
                text: 'For some great tips press the button:'
                size_hint_x: 0.2
                color: 0, 0, 0, 1    

        BoxLayout:
            size_hint: 1, None
            height: dp(50)
            spacing: dp(22)
            Button:
                text: 'GET EMAIL'
                font_size: '20sp'
                background_color: 0.2, 0.5, 0.2, 1  # Dark green button
                background_normal: ''
                on_release: root.send_email_tips()


        

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(30)

            Label:
                text: 'Your monthly budget: '
                color: 0, 0, 0, 1
                size_hint_x: 0.3
                size: dp(60), dp(30)

            Label:
                id: budget_label
                text: '0'
                color: 0, 0, 0, 1
                size_hint_x: 0.2
            
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None 
            height: dp(30)

            Label:
                text: 'Do you wish to change it?'
                size_hint_x: 0.2
                color: 0, 0, 0, 1

            BoxLayout:
                size_hint: None,None
                size: dp(60), dp(30)
                TextInput:
                    id: budget_input

            Button:
                text: 'Edit'
                size_hint: None,None
                size: dp(60), dp(30)
                background_normal: '../BMassets/button2.png'
                background_down: '../BMassets/button1.png'
                on_release: root.edit_budget()
            
        BoxLayout:
            size_hint: 1, None
            height: dp(40)
            canvas.before:
                Color:
                    rgba: (199/255, 233/255, 176/255, 1)  # DDFFBB
                Rectangle:
                    pos: self.pos
                    size: self.size

        BoxLayout:
            size_hint: 1, None
            height: dp(10)
            canvas.before:
                Color:
                    rgba: (199/255, 233/255, 176/255, 1)  # DDFFBB
                Rectangle:
                    pos: self.pos
                    size: self.size

        BoxLayout:
            size_hint: 1, None
            height: dp(10)
            canvas.before:
                Color:
                    rgba: (199/255, 233/255, 176/255, 1)
                Rectangle:
                    pos: self.pos
                    size: self.size

        BoxLayout:
            size_hint: 1, None
            height: dp(50)
            spacing: dp(22)
            Button:
                size_hint: None,None
                size: dp(50), dp(50)
                background_normal:'../BMassets/exit.png'
                on_release: app.stop()
            Button:
                size_hint: None,None
                size: dp(50), dp(50)
                background_normal:'../BMassets/logout.png'
                on_release: root.manager.current = 'login_screen'
            Button:
                size_hint: None,None
                size: dp(50), dp(50)
                background_normal:'../BMassets/home.png'
                on_release: root.show_popup()
            Button:
                size_hint: None,None
                size: dp(50), dp(50)
                background_normal:'../BMassets/expenses.png'
                on_release: root.manager.current = 'add_expense_screen'
            Button:
                size_hint: None,None
                size: dp(50), dp(50)
                background_normal:'../BMassets/statistics.png'
                on_release: root.manager.current = 'statistics_screen'

''')

class HomeScreen(Screen):
    def on_pre_enter(self):
        self.update_budget_label()
        

    def update_budget_label(self):
        budget = self.get_budget_value()
        self.ids.budget_label.text = str(budget)+'$'

    def edit_budget(self):
        newbudget = self.ids.budget_input.text
        conn = create_connection()
        if conn is not None:
            update_income(conn,newbudget)
            close_connection(conn)
        self.ids.budget_label.text = str(newbudget)+'$' 

    def get_budget_value(self):
        conn = create_connection()
        user = UserManager.get_current_user()
        if conn is not None:
            inc = get_income(conn,user.username)
            close_connection(conn)
            return inc

    def show_popup(self):
        popup_content = Label(text='You are already on Home Screen')
        popup = Popup(title='Warning', content=popup_content, size_hint=(None, None), size=(250, 100))
        popup.open()

    def send_email_tips(self):
        user = UserManager.get_current_user()
        conn = create_connection()
        tip = get_tip(conn)
        close_connection(conn)
        self.send_email(user.email,tip)

    def send_email(self,email,message):
        # Email configuration
        sender_email = 'tdusan2002@gmail.com'
        sender_password = 'fmtt ivvi rtqg vtyf'
        receiver_email = email
        subject = 'Tip of the day'

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






    