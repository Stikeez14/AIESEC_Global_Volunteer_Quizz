import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import random

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

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Be A Global Volunteer Quizz")
        self.question_index = 0

        # Frame to hold quiz content
        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack()

        # Load the image
        self.image = PhotoImage(file="batman.png")

        # Display the image
        self.image_label = tk.Label(self.frame, image=self.image)
        self.image_label.pack(pady=10)

        self.question_label = tk.Label(self.frame, text="", font=("Arial", 16), wraplength=400)
        self.question_label.pack(pady=10)

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
                command=lambda  i=i: self.select_option(i)
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
        btn = self.buttons[index]
        original_color = btn.cget("background")

        # Change button color to green with white text
        btn.config(
            background="#0b411c",
            activebackground="#0b411c",
            foreground="white",
            activeforeground="white"  # Ensures the text remains white while the button is pressed
        )

        self.root.after(400, lambda: self.process_selection(index, btn, original_color))

    def process_selection(self, index, btn, original_color):
        # Ensure the button stays green with white text after selection
        btn.config(
            background="#0b411c",
            activebackground="#0b411c",
            foreground="white",
            activeforeground="white"  # Ensure text stays white while the button is active
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
        result_window = tk.Toplevel(self.root)
        result_window.title("Your Matched Profile")
        result_window.geometry("800x600")  # Set a fixed, larger size

        result_label = tk.Label(
            result_window,
            text=f"{title}!\n\nProject: {project}\nCountry: {country}",
            font=("Arial", 16),
            wraplength=600,
            justify="center",
            padx=20,
            pady=20
        )
        result_label.pack(expand=True)

        close_button = tk.Button(result_window, text="Close", command=self.root.quit, font=("Arial", 12))
        close_button.pack(pady=10)

# LAUNCH QUIZZ
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
