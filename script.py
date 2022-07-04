from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json, glob
from datetime import datetime
from pathlib import Path
import random

Builder.load_file('design.kv')

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"

    def login(self, user, pw):
        with open("users.json") as file:
            users = json.load(file)
        if user in users and users[user]['password'] == pw:
            self.manager.current = "login_screen_success"    
        else:
            self.ids.login_wrong.text = "Incorrect password or username"
        
class SignUpScreen(Screen):
    def add_user(self, user, pw):
        with open("users.json") as file:
            users = json.load(file)

        users[user] = {'username': user, 'password': pw,
            'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
        with open("users.json", 'w') as file:
            json.dump(users, file)

        self.manager.current = "sign_up_screen_success"

class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

class LoginScreenSuccess(Screen):
    def logout(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

    def get_quote(self, feels):
        feels = feels.lower()
        available_feelings = glob.glob("quotes/*txt")
        available_feelings = [Path(filename).stem for filename in available_feelings]

        if feels in available_feelings:
            with open(f"quotes/{feels}.txt") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try another feeling"


class RootWidget(ScreenManager):
    pass

class ImageButton(HoverBehavior, ButtonBehavior, Image):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    MainApp().run()
