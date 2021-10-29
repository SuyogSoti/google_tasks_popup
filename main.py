#!/Users/suyogsoti/code/add_task/venv/bin/python
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from kivymd.uix.screen import Screen
from kivy.uix.scrollview import ScrollView
from kivymd.uix.gridlayout import MDGridLayout
from dataclasses import asdict
from parser import parse_text, Task
import json
from google_task import create_task, get_tasks


class TaskInput(MDTextField):
    def keyboard_on_key_down(self, window, keycode: tuple[int, str], text,
                             modifiers):
        if keycode[1] == "escape":
            MDApp.get_running_app().stop()
            Window.close()
        return MDTextField.keyboard_on_key_down(self, window, keycode, text,
                                                modifiers)


def on_enter(instance):
    MDApp.get_running_app().stop()
    Window.close()
    task = parse_text(instance.text)
    create_task(task)


def get_on_text(label: MDLabel) -> callable:
    def on_text(intance: TaskInput, value: str) -> None:
        if not value:
            label.text = format_tasks(get_tasks())
            return
        task = parse_text(value)
        label.text = json.dumps(asdict(task), indent=4)

    return on_text


def build_input_box(label: MDLabel):
    tsk_input = TaskInput(text='', multiline=False)
    tsk_input.bind(on_text_validate=on_enter)
    tsk_input.bind(text=get_on_text(label))
    tsk_input.font_size = 45
    tsk_input.focus = True
    return tsk_input


def format_tasks(tasks: list[Task]) -> str:
    text = "\n\n\n"
    for t in tasks:
        text += f"""
            title: {t.title}
                    notes: {t.description}
                    due:   {t.duedate}
        """
    print(text)
    return text

class AddGoogleTask(MDApp):
    def build(self):
        Window.size = (900, 900)
        label = MDLabel(text=format_tasks(get_tasks()))
        scrollview = ScrollView(do_scroll_x=True, do_scroll_y=True)
        scrollview.add_widget(label)
        screen = Screen()
        layout = MDGridLayout(rows=2)
        layout.add_widget(build_input_box(label))
        layout.add_widget(scrollview)
        screen.add_widget(layout)
        return screen


if __name__ == '__main__':
    AddGoogleTask().run()
