import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock

from kivy.core.window import Window


import random as rand

size = (720, 1280)
Window.size = (720, 1280)

class ImmageButton(ButtonBehavior, Image):
    pass

class COIN(Image):
    def __init__(self, **kwargs):
        super(COIN, self).__init__(**kwargs)

        self.velocity_y = 0
        self.gravity = -0.5
        
        self.velocity_x = 0
    
    def bounce(self):
        self.velocity_y = 10
        self.velocity_x = rand.randint(-5, 5)
    
    def update(self, dt):
        self.y += self.velocity_y
        self.velocity_y += self.gravity
        self.x += self.velocity_x
    

class Main(App):
    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)
        
        
        
    count = 0
    tick = 0
    
    def build(self):
        self.layout = FloatLayout()
        
        self.count_text = Label(
            text=f"Click Coin: {self.count}",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.8},
            font_size='24sp'
        )
        self.layout.add_widget(self.count_text)
        
        self.button_img = ImmageButton(
            source='src/full_button.png',
            size_hint=(None, None),
            size=(100, 100),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
            on_press=self.on_button_click,
            on_release=self.on_button_release,
            allow_stretch=True,
            keep_ratio=True
        )
        
        self.layout.add_widget(self.button_img)
        
        self.coins: list[COIN] = []
        for _ in range(30):
            
            coin = COIN(
                source='src/coin.png',
                size_hint=(None, None),
                size=(64, 64),
                pos=(-100, -100),
                allow_stretch=True,
                keep_ratio=True
            )
            self.coins.append(
                coin
            )
            self.layout.add_widget(coin)
        
        
        Clock.schedule_interval(self.update_tick, 1.0 / 60.0)
        

        return self.layout
    
    c_pos = 0
    actives: list[COIN] = []
    def flip_coin(self):
        global size
        if self.c_pos > len(self.coins) - 1:
            self.c_pos = 0
        self.coins[self.c_pos].pos = (size[0] / 2 - self.coins[self.c_pos].size[0] / 2, size[1] / 2 - self.coins[self.c_pos].size[1] / 2)
        self.coins[self.c_pos].bounce()
        self.actives.append(self.coins[self.c_pos])
        self.c_pos += 1
        
        
    def on_button_click(self, instance):
        # print("Button clicked!")
        self.button_img.source = 'src/button_press.png'
        self.flip_coin()
        self.count += 1
    
    
        
    
    def on_button_release(self, instance):
        # print("Button released!")
        self.button_img.source = 'src/full_button.png'
        
    
    def update_tick(self, dt):
        self.count_text.text = f"Clicks Coin: {self.count}"
        
        for active in self.actives:
            active.update(dt)
            if active.y < -100:
                active.pos = (-100, -100)
                self.actives.remove(active)


if __name__ == "__main__":
    Main().run()