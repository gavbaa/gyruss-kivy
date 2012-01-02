from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty, ObjectProperty
import math

class Bullet(Widget):
    bullet_size = NumericProperty(5)


class Ship(Widget):
    pass


class Space(FloatLayout):
    app = ObjectProperty(None)
    ship = ObjectProperty(None)

    last_bullet = None
    bullets = None
    is_shooting = False

    def __init__(self, *args, **kwargs):
        super(Space, self).__init__(*args, **kwargs)
        self.bullets = []
        Clock.schedule_interval(self.game_loop, 1 / 30.)

    def game_loop(self, dt):
        #print 'looping', dt
        if self.is_shooting and (self.last_bullet is None or Clock.get_time() - self.last_bullet > 0.25):
            self.add_bullet()
            self.last_bullet = Clock.get_time()
        for b in self.bullets:
            cur_angle = math.atan2((b.y - self.center_y), (b.x - self.center_x))
            magnitude = math.sqrt( math.pow(b.y - self.center_y, 2) + math.pow(b.x - self.center_x, 2) ) - 2
            b.bullet_size = (magnitude / 200.) * 5.
            if magnitude < 2:
                self.bullets.remove(b)
                self.remove_widget(b)
            else:
                b.pos = (self.center_x + math.cos(cur_angle) * magnitude, self.center_y + math.sin(cur_angle) * magnitude)

    def add_bullet(self):
        b = Bullet()
        b.pos = self.ship.pos
        self.add_widget(b)
        self.bullets.append(b)

    def reposition_ship(self, touch):
        #print touch.x, touch.y, self.ship
        #self.ship.pos = touch.pos
        #print self.center_x, self.center_y

        cur_angle = math.atan2((touch.y - self.center_y), (touch.x - self.center_x))
        #print cur_angle
        self.ship.pos = (self.center_x + math.cos(cur_angle) * 200, self.center_y + math.sin(cur_angle) * 200)

    def on_touch_down(self, touch):
        self.is_shooting = True
        self.reposition_ship(touch)

    def on_touch_move(self, touch):
        self.reposition_ship(touch)

    def on_touch_up(self, touch):
        self.is_shooting = False
        self.reposition_ship(touch)


class Gyruss(App):
    def build(self):
        self.root = FloatLayout()
        self.ship = Ship()
        self.space = Space(app=self, ship=self.ship)
        self.root.add_widget(self.space)
        self.space.add_widget(self.ship)
        return self.root


Gyruss().run()
