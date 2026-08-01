import threading
import time
import webbrowser
import customtkinter as ctk
from PIL import Image, ImageEnhance
import mss
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor
ctk.set_appearance_mode("Dark")
BG_DARK = "#08090D"
CARD_BG = "#12141D"
CARD_BORDER = "#1E2233"
ACCENT_CYAN = "#06B6D4"
ACCENT_PURPLE = "#8B5CF6"
ACCENT_GREEN = "#10B981"
ACCENT_RED = "#EF4444"
TEXT_MUTED = "#6B7280"
class LuminaRGBPro(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Keyboard Enchanter")
        self.geometry("460x730")
        self.resizable(False, False)
        self.configure(fg_color=BG_DARK)

        self.client = None
        self.keyboards = []
        self.is_running = False
        self.worker_thread = None

        self.curr_r, self.curr_g, self.curr_b = 0, 0, 0

        self.init_openrgb()
        self.build_gui()

    def init_openrgb(self):
        """Attempts connection to local OpenRGB SDK server."""
        try:
            self.client = OpenRGBClient(address='127.0.0.1', port=6742)
            self.keyboards = [dev for dev in self.client.devices if dev.type.name == 'KEYBOARD']
        except Exception:
            self.client = None
            self.keyboards = []

    def open_instagram(self):
        """Opens user Instagram profile in default browser."""
        webbrowser.open("https://instagram.com/matei.tem")

    def build_gui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=24, pady=(20, 8))

        title_box = ctk.CTkFrame(header, fg_color="transparent")
        title_box.pack(side="left")

        title_label = ctk.CTkLabel(
            title_box,
            text="Screen Miroring on Keyboard", #I don't have any better name for this, if you have a better name, please tell me 
            font=ctk.CTkFont(family="Inter", size=22, weight="bold"),
            text_color="#FFFFFF"
        )
        title_label.pack(anchor="w")

        sub_label = ctk.CTkLabel(
            title_box,
            text="Screen Ambience Engine",
            font=ctk.CTkFont(size=11),
            text_color=TEXT_MUTED
        )
        sub_label.pack(anchor="w")

        self.status_badge = ctk.CTkLabel(
            header,
            text="● IDLE",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=TEXT_MUTED,
            fg_color="#1A1D2B",
            corner_radius=12,
            padx=12,
            pady=5
        )
        self.status_badge.pack(side="right")

        social_card = ctk.CTkFrame(self, fg_color=CARD_BG, border_color=CARD_BORDER, border_width=1, corner_radius=12)
        social_card.pack(fill="x", padx=20, pady=6)

        ctk.CTkLabel(
            social_card,
            text="CREATED BY",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=TEXT_MUTED
        ).pack(side="left", padx=(14, 6), pady=8)

        insta_btn = ctk.CTkButton(
            social_card,
            text="📸 @matei.tem",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#251A38",
            hover_color="#3B265C",
            text_color=ACCENT_PURPLE,
            height=28,
            corner_radius=8,
            command=self.open_instagram
        )
        insta_btn.pack(side="left", pady=8)

        ctk.CTkLabel(
            social_card,
            text="Click to open",
            font=ctk.CTkFont(size=10),
            text_color=TEXT_MUTED
        ).pack(side="right", padx=14)

        hw_card = ctk.CTkFrame(self, fg_color=CARD_BG, border_color=CARD_BORDER, border_width=1, corner_radius=14)
        hw_card.pack(fill="x", padx=20, pady=6)

        ctk.CTkLabel(
            hw_card, 
            text="HARDWARE & SOURCE", 
            font=ctk.CTkFont(size=11, weight="bold"), 
            text_color=ACCENT_CYAN
        ).pack(anchor="w", padx=16, pady=(12, 6))

        dev_row = ctk.CTkFrame(hw_card, fg_color="transparent")
        dev_row.pack(fill="x", padx=16, pady=(0, 8))

        kb_options = ["All Keyboards"] + [kb.name for kb in self.keyboards] if self.keyboards else ["No OpenRGB Found"]
        self.device_var = ctk.StringVar(value=kb_options[0])
        
        self.device_dropdown = ctk.CTkOptionMenu(
            dev_row, 
            variable=self.device_var, 
            values=kb_options,
            fg_color="#181B28",
            button_color="#262B3E",
            dropdown_fg_color="#12141D",
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=12)
        )
        self.device_dropdown.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.refresh_btn = ctk.CTkButton(
            dev_row,
            text="↻",
            width=36,
            height=28,
            fg_color="#181B28",
            hover_color="#262B3E",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.refresh_devices
        )
        self.refresh_btn.pack(side="right")

        with mss.mss() as sct:
            monitor_count = len(sct.monitors) - 1
        mon_options = [f"Display {i}" for i in range(1, max(2, monitor_count + 1))]
        
        self.monitor_var = ctk.StringVar(value=mon_options[0])
        self.mon_dropdown = ctk.CTkOptionMenu(
            hw_card,
            variable=self.monitor_var,
            values=mon_options,
            fg_color="#181B28",
            button_color="#262B3E",
            dropdown_fg_color="#12141D",
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=12)
        )
        self.mon_dropdown.pack(fill="x", padx=16, pady=(0, 12))

        vis_card = ctk.CTkFrame(self, fg_color=CARD_BG, border_color=CARD_BORDER, border_width=1, corner_radius=14)
        vis_card.pack(fill="x", padx=20, pady=6)

        ctk.CTkLabel(
            vis_card, 
            text="LIVE COLOR STREAM", 
            font=ctk.CTkFont(size=11, weight="bold"), 
            text_color=ACCENT_CYAN
        ).pack(anchor="w", padx=16, pady=(10, 6))

        self.preview_box = ctk.CTkFrame(vis_card, height=44, corner_radius=10, fg_color="#0A0B10")
        self.preview_box.pack(fill="x", padx=16, pady=(0, 10))
        self.preview_box.pack_propagate(False)

        self.hex_label = ctk.CTkLabel(
            self.preview_box, 
            text="#000000", 
            font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
            text_color="#4B5563"
        )
        self.hex_label.pack(expand=True)

        sliders_card = ctk.CTkFrame(self, fg_color=CARD_BG, border_color=CARD_BORDER, border_width=1, corner_radius=14)
        sliders_card.pack(fill="x", padx=20, pady=6)

        self.sat_label = ctk.CTkLabel(sliders_card, text="Color Saturation: 2.2x", font=ctk.CTkFont(size=12), text_color="#E5E7EB")
        self.sat_label.pack(anchor="w", padx=16, pady=(10, 0))
        self.sat_slider = ctk.CTkSlider(
            sliders_card, from_=1.0, to=4.0, button_color=ACCENT_CYAN, progress_color=ACCENT_CYAN, command=self.update_slider_labels
        )
        self.sat_slider.set(2.2)
        self.sat_slider.pack(fill="x", padx=16, pady=(2, 6))

        self.bright_label = ctk.CTkLabel(sliders_card, text="Brightness Boost: 1.2x", font=ctk.CTkFont(size=12), text_color="#E5E7EB")
        self.bright_label.pack(anchor="w", padx=16, pady=(2, 0))
        self.bright_slider = ctk.CTkSlider(
            sliders_card, from_=0.5, to=2.0, button_color=ACCENT_CYAN, progress_color=ACCENT_CYAN, command=self.update_slider_labels
        )
        self.bright_slider.set(1.2)
        self.bright_slider.pack(fill="x", padx=16, pady=(2, 6))

        self.smooth_label = ctk.CTkLabel(sliders_card, text="Color Smoothness: Fast (80%)", font=ctk.CTkFont(size=12), text_color="#E5E7EB")
        self.smooth_label.pack(anchor="w", padx=16, pady=(2, 0))
        self.smooth_slider = ctk.CTkSlider(
            sliders_card, from_=0.1, to=1.0, button_color=ACCENT_CYAN, progress_color=ACCENT_CYAN, command=self.update_slider_labels
        )
        self.smooth_slider.set(0.8)
        self.smooth_slider.pack(fill="x", padx=16, pady=(2, 6))

        self.fps_label = ctk.CTkLabel(sliders_card, text="Target Refresh Rate: 30 FPS", font=ctk.CTkFont(size=12), text_color="#E5E7EB")
        self.fps_label.pack(anchor="w", padx=16, pady=(2, 0))
        self.fps_slider = ctk.CTkSlider(
            sliders_card, from_=15, to=60, number_of_steps=45, button_color=ACCENT_CYAN, progress_color=ACCENT_CYAN, command=self.update_slider_labels
        )
        self.fps_slider.set(30)
        self.fps_slider.pack(fill="x", padx=16, pady=(2, 12))

        self.start_btn = ctk.CTkButton(
            self, 
            text="ENABLE SCREEN AMBIENCE", 
            font=ctk.CTkFont(size=14, weight="bold"), 
            height=48, 
            corner_radius=12,
            fg_color=ACCENT_CYAN,
            hover_color="#0891B2",
            text_color="#000000",
            command=self.toggle_sync
        )
        self.start_btn.pack(fill="x", padx=20, pady=(12, 16))

    def refresh_devices(self):
        self.init_openrgb()
        kb_options = ["All Keyboards"] + [kb.name for kb in self.keyboards] if self.keyboards else ["No OpenRGB Found"]
        self.device_dropdown.configure(values=kb_options)
        self.device_var.set(kb_options[0])

    def update_slider_labels(self, _=None):
        self.sat_label.configure(text=f"Color Saturation: {self.sat_slider.get():.1f}x")
        self.bright_label.configure(text=f"Brightness Boost: {self.bright_slider.get():.1f}x")
        
        smooth_val = int(self.smooth_slider.get() * 100)
        smooth_text = "Ultra Smooth" if smooth_val < 35 else ("Fluid" if smooth_val < 70 else "Fast")
        self.smooth_label.configure(text=f"Color Smoothness: {smooth_text} ({smooth_val}%)")

        self.fps_label.configure(text=f"Target Refresh Rate: {int(self.fps_slider.get())} FPS")

    def toggle_sync(self):
        if not self.is_running:
            if not self.client or not self.keyboards:
                self.init_openrgb()
                if not self.keyboards:
                    self.status_badge.configure(text="● SERVER OFFLINE", text_color=ACCENT_RED, fg_color="#3B1D1D")
                    return

            self.is_running = True
            self.start_btn.configure(text="STOP ENGINE", fg_color=ACCENT_RED, hover_color="#DC2626", text_color="#FFFFFF")
            self.status_badge.configure(text="● ACTIVE", text_color=ACCENT_GREEN, fg_color="#18382B")

            self.worker_thread = threading.Thread(target=self.sync_loop, daemon=True)
            self.worker_thread.start()
        else:
            self.is_running = False
            self.start_btn.configure(text="ENABLE SCREEN AMBIENCE", fg_color=ACCENT_CYAN, hover_color="#0891B2", text_color="#000000")
            self.status_badge.configure(text="● IDLE", text_color=TEXT_MUTED, fg_color="#1A1D2B")
            self.preview_box.configure(fg_color="#0A0B10")
            self.hex_label.configure(text="#000000", text_color="#4B5563")

    def get_target_keyboards(self):
        selected = self.device_var.get()
        if selected == "All Keyboards":
            return self.keyboards
        return [kb for kb in self.keyboards if kb.name == selected]

    def sync_loop(self):
        """Screen capture loop with color smoothing."""
        with mss.mss() as sct:
            while self.is_running:
                t_start = time.perf_counter()

                # Get monitor index
                try:
                    mon_index = int(self.monitor_var.get().split(" ")[-1])
                    monitor = sct.monitors[mon_index]
                except (IndexError, ValueError):
                    monitor = sct.monitors[1]

                sct_img = sct.grab(monitor)
                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
                dominant_pixel = img.resize((1, 1), Image.Resampling.BILINEAR)

                sat_val = self.sat_slider.get()
                bright_val = self.bright_slider.get()

                if sat_val != 1.0:
                    dominant_pixel = ImageEnhance.Color(dominant_pixel).enhance(sat_val)
                if bright_val != 1.0:
                    dominant_pixel = ImageEnhance.Brightness(dominant_pixel).enhance(bright_val)

                target_r, target_g, target_b = dominant_pixel.getpixel((0, 0))

                speed = self.smooth_slider.get()
                self.curr_r += (target_r - self.curr_r) * speed
                self.curr_g += (target_g - self.curr_g) * speed
                self.curr_b += (target_b - self.curr_b) * speed

                r, g, b = int(self.curr_r), int(self.curr_g), int(self.curr_b)
                color = RGBColor(r, g, b)

                for kb in self.get_target_keyboards():
                    try:
                        kb.set_color(color)
                    except Exception:
                        pass

                hex_code = f"#{r:02x}{g:02x}{b:02x}".upper()
                text_col = "#FFFFFF" if (r * 0.299 + g * 0.587 + b * 0.114) < 128 else "#000000"
                
                try:
                    self.preview_box.configure(fg_color=hex_code)
                    self.hex_label.configure(text=f"{hex_code}  |  RGB({r}, {g}, {b})", text_color=text_col)
                except Exception:
                    pass

                target_fps = self.fps_slider.get()
                interval = 1.0 / target_fps
                elapsed = time.perf_counter() - t_start
                if interval > elapsed:
                    time.sleep(interval - elapsed)


if __name__ == "__main__":
    app = LuminaRGBPro()
    app.mainloop()
