import tkinter as tk
from tkinter import PhotoImage
import random
import pygame

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
            ('Lead workshops on topics I`m passionate about', 'growth'),
        ]
    },
]

trait_scores = {
    'growth': 0,
    'explorer': 0,
    'impact': 0
}

# Initialize pygame mixer for sound playback
pygame.mixer.init()


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

    return original_color


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Be A Global Volunteer Quiz")
        self.question_index = 0
        self.result_window = None

        self.root.geometry("1200x1600")
        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack()

        # Try to load the image (with error handling)
        try:
            self.image = PhotoImage(file="green.png")
            self.image_label = tk.Label(self.frame, image=self.image)
            self.image_label.pack(pady=10)
        except:
            pass  # Continue without image if it fails to load

        self.question_label = tk.Label(self.frame, text="", font=("Arial", 16, "bold"), wraplength=600)
        self.question_label.pack(pady=30)

        self.buttons = []
        for i in range(3):
            btn = tk.Button(
                self.frame,
                text="",
                font=("Arial", 12),
                wraplength=500,
                justify="center",
                height=3,
                width=40,
                command=lambda i=i: self.select_option(i)
            )
            btn.pack(pady=5)
            self.buttons.append(btn)

        self.show_question()

    def show_question(self):
        q = questions[self.question_index]
        self.question_label.config(text=q['question'])

        default_bg = "#f0f0f0"

        for i, (text, _) in enumerate(q['options']):
            self.buttons[i].config(
                text=text,
                background=default_bg,
                activebackground="white",
                foreground="black",
                activeforeground='black'
            )

    def select_option(self, index):
        if self.result_window:
            return

        btn = self.buttons[index]
        original_color = animate_button(btn)

        self.root.after(400, lambda: self.process_selection(index, btn, original_color))

    def process_selection(self, index, btn, original_color):
        trait = questions[self.question_index]['options'][index][1]
        trait_scores[trait] += 1
        self.question_index += 1

        if self.question_index < len(questions):
            self.show_question()
        else:
            self.show_result()

    def show_result(self):
        max_score = max(trait_scores.values())
        top_traits = [trait for trait, score in trait_scores.items() if score == max_score]

        recommendations = {
            'growth': [('Fingerprint', 'Brazil'), ('Heartbeat', 'Morocco')],
            'explorer': [('Aquatica', 'Tunisia'), ('Skill Up!', 'Egypt')],
            'impact': [('Global Classroom', 'Turkiye'), ('Happy Bus', 'India')],
        }

        chosen_trait = random.choice(top_traits)
        project, country = random.choice(recommendations[chosen_trait])

        trait_titles = {
            'growth': "🌱 Growth Seeker",
            'explorer': "🌍 Culture Explorer",
            'impact': "🤝 Impact Maker"
        }

        title = trait_titles[chosen_trait]

        self.result_window = tk.Toplevel(self.root)
        self.result_window.title("Your Matched Profile")
        self.result_window.geometry("600x400")

        result_label = tk.Label(
            self.result_window,
            text=f"{title}!\n\nProject: {project}\nCountry: {country}",
            font=("Arial", 14, "bold"),
            wraplength=500,
            justify="center",
            padx=20,
            pady=20
        )
        result_label.pack(expand=True)

        close_button = tk.Button(
            self.result_window,
            text="Start Over",
            command=self.reset_quiz,
            font=("Arial", 12),
            height=2,
            width=15,
            background="#f0f0f0",
            activebackground="white",
            foreground="black"
        )
        close_button.pack(pady=20)

        self.disable_frame()

    def reset_quiz(self):
        if self.result_window:
            for child in self.result_window.winfo_children():
                if isinstance(child, tk.Button) and child.cget("text") == "Start Over":
                    animate_button(child)
                    break

        self.root.after(400, self._perform_reset)

    def _perform_reset(self):
        if self.result_window:
            self.result_window.destroy()
            self.result_window = None

        global trait_scores
        trait_scores = {'growth': 0, 'explorer': 0, 'impact': 0}
        self.question_index = 0

        for i, button in enumerate(self.buttons):
            button.config(
                text="",
                background="#f0f0f0",
                foreground="black",
                command=lambda i=i: self.select_option(i)
            )

        self.enable_frame()
        self.show_question()

    def disable_frame(self):
        for button in self.buttons:
            button.config(state=tk.DISABLED)

    def enable_frame(self):
        for button in self.buttons:
            button.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()