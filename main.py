from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from datetime import date
import sqlite3
import os
from kivy.utils import platform



class ErrorPopup(Popup):
    def __init__(self, message, **kwargs):
        super(ErrorPopup, self).__init__(**kwargs)
        self.title = "Error"
        self.content = Label(text=message)


class NoteApp(App):
    def build(self):
        self.screen_manager = ScreenManager()
        self.main_screen = Screen(name="first")

        self.layout = GridLayout(cols=2, spacing=10)
        self.layout.pos_hint = {'top': 1} 
        self.layout.size_hint = (1, 0.4)


        self.note_list = BoxLayout(orientation="vertical")
        Clock.schedule_interval(self.refresh_data, 1.0)

        add_button = Button(text="+", size_hint=(None, None), size=(50, 50))
        add_button.bind(on_press=self.save_json_data)
        self.layout.add_widget(add_button)

        main_label = Label(text="Notes :)", font_size="20sp", size_hint=(1, 0.1))
        self.layout.add_widget(main_label)


        name_label = Label(text="Nombre: ", size_hint=(0.5, 0.1))
        self.layout.add_widget(name_label)
        self.note_input = TextInput(hint_text="Ingresa tu nombre ", size_hint=(None, None), size=(240, 40))
        self.layout.add_widget(self.note_input)  # agrega la entrada de texto al self.layout

        # horas 
        hours_label = Label(text="Horas:", size_hint=(0.5, 0.1))
        self.layout.add_widget(hours_label)
        self.hours_input = TextInput(input_filter="int", hint_text="Horas", size_hint=(None, None), size=(240, 40))
        self.layout.add_widget(self.hours_input)

        #minutos
        minutes_label = Label(text="Minutos:", size_hint=(0.5, 0.1))
        self.layout.add_widget(minutes_label)
        self.minutes_input = TextInput(input_filter="int", hint_text="Minutos", size_hint=(None, None), size=(240, 40))
        self.layout.add_widget(self.minutes_input) 

        # publicaciones
        pub_label = Label(text="Publicaciones:", size_hint=(0.5, 0.1))
        self.layout.add_widget(pub_label)
        self.pub_input = TextInput(input_filter="int", hint_text="Publicaciones", size_hint=(None, None), size=(240, 40))
        self.layout.add_widget(self.pub_input)

        # revisitas 
        rev_label = Label(text="Revisitas", size_hint=(0.5, 0.1))
        self.layout.add_widget(rev_label)
        self.rev_input = TextInput(input_filter="int", hint_text="Revisitas", size_hint=(None, None), size=(240, 40))
        self.layout.add_widget(self.rev_input)

        # videos
        video_label = Label(text="Vidoes",  size_hint=(0.5, 0.1))
        self.layout.add_widget(video_label)
        self.video_input = TextInput(input_filter="int", hint_text="Videos", size_hint=(None, None), size=(240, 40))
        self.layout.add_widget(self.video_input)

        # eliminacion
        delete_button = Button(text="Eliminar todo", size_hint=(None, None), size=(100, 30))
        delete_button.bind(on_press=self.delete_data)
        delete_button.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.layout.add_widget(delete_button)

        #ver datos
        change_to_second_screen = Button(text="Ver datos", size_hint=(None, None), size=(100, 30))
        change_to_second_screen.bind(on_press=self.change_to_second_screen)
        change_to_second_screen.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.layout.add_widget(change_to_second_screen)


        self.main_screen.bind(on_touch_down=self.on_touch_down)
        #regresar
        self.second_screen = Screen(name="second")

        second_screen_layout = BoxLayout(orientation="vertical", spacing=20)
        second_screen_layout.add_widget(self.note_list)

        change_to_first_screen = Button(text="Añadir", size_hint=(None, None), size=(100, 30))
        change_to_first_screen.bind(on_press=self.change_to_first_screen)
        change_to_first_screen.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        second_screen_layout.add_widget(change_to_first_screen)
       
        #SCREEN PLACE ! CHANGE THE ORDER ONLY IF IS IMPORTANT

        self.second_screen.add_widget(second_screen_layout)
        self.screen_manager.add_widget(self.second_screen)

        #Principal screen
        self.main_screen.add_widget(self.layout)
        self.screen_manager.add_widget(self.main_screen)


        self.db_file = os.path.join(App().user_data_dir, "datos.db") 
        

        return self.screen_manager

    def on_touch_down(self, instance, touch):
        if touch.dx > 0:
            screen_manager = App.get_running_app().root
            current_screen_name = screen_manager.current
            if current_screen_name == "first":
                screen_manager.current = "second"

    def show_error_popup(self, message):
        error_popup = ErrorPopup(message)
        error_popup.open()     

    def change_to_second_screen(self, instance):
        self.screen_manager.switch_to(self.second_screen)
    
    def change_to_first_screen(self, instance):
        self.screen_manager.switch_to(self.main_screen)

    def on_start(self):
        if platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
        self.load_data_on_uix()

    def refresh_data(self, dt):
        self.load_data_on_uix()

    def save_json_data(self, instace):
        # create connection 
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS datos (name TEXT, date DATE, hours INTEGER, minutes INTEGER, publications INTEGER, revisits INTEGER, videos INTEGER)")
        today = date.today()
        data = self.get_input_data()

        try:
            new_data = (data["name"], today, int(data["hours"]), int(data["minutes"]), int(data["publications"]), int(data["revisit"]), int(data["videos"]))
            cursor.execute("INSERT INTO datos VALUES (?, ?, ?, ?, ?, ?, ?)", new_data)
            connection.commit()
            connection.close()
        except ValueError:
            self.show_error_popup("No valores vacios")

    def get_input_data(self):

            data = {
                "name": self.note_input.text,
                "hours": self.hours_input.text,
                "minutes": self.minutes_input.text,
                "publications": self.pub_input.text,
                "revisit": self.rev_input.text,
                "videos": self.video_input.text,
            }

            return data


    def load_data(self):
        data = ()
        try:
            connection_load = sqlite3.connect(self.db_file)
            cursor_load = connection_load.cursor()
            cursor_load.execute("SELECT * FROM datos")
            data = cursor_load.fetchall()
            connection_load.close()
        except:
            cursor_load.execute("CREATE TABLE IF NOT EXISTS datos (name TEXT, date DATE, hours INTEGER, minutes INTEGER, publications INTEGER, revisits INTEGER, videos INTEGER)")  
            connection_load.close()    


        return data 

    def delete_data(self, instance):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM datos")
        connection.commit()
        connection.close()
        self.note_list.clear_widgets()


    def load_data_on_uix(self):
        self.note_list.clear_widgets()
        fetched_data = self.load_data()
        for current_data in fetched_data:
            name_label = Label(text="Nombre: " + current_data[0] + " " + "Fecha: " + current_data[1] + " " + "Horas: " + str(current_data[2]) + " " + "Minutes: " + str(current_data[3]) + " " + "Publicaciones: " + str(current_data[4]) + "\n" + "Revisitas: " + str(current_data[5]) + " " + "Videos: " + str(current_data[6]) + " ")
            self.note_list.add_widget(name_label)


if __name__ == "__main__":

    NoteApp().run()