from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFloatingActionButton, MDFlatButton, MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen 
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivy.graphics import Color, Line
import os
import json
import random


class Task_Manager(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.screen = MDScreen()

        # Create a scrollable area for tasks
        self.scroll_view = MDScrollView(size_hint=(1, 0.8), pos_hint={"top": 0.9})
        self.task_layout = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing="10dp",  # Gap between tasks
            padding="10dp",
        )
        self.task_layout.bind(minimum_height=self.task_layout.setter("height"))
        self.scroll_view.add_widget(self.task_layout)

        self.screen.add_widget(self.scroll_view)

        # Load saved tasks
        self.load_tasks()

        # Top bar layout
        layout = MDBoxLayout(
            pos_hint={"top": 1},
            md_bg_color=[101 / 255, 71 / 255, 1, 1],
            size_hint_y=0.1,
        )
        self.screen.add_widget(layout)

        # Title label
        label = MDLabel(
            text="Task Manager",
            bold=True,
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.95},
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
        )
        self.screen.add_widget(label)

        # Floating action button for adding tasks
        add_button = MDFloatingActionButton(
            icon="plus",
            pos_hint={"center_x": 0.9, "center_y": 0.1},
            md_bg_color=[101 / 255, 71 / 255, 1, 1],
            on_release=self.add_task_box,
        )
        self.screen.add_widget(add_button)

        return self.screen

    def add_task_box(self, *args):
        close_button = MDFlatButton(
            text="Close",
            md_bg_color=[101 / 255, 71 / 255, 1, 1],
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            on_release=lambda x: self.dialog.dismiss(),
        )
        add_button = MDFlatButton(
            text="Add Task",
            md_bg_color=[101 / 255, 71 / 255, 1, 1],
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            on_release=self.save_task,
        )
        self.task_input = MDTextField(
            hint_text="Enter Task",
            mode="rectangle",
            size_hint_x=0.8,
        )
        layout = MDBoxLayout(
            orientation="vertical",
            spacing="10dp",
            size_hint=(1, None),
        )
        layout.add_widget(self.task_input)
        self.dialog = MDDialog(
            title="Add Task",
            type="custom",
            content_cls=layout,
            buttons=[add_button, close_button],
        )
        self.dialog.open()

    def save_task(self, *args):
        file = "Tasks.json"
        task_text = self.task_input.text.strip()
        if not task_text:
            return  # Avoid saving empty tasks

        # Load existing tasks
        if os.path.exists(file):
            with open(file, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {"tasks": []}

        # Add the task
        self.data["tasks"].append(task_text)
        with open(file, "w") as f:
            json.dump(self.data, f)

        self.add_task_card(len(self.data["tasks"]), task_text)
        self.dialog.dismiss()

    def add_task_card(self, task_number, task_text):
        # Random color generator
        random_color = [random.uniform(0.3, 0.9) for _ in range(3)] + [1]

        # Task card
        task_card = MDCard(
            orientation="horizontal",
            size_hint=(1, None),
            height="50dp",
            md_bg_color=random_color,
        )

        task_label = MDLabel(
            text=f"{task_number}. {task_text}",
            size_hint=(0.6, None),
            height="50dp",
            halign="left",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
        )

        tick_button = MDIconButton(
            icon="check-circle",
            theme_icon_color="Custom",
            icon_color=[0, 1, 0, 1],
            on_release=lambda x: self.complete_task(task_card, task_text),
        )

        delete_button = MDIconButton(
            icon="delete",
            theme_icon_color="Custom",
            icon_color=[1, 0, 0, 1],
            on_release=lambda x: self.delete_task(task_card, task_text),
        )

        task_card.add_widget(task_label)
        task_card.add_widget(tick_button)
        task_card.add_widget(delete_button)
        self.task_layout.add_widget(task_card)

    def complete_task(self, task_card, task_text):
    # Remove delete and tick buttons
        self.task_text=task_text
        task_card.clear_widgets()

    # Add "Completed" text
        completed_label = MDLabel(
            text="Completed",
            halign="right",
            valign="center",
            theme_text_color="Custom",
            text_color=[0, 1, 0, 1],  # Green color
            size_hint=(1, None),
            height="50dp",
        )
        task_card.add_widget(completed_label)

    # Add a line over the task to mark it as completed
        with task_card.canvas:
            Color(0, 1, 0, 1)  # Green line
            Line(
                points=[
                    task_card.x + 10, task_card.y + task_card.height / 2,  # Start point
                    task_card.right - 10, task_card.y + task_card.height / 2,  # End point
                ],
                width=2,
            )

        self.remove_task_from_file(task_text)
    # Show confirmation dialog
        self.dialog = MDDialog(
            title="Congrats!",
            text=f" You completed: {self.task_text}",
            buttons=[
                MDFlatButton(
                    text="OK",
                    md_bg_color=[101 / 255, 71 / 255, 1, 1],
                    text_color=[1, 1, 1, 1],
                    on_release= lambda x : self.dialog.dismiss(),
                )
            ], 
        )
        self.dialog.open() 

    def load_tasks(self):
        file = "Tasks.json"
        if os.path.exists(file):
            with open(file, "r") as f:
                self.data = json.load(f)
            for i, task_text in enumerate(self.data["tasks"]):
                self.add_task_card(i + 1, task_text)

    def delete_task(self, task_card, task_text):
        file = "Tasks.json"
        self.task_layout.remove_widget(task_card)
        if os.path.exists(file):
            with open(file, "r") as f:
                self.data = json.load(f)
            self.data["tasks"].remove(task_text)
            with open(file, "w") as f:
                json.dump(self.data, f)
    
    def remove_task_from_file(self, task_text):
        file = "Tasks.json"
        if os.path.exists(file):
            with open(file, "r") as f:
                self.data = json.load(f)
            # Safely remove the task if it exists
            if task_text in self.data["tasks"]:
                self.data["tasks"].remove(task_text)
                with open(file, "w") as f:
                    json.dump(self.data, f)       

Task_Manager().run()