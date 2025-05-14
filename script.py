import tkinter as tk
import random
import pygame
from PIL import Image, ImageTk
from pathlib import Path

# Initialize pygame mixer
pygame.mixer.init()

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
        click_sound = pygame.mixer.Sound("click_sound.wav")
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
        self.root.result_window = ResultWindow(self.root, chosen_trait)

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
        # Reset scores and question index
        self.trait_scores = {'growth': 0, 'explorer': 0, 'impact': 0}
        self.question_index = 0

        # Close result window if it exists
        if hasattr(self, 'result_window') and self.result_window:
            self.result_window.window.destroy()

        # Show first question immediately

        self.start_quiz()

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

    def load_images(self):
        """Load and resize images"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Background image
        original_bg = Image.open("main_menu_background")
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
            btn.bind("<Button-1>", lambda e, b=btn: animate_button(b))

    def start_quiz(self):
        """Start the quiz"""
        QuizApp(self.root)

    def show_settings(self):
        """Show settings window"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.resizable(False, False)

        # Center the settings window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 300) // 2
        settings_window.geometry(f"400x300+{x}+{y}")

        tk.Label(
            settings_window,
            text="Settings",
            font=("Raleway", 18, "bold")
        ).pack(pady=20)

        # Volume control
        volume_frame = tk.Frame(settings_window)
        volume_frame.pack(pady=10)

        tk.Label(
            volume_frame,
            text="Volume:",
            font=("Raleway", 12)
        ).pack(side="left")

        volume_slider = tk.Scale(
            volume_frame,
            from_=0,
            to=100,
            orient="horizontal"
        )
        volume_slider.pack(side="left", padx=10)

        # Close button
        close_btn = tk.Button(
            settings_window,
            text="Close",
            command=settings_window.destroy,
            font=("Raleway", 12),
            width=15,
            bg="#0b411c",
            fg="white"
        )
        close_btn.pack(pady=20)
        close_btn.bind("<Button-1>", lambda e, b=close_btn: animate_button(b))


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
        #self.quiz_app.reset_quiz()
        print("Restarting the quiz")
        self.parent.reset_quiz()

    def return_to_menu(self):
        """Return to main menu"""
        self.window.destroy()
        self.parent.return_to_menu()


if __name__ == "__main__":
    root = tk.Tk()
    menu = MainMenu(root)
    root.mainloop()
