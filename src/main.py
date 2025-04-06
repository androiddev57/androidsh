import subprocess
import platform
import os
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView


class TerminalApp(App):
    def build(self):
        self.history = Label(size_hint_y=None, height=400, font_size=15)
        self.history.text = "Welcome to Android Shell Interface\nType commands below:\n\n"
        
        self.command_input = TextInput(size_hint_y=None, height=40, multiline=False, font_size=18, foreground_color=(1,1,1,1), background_color=(0, 0, 0, 1), hint_text="$ Type command...")

        self.command_input.bind(on_text_validate=self.on_enter)

        layout = BoxLayout(orientation='vertical', spacing=10)
        scroll = ScrollView()
        scroll.add_widget(self.history)

        command_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        command_layout.add_widget(self.command_input)

        layout.add_widget(scroll)
        layout.add_widget(command_layout)

        return layout

    def on_enter(self, instance):
        command = self.command_input.text.strip()

        if command == "name":
            device_name = self.get_device_name()
            self.update_history(f"$ {command}\n{device_name}\n")
        
        elif command == "battery":
            battery_info = self.get_battery_info()
            self.update_history(f"$ {command}\n{battery_info}\n")
        
        elif command == "cpu":
            cpu_info = self.get_cpu_info()
            self.update_history(f"$ {command}\n{cpu_info}\n")

        elif command == "memory":
            memory_info = self.get_memory_info()
            self.update_history(f"$ {command}\n{memory_info}\n")
        
        elif command == "storage":
            storage_info = self.get_storage_info()
            self.update_history(f"$ {command}\n{storage_info}\n")

        elif command == "network":
            network_info = self.get_network_info()
            self.update_history(f"$ {command}\n{network_info}\n")

        elif command == "os":
            os_info = self.get_os_info()
            self.update_history(f"$ {command}\n{os_info}\n")

        elif command == "uptime":
            uptime_info = self.get_uptime_info()
            self.update_history(f"$ {command}\n{uptime_info}\n")

        elif command == "time":
            time_info = self.get_time_info()
            self.update_history(f"$ {command}\n{time_info}\n")

        elif command == "files":
            file_list = self.list_files()
            self.update_history(f"$ {command}\n{file_list}\n")

        elif command.startswith("cd"):
            directory = command[3:].strip()
            if self.change_directory(directory):
                self.update_history(f"$ {command}\nChanged directory to {directory}\n")
            else:
                self.update_history(f"$ {command}\nDirectory not found.\n")

        elif command == "path":
            path_info = self.get_path_info()
            self.update_history(f"$ {command}\n{path_info}\n")

        elif command == "exit":
            self.update_history(f"$ {command}\nExiting Terminal...\n")
            self.stop()

        else:
            self.update_history(f"$ {command}\nCommand not found. Try 'name', 'battery', or 'exit'.\n")

        self.command_input.text = ""

    def update_history(self, text):
        self.history.text += text

    def get_device_name(self):
        try:
            if platform.system() == 'Linux':
                device_name = subprocess.check_output("hostname", shell=True).decode('utf-8').strip()
            else:
                device_name = "Device name not found."
            return f"Device Name: {device_name}"
        except subprocess.CalledProcessError as e:
            return "Error retrieving device name."

    def get_battery_info(self):
        try:
            battery_info = subprocess.check_output("cat /sys/class/power_supply/battery/capacity", shell=True).decode('utf-8').strip()
            return f"Battery Level: {battery_info}%"
        except subprocess.CalledProcessError as e:
            return "Error retrieving battery info."

    def get_cpu_info(self):
        try:
            cpu_info = subprocess.check_output("cat /proc/cpuinfo", shell=True).decode('utf-8')
            return f"CPU Info: \n{cpu_info}"
        except subprocess.CalledProcessError as e:
            return "Error retrieving CPU info."

    def get_memory_info(self):
        try:
            memory_info = subprocess.check_output("cat /proc/meminfo", shell=True).decode('utf-8')
            return f"Memory Info: \n{memory_info}"
        except subprocess.CalledProcessError as e:
            return "Error retrieving memory info."

    def get_storage_info(self):
        try:
            storage_info = subprocess.check_output("df -h", shell=True).decode('utf-8')
            return f"Storage Info: \n{storage_info}"
        except subprocess.CalledProcessError as e:
            return "Error retrieving storage info."

    def get_network_info(self):
        try:
            network_info = subprocess.check_output("ifconfig", shell=True).decode('utf-8')
            return f"Network Info: \n{network_info}"
        except subprocess.CalledProcessError as e:
            return "Error retrieving network info."

    def get_os_info(self):
        try:
            os_info = subprocess.check_output("uname -a", shell=True).decode('utf-8')
            return f"OS Info: \n{os_info}"
        except subprocess.CalledProcessError as e:
            return "Error retrieving OS info."

    def get_uptime_info(self):
        try:
            uptime_info = subprocess.check_output("uptime", shell=True).decode('utf-8')
            return f"Uptime Info: \n{uptime_info}"
        except subprocess.CalledProcessError as e:
            return "Error retrieving uptime info."

    def get_time_info(self):
        try:
            time_info = subprocess.check_output("date", shell=True).decode('utf-8')
            return f"Current Time: {time_info}"
        except subprocess.CalledProcessError as e:
            return "Error retrieving time info."

    def list_files(self):
        try:
            file_list = subprocess.check_output("ls -l", shell=True).decode('utf-8')
            return f"Files in current directory: \n{file_list}"
        except subprocess.CalledProcessError as e:
            return "Error listing files."

    def change_directory(self, directory):
        try:
            if os.path.isdir(directory):
                os.chdir(directory)
                return True
            else:
                return False
        except Exception as e:
            return False

    def get_path_info(self):
        try:
            path_info = os.environ.get('PATH', 'No PATH information available.')
            return f"Path Info: {path_info}"
        except Exception as e:
            return "Error retrieving PATH info."


if __name__ == '__main__':
    TerminalApp().run()
