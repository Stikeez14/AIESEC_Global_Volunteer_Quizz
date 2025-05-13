import tkinter as tk
from tkinter import messagebox
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
        'question': "I’m most looking forward to…",
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
        'question': "It would be interesting to…",
        'options': [
            ('Teach and support others in learning', 'impact'),
            ('Help protect marine life on a sunny beach', 'explorer'),
            ('Lead workshops on topics I’m passionate about', 'growth'),
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

# Load a sound file (make sure the sound file exists in the directory)
click_sound = pygame.mixer.Sound("click_sound.wav")

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Be A Global Volunteer Quizz")
        self.question_index = 0
        self.result_window = None  # Store the reference to result window

        # Frame to hold quiz content
        self.root.geometry("1200x1600")
        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack()

        # Load the image
        self.image = PhotoImage(file="green.png")

        # Display the image
        self.image_label = tk.Label(self.frame, image=self.image)
        self.image_label.pack(pady=10)

        self.question_label = tk.Label(self.frame, text="", font=("Arial", 16, "bold"), wraplength=800)
        self.question_label.pack(pady=30)

        self.buttons = []
        for i in range(3):
            btn = tk.Button(
                self.frame,
                text="",
                font=("Arial", 14),
                wraplength=600,  # wraps text
                justify="center",  # aligns text
                anchor="center",  # places text
                height=3,  # ensures consistent height
                width=40,  # same visual width
                command=lambda i=i: self.select_option(i)  # bind the correct function
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
        # Check if result window is open, if so, prevent click
        if self.result_window:
            return

        btn = self.buttons[index]
        original_color = btn.cget("background")

        # Play the click sound when a button is clicked
        click_sound.play()

        btn.config(
            background="#0b411c",  # the raw moment colour
            activebackground="#0b411c",
            foreground="white",
            activeforeground="white"
        )

        self.root.after(400, lambda: self.process_selection(index, btn, original_color))

    def process_selection(self, index, btn, original_color):
        btn.config(
            background="#0b411c",  # the raw moment colour
            activebackground="#0b411c",
            foreground="white",
            activeforeground="white"
        )

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

        # Final project assignments
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

        # Create a new top-level window
        self.result_window = tk.Toplevel(self.root)
        self.result_window.title("Your Matched Profile")
        self.result_window.geometry("800x600")  # Set a fixed, larger size

        result_label = tk.Label(
            self.result_window,
            text=f"{title}!\n\nProject: {project}\nCountry: {country}",
            font=("Arial", 16, "bold"),
            wraplength=600,
            justify="center",
            padx=20,
            pady=20
        )
        result_label.pack(expand=True)

        # Modify the close button to reset the quiz
        close_button = tk.Button(
            self.result_window,
            text="Start Over",
            command=self.reset_quiz,
            font=("Arial", 12)
        )
        close_button.pack(pady=10)

        # Disable the main frame while the result window is open
        self.disable_frame()

    def reset_quiz(self):
        # Destroy the result window and clear the reference
        if self.result_window:
            self.result_window.destroy()
            self.result_window = None  # This is the critical fix

        # Reset all the necessary variables
        global trait_scores
        trait_scores = {'growth': 0, 'explorer': 0, 'impact': 0}
        self.question_index = 0

        # Clear all the buttons and the question label
        for button in self.buttons:
            button.config(text="",
                          background="#f0f0f0",
                          foreground="black",
                          command=lambda i=self.buttons.index(button): self.select_option(i))

        # Re-enable the main frame
        self.enable_frame()

        # Show the first question again
        self.show_question()

    def disable_frame(self):
        # Disable all buttons and widgets on the main frame
        for button in self.buttons:
            button.config(state=tk.DISABLED)
        self.question_label.config(state=tk.DISABLED)

    def enable_frame(self):
        # Re-enable all buttons and widgets on the main frame
        for button in self.buttons:
            button.config(state=tk.NORMAL)
        self.question_label.config(state=tk.NORMAL)


# LAUNCH QUIZZ
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
