import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage

questions = [
    {
        'question': "What motivates you to join an exchange program?",
        'options': [
            ('Personal growth and development', 'development'),
            ('Making a positive impact in local communities', 'impact'),
            ('Exploring new places and cultures', 'traveler'),
        ]
    },
    {
        'question': "Which experience excites you the most?",
        'options': [
            ('Which experience excites you the most?', 'adventurous'),
            ('Riding a tuk-tuk through bustling local streets', 'creative'),
            ('Tasting fresh mangoes straight from the market', 'analytical'),
        ]
    },
{
        'question': "I’m most looking forward to…",
        'options': [
            ('Making lots of new friends abroad', 'impact'),
            ('Understanding new cultures', 'traveler'),
            ('Having a lot of fun along the way', 'development'),
        ]
    },
{
        'question': "What concerns you the most?",
        'options': [
            ('High transportation costs', 'impact'),
            ('Struggling to adapt to a new environment', 'traveler'),
            ('Not enjoying the local food', 'development'),
        ]
    },
{
        'question': "It would be interesting to…",
        'options': [
            ('Teach and support others in learning', 'impact'),
            ('Help protect marine life on a sunny beach', 'traveler'),
            ('Lead workshops on topics I’m passionate about', 'development'),
        ]
    },
]

trait_scores = {'traveler': 0, 'impact': 0, 'development': 0}

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
        for i in range(4):
            btn = tk.Button(self.frame, text="", font=("Arial", 14), width=30, command=lambda i=i: self.select_option(i))
            btn.pack(pady=5)
            self.buttons.append(btn)

        self.show_question()

    def show_question(self):
        q = questions[self.question_index]
        self.question_label.config(text=q['question'])

        for i, (text, _) in enumerate(q['options']):
            self.buttons[i].config(text=text)

    def select_option(self, index):
        trait = questions[self.question_index]['options'][index][1]
        trait_scores[trait] += 1
        self.question_index += 1

        if self.question_index < len(questions):
            self.show_question()
        else:
            self.show_result()

    def show_result(self):
        dominant_trait = max(trait_scores, key=trait_scores.get)
        if dominant_trait == 'adventurous':
            project, country = "Volunteer Abroad Project", "New Zealand"
        elif dominant_trait == 'creative':
            project, country = "Art Residency", "France"
        elif dominant_trait == 'analytical':
            project, country = "Tech Internship", "Germany"
        elif dominant_trait == 'social':
            project, country = "NGO Project", "Brazil"
        else:
            project, country = "General Project", "USA"

        messagebox.showinfo("Your Result", f"Project: {project}\nCountry: {country}")
        self.root.quit()


# Launch app
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
