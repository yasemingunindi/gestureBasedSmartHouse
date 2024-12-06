import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from datetime import datetime

class SmartHouseGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # Base path to the 'icons' folder
        self.icons_folder = os.path.join(os.path.dirname(__file__), "icons")

        self.title("Smart House Home Page")
        self.geometry("800x600")
        self.configure(bg="#f0f0f0")

        # Initialize the welcome screen
        self.show_main_menu()
    
    def apply_hover_effect(self, button, hover_bg="#d9d9d9", hover_fg="#000000", normal_bg="#ffffff", normal_fg="#000000"):
        """Apply hover effect to a button."""
        button.bind("<Enter>", lambda e: button.config(bg=hover_bg, fg=hover_fg))
        button.bind("<Leave>", lambda e: button.config(bg=normal_bg, fg=normal_fg))

    def show_main_menu(self):
        """Display the main menu with a welcome message and a 'Menu' button."""
        # Clear the existing window
        for widget in self.winfo_children():
            widget.destroy()

        # Welcome Message
        hello_label = tk.Label(
            self, text="Hello,",
            font=("Lucida Calligraphy", 40, "bold"), bg="#f0f0f0", fg="#333333"
        )
        hello_label.pack(pady=20)

        welcome_label = tk.Label(
            self, text="Welcome Home!",
            font=("Cooper Black", 55, "bold"), bg="#f0f0f0", fg="#333333"
        )
        welcome_label.pack(pady=20)

        # Menu Button
        menu_button = tk.Button(
            self, text="Menu", font=("Helvetica", 24, "bold"),
            bg="#4CAF50", fg="#ffffff", width=10, height=2,
            command=self.open_room_list
        )
        menu_button.pack(pady=50)
        self.apply_hover_effect(menu_button, hover_bg="#45a049", normal_bg="#4CAF50")  # Green highlight effect



    def open_room_list(self):
        """Display the room list view."""
        # Clear the existing window
        for widget in self.winfo_children():
            widget.destroy()

        # Create a header frame for the Go Back button and title
        header_frame = tk.Frame(self, bg="#f0f0f0")
        header_frame.pack(fill=tk.X, pady=10)

        # Go Back Button with left arrow symbol
        back_button = tk.Button(
            header_frame, text="⬅", font=("Helvetica", 18, "bold"),
            bg="#f0f0f0", fg="#4CAF50", borderwidth=0,
            command=self.show_main_menu
        )
        back_button.pack(side=tk.LEFT, padx=10)
        self.apply_hover_effect(back_button, hover_fg="#007bff", normal_fg="#4CAF50")  # Blue highlight effect for arrow

        # Title aligned with the Go Back button
        title_label = tk.Label(
            header_frame, text="Select a Room",
            font=("Cooper Black", 30, "bold"), bg="#f0f0f0", fg="#333333"
        )
        title_label.pack(side=tk.LEFT, padx=10)

        # Room list in a scrollable frame
        room_frame = tk.Frame(self, bg="#f0f0f0")
        room_frame.pack(fill=tk.BOTH, expand=True, pady=20, padx=50)

        room_canvas = tk.Canvas(room_frame, bg="#f0f0f0")
        room_scroll_y = tk.Scrollbar(room_frame, orient="vertical", command=room_canvas.yview)
        room_canvas.configure(yscrollcommand=room_scroll_y.set)

        room_list_frame = tk.Frame(room_canvas, bg="#f0f0f0")
        room_canvas.create_window((0, 0), window=room_list_frame, anchor="nw")
        room_canvas.pack(side="left", fill="both", expand=True)
        room_scroll_y.pack(side="right", fill="y")

        # Add room widgets
        self.add_room_widgets(room_list_frame)

        # Adjust scroll region
        room_list_frame.bind(
            "<Configure>", lambda e: room_canvas.configure(
                scrollregion=room_canvas.bbox("all")
            )
        )


    def add_room_widgets(self, parent):
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

            btn = tk.Button(
                parent, text=room_name, font=("Helvetica", 16),
                bg="#ffffff", fg="#000000", image=room_icon, compound="top",
                width=200, height=200, command=lambda room=room_name: self.on_room_click(room)
            )
            btn.image = room_icon
            btn.grid(row=row, column=col, padx=20, pady=20)
            self.apply_hover_effect(btn, hover_bg="#e6e6e6", normal_bg="#ffffff")  # Light gray highlight for rooms

    def on_room_click(self, room_name):
        """Handle room button clicks."""
        new_window = tk.Toplevel(self)
        new_window.title(f"{room_name} Controls")
        new_window.geometry("800x600")
        new_window.configure(bg="#f0f0f0")

        # Create a header frame for the Go Back button and title
        header_frame = tk.Frame(new_window, bg="#f0f0f0")
        header_frame.pack(fill=tk.X, pady=10)

        # Go Back Button with left arrow symbol
        back_button = tk.Button(
            header_frame, text="⬅", font=("Helvetica", 18, "bold"),
            bg="#f0f0f0", fg="#4CAF50", borderwidth=0,
            command=lambda: [new_window.destroy(), self.open_room_list()]
        )
        back_button.pack(side=tk.LEFT, padx=10)
        self.apply_hover_effect(back_button, hover_fg="#007bff", normal_fg="#4CAF50")  # Blue highlight effect for arrow

        # Title aligned with the Go Back button
        title_label = tk.Label(
            header_frame, text=f"{room_name} Controls",
            font=("Helvetica", 24), bg="#f0f0f0", fg="#333333"
        )
        title_label.pack(side=tk.LEFT, padx=10)
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

if __name__ == "__main__":
    app = SmartHouseGUI()
    app.mainloop()
