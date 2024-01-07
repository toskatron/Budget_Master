import sys
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from kivy.metrics import dp
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.popup import Popup
import matplotlib.pyplot as plt
from collections import defaultdict
from user_manager import UserManager
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
sys.path.append('BMdata')
from database import *
from kivy.core.window import Window
from kivy.config import Config

Window.size = (360, 640)
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'fullscreen', '0')

Builder.load_string('''
<StatisticsScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)
        canvas.before:
            Color:
                rgba: (221/255, 1, 187/255, 1)
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: 'Statistics'
            font_size: '20sp'
        Button:
            text: 'Get advanced statistics'
            background_color: 0.2, 0.5, 0.2, 1  # Dark green button
            background_normal: ''
            canvas.before:
                Color:
                    rgba: 0, 0.3, 0, 1  # Slightly different green for the button
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [25,]
            on_release: root.advanced_statistics()

        BoxLayout:
            id: pie_chart_layout
            size_hint_y: None
            height: dp(200)
            rgba: (221/255, 1, 187/255, 1)

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(30)

            Label:
                text: 'Total Expenses: '
                size_hint_x: 0.3
                color: 0, 0, 0, 1

            Label:
                id: total_expenses_label
                text: '0'
                size_hint_x: 0.7
                color: 0, 0, 0, 1

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(30)

            Label:
                text: 'Money Left:: '
                size_hint_x: 0.3
                color: 0, 0, 0, 1

            Label:
                id: money_left_label
                text: '0'
                size_hint_x: 0.7
                color: 0, 0, 0, 1

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
                on_release: root.manager.current = 'home_screen'
            Button:
                size_hint: None,None
                size: dp(50), dp(50)
                background_normal:'../BMassets/expenses.png'
                on_release: root.manager.current = 'add_expense_screen'
            Button:
                size_hint: None,None
                size: dp(50), dp(50)
                background_normal:'../BMassets/statistics.png'
                on_release: root.show_popup()
''')

class StatisticsScreen(Screen):
    def draw_new_pie_chart(self):
        self.ids.pie_chart_layout.clear_widgets()  
        self.draw_pie_chart()  

    def on_pre_enter(self):
        self.update_statistics_labels()
        self.draw_pie_chart()

    def update_statistics_labels(self):
        total_expenses = self.calculate_total_expenses()
        money_left_expense = self.calculate_money_left_expense(total_expenses)

        self.ids.total_expenses_label.text = str(total_expenses) + '$'
        self.ids.money_left_label.text = str(money_left_expense) + '$'

    def calculate_total_expenses(self):
        connection = create_connection()
        cursor = connection.cursor()
        query = "SELECT sum(amount) FROM expenses"
        cursor.execute(query)
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if result[0]:
            return result[0]
        else:
            return 0

    def calculate_money_left_expense(self, total):
        connection = create_connection()
        user = UserManager.get_current_user()

        income_amount = get_income(connection,user.username)
        money_left = income_amount - int(total)
        print(income_amount)
        print(total)
        return money_left
    
        close_connection(connection)
        

    def show_popup(self):
        popup_content = Label(text='You are already on Statistics')
        popup = Popup(title='Warning', content=popup_content, size_hint=(None, None), size=(250, 100))
        popup.open()

    def draw_pie_chart(self):
        conn = create_connection()
        if conn is not None:
            user = UserManager.get_current_user()
            expenses_User = get_expenses_of_user(conn,user.username)
            category_expenses = {}
            for expense in expenses_User:
                category = expense['category']
                amount = expense['amount']

                if category in category_expenses:
                    category_expenses[category] += amount
                else:
                    category_expenses[category] = amount
            fig, ax = plt.subplots()
            labels = list(category_expenses.keys())
            expenses_User = list(category_expenses.values())

            ax.pie(expenses_User, labels=labels, autopct='%1.1f%%')
            pie_chart_widget = FigureCanvasKivyAgg(figure=fig)

            self.ids.pie_chart_layout.clear_widgets()
            self.ids.pie_chart_layout.add_widget(pie_chart_widget)
            pie_chart_widget.size_hint = (1, 1) 

            close_connection(conn)

    def advanced_statistics(self):
        conn = create_connection()
        user = UserManager.get_current_user()
        username = user.username
        cursor = conn.cursor()

        query = "SELECT category, description, amount FROM expenses WHERE user = %s"
        cursor.execute(query, (user.username,))
        expenses = cursor.fetchall()

        # Initialize dictionaries to store category-wise and description-wise totals
        category_totals = {}
        description_totals = {}

        # Initialize variables to track the day with the most expenses
        day_expenses = {}
        max_day = None
        max_expenses = 0

        # Calculate totals and identify the day with the most expenses
        for category, description, amount in expenses:
            if category not in category_totals:
                category_totals[category] = 0
            if description not in description_totals:
                description_totals[description] = 0

            category_totals[category] += amount
            description_totals[description] += amount

        close_connection(conn)    
        # Create the statistics message
        message = f"Dear {username}, here are your advanced statistics:\n"
        for category, total in category_totals.items():
            message += f"{category}: {total:.2f}\n"

        
        self.send_email(user.email,message)
        print('Email sent succesfully!')




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


