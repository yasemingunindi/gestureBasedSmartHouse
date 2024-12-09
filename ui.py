from multiprocessing import Process, Queue
import time  # Import time for debounce logic
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import pyautogui
from datetime import datetime
from gestures import gesture_recognition  # Ensure gestures.py is in the same directory or adjust the import path
class FeedbackPopUp:
    def __init__(self, parent, message, duration=2000):
        """
        Create a self-disappearing pop-up.

        Args:
            parent: Parent tkinter widget.
            message (str): Message to display in the pop-up.
            duration (int): Duration in milliseconds before the pop-up disappears.
        """
        self.popup = tk.Toplevel(parent)
        self.popup.geometry("300x100")  # Adjust size as needed
        self.popup.title("Feedback")
        self.popup.configure(bg="lightyellow")
        self.popup.resizable(False, False)
        # Remove window decorations
        self.popup.overrideredirect(True)
        # Set transparency to 90%
        self.popup.attributes("-alpha", 0.9)
        # Center the pop-up on the parent window
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        popup_width = 300
        popup_height = 100
        x_offset = parent_x + (parent_width - popup_width) // 2
        y_offset = parent_y + (parent_height - popup_height) // 2
        self.popup.geometry(f"{popup_width}x{popup_height}+{x_offset}+{y_offset}")

        # Add a label to display the feedback message
        tk.Label(
            self.popup, text=message, bg="lightyellow", font=("Arial", 12), wraplength=280
        ).pack(expand=True, fill=tk.BOTH, pady=20)

        # Schedule the pop-up to close after the specified duration
        self.popup.after(duration, self.popup.destroy)

class SmartHouseGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.queue = queue
        # Base path to the 'icons' folder
        self.icons_folder = os.path.join(os.path.dirname(__file__), "icons")
        self.title("Smart House Home Page")
        self.geometry("800x600")
        self.configure(bg="#f0f0f0")
        
        self.last_gesture = None  # Store the last gesture processed
        self.last_gesture_time = 0  # Timestamp of the last gesture
        
        # Initialize the welcome screen
        self.show_main_menu()
        self.check_gestures()
        
    def check_gestures(self):
        """Poll for gestures from the queue and handle them."""
        try:
            while not self.queue.empty():
                gesture = self.queue.get()
                 # Ensure gesture_label exists before updating it
                self.handle_gesture(gesture)
        except Exception as e:
            print(f"Error handling gestures: {e}")
        self.after(100, self.check_gestures)  # Check for gestures every 100ms

    def handle_gesture(self, gesture):
        current_time = time.time()  # Current time in seconds

        # Debounce logic: Process the gesture only if it's new or after cooldown
        if gesture == self.last_gesture and (current_time - self.last_gesture_time) < 5:
            print(f"Ignored duplicate gesture: {gesture}")
            return

        self.last_gesture = gesture
        self.last_gesture_time = current_time
        """Handle specific gestures and map them to UI actions."""
               
        if gesture == "INDEX POINTING UP":
            print("Controller Mode Activated")
        elif gesture == "PEACE SIGN":
            print("Scroll Triggered")
            self.scroll_page()# Add specific UI scroll logic here if needed
        elif gesture == "THREE":
            print("Opening Room List...")
            self.open_room_list()
        elif gesture == "ROCK'N ROLL!!!":
            self.show_main_menu()
        elif gesture == "FOUR":
            print("Performing Click...")
            pyautogui.click()  # Simulates a click
            print("Click Performed")
        elif gesture == "SCROLL UP":
            self.scroll_page(direction="up")
            print("Scrolled Up")
        elif gesture == "SCROLL DOWN":
            self.scroll_page(direction="down")
            print("Scrolled Down")
        elif gesture == "THUMBS UP":
            self.adjust_volume(up=True)
        elif gesture == "THUMBS DOWN":
            self.adjust_volume(up=False)
        else:
            print(f"Unhandled gesture: {gesture}")
    
 
    def adjust_volume(self, up):
        """Adjust volume up or down based on the gesture."""
        volume_control = self.music_volume_scale if hasattr(self, 'music_volume_scale') else None
        if volume_control:
            current_volume = volume_control.get()
            new_volume = min(current_volume + 5, 100) if up else max(current_volume - 5, 0)
            volume_control.set(new_volume)
            print(f"Volume {'Increased' if up else 'Decreased'} to {new_volume}")

    def apply_hover_effect(self, button, hover_bg="#d9d9d9", hover_fg="#ffffff", normal_bg="#ffffff", normal_fg="#000000"):
        """Apply hover effect to a button, ensuring it returns to its default colors."""
        def on_enter(e):
            button.config(bg=hover_bg, fg=hover_fg)

        def on_leave(e):
            button.config(bg=normal_bg, fg=normal_fg)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def scroll_page(self, direction="up"):
        """Scroll the page up or down."""
        scroll_amount = 100 if direction == "up" else -100
        pyautogui.scroll(scroll_amount)
        print(f"Scrolled {direction} by {scroll_amount}")


    def show_main_menu(self):
        """Display the main menu with a welcome message and a 'Menu' button."""
        # Clear the existing window
        for widget in self.winfo_children():
            widget.destroy()
            
        # Create a canvas to draw the white rectangle and add the text and image
        canvas = tk.Canvas(self, bg="#f0f0f0", width=700, height=200, highlightthickness=0)
        canvas.pack(pady=20)

        # Adjust the rectangle dimensions to fit the icon and text
        rect_x1, rect_y1, rect_x2, rect_y2 = 100, 50, 650, 200
        canvas.create_rectangle(rect_x1, rect_y1, rect_x2, rect_y2, fill="white", outline="white")

        # Load the house icon
        house_icon_path = os.path.join(self.icons_folder, "house_icon.jpg")
        try:
            house_image = Image.open(house_icon_path).resize((150, 150), Image.LANCZOS)  # Adjust icon height for alignment
            house_icon = ImageTk.PhotoImage(house_image)
            # Align icon to the left of the text
            canvas.create_image(rect_x1 + 60, (rect_y1 + rect_y2) // 2, image=house_icon, anchor="center")
            canvas.house_icon = house_icon  # Keep a reference to avoid garbage collection
        except Exception as e:
            print(f"Error loading house icon: {e}")

        # Add the "Welcome" text
        canvas.create_text(
            rect_x1 + 180, rect_y1 + 10,
            text="Welcome", font=("Helvetica", 50, "bold"), fill="#000000", anchor="nw"
        )

        # Add the "Home" text aligned with the bottom of the icon
        canvas.create_text(
            rect_x1 + 180, rect_y1 + 70,
            text="Home.", font=("Helvetica", 50, "bold"), fill="#000000", anchor="nw"
        )

        # Time and Temperature Frame
        info_frame = tk.Frame(self, bg="#f0f0f0")
        info_frame.pack(pady=20)

        # Clock Icon and Time
        clock_icon_path = os.path.join(self.icons_folder, "clock_icon.png")
        try:
            clock_image = Image.open(clock_icon_path).resize((50, 50), Image.LANCZOS)
            clock_icon = ImageTk.PhotoImage(clock_image)
            clock_label = tk.Label(info_frame, image=clock_icon, bg="#f0f0f0")
            clock_label.image = clock_icon
            clock_label.pack(side=tk.LEFT, padx=10)
        except Exception as e:
            print(f"Error loading clock icon: {e}")

        self.time_label = tk.Label(
            info_frame, text="", font=("Helvetica", 20), bg="#f0f0f0", fg="#333333"
        )
        self.time_label.pack(side=tk.LEFT, padx=10)
        self.update_time()

        # Temperature Icon and Value
        temp_icon_path = os.path.join(self.icons_folder, "temperature_icon.png")
        try:
            temp_image = Image.open(temp_icon_path).resize((50, 50), Image.LANCZOS)
            temp_icon = ImageTk.PhotoImage(temp_image)
            temp_label = tk.Label(info_frame, image=temp_icon, bg="#f0f0f0")
            temp_label.image = temp_icon
            temp_label.pack(side=tk.LEFT, padx=10)
        except Exception as e:
            print(f"Error loading temperature icon: {e}")

        temperature_label = tk.Label(
            info_frame, text="22.5°C", font=("Helvetica", 20), bg="#f0f0f0", fg="#333333"
        )
        temperature_label.pack(side=tk.LEFT, padx=10)

        # Menu Button
        menu_button = tk.Button(
            self, text="Rooms", font=("Helvetica", 24, "bold"),
            bg="#5c3a92", fg="#ffffff", width=10, height=2,
            command=self.open_room_list
        )
        menu_button.pack(pady=50)
        self.apply_hover_effect(menu_button, hover_bg="#8a64d6", normal_bg="#5c3a92") 



    def update_time(self):
        """Update the time displayed on the welcome page."""
        current_time = datetime.now().strftime("%H:%M:%S")
        if hasattr(self, "time_label") and self.time_label.winfo_exists():  # Check if time_label exists
            self.time_label.config(text=current_time)
            self.after(1000, self.update_time)  # Reschedule only if the widget exists


    def open_room_list(self):
        """Display the room list view."""
        # Clear the existing window
        for widget in self.winfo_children():
            widget.destroy()
        
        # Create a header frame for the Go Back button and title
        header_frame = tk.Frame(self, bg="#5c3a92")  # Purple background
        header_frame.pack(fill=tk.X, pady=10)

        # Go Back Button with left arrow symbol
        back_button = tk.Button(
            header_frame, text="⬅", font=("Helvetica", 18, "bold"),
            bg="#5c3a92", fg="#ffffff", borderwidth=0,  # Match the header frame background
            command=self.show_main_menu
        )
        back_button.pack(side=tk.LEFT, padx=10)
        self.apply_hover_effect(back_button, hover_bg="#8a64d6", normal_bg="#5c3a92", normal_fg="#ffffff")


        # Title aligned with the Go Back button
        title_label = tk.Label(
            header_frame, text="Rooms",
            font=("Helvetica", 30, "bold"), bg="#5c3a92", fg="#ffffff"
        )
        title_label.pack(side=tk.LEFT, padx=10)

        # Room list in a scrollable frame
        room_frame = tk.Frame(self, bg="#5c3a92")  # Purple background
        room_frame.pack(fill=tk.BOTH, expand=True, pady=20, padx=50)

        room_canvas = tk.Canvas(room_frame, bg="#5c3a92")  # Purple background
        room_scroll_x = tk.Scrollbar(room_frame, orient="horizontal", command=room_canvas.xview)
        room_scroll_x.config(width=30)
        room_canvas.configure(xscrollcommand=room_scroll_x.set)

        room_list_frame = tk.Frame(room_canvas, bg="#5c3a92")  # Purple background
        room_canvas.create_window((0, 0), window=room_list_frame, anchor="nw")
        room_canvas.pack(side="top", fill="both", expand=True)
        room_scroll_x.pack(side="bottom", fill="x")

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

        # Set layout as 2 rows and 4 columns
        columns = 4
        for i, (room_name, icon_file) in enumerate(rooms):
            row = i // columns
            col = i % columns

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
            btn.grid(row=row, column=col, padx=20, pady=10)
            self.apply_hover_effect(btn, hover_bg="#0cead9", normal_bg="#ffffff")


    def on_room_click(self, room_name):
        """Handle room button clicks and display room controls in the main window."""
        # Clear the existing window content
        for widget in self.winfo_children():
            widget.destroy()

        # Header for navigation
        header_frame = tk.Frame(self, bg="#5c3a92")
        header_frame.pack(fill=tk.X, pady=10)

        # Back button
        back_button = tk.Button(
            header_frame, text="⬅", font=("Helvetica", 18, "bold"),
            bg="#5c3a92", fg="#ffffff", borderwidth=0,
            command=self.open_room_list
        )
        back_button.pack(side=tk.LEFT, padx=10)
        self.apply_hover_effect(back_button, hover_bg="#8a64d6", normal_bg="#5c3a92", normal_fg="#ffffff")

        # Room title
        title_label = tk.Label(
            header_frame, text=f"{room_name} Controls",
            font=("Helvetica", 30, "bold"), bg="#5c3a92", fg="#ffffff"
        )
        title_label.pack(side=tk.LEFT, padx=10)

        # Scrollable content area for room controls
        content_frame = tk.Frame(self, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(content_frame, bg="#f0f0f0")
        scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add common controls for the room
        self.add_thermostat_controls(scrollable_frame)
        self.add_lights_controls(scrollable_frame)

        # Add specific controls for each room
        if room_name == "Living Room":
            self.add_tv_controls(scrollable_frame)
            self.add_music_controls(scrollable_frame)
            self.add_ac_controls(scrollable_frame)
        elif room_name == "Kitchen":
            self.add_appliance_controls(scrollable_frame, "Air Fryer", ["Temp Up", "Temp Down", "Time Up", "Time Down", "Start/Stop"])
            self.add_appliance_controls(scrollable_frame, "Coffee Machine", ["Program Selection", "On/Off"])
        elif room_name == "Bedroom":
            self.add_appliance_controls(scrollable_frame, "Curtains", ["Open", "Close"])
            self.add_ac_controls(scrollable_frame)
        elif room_name == "Bathroom":
            self.add_appliance_controls(scrollable_frame, "Ventilation", ["On", "Off", "Fan Speed Up", "Fan Speed Down"])
        elif room_name == "Garage":
            self.add_appliance_controls(scrollable_frame , "Garage Door", ["Open", "Close"])
        # Add other room-specific controls similarly

    def add_lights_controls(self, window):
        """Add light controls with power button, light bulb icon, color buttons, and brightness slider."""
        frame = tk.LabelFrame(window, text="Lights", font=("Helvetica", 16), bg="#f0f0f0", fg="#000000")
        frame.pack(pady=10, fill="x")

        # Initial state of the light
        self.light_on = False
        self.current_color = "white"
        self.brightness = 0  # Default brightness at 0 when off

        # Load icons
        try:
            power_icon_path = os.path.join(self.icons_folder, "power_icon.png")
            lights_off_icon_path = os.path.join(self.icons_folder, "lights_off_icon.png")
            self.power_icon = ImageTk.PhotoImage(Image.open(power_icon_path).resize((50, 50), Image.LANCZOS))
            self.lights_off_icon = ImageTk.PhotoImage(Image.open(lights_off_icon_path).resize((300, 300), Image.LANCZOS))
            self.lights_on_icons = {
                color: ImageTk.PhotoImage(Image.open(os.path.join(self.icons_folder, f"lights_on_{color}_icon.png")).resize((300, 300), Image.LANCZOS))
                for color in ["white", "red", "orange", "yellow", "green", "blue", "purple", "pink"]
            }
        except Exception as e:
            print(f"Error loading icons: {e}")
            return

        self.lights_on_icon = self.lights_on_icons["white"]  # Default icon

        # Create a container frame for the layout
        layout_frame = tk.Frame(frame, bg="#f0f0f0")
        layout_frame.pack(fill="x", padx=20, pady=10)

        # Left column (Power button and color buttons)
        left_frame = tk.Frame(layout_frame, bg="#f0f0f0")
        left_frame.grid(row=0, column=0, sticky="n")

        # Power button
        self.power_button = tk.Button(
            left_frame, image=self.power_icon, bg="green", borderwidth=0,
            activebackground="gray", command=self.toggle_light
        )
        self.power_button.pack(pady=10)  # Add vertical spacing for alignment

        # Apply hover effect to the power button
        self.apply_hover_effect(self.power_button, hover_bg="lightgreen", normal_bg="green")

        # Color buttons (below the power button)
        for color, icon in self.lights_on_icons.items():
            color_button = tk.Button(
                left_frame, bg=color, borderwidth=2, relief="raised", width=6, height=1,
                command=lambda c=color: self.change_bulb_color(c)
            )
            color_button.pack(pady=5)
            # Apply hover effect to each color button
            hover_color = self.get_hover_color(color)
            self.apply_hover_effect(color_button, hover_bg=hover_color, normal_bg=color)

        # Middle column (Light bulb)
        middle_frame = tk.Frame(layout_frame, bg="#f0f0f0")
        middle_frame.grid(row=0, column=1, padx=10)

        self.light_bulb_label = tk.Label(middle_frame, image=self.lights_off_icon, bg="#f0f0f0")
        self.light_bulb_label.pack()

        # Right column (Brightness slider)
        right_frame = tk.Frame(layout_frame, bg="#f0f0f0")
        right_frame.grid(row=0, column=2, sticky="n", padx=8)

        tk.Label(right_frame, text="Brightness", font=("Helvetica", 12), bg="#f0f0f0", fg="#333333").pack(pady=10)

        self.brightness_slider = tk.Scale(
            right_frame, from_=100, to=0, orient=tk.VERTICAL, length=200, width=50,  # Vertical slider
            font=("Helvetica", 10), bg="#f0f0f0", fg="#333333",
            highlightbackground="#f0f0f0", troughcolor="#D3D3D3", activebackground="#4CAF50",
            command=self.change_brightness
        )
        self.brightness_slider.set(0)  # Set initial brightness to 0 (off)
        self.brightness_slider.pack()



    def apply_hover_effect(self, button, hover_bg, normal_bg, hover_fg=None, normal_fg=None):
        """Apply hover effect to a button."""
        def on_enter(e):
            button.config(bg=hover_bg)
            if hover_fg:
                button.config(fg=hover_fg)

        def on_leave(e):
            button.config(bg=normal_bg)
            if normal_fg:
                button.config(fg=normal_fg)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def get_hover_color(self, color):
        """Return a slightly lighter hover color for the given color."""
        hover_colors = {
            "red": "#ff9999",
            "orange": "#ffcc99",
            "yellow": "#ffff99",
            "green": "#ccffcc",
            "blue": "#99ccff",
            "purple": "#d1c4e9",
            "pink": "#ffcce6",
            "white": "#e0e0e0"
        }
        return hover_colors.get(color, "#d9d9d9")  # Default to light gray if color not found

    def toggle_light(self):
        """Toggle light state and update icons."""
        if self.light_on:
            # Turn off the light
            self.light_bulb_label.config(image=self.lights_off_icon)
            self.power_button.config(bg="green")  # Green when off
            self.brightness_slider.set(0)  # Reset brightness to 0
            print("Lights turned off")
        else:
            # Turn on the light
            self.light_bulb_label.config(image=self.lights_on_icons[self.current_color])
            self.power_button.config(bg="red")  # Red when on
            self.brightness_slider.set(50)  # Set brightness to 50% by default
            print("Lights turned on with default brightness 50%")
        
        # Update the hover effect based on state
        self.apply_hover_effect(self.power_button,
                                hover_bg="darkred" if not self.light_on else "lightgreen",
                                normal_bg="red" if not self.light_on else "green")
        self.light_on = not self.light_on  # Toggle the state



    def change_brightness(self, value):
        """Update the brightness based on the slider's position."""
        if self.light_on:  # Check if the lights are on
            self.brightness = int(value)
            print(f"Brightness set to {self.brightness}%")
        else:
            # Reset the slider to 0 if lights are off
            self.brightness_slider.set(0)
            print("Brightness adjustment is disabled because lights are off.")


    def change_bulb_color(self, color):
        """Change the bulb's color when a color button is clicked."""
        if self.light_on:
            self.current_color = color
            self.light_bulb_label.config(image=self.lights_on_icons[color])
            # Show feedback pop-up
            FeedbackPopUp(self, f"Light color changed to {color.capitalize()}!", duration=2000)
        else:
            print("Turn on the light before changing the color.")
            FeedbackPopUp(self, "Turn on the light before changing the color.", duration=2000)

    def add_tv_controls(self, window):
        """Add TV controls."""
        frame = tk.LabelFrame(window, text="TV", font=("Helvetica", 16), bg="#f0f0f0", fg="#000000")
        frame.pack(pady=10, fill="x")

        # Left panel for TV image and On/Off button
        left_panel = tk.Frame(frame, bg="#f0f0f0")
        left_panel.pack(side=tk.LEFT, padx=10)

        try:
            tv_icon_path = os.path.join(self.icons_folder, "tv_icon.png")
            self.tv_icon = Image.open(tv_icon_path).resize((200, 150), Image.LANCZOS)  # Resize the image
            self.tv_icon_photo = ImageTk.PhotoImage(self.tv_icon)  # Convert to PhotoImage
            self.tv_label = tk.Label(left_panel, image=self.tv_icon_photo)  # Use the correct PhotoImage object
            self.tv_label.pack(pady=10)
        except FileNotFoundError:
            self.tv_label = tk.Label(left_panel, text="[TV Image Missing]", bg="#f0f0f0", font=("Helvetica", 14))
            self.tv_label.pack(pady=10)

        # On/Off toggle button
        self.tv_state = False  # TV is initially off
        self.toggle_button = tk.Button(
            left_panel,
            text="Off",
            bg="red",
            fg="white",
            font=("Helvetica", 12),
            width=10,
            command=self.toggle_tv
        )
        self.toggle_button.pack(pady=5)
        self.apply_hover_effect(self.toggle_button, hover_bg="lightblue", normal_bg="red", hover_fg="black", normal_fg="white")

        # Middle panel for Channel controls
        middle_panel = tk.Frame(frame, bg="#f0f0f0")
        middle_panel.pack(side=tk.LEFT, padx=10)

        channel_label = tk.Label(middle_panel, text="Channel", bg="#f0f0f0", font=("Helvetica", 12))
        channel_label.pack(pady=5)

        channel_up = tk.Button(middle_panel, text="▲", font=("Helvetica", 14), command=self.channel_up)
        channel_up.pack(pady=5)
        self.apply_hover_effect(channel_up, hover_bg="lightblue", normal_bg="SystemButtonFace")

        channel_down = tk.Button(middle_panel, text="▼", font=("Helvetica", 14), command=self.channel_down)
        channel_down.pack(pady=5)
        self.apply_hover_effect(channel_down, hover_bg="lightblue", normal_bg="SystemButtonFace")

        # Right panel for Volume control
        right_panel = tk.Frame(frame, bg="#f0f0f0")
        right_panel.pack(side=tk.LEFT, padx=10)

        volume_label = tk.Label(right_panel, text="Volume", bg="#f0f0f0", font=("Helvetica", 12))
        volume_label.pack(pady=5)

        self.volume_scale = ttk.Scale(right_panel, from_=100, to=0, orient="vertical", command=self.change_volume)
        self.volume_scale.set(50)  # Default volume level
        self.volume_scale.pack()

    def toggle_tv(self):
        """Toggle the TV on and off."""
        self.tv_state = not self.tv_state
        if self.tv_state:
            self.toggle_button.config(text="On", bg="green", fg="white")
            self.apply_hover_effect(self.toggle_button, hover_bg="lightblue", normal_bg="green", hover_fg="black", normal_fg="white")
        else:
            self.toggle_button.config(text="Off", bg="red", fg="white")
            self.apply_hover_effect(self.toggle_button, hover_bg="lightblue", normal_bg="red", hover_fg="black", normal_fg="white")
    def channel_up(self):
        print("Channel Up")

    def channel_down(self):
        print("Channel Down")

    def change_volume(self, val):
        print(f"Volume: {int(float(val))}")


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

        # Left panel for Icon and On/Off button
        left_panel = tk.Frame(frame, bg="#f0f0f0")
        left_panel.pack(side=tk.LEFT, padx=10)

        # Load and display Music Icon
        try:
            music_icon_path = os.path.join(self.icons_folder, "music_icon.png")  # Ensure you have this file
            self.music_icon = Image.open(music_icon_path).resize((200, 200), Image.LANCZOS)  # Resize the image
            self.music_icon_photo = ImageTk.PhotoImage(self.music_icon)
            self.music_icon_label = tk.Label(left_panel, image=self.music_icon_photo, bg="#f0f0f0")
            self.music_icon_label.pack(pady=10)
        except FileNotFoundError:
            self.music_icon_label = tk.Label(left_panel, text="[Music Icon Missing]", bg="#f0f0f0", font=("Helvetica", 12))
            self.music_icon_label.pack(pady=10)

        # On/Off button
        self.music_state = False  # Music system initially off
        self.music_toggle_button = tk.Button(
            left_panel,
            text="Off",
            bg="red",
            fg="white",
            font=("Helvetica", 12),
            width=10,
            command=self.toggle_music
        )
        self.music_toggle_button.pack(pady=5)
        self.apply_hover_effect(self.music_toggle_button, hover_bg="lightblue", normal_bg="red", hover_fg="black", normal_fg="white")

        # Middle panel for volume controls
        middle_panel = tk.Frame(frame, bg="#f0f0f0")
        middle_panel.pack(side=tk.LEFT, padx=10)

        volume_label = tk.Label(middle_panel, text="Volume", bg="#f0f0f0", font=("Helvetica", 12))
        volume_label.pack(pady=5)

        self.music_volume_scale = ttk.Scale(
            middle_panel, from_=0, to=100, orient="vertical", command=self.change_music_volume
        )
        self.music_volume_scale.set(50)  # Default volume level
        self.music_volume_scale.pack()

        # Right panel for song controls
        right_panel = tk.Frame(frame, bg="#f0f0f0")
        right_panel.pack(side=tk.LEFT, padx=10)

        song_controls_frame = tk.Frame(right_panel, bg="#f0f0f0")
        song_controls_frame.pack(pady=5)

        prev_button = tk.Button(
            song_controls_frame,
            text="◀ Previous Song",
            font=("Helvetica", 12),
            width=15,
            command=self.previous_song
        )
        prev_button.pack(side=tk.LEFT, padx=5)
        self.apply_hover_effect(prev_button, hover_bg="lightblue", normal_bg="SystemButtonFace")

        next_button = tk.Button(
            song_controls_frame,
            text="Next Song ▶",
            font=("Helvetica", 12),
            width=15,
            command=self.next_song
        )
        next_button.pack(side=tk.LEFT, padx=5)
        self.apply_hover_effect(next_button, hover_bg="lightblue", normal_bg="SystemButtonFace")

    def toggle_music(self):
        """Toggle the music system on and off."""
        self.music_state = not self.music_state
        if self.music_state:
            self.music_toggle_button.config(text="On", bg="green", fg="white")
            self.apply_hover_effect(self.music_toggle_button, hover_bg="lightblue", normal_bg="green", hover_fg="black", normal_fg="white")
            print("Music System: On")
        else:
            self.music_toggle_button.config(text="Off", bg="red", fg="white")
            self.apply_hover_effect(self.music_toggle_button, hover_bg="lightblue", normal_bg="red", hover_fg="black", normal_fg="white")
            print("Music System: Off")

    def change_music_volume(self, val):
        """Adjust the music volume."""
        volume = int(float(val))
        print(f"Music Volume: {volume}")

    def next_song(self):
        """Skip to the next song."""
        print("Playing Next Song")

    def previous_song(self):
        """Play the previous song."""
        print("Playing Previous Song")

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
    
    def on_hover(self, event, button, hover_bg):
        """Change button background color on hover."""
        button.config(bg=hover_bg)

    def on_leave(self, event, button, default_bg):
        """Revert button background color when not hovering."""
        button.config(bg=default_bg)

    def add_thermostat_controls(self, window):
        """Add thermostat controls with Temperature, Mode, Fan, and a centered fan icon."""
        frame = tk.LabelFrame(window, text="Thermostat", font=("Helvetica", 16), bg="#f0f0f0", fg="#000000")
        frame.pack(pady=10, fill="x")

        # Initialize current fan state
        self.current_fan_state = "low"
        # Initialize fan icons dictionary
        self.fan_icons = {
            "low": os.path.join(self.icons_folder, "fan_on_low_icon.png"),
            "medium": os.path.join(self.icons_folder, "fan_on_medium_icon.png"),
            "high": os.path.join(self.icons_folder, "fan_on_high_icon.png"),
            "off": os.path.join(self.icons_folder, "fan_off_icon.png"),
        }

        # Create a container frame for the layout
        layout_frame = tk.Frame(frame, bg="#f0f0f0")
        layout_frame.pack(fill="x", padx=20, pady=10)

        # Column 1: Temperature Control
        temp_frame = tk.Frame(layout_frame, bg="#f0f0f0")
        temp_frame.grid(row=0, column=0, padx=10)

        tk.Label(temp_frame, text="Temperature", font=("Helvetica", 14), bg="#f0f0f0").pack(pady=5)
        self.temp_slider = tk.Scale(
            temp_frame, from_=32, to=18, orient=tk.VERTICAL, length=200, width=40,
            bg="#f0f0f0", troughcolor="#d3d3d3", activebackground="#4CAF50",
            font=("Helvetica", 10), command=self.update_temperature
        )
        self.temp_slider.set(22)  # Default temperature
        self.temp_slider.pack(pady=5)

        self.temp_label = tk.Label(temp_frame, text="22°C", font=("Helvetica", 14), bg="#f0f0f0")
        self.temp_label.pack(pady=5)

        # Column 2: Mode Control
        mode_frame = tk.Frame(layout_frame, bg="#f0f0f0")
        mode_frame.grid(row=0, column=1, padx=10)

        tk.Label(mode_frame, text="Mode", font=("Helvetica", 14), bg="#f0f0f0").pack(pady=5)

        self.mode_buttons = {}
        for mode, color in [("Heating", "orange"), ("Cooling", "light blue"), ("Auto", "light green")]:
            button = tk.Button(
                mode_frame, text=mode, bg=color, font=("Helvetica", 25),
                command=lambda m=mode: self.set_mode(m)
            )
            button.pack(pady=5, fill=tk.X)
            self.mode_buttons[mode] = button

            # Add hover effect
            button.bind("<Enter>", lambda e, btn=button, hover_bg="#ffcccb": self.on_hover(e, btn, hover_bg))
            button.bind("<Leave>", lambda e, btn=button, default_bg=color: self.on_leave(e, btn, default_bg))

        # Column 3: Fan Control
        fan_frame = tk.Frame(layout_frame, bg="#f0f0f0")
        fan_frame.grid(row=0, column=3, padx=10)

        tk.Label(fan_frame, text="Fan", font=("Helvetica", 14), bg="#f0f0f0").pack(pady=5)

        self.fan_buttons = {}
        for state in ["Low", "Medium", "High", "Off"]:
            button = tk.Button(
                fan_frame, text=state, font=("Helvetica", 20),
                command=lambda s=state.lower(): self.set_fan_state(s)
            )
            button.pack(pady=5, fill=tk.X)
            self.fan_buttons[state.lower()] = button

            # Add hover effect
            button.bind("<Enter>", lambda e, btn=button, hover_bg="#ffcccb": self.on_hover(e, btn, hover_bg))
            button.bind("<Leave>", lambda e, btn=button, default_bg="#f0f0f0": self.on_leave(e, btn, default_bg))

        # Highlight default fan state
        self.highlight_fan_button("low")

        # Center Fan Icon
        fan_icon_frame = tk.Frame(layout_frame, bg="#f0f0f0")
        fan_icon_frame.grid(row=0, column=2, padx=10)

        self.fan_icon_label = tk.Label(fan_icon_frame, bg="#f0f0f0")
        self.update_fan_icon()
        self.fan_icon_label.pack(pady=5)




    def load_and_resize_icon(self, filename, width, height):
        """Load and resize an image file."""
        try:
            image_path = os.path.join(self.icons_folder, filename)
            img = Image.open(image_path)  # Open the image file
            img = img.resize((width, height), Image.Resampling.LANCZOS)  # Resize the image
            return ImageTk.PhotoImage(img)  # Convert to PhotoImage for tkinter
        except Exception as e:
            print(f"Error loading fan icon: {e}")
            return None  # Return None if there's an error

    def update_temperature(self, value):
        """Update the temperature label dynamically."""
        self.temp_label.config(text=f"{int(float(value))}°C")

    def set_mode(self, mode):
        """Update the mode state and print the current selection."""
        for button in self.mode_buttons.values():
            button.config(relief=tk.RAISED)
        self.mode_buttons[mode].config(relief=tk.SUNKEN)
        print(f"Mode set to: {mode}")

    def set_fan_state(self, state):
        """Update the fan state and icon dynamically."""
        self.current_fan_state = state
        self.update_fan_icon()
        self.highlight_fan_button(state)
        print(f"Fan set to: {state.capitalize()}")

    def update_fan_icon(self, width=185, height=185):
        """Update the displayed fan icon based on the current state and specified size."""
        try:
            # Retrieve the file path for the current fan state
            img_path = self.fan_icons.get(self.current_fan_state)
            
            if not img_path:
                raise FileNotFoundError(f"Icon for state '{self.current_fan_state}' not found.")
            
            # Open and resize the image
            img = Image.open(img_path).resize((width, height), Image.Resampling.LANCZOS)
            
            # Convert the resized image to a PhotoImage for tkinter
            self.fan_icon = ImageTk.PhotoImage(img)
            
            # Update the fan icon label with the new image
            self.fan_icon_label.config(image=self.fan_icon)
        except FileNotFoundError as fnfe:
            print(f"File not found: {fnfe}")
            self.fan_icon_label.config(text="Icon Missing", image="")
        except Exception as e:
            print(f"Error updating fan icon: {e}")
            self.fan_icon_label.config(text="Error", image="")




    def highlight_fan_button(self, state):
        """Highlight the active fan button."""
        for s, button in self.fan_buttons.items():
            button.config(relief=tk.SUNKEN if s == state else tk.RAISED)


if __name__ == "__main__":
    queue = Queue()
    p = Process(target=gesture_recognition, args=(queue,))
    p.start()
    app = SmartHouseGUI()
    app.mainloop()
    p.join()