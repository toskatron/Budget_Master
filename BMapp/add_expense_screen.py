import sys

from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.dropdown import DropDown
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from datetime import date
from user_manager import UserManager
sys.path.append('BMdata')
sys.path.append('BMassets')
from database import *

Builder.load_string('''
<AddExpenseScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        padding: dp(10)
        canvas.before:
            Color:
                rgba: (221/255, 1, 187/255, 1)
            Rectangle:
                pos: self.pos
                size: self.size

        BoxLayout:
            size_hint: 1, None
            height: dp(200)
            BoxLayout:
                orientation: 'vertical'
                size_hint_x: None
                width: self.minimum_width
                Image:
                    source: '../BMassets/mylogo.png'  
                    size_hint: None, None
                    size: dp(200), dp(200)
                    width:dp(340)
                    allow_stretch: True
                    pos_hint: {'center_x': 0.5}

        BoxLayout:
            size_hint: 1, None
            height: dp(40)
            canvas.before:
                Color:
                    rgba: 0xdd / 255, 0xff / 255, 0xbb / 255, 1  # DDFFBB
                Rectangle:
                    pos: self.pos
                    size: self.size

        BoxLayout:
            size_hint: 1, None
            height: dp(10)
            canvas.before:
                Color:
                    rgba: 0xdd / 255, 0xff / 255, 0xbb / 255, 1  # DDFFBB
                Rectangle:
                    pos: self.pos
                    size: self.size

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(30)

            Label:
                text: 'Category: '
                size_hint_x: 0.2
                color: 0, 0, 0, 1 

            BoxLayout:
                size_hint_x: 0.3
                Spinner:
                    id: category_spinner
                    text: ''
                    values: ['Food', 'Transportation', 'Entertainment', 'Shopping', 'Bills', 'Other']
                    background_normal:'../BMassets/category.png'
            BoxLayout:
                size_hint_x: 0.5
                
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(30)

            Label:
                text: 'Amount: '
                size_hint_x: 0.2
                color: 0, 0, 0, 1 

            BoxLayout:
                size_hint_x: 0.3
                TextInput:
                    id: amount_input
                    
            BoxLayout:
                size_hint_x: 0.5
                
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(30)

            Label:
                text: 'Price: '
                size_hint_x: 0.2
                color: 0, 0, 0, 1 

            BoxLayout:
                size_hint_x: 0.3
                TextInput:
                    id: price_input
                    
            BoxLayout:
                size_hint_x: 0.5
                
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(30)

            Label:
                text: 'Description: '
                size_hint_x: 0.2
                color: 0, 0, 0, 1 

            BoxLayout:
                size_hint_x: 0.3
                TextInput:
                    id: description_input
                    
            BoxLayout:
                size_hint_x: 0.5

        Button:
            text: 'Add Expense'
            background_normal: '../BMassets/button2.png'
            background_down: '../BMassets/button1.png'
            on_release: root.add_expense()
            size_hint_y: None
            height: dp(40)
            
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
                on_release: root.show_popup('Already in Add expense')
            Button:
                size_hint: None,None
                size: dp(50), dp(50)
                background_normal:'../BMassets/statistics.png'
                on_release: root.manager.current = 'statistics_screen'

''')



class AddExpenseScreen(Screen):

    def add_expense(self):
        category = self.ids.category_spinner.text
        amount_input = self.ids.amount_input.text
        description = self.ids.description_input.text
        price=self.ids.price_input.text
        user = UserManager.get_current_user()
        if category == 'Select Category':
            self.show_popup('Please select a category.')
            return
        if amount_input:
            try:
                amount = float(amount_input)
            except ValueError:
                self.show_popup('Invalid amount input.')
                return
        else:
            self.show_popup('Please enter the amount.')
            return
        if not description:
            self.show_popup('Please enter a description.')
            return

        conn = create_connection()
        if conn is not None:
            create_expenses_table(conn)
            today = date.today().strftime("%Y-%m-%d")
            final=int(amount)*int(price)
           
            insert_expense(conn, user.username, today, category, description,final)
            close_connection(conn)
        else:
            self.show_popup('Failed to connect to the database.')

        self.ids.category_spinner.text = ''
        self.ids.amount_input.text = ''
        self.ids.description_input.text = ''
        self.ids.price_input.text = ''
        self.show_popup('Expense added successfully.')

    def show_popup(self, message):
        popup = Popup(title='BudgetMaster', content=Label(text=message), size_hint=(None, None), size=(250, 100))
        popup.open()

    
