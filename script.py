import os
import tkinter as tk
import random
import pygame
from PIL import Image, ImageTk
from pathlib import Path

from pygame import mixer

# Initialize pygame mixer
pygame.mixer.init()
SOUNDTRACK = {
    'menu_playlist': [
        'music/song1.mp3',
        'music/song2.mp3',
        'music/song3.mp3'
    ],
    'quiz_playlist': [
        'music/quiz1.mp3',
        'music/quiz2.mp3'
    ],
    'result_playlist': [
        'music/result1.mp3',
        'music/result2.mp3'
    ],
    'button_click': 'sounds/click.wav'
}

# Quiz questions and data
questions = [
    {
        'question': "What motivates you to join an exchange program?",
        'options': [
            ('Personal growth and development', 'growth'),
            ('Making a positive impact in local communities', 'impact'),
            ('Exploring new places and cultures', 'explorer'),
        ]
    },
    {
        'question': "Which experience excites you the most?",
        'options': [
            ('Starting the day with a delicious Turkish breakfast', 'explorer'),
            ('Riding a tuk-tuk through bustling local streets', 'explorer'),
            ('Tasting fresh mangoes straight from the market', 'growth'),
        ]
    },
    {
        'question': "I'm most looking forward to...",
        'options': [
            ('Making lots of new friends abroad', 'impact'),
            ('Understanding new cultures', 'explorer'),
            ('Having a lot of fun along the way', 'growth'),
        ]
    },
    {
        'question': "What concerns you the most?",
        'options': [
            ('High transportation costs', 'impact'),
            ('Struggling to adapt to a new environment', 'explorer'),
            ('Not enjoying the local food', 'growth'),
        ]
    },
    {
        'question': "It would be interesting to...",
        'options': [
            ('Teach and support others in learning', 'impact'),
            ('Help protect marine life on a sunny beach', 'explorer'),
            ('Lead workshops on topics Im passionate about', 'growth'),
        ]
    },
]

trait_scores = {
    'growth': 0,
    'explorer': 0,
    'impact': 0
}
recommendations = {
    'growth': [
        {'name': 'Fingerprint', 'country': 'Brazil', 'image': 'images/india.jpg',
         'logo': 'images/fingerprint_logo.jpeg'},
        {'name': 'Heartbeat', 'country': 'Morocco', 'image': 'images/india.jpg', 'logo': 'images/heartbeat_logo.jpeg'}
    ],
    'explorer': [
        {'name': 'Aquatica', 'country': 'Tunisia', 'image': 'images/india.jpg', 'logo': 'images/aquatica_logo.jpeg'},
        {'name': 'Skill Up!', 'country': 'Egypt', 'image': 'images/india.jpg', 'logo': 'images/skillup_logo.jpeg'}
    ],
    'impact': [
        {'name': 'Global Classroom', 'country': 'Turkiye', 'image': 'images/india.jpg', 'logo': 'images/glologo.jpeg'},
        {'name': 'Happy Bus', 'country': 'India', 'image': 'images/india.jpg', 'logo': 'images/happybus_logo.jpeg'}
    ]
}
trait_titles = {
    'growth': "🌱 Growth Seeker",
    'explorer': "🌍 Culture Explorer",
    'impact': "🤝 Impact Maker"
}


def animate_button(button, original_color=None):
    """Handle button animation and sound effect"""
    try:
        click_sound = pygame.mixer.Sound("music/click_sound.wav")
        click_sound.play()
    except:
        pass  # Continue without sound if file not found

    if original_color is None:
        original_color = button.cget("background")

    button.config(
        background="#0b411c",
        activebackground="#0b411c",
        foreground="white",
        activeforeground="white"
    )
    button.after(200, lambda: button.config(
        background=original_color,
        activebackground=original_color,
        foreground="black",
        activeforeground="black"
    ))


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.quiz_app = self
        self.root.title("Be A Global Volunteer Quiz")
        trait_scores = {'growth': 0, 'explorer': 0, 'impact': 0}

        # Full-screen setup
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")

        # Reset scores
        self.reset_scores()

        # Load images
        self.load_images()

        # Setup UI
        self.setup_ui()

        # Show first question
        self.show_question()

    def reset_scores(self):
        global trait_scores
        trait_scores = {'growth': 0, 'explorer': 0, 'impact': 0}
        self.question_index = 0
        self.result_window = None

    def load_images(self):
        """Load and resize images"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Background image
        original_bg = Image.open("background.png")
        resized_bg = original_bg.resize((screen_width, screen_height))
        self.bg_image = ImageTk.PhotoImage(resized_bg)

        # Logo image
        original_logo = Image.open("white.png")
        logo_width = int(screen_width * 0.3)
        logo_height = int(original_logo.height * (logo_width / original_logo.width))
        resized_logo = original_logo.resize((logo_width, logo_height))
        self.logo_image = ImageTk.PhotoImage(resized_logo)

    def setup_ui(self):
        """Create all UI elements"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create canvas
        self.canvas = tk.Canvas(self.root, width=self.root.winfo_screenwidth(),
                                height=self.root.winfo_screenheight(), highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Background image
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Logo
        self.canvas.create_image(self.root.winfo_screenwidth() / 2,
                                 self.root.winfo_screenheight() / 5,
                                 image=self.logo_image, anchor="center")

        # Question label
        self.question_label = tk.Label(
            self.canvas,
            text="",
            font=("Raleway", 25, "bold italic"),
            fg="black",
            bg="white",
            wraplength=self.root.winfo_screenwidth() * 0.8,
            justify="center"
        )
        self.canvas.create_window(
            self.root.winfo_screenwidth() / 2,
            self.root.winfo_screenheight() * 0.4,
            window=self.question_label,
            anchor="center"
        )

        # Answer buttons
        self.buttons = []
        button_positions = [0.5, 0.65, 0.8]  # Relative y positions

        for i in range(3):
            btn = tk.Button(
                self.canvas,
                text="",
                font=("Raleway", 17, "italic"),
                wraplength=self.root.winfo_screenwidth(),
                justify="center",
                width=40,
                height=4,
                bg="white",
                fg="black",
                command=lambda i=i: self.select_option(i)
            )
            self.canvas.create_window(
                self.root.winfo_screenwidth() / 2,
                self.root.winfo_screenheight() * button_positions[i],
                window=btn,
                anchor="center"
            )
            btn.bind("<Button-1>", lambda e, b=btn: animate_button(b))
            self.buttons.append(btn)

        # Back to Menu button
        self.menu_btn = tk.Button(
            self.canvas,
            text="Back to Menu",
            font=("Raleway", 20),
            bg="#0b411c",
            fg="white",
            command=self.return_to_menu
        )
        self.canvas.create_window(
            self.root.winfo_screenwidth() - 100,
            self.root.winfo_screenheight() - 50,
            window=self.menu_btn,
            anchor="center"
        )
        self.menu_btn.bind("<Button-1>", lambda e, b=self.menu_btn: animate_button(b))

    def show_question(self):
        """Display the current question"""
        if self.question_index < len(questions):
            q = questions[self.question_index]
            self.question_label.config(text=q['question'])

            for i, (text, _) in enumerate(q['options']):
                self.buttons[i].config(text=text)
        else:
            self.show_result()

    def select_option(self, index):
        """Handle answer selection"""
        trait = questions[self.question_index]['options'][index][1]
        trait_scores[trait] += 1
        self.question_index += 1
        self.show_question()

    def show_result(self):
        """Display the quiz results"""
        max_score = max(trait_scores.values())
        top_traits = [trait for trait, score in trait_scores.items() if score == max_score]
        chosen_trait = random.choice(top_traits)
        self.result_window = ResultWindow(self.root, chosen_trait)

    def return_to_menu(self):
        """Return to the main menu"""
        if self.result_window:
            self.result_window.destroy()
        MainMenu(self.root)

    def start_quiz(self):
        """Start the quiz"""

        QuizApp(self.root)

    def reset_quiz(self):
        """Reset the quiz to start immediately"""
        # Reset scores
        global trait_scores
        trait_scores = {'growth': 0, 'explorer': 0, 'impact': 0}
        self.question_index = 0

        # Close result window if it exists
        if hasattr(self, 'result_window') and self.result_window:
            self.result_window.window.destroy()

        # Show first question
        self.show_question()

    def return_to_menu(self):
        """Return to main menu"""
        # Destroy all quiz widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        # Recreate main menu
        MainMenu(self.root)


class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Be A Global Volunteer")

        # Full-screen setup
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")

        # Load images
        self.load_images()

        # Setup UI
        self.setup_ui()
        self.root.music_player.load_playlist('menu_playlist')

    def load_images(self):
        """Load and resize images"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Background image
        original_bg = Image.open("main_menu_background.png")
        resized_bg = original_bg.resize((screen_width, screen_height))
        self.bg_image = ImageTk.PhotoImage(resized_bg)

        # Logo image
        original_logo = Image.open("green.png")
        logo_width = int(screen_width * 0.3)
        logo_height = int(original_logo.height * (logo_width / original_logo.width))
        resized_logo = original_logo.resize((logo_width, logo_height))
        self.logo_image = ImageTk.PhotoImage(resized_logo)

    def setup_ui(self):
        """Create all UI elements"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create canvas
        self.canvas = tk.Canvas(self.root, width=self.root.winfo_screenwidth(),
                                height=self.root.winfo_screenheight(), highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Background image
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Logo
        self.canvas.create_image(self.root.winfo_screenwidth() / 2,
                                 self.root.winfo_screenheight() / 4,
                                 image=self.logo_image, anchor="center")

        # Menu buttons
        button_frame = tk.Frame(self.canvas, bg="")
        self.canvas.create_window(
            self.root.winfo_screenwidth() / 2,
            self.root.winfo_screenheight() * 0.6,
            window=button_frame,
            anchor="center"
        )

        buttons = [
            ("Start Quiz", self.start_quiz),
            ("Settings", self.show_settings),
            ("Exit", self.root.destroy)
        ]

        for text, command in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                font=("Raleway", 16, "bold"),
                width=20,
                height=2,
                bg="#0b411c",
                fg="white",
                activebackground="#0b411c",
                activeforeground="white",
                command=command
            )
            btn.pack(pady=10)



    def start_quiz(self):
        """Start the quiz"""
        QuizApp(self.root)

    def show_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Music Settings")
        settings_window.geometry("450x400")  # Slightly larger for all controls
        settings_window.resizable(False, False)

        # Make settings window modal
        settings_window.grab_set()

        # Music Controls Frame
        controls_frame = tk.Frame(settings_window, padx=20, pady=10)
        controls_frame.pack(fill="x")

        # Now Playing Label
        self.now_playing_label = tk.Label(
            controls_frame,
            text=self.get_current_track_name(),
            font=("Raleway", 12, "italic"),
            wraplength=400
        )
        self.now_playing_label.pack(pady=5)

        # Playback Buttons
        btn_frame = tk.Frame(controls_frame)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="⏮ Previous",
            command=self.previous_track,
            width=10
        ).pack(side="left", padx=5)

        self.play_pause_btn = tk.Button(
            btn_frame,
            text="⏸ Pause" if mixer.music.get_busy() else "▶ Play",
            command=self.toggle_playback,
            width=10
        )
        self.play_pause_btn.pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="⏭ Next",
            command=self.next_track,
            width=10
        ).pack(side="left", padx=5)

        # Volume Control Frame
        volume_frame = tk.Frame(controls_frame)
        volume_frame.pack(fill="x", pady=10)

        tk.Label(
            volume_frame,
            text="Volume:",
            font=("Raleway", 12)
        ).pack(side="left")

        self.volume_slider = tk.Scale(
            volume_frame,
            from_=0,
            to=100,
            orient="horizontal",
            command=self.update_volume,
            length=300
        )
        self.volume_slider.set(int(self.root.music_player.volume * 100))
        self.volume_slider.pack(side="left", padx=10)

        self.mute_btn = tk.Button(
            volume_frame,
            text="🔇 Mute" if self.root.music_player.volume == 0 else "🔊 Unmute",
            command=self.toggle_mute,
            width=8
        )
        self.mute_btn.pack(side="left", padx=5)

        # Close Button
        close_btn = tk.Button(
            settings_window,
            text="Close Settings",
            command=settings_window.destroy,
            font=("Raleway", 12),
            width=15,
            bg="#0b411c",
            fg="white"
        )
        close_btn.pack(pady=20)
        close_btn.bind("<Button-1>", lambda e, b=close_btn: animate_button(b))
        def update_volume(self, val):
            """Update volume from slider"""
            volume = float(val) / 100
            self.root.music_player.set_volume(volume)
            # Update mute button state
            self.mute_btn.config(
                text="🔇 Mute" if volume == 0 else "🔊 Unmute"
            )

        def toggle_mute(self):
            """Toggle mute state"""
            if self.root.music_player.volume > 0:
                self.saved_volume = self.root.music_player.volume
                self.root.music_player.set_volume(0)
                self.volume_slider.set(0)
                self.mute_btn.config(text="🔇 Mute")
            else:
                self.root.music_player.set_volume(self.saved_volume)
                self.volume_slider.set(int(self.saved_volume * 100))
                self.mute_btn.config(text="🔊 Unmute")

    def get_current_track_name(self):
        """Get formatted current track name"""
        player = self.root.music_player
        if player.current_playlist:
            filename = player.current_playlist[player.current_track_index]
            name = os.path.splitext(os.path.basename(filename))[0]
            return f"Now Playing: {name}"
        return "No track playing"

    def toggle_playback(self):
        """Toggle between play/pause"""
        if mixer.music.get_busy():
            mixer.music.pause()
            self.play_pause_btn.config(text="▶ Play")
        else:
            mixer.music.unpause()
            self.play_pause_btn.config(text="⏸ Pause")

    def next_track(self):
        """Skip to next track"""
        self.root.music_player.next_track()
        self.now_playing_label.config(text=self.get_current_track_name())

    def previous_track(self):
        """Go to previous track"""
        player = self.root.music_player
        player.current_track_index = (player.current_track_index - 1) % len(player.current_playlist)
        player.play_current_track()
        self.now_playing_label.config(text=self.get_current_track_name())

    def update_volume(self, val):
        """Update volume from slider"""
        volume = float(val) / 100
        self.root.music_player.set_volume(volume)
        self.mute_btn.config(text="🔇 Mute" if volume == 0 else "🔊 Unmute")

    def toggle_mute(self):
        """Toggle mute state"""
        if self.root.music_player.volume > 0:
            self.saved_volume = self.root.music_player.volume
            self.root.music_player.set_volume(0)
            self.volume_slider.set(0)
            self.mute_btn.config(text="🔇 Mute")
        else:
            self.root.music_player.set_volume(self.saved_volume)
            self.volume_slider.set(int(self.saved_volume * 100))
            self.mute_btn.config(text="🔊 Unmute")

class ResultWindow:
    def __init__(self, parent, chosen_trait):
        self.parent = parent
        self.chosen_trait = chosen_trait
        self.project = random.choice(recommendations[chosen_trait])

        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title("Your Matched Profile")

        # Set window size and position
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        window_width = 800
        window_height = 600
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.window.resizable(False, False)

        # Load images
        self.load_images()

        # Setup UI
        self.setup_ui()

    def load_images(self):
        """Load background and logo images with error handling"""
        try:
            # Load background image
            bg_path = Path(self.project['image'])
            original_bg = Image.open(bg_path)
            self.bg_image = ImageTk.PhotoImage(original_bg.resize((800, 600)))

            # Load logo image
            logo_path = Path(self.project['logo'])
            original_logo = Image.open(logo_path)
            # Resize logo to be about 30% of window width
            logo_width = int(800 * 0.3)
            logo_height = int(original_logo.height * (logo_width / original_logo.width))
            self.logo_image = ImageTk.PhotoImage(original_logo.resize((logo_width, logo_height)))

        except Exception as e:
            print(f"Error loading images: {e}")
            # Fallback to solid color if images don't exist
            self.bg_image = ImageTk.PhotoImage(Image.new('RGB', (800, 600), '#0b411c'))
            self.logo_image = None

    def setup_ui(self):
        """Create all UI elements for the result window"""
        # Create canvas for background
        self.canvas = tk.Canvas(self.window, width=800, height=600, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Add background image
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Create a semi-transparent overlay using a rectangle with stipple pattern
        self.canvas.create_rectangle(0, 0, 800, 600, fill="black", stipple="gray25")

        # Add project logo in center
        if self.logo_image:
            self.canvas.create_image(400, 200, image=self.logo_image, anchor="center")

        # Create a white frame for the text
        text_frame = tk.Frame(self.window, bg="white", bd=2, relief="ridge")
        text_frame.place(relx=0.5, rely=0.6, anchor="center", width=600, height=200)

        # Add result text
        title = trait_titles[self.chosen_trait]
        result_text = f"{title}!\n\nProject: {self.project['name']}\nCountry: {self.project['country']}"

        result_label = tk.Label(
            text_frame,
            text=result_text,
            font=("Raleway", 16, "bold"),
            fg="black",
            bg="white",
            wraplength=550,
            justify="center",
            padx=20,
            pady=20
        )
        result_label.pack(expand=True)

        # Add buttons
        button_frame = tk.Frame(self.window, bg="")
        button_frame.place(relx=0.5, rely=0.85, anchor="center")

        restart_btn = tk.Button(
            button_frame,
            text="Start Over",
            command=self.restart_quiz,
            font=("Raleway", 12),
            width=15,
            bg="#0b411c",
            fg="white"
        )
        restart_btn.pack(side="left", padx=10)
        restart_btn.bind("<Button-1>", lambda e, b=restart_btn: animate_button(b))

        menu_btn = tk.Button(
            button_frame,
            text="Main Menu",
            command=self.return_to_menu,
            font=("Raleway", 12),
            width=15,
            bg="#0b411c",
            fg="white"
        )
        menu_btn.pack(side="left", padx=10)
        menu_btn.bind("<Button-1>", lambda e, b=menu_btn: animate_button(b))

    def restart_quiz(self):
        """Restart the quiz"""
        self.window.destroy()
        if hasattr(self.parent, 'quiz_app'):
            self.parent.quiz_app.reset_quiz()

    def return_to_menu(self):
        """Return to main menu"""
        self.window.destroy()
        if hasattr(self.parent, 'quiz_app'):
            self.parent.quiz_app.return_to_menu()


class MusicPlayer:
    def __init__(self):
        self.current_playlist = []
        self.current_track_index = 0
        self.current_section = None
        self.volume = 0.5  # Default volume (50%)
        mixer.music.set_endevent(pygame.USEREVENT)
        mixer.music.set_volume(self.volume)

    def load_playlist(self, playlist_name, force_restart=False):
        """Load a new playlist only if different from current"""
        if force_restart or playlist_name != self.current_section:
            self.current_playlist = SOUNDTRACK.get(playlist_name, [])
            self.current_track_index = 0
            self.current_section = playlist_name
            if self.current_playlist:
                self.play_current_track()

    def set_volume(self, volume):
        """Set volume (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))  # Clamp between 0-1
        mixer.music.set_volume(self.volume)

    def play_current_track(self):
        """Play the current track in the playlist"""
        if self.current_playlist:
            try:
                mixer.music.load(self.current_playlist[self.current_track_index])
                mixer.music.set_volume(0.5)
                mixer.music.play()
            except Exception as e:
                print(f"Error playing track: {e}")
                self.next_track()

    def next_track(self):
        """Move to next track in playlist"""
        if self.current_playlist:
            self.current_track_index = (self.current_track_index + 1) % len(self.current_playlist)
            self.play_current_track()

    def check_event(self, event):
        """Handle music end events"""
        if event.type == pygame.USEREVENT:
            self.next_track()


if __name__ == "__main__":
    pygame.init()
    mixer.init()
    music_player = MusicPlayer()

    root = tk.Tk()
    root.music_player = music_player  # Make accessible everywhere

    def check_pygame_events():
        for event in pygame.event.get():
            music_player.check_event(event)
        root.after(100, check_pygame_events)  # Check every 100ms

    root.after(100, check_pygame_events)
    menu = MainMenu(root)
    root.mainloop()
