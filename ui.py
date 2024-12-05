import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime

class SmartHouseGUI(tk.Tk):
    def __init__(self):
        super().__init__()

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
        # Clock
        try:
            clock_image = Image.open("D:\\YASEMIN\\F24\\cs449\\cs449\\icons\\clock_icon.png").resize((70, 70), Image.LANCZOS)
            self.clock_icon = ImageTk.PhotoImage(clock_image)
            clock_label = tk.Label(parent, image=self.clock_icon, bg="#f0f0f0")
            clock_label.pack(side=tk.LEFT, padx=10)
        except Exception as e:
            clock_label = tk.Label(
                parent, text="Clock icon not found",
                font=("Helvetica", 14), bg="#f0f0f0", fg="#ff0000"
            )
            clock_label.pack(side=tk.LEFT, padx=10)
            print(f"Error loading clock icon: {e}")

        self.time_label = tk.Label(
            parent, text="", font=("Helvetica", 28), bg="#f0f0f0", fg="#333333"
        )
        self.time_label.pack(side=tk.LEFT, padx=10)
        self.update_time()

        # Temperature
        try:
            temp_image = Image.open("D:\\YASEMIN\\F24\\cs449\\cs449\\icons\\temperature_icon.png").resize((70, 70), Image.LANCZOS)
            self.temp_icon = ImageTk.PhotoImage(temp_image)
            temp_label = tk.Label(parent, image=self.temp_icon, bg="#f0f0f0")
            temp_label.pack(side=tk.LEFT, padx=10)
        except Exception as e:
            temp_label = tk.Label(
                parent, text="Temp icon not found",
                font=("Helvetica", 14), bg="#f0f0f0", fg="#ff0000"
            )
            temp_label.pack(side=tk.LEFT, padx=10)
            print(f"Error loading temperature icon: {e}")

        self.temperature_label = tk.Label(
            parent, text="22°C", font=("Helvetica", 28), bg="#f0f0f0", fg="#333333"
        )
        self.temperature_label.pack(side=tk.LEFT, padx=10)

        # Humidity
        try:
            humidity_image = Image.open("D:\\YASEMIN\\F24\\cs449\\cs449\\icons\\humidity_icon.png").resize((70, 70), Image.LANCZOS)
            self.humidity_icon = ImageTk.PhotoImage(humidity_image)
            humidity_label = tk.Label(parent, image=self.humidity_icon, bg="#f0f0f0")
            humidity_label.pack(side=tk.LEFT, padx=10)
        except Exception as e:
            humidity_label = tk.Label(
                parent, text="Humidity icon not found",
                font=("Helvetica", 14), bg="#f0f0f0", fg="#ff0000"
            )
            humidity_label.pack(side=tk.LEFT, padx=10)
            print(f"Error loading humidity icon: {e}")

        self.humidity_label = tk.Label(
            parent, text="50%", font=("Helvetica", 28), bg="#f0f0f0", fg="#333333"
        )
        self.humidity_label.pack(side=tk.LEFT, padx=10)

        # Energy Consumption
        try:
            energy_image = Image.open("D:\\YASEMIN\\F24\\cs449\\cs449\\icons\\energy_icon.png").resize((70, 70), Image.LANCZOS)
            self.energy_icon = ImageTk.PhotoImage(energy_image)
            energy_label = tk.Label(parent, image=self.energy_icon, bg="#f0f0f0")
            energy_label.pack(side=tk.LEFT, padx=10)
        except Exception as e:
            energy_label = tk.Label(
                parent, text="Energy icon not found",
                font=("Helvetica", 14), bg="#f0f0f0", fg="#ff0000"
            )
            energy_label.pack(side=tk.LEFT, padx=10)
            print(f"Error loading energy icon: {e}")

        self.energy_label = tk.Label(
            parent, text="450 kWh", font=("Helvetica", 28), bg="#f0f0f0", fg="#333333"
        )
        self.energy_label.pack(side=tk.LEFT, padx=10)

        # Light Percentage
        try:
            light_image = Image.open("D:\\YASEMIN\\F24\\cs449\\cs449\\icons\\light_icon.png").resize((70, 70), Image.LANCZOS)
            self.light_icon = ImageTk.PhotoImage(light_image)
            light_label = tk.Label(parent, image=self.light_icon, bg="#f0f0f0")
            light_label.pack(side=tk.LEFT, padx=10)
        except Exception as e:
            light_label = tk.Label(
                parent, text="Light icon not found",
                font=("Helvetica", 14), bg="#f0f0f0", fg="#ff0000"
            )
            light_label.pack(side=tk.LEFT, padx=10)
            print(f"Error loading light icon: {e}")

        self.light_label = tk.Label(
            parent, text="75%", font=("Helvetica", 28), bg="#f0f0f0", fg="#333333"
        )
        self.light_label.pack(side=tk.LEFT, padx=10)

        # Air Quality Index (AQI)
        try:
            aqi_image = Image.open("D:\\YASEMIN\\F24\\cs449\\cs449\\icons\\aqi_icon.png").resize((70, 70), Image.LANCZOS)
            self.aqi_icon = ImageTk.PhotoImage(aqi_image)
            aqi_label = tk.Label(parent, image=self.aqi_icon, bg="#f0f0f0")
            aqi_label.pack(side=tk.LEFT, padx=10)
        except Exception as e:
            aqi_label = tk.Label(
                parent, text="AQI icon not found",
                font=("Helvetica", 14), bg="#f0f0f0", fg="#ff0000"
            )
            aqi_label.pack(side=tk.LEFT, padx=10)
            print(f"Error loading AQI icon: {e}")

        self.aqi_label = tk.Label(
            parent, text="AQI: 45", font=("Helvetica", 28), bg="#f0f0f0", fg="#333333"
        )
        self.aqi_label.pack(side=tk.LEFT, padx=10)

    def add_room_widgets(self):
        rooms = [
            ("Bedroom", "D:\\YASEMIN\\F24\\cs449\\cs449\\icons\\bedroom_icon.png"),
            ("Kids Room", "D:\\YASEMIN\\F24\\cs449\\cs449\\icons\\kidsroom_icon.png"),
            ("Living Room", "D:\\YASEMIN\\F24\\cs449\\cs449\\icons\\livingroom_icon.png"),
            ("Office", "D:\\YASEMIN\\F24\\cs449\\cs449\\icons\\office_icon.png"),
            ("Kitchen", "D:\\YASEMIN\\F24\\cs449\\cs449\\icons\\kitchen_icon.png"),
            ("Bathroom", "D:\\YASEMIN\\F24\\cs449\\cs449\\icons\\bathroom_icon.png"),
            ("Dressing Room", "D:\\YASEMIN\\F24\\cs449\\cs449\\icons\\dressingroom_icon.png"),
            ("Garage", "D:\\YASEMIN\\F24\\cs449\\cs449\\icons\\garage_icon.png")
        ]

        for i, (room_name, icon_path) in enumerate(rooms):
            row = i // 2
            col = i % 2

            try:
                room_image = Image.open(icon_path).resize((150, 150), Image.LANCZOS)
                room_icon = ImageTk.PhotoImage(room_image)
            except Exception as e:
                print(f"Error loading icon for {room_name}: {e}")
                room_icon = None

            btn_frame = tk.Frame(self.room_list_frame, bg="#d9d9d9", bd=2, relief="raised", width=400, height=300)
            btn_frame.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
            btn_frame.grid_propagate(False)  # Prevent frame resizing to fit content

            def on_room_click(room=room_name):
                print(f"{room} clicked")

            btn = tk.Button(
                btn_frame, text=room_name, font=("Helvetica", 16),
                bg="#ffffff", fg="#000000", image=room_icon, compound="top",
                width=400, height=300, command=on_room_click
            )
            btn.image = room_icon  # Keep a reference to avoid garbage collection
            btn.pack(fill="both", expand=True)

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.configure(text=current_time)
        self.after(1000, self.update_time)

if __name__ == "__main__":
    app = SmartHouseGUI()
    app.mainloop()
