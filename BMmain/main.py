import sys
import smtplib
import random
from kivy.metrics import dp
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.image import Image
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from kivy.core.window import Window
from kivy.config import Config
sys.path.append('BMapp')
sys.path.append('BMassets')

from login_screen import LoginScreen
from signup_screen import SignUpScreen
from home_screen import HomeScreen
from add_expense_screen import AddExpenseScreen
from statistics_screen import StatisticsScreen

Window.size = (360, 640)
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'fullscreen', '0')

Builder.load_string('''
<MenuScreen>:
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: 199/255, 233/255, 176/255, 1
            Rectangle:
                pos: self.pos
                size: self.size
        Image:
            source: '../BMassets/mylogo.png'

        BoxLayout:
            orientation: 'vertical'
            padding: dp(50)
            spacing: dp(20)
            
            Button:
                text: 'Login'
                font_size: '20sp'
                size_hint: None, None
                size: dp(250), dp(50)
                pos_hint: {'center_x': 0.5}
                background_color: 0.2, 0.5, 0.2, 1  # Dark green button
                background_normal: ''
                canvas.before:
                    Color:
                        rgba: 0, 0.3, 0, 1  # Slightly different green for the button
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [25,]
                on_release: root.manager.current = 'login_screen'

            Button:
                text: 'Sign Up'
                font_size: '20sp'
                size_hint: None, None
                size: dp(250), dp(50)
                pos_hint: {'center_x': 0.5}
                background_color: 0.2, 0.5, 0.2, 1  # Dark green button
                background_normal: ''
                canvas.before:
                    Color:
                        rgba: 0, 0.3, 0, 1  # Slightly different green for the button
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [25,]
                on_release: root.manager.current = 'signup_screen'
''')

class MenuScreen(Screen):
    pass



class BudgetMaster(App):
    def build(self):
        sm = ScreenManager()  
        sm.add_widget(MenuScreen(name='menu_screen'))
        sm.add_widget(LoginScreen(name='login_screen'))
        sm.add_widget(SignUpScreen(name='signup_screen'))
        sm.add_widget(HomeScreen(name='home_screen'))
        sm.add_widget(AddExpenseScreen(name='add_expense_screen'))
        sm.add_widget(StatisticsScreen(name='statistics_screen'))
        sm.current = 'menu_screen'
        return sm






if __name__ == '__main__':
    BudgetMaster().run()