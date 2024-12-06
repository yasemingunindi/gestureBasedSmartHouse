import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime

class SmartHouseGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # Base path to the 'icons' folder
        self.icons_folder = os.path.join(os.path.dirname(__file__), "icons")

        self.title("Smart House Home Page")
        self.geometry("1200x800")
        self.configure(bg="#f0f0f0")

        # Welcome Message
        hello_label = tk.Label(
            self, text="Hello,",
            font=("Lucida Calligraphy", 50, "bold"), bg="#f0f0f0", fg="#333333"
        )
        hello_label.pack(pady=0)

        welcome_label = tk.Label(
            self, text="Welcome Home!",
            font=("Cooper Black", 75, "bold"), bg="#f0f0f0", fg="#333333"
        )
        welcome_label.pack(pady=0)

        # Scrollable Frame for Time, Temperature, Humidity, Energy, Light, and AQI
        info_frame = tk.Frame(self, bg="#f0f0f0")
        info_frame.pack(fill=tk.BOTH, expand=True, pady=20, padx=50)

        canvas = tk.Canvas(info_frame, bg="#f0f0f0", height=50)
        scroll_x = tk.Scrollbar(info_frame, orient="horizontal", command=canvas.xview)
        canvas.configure(xscrollcommand=scroll_x.set)

        data_frame = tk.Frame(canvas, bg="#f0f0f0")
        canvas.create_window((0, 0), window=data_frame, anchor="nw")

        # Pack canvas and scrollbar
        canvas.pack(side="top", fill="both", expand=True)
        scroll_x.pack(side="bottom", fill="x")

        # Add widgets for environmental data
        self.add_info_widgets(data_frame)

        # Adjust scroll region
        data_frame.bind(
            "<Configure>", lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # Scrollable Room List
        room_frame = tk.Frame(self, bg="#f0f0f0")
        room_frame.pack(fill=tk.BOTH, expand=True, pady=20, padx=50)

        room_canvas = tk.Canvas(room_frame, bg="#f0f0f0")
        room_scroll_y = tk.Scrollbar(room_frame, orient="vertical", command=room_canvas.yview)
        room_canvas.configure(yscrollcommand=room_scroll_y.set)

        self.room_list_frame = tk.Frame(room_canvas, bg="#f0f0f0")
        self.room_list_frame.grid_columnconfigure(0, weight=1)
        self.room_list_frame.grid_columnconfigure(1, weight=1)

        room_canvas.create_window((0, 0), window=self.room_list_frame, anchor="nw")
        room_canvas.pack(side="left", fill="both", expand=True)
        room_scroll_y.pack(side="right", fill="y")

        # Populate room list
        self.add_room_widgets()

        # Adjust scroll region for room list
        self.room_list_frame.bind(
            "<Configure>", lambda e: room_canvas.configure(
                scrollregion=room_canvas.bbox("all")
            )
        )

    def add_info_widgets(self, parent):
        # Icon paths
        icon_paths = {
            "clock": "clock_icon.png",
            "temperature": "temperature_icon.png",
            "humidity": "humidity_icon.png",
            "energy": "energy_icon.png",
            "light": "light_icon.png",
            "aqi": "aqi_icon.png"
        }

        # Helper to load and display icons dynamically
        def load_icon(icon_name):
            try:
                icon_path = os.path.join(self.icons_folder, icon_name)
                icon_image = Image.open(icon_path).resize((70, 70), Image.LANCZOS)
                return ImageTk.PhotoImage(icon_image)
            except Exception as e:
                print(f"Error loading icon {icon_name}: {e}")
                return None

        # Add widgets with icons
        self.clock_icon = load_icon(icon_paths["clock"])
        clock_label = tk.Label(parent, image=self.clock_icon, bg="#f0f0f0")
        clock_label.pack(side=tk.LEFT, padx=10)

        self.time_label = tk.Label(
            parent, text="", font=("Helvetica", 28), bg="#f0f0f0", fg="#333333"
        )
        self.time_label.pack(side=tk.LEFT, padx=10)
        self.update_time()

        self.temp_icon = load_icon(icon_paths["temperature"])
        temp_label = tk.Label(parent, image=self.temp_icon, bg="#f0f0f0")
        temp_label.pack(side=tk.LEFT, padx=10)

        self.temperature_label = tk.Label(
            parent, text="22°C", font=("Helvetica", 28), bg="#f0f0f0", fg="#333333"
        )
        self.temperature_label.pack(side=tk.LEFT, padx=10)

        self.humidity_icon = load_icon(icon_paths["humidity"])
        humidity_label = tk.Label(parent, image=self.humidity_icon, bg="#f0f0f0")
        humidity_label.pack(side=tk.LEFT, padx=10)

        self.humidity_label = tk.Label(
            parent, text="50%", font=("Helvetica", 28), bg="#f0f0f0", fg="#333333"
        )
        self.humidity_label.pack(side=tk.LEFT, padx=10)

        self.energy_icon = load_icon(icon_paths["energy"])
        energy_label = tk.Label(parent, image=self.energy_icon, bg="#f0f0f0")
        energy_label.pack(side=tk.LEFT, padx=10)

        self.energy_label = tk.Label(
            parent, text="450 kWh", font=("Helvetica", 28), bg="#f0f0f0", fg="#333333"
        )
        self.energy_label.pack(side=tk.LEFT, padx=10)

        self.light_icon = load_icon(icon_paths["light"])
        light_label = tk.Label(parent, image=self.light_icon, bg="#f0f0f0")
        light_label.pack(side=tk.LEFT, padx=10)

        self.light_label = tk.Label(
            parent, text="75%", font=("Helvetica", 28), bg="#f0f0f0", fg="#333333"
        )
        self.light_label.pack(side=tk.LEFT, padx=10)

        self.aqi_icon = load_icon(icon_paths["aqi"])
        aqi_label = tk.Label(parent, image=self.aqi_icon, bg="#f0f0f0")
        aqi_label.pack(side=tk.LEFT, padx=10)

        self.aqi_label = tk.Label(
            parent, text="AQI: 45", font=("Helvetica", 28), bg="#f0f0f0", fg="#333333"
        )
        self.aqi_label.pack(side=tk.LEFT, padx=10)

    def add_room_widgets(self):
        rooms = [
            ("Bedroom", "bedroom_icon.png"),
            ("Kids Room", "kidsroom_icon.png"),
            ("Living Room", "livingroom_icon.png"),
            ("Office", "office_icon.png"),
            ("Kitchen", "kitchen_icon.png"),
            ("Bathroom", "bathroom_icon.png"),
            ("Dressing Room", "dressingroom_icon.png"),
            ("Garage", "garage_icon.png")
        ]

        for i, (room_name, icon_file) in enumerate(rooms):
            row = i // 2
            col = i % 2

            try:
                icon_path = os.path.join(self.icons_folder, icon_file)
                room_image = Image.open(icon_path).resize((150, 150), Image.LANCZOS)
                room_icon = ImageTk.PhotoImage(room_image)
            except Exception as e:
                print(f"Error loading icon for {room_name}: {e}")
                room_icon = None

            btn_frame = tk.Frame(self.room_list_frame, bg="#d9d9d9", bd=2, relief="raised", width=400, height=300)
            btn_frame.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
            btn_frame.grid_propagate(False)  # Prevent frame resizing to fit content

            btn = tk.Button(
                btn_frame, text=room_name, font=("Helvetica", 16),
                bg="#ffffff", fg="#000000", image=room_icon, compound="top",
                width=400, height=300, command=lambda room=room_name: self.on_room_click(room)
            )
            btn.image = room_icon
            btn.pack(fill="both", expand=True)
            
    def on_room_click(self, room_name):
        """Handle room button clicks."""
        new_window = tk.Toplevel(self)
        new_window.title(f"{room_name} Controls")
        new_window.geometry("800x600")
        new_window.configure(bg="#f0f0f0")

        title = tk.Label(
            new_window, text=f"{room_name} Controls",
            font=("Helvetica", 24), bg="#f0f0f0", fg="#333333"
        )
        title.pack(pady=10)
        if room_name == "Living Room":
            self.open_living_room(new_window)
        elif room_name == "Kitchen":
            self.open_kitchen(new_window)
        elif room_name == "Bedroom":
            self.open_bedroom(new_window)
        elif room_name == "Bathroom":
            self.open_bathroom(new_window)
        elif room_name == "Office":
            self.open_bathroom(new_window)
        elif room_name == "Garage":
            self.open_garage(new_window)
        elif room_name == "Kids Room":
            self.open_kids_room(new_window)
        else:
            print(f"No page implemented for {room_name}.")

    def open_living_room(self, window):
        """Add Living Room controls."""
        self.add_lights_controls(window)
        self.add_tv_controls(window)
        self.add_ac_controls(window)
        self.add_music_controls(window)
        self.add_thermostat_controls(window)
        self.add_vacuum_controls(window) 
        
    def open_kitchen(self, window):
        """Add Kitchen controls."""
        self.add_lights_controls(window)
        self.add_appliance_controls(window, "Air Fryer", ["Temp Up", "Temp Down", "Time Up", "Time Down", "Start/Stop"])
        self.add_appliance_controls(window, "Coffee Machine", ["Program Selection", "On/Off"])

    def open_bedroom(self, window):
        """Add Bedroom controls."""
        self.add_lights_controls(window)
        self.add_appliance_controls(window, "Curtains", ["Open", "Close"])
        self.add_ac_controls(window)        

    def open_bathroom(self, window):
        """Add Bathroom controls."""
        self.add_lights_controls(window)
        self.add_appliance_controls(window, "Ventilation", ["On", "Off", "Fan Speed Up", "Fan Speed Down"])


    def add_lights_controls(self, window):
        """Add light controls."""
        frame = tk.LabelFrame(window, text="Lights", font=("Helvetica", 16), bg="#f0f0f0", fg="#000000")
        frame.pack(pady=10, fill="x")

        # Initial state of the light
        self.light_on = False

        toggle_canvas = tk.Canvas(frame, width=100, height=50, bg="#f0f0f0", highlightthickness=0)
        toggle_canvas.pack(pady=30)

        # Draw the toggle background
        toggle_bg = toggle_canvas.create_rectangle(0, 10, 100, 50, fill="#D3D3D3", outline="")  # Gray for Off

        # Draw the toggle circle (slider)
        toggle_circle = toggle_canvas.create_rectangle(0, 10, 50, 50, fill="white", outline="")

        def toggle_switch(event):
            """Toggle the switch between On and Off states."""
            if self.light_on:
                # Move circle to the left (Off state)
                toggle_canvas.itemconfig(toggle_circle, fill="white")
                toggle_canvas.itemconfig(toggle_bg, fill="#D3D3D3")  # Gray for Off
                toggle_canvas.move(toggle_circle, -50, 0)  # Slide left
                print("Light turned Off")
            else:
                # Move circle to the right (On state)
                toggle_canvas.itemconfig(toggle_circle, fill="white")
                toggle_canvas.itemconfig(toggle_bg, fill="#4CAF50")  # Green for On
                toggle_canvas.move(toggle_circle, 50, 0)  # Slide right
                print("Light turned On")
            self.light_on = not self.light_on  # Toggle the state

        # Bind a click event to the canvas
        toggle_canvas.bind("<Button-1>", toggle_switch)

        # Ensure the background is behind the circle
        toggle_canvas.tag_lower(toggle_bg)

        # Slider Frame for better alignment
        slider_frame = tk.Frame(frame, bg="#f0f0f0")
        slider_frame.pack(pady=10)

        # Slider
        brightness_scale = tk.Scale(
            slider_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=300,
            font=("Helvetica", 10), bg="#f0f0f0", fg="#4CAF50",
            highlightbackground="#f0f0f0", troughcolor="#D3D3D3", activebackground="#4CAF50"
        )
        brightness_scale.pack(padx=10)

        # Dynamic Value Label
        value_label = tk.Label(
            frame, text="0%", font=("Helvetica", 12), bg="#f0f0f0", fg="#4CAF50"
        )
        value_label.pack(pady=10)

        # Function to update the label dynamically
        def update_brightness(value):
            value_label.config(text=f" {value}%")

        # Bind slider to update function
        brightness_scale.config(command=update_brightness)

    def add_tv_controls(self, window):
        """Add TV controls."""
        frame = tk.LabelFrame(window, text="TV", font=("Helvetica", 16), bg="#f0f0f0", fg="#000000")
        frame.pack(pady=10, fill="x")
        buttons = ["On", "Off", "Channel Up", "Channel Down", "Volume Up", "Volume Down", "Change Source"]
        for btn_text in buttons:
            tk.Button(frame, text=btn_text, width=15).pack(side=tk.LEFT, padx=5, pady=5)

    def add_ac_controls(self, window):
        """Add Air Conditioner controls."""
        frame = tk.LabelFrame(window, text="Air Conditioner", font=("Helvetica", 16), bg="#f0f0f0", fg="#000000")
        frame.pack(pady=10, fill="x")
        buttons = ["On", "Off", "Mode", "Temp Up", "Temp Down", "Fan Speed Up", "Fan Speed Down"]
        for btn_text in buttons:
            tk.Button(frame, text=btn_text, width=15).pack(side=tk.LEFT, padx=5, pady=5)

    def add_music_controls(self, window):
        """Add Music System controls."""
        frame = tk.LabelFrame(window, text="Music System", font=("Helvetica", 16), bg="#f0f0f0", fg="#000000")
        frame.pack(pady=10, fill="x")
        buttons = ["On", "Off", "Volume Up", "Volume Down", "Next Song", "Previous Song"]
        for btn_text in buttons:
            tk.Button(frame, text=btn_text, width=15).pack(side=tk.LEFT, padx=5, pady=5)

    def add_thermostat_controls(self, window):
        """Add Thermostat controls."""
        frame = tk.LabelFrame(window, text="Thermostat", font=("Helvetica", 16), bg="#f0f0f0", fg="#000000")
        frame.pack(pady=10, fill="x")
        buttons = ["Temp Up", "Temp Down"]
        for btn_text in buttons:
            tk.Button(frame, text=btn_text, width=15).pack(side=tk.LEFT, padx=5, pady=5)

    def add_vacuum_controls(self, window):
        """Add Robot Vacuum Cleaner controls."""
        frame = tk.LabelFrame(window, text="Robot Vacuum Cleaner", font=("Helvetica", 16), bg="#f0f0f0", fg="#000000")
        frame.pack(pady=10, fill="x")
        buttons = ["On", "Off", "Select Program"]
        for btn_text in buttons:
            tk.Button(frame, text=btn_text, width=15).pack(side=tk.LEFT, padx=5, pady=5)

    def add_appliance_controls(self, window, appliance_name, button_texts):
        """Add controls for a specific appliance."""
        frame = tk.LabelFrame(window, text=appliance_name, font=("Helvetica", 16), bg="#f0f0f0", fg="#000000")
        frame.pack(pady=10, fill="x")
        for btn_text in button_texts:
            tk.Button(frame, text=    btn_text, width=15).pack(side=tk.LEFT, padx=5, pady=5)
    
    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.configure(text=current_time)
        self.after(1000, self.update_time)

if __name__ == "__main__":
    app = SmartHouseGUI()
    app.mainloop()
