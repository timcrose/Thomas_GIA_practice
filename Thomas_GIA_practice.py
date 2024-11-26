# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 15:36:15 2024

@author: timcr
"""
import random
import time
import tkinter as tk
import string
from python_utils import list_utils, config_utils
config_fpath = 'Thomas_GIA.conf'
config = config_utils.Instruct(config_fpath)
config.get_config_dct()


class Thomas_GIA:
    def __init__(self):
        # User Input
        self.time_limit = self.seconds_per_question * self.total_number_of_questions
        # Initial Values
        self.buttons = []
        self.correct_answers = []
        self.selections = []
        self.started = False
        # Setup
        self.root = tk.Tk()
        # Set the fixed window size width x height
        self.root.geometry("800x150")
        self.start_time = time.time()
        self.label = tk.Label(self.root, text=str(self.time_limit) + " secs, " + str(self.total_number_of_questions) + " questions.\nReady?")
        self.label.pack(pady=10)

    
    def results_textbox(self):
        time_taken = time.time() - self.start_time
        if len(self.selections) != len(self.correct_answers) and len(self.correct_answers) > len(self.selections):
            del self.correct_answers[len(self.correct_answers) - 1]
        assert(len(self.selections) == len(self.correct_answers))
        num_correct = sum([int(self.selections[i] == self.correct_answers[i]) for i in range(len(self.selections))])
        if len(self.selections) == 0:
            accuracy_pct = 0
        else:
            accuracy_pct = num_correct / len(self.selections)
        results_str = 'time taken: ' + str(round(time_taken, 1)) + ' secs. Time remaining: ' + str(round(self.time_limit - time_taken, 1)) + ' secs'
        results_str += '\n'
        results_str += 'time taken per question: ' + str(round(time_taken / self.total_number_of_questions, 1)) + ' secs'
        results_str += '\n'
        results_str += 'Accuracy: ' + str(num_correct) + '/' + str(len(self.selections)) + ' (' + str(round(accuracy_pct * 100, 1)) + '%)'
        results_str += '\n'
        results_str += 'Score: ' + str(num_correct) + '/' + str(self.total_number_of_questions) + ' (' + str(100 * num_correct / self.total_number_of_questions) + '%)'
        self.label.config(text=results_str)
        for i in range(len(self.buttons)):
            self.buttons[i].destroy()
    
    
    def on_button_press(self, b_id):
        if self.started:
            self.selections.append(b_id)
        else:
            self.started = True
            self.start_time = time.time()
        self.update_textbox()


    def update_textbox(self):
        self.new_question()
        self.label.config(text=self.question_str)
        for i in range(len(self.buttons)):
            self.buttons[i].config(text=self.button_texts[i])
        self.question_number = 1 + len(self.selections)
        if self.question_number <= self.total_number_of_questions or time.time() - self.start_time > self.time_limit:
            self.root.title(str(self.question_number))
        else:
            self.results_textbox()


class Perceptual_Speed(Thomas_GIA):
    def __init__(self):
        # User Input
        self.seconds_per_question = config.get_value('Perceptual_Speed', 'seconds_per_question', desired_type=float, default_value=8.0)
        self.total_number_of_questions = config.get_value('Perceptual_Speed', 'total_number_of_questions', desired_type=int, default_value=20)
        super().__init__()
        # Constants
        self.num_buttons = 5
        self.relx = [0.4375 + b * 0.03125 for b in range(self.num_buttons)]
        # Setup
        self.root.title("Perceptual Speed Section")
        for b_id in range(self.num_buttons):
            self.buttons.append(tk.Button(self.root, text='Go', command=lambda b_id=b_id: self.on_button_press(b_id), width=2, height=2))
            self.buttons[b_id].place(relx=self.relx[b_id], rely=0.5, anchor=tk.CENTER)
        self.button_texts = [str(i) for i in range(self.num_buttons)]
        # Run
        self.root.mainloop()


    def new_question(self):
        self.question_number = len(self.selections) + 1
        if self.question_number > self.total_number_of_questions:
            return
        lowercase_letters = list(string.ascii_lowercase)
        random_number = random.random()
        # Use a uniform distribution since I don't know the true distribution.
        if random_number < 0.2:
            r = 0
        elif random_number < 0.4:
            r = 1
        elif random_number < 0.6:
            r = 2
        elif random_number < 0.8:
            r = 3
        else:
            r = 4
        self.correct_answers.append(r)
        lowercase_letters_sample = random.sample(lowercase_letters, 4)
        same_letter_sample = random.sample(lowercase_letters_sample, r)
        uppercase_letters_sample = list(list_utils.randomsubset_not_in_other_set(4 - r, set(lowercase_letters_sample) - set(same_letter_sample), set(lowercase_letters) - set(same_letter_sample)))
        uppercase_letters_sample = [c.upper() for c in uppercase_letters_sample + same_letter_sample]
        num_matching = sum([lowercase_letters_sample[i].upper() == uppercase_letters_sample[i] for i in range(len(lowercase_letters_sample))])
        while num_matching != r:
            random.shuffle(uppercase_letters_sample)
            num_matching = sum([lowercase_letters_sample[i].upper() == uppercase_letters_sample[i] for i in range(len(lowercase_letters_sample))])
        # Flip a coin to see whether lower or uppercase will be on the top row.
        if random.random() < 0.5:
            self.question_str = ' '.join(lowercase_letters_sample) + '\n' + ' '.join(uppercase_letters_sample)
        else:
            self.question_str = ' '.join(uppercase_letters_sample) + '\n' + ' '.join(lowercase_letters_sample)
            
    
class Number_Speed(Thomas_GIA):
    def __init__(self):
        # User Input
        self.seconds_per_question = config.get_value('Number_Speed', 'seconds_per_question', desired_type=float, default_value=8.0)
        self.total_number_of_questions = config.get_value('Number_Speed', 'total_number_of_questions', desired_type=int, default_value=20)
        self.number_range = config.get_value('Number_Speed', 'number_range', desired_type=list, default_value=[2, 28])
        self.diff_range = config.get_value('Number_Speed', 'diff_range', desired_type=list, default_value=[1, 7])
        self.delta_range = config.get_value('Number_Speed', 'delta_range', desired_type=list, default_value=[1, 5])
        super().__init__()
        # Constants
        self.num_buttons = 3
        self.relx = [0.4 + b * 0.1 for b in range(self.num_buttons)]
        # Setup
        self.root.title("Number Speed Section")
        for b_id in range(self.num_buttons):
            self.buttons.append(tk.Button(self.root, text='Go', command=lambda b_id=b_id: self.on_button_press(b_id), width=15, height=2))
            self.buttons[b_id].place(relx=self.relx[b_id], rely=0.5, anchor=tk.CENTER)
        # Run
        self.root.mainloop()
        
        
    def choose_numbers(self):
        self.median_choice = random.choice(self.number_choices)
        self.diff_choice = random.choice(self.diff_choices)
        self.delta_choice = random.choice(self.delta_choices)
        self.sign_choice = random.choice(self.sign_choices)
        self.min_number = self.median_choice - self.diff_choice + self.sign_choice * self.delta_choice


    def new_question(self):
        '''
        number_range: list of int
            Range of possible integers to be the median.
            
        diff_range: list of int
            Range of possible integers that the max value will be away from the median
            
        delta_range: list of int
            Range of possible integers that the min value will differ in the amount the
            max value is away from the median
            
        Method
        ------
        1. Choose a number in number_range to be the median.
        2. The max value will be median + diff_choice
        3. The min value will be median - diff_choice +- delta_choice
        4. If min value >= median, repeat steps 1-3.
        '''
        self.question_number = len(self.selections) + 1
        if self.question_number > self.total_number_of_questions:
            return
        self.number_choices = list(range(self.number_range[0], self.number_range[1]))
        self.diff_choices = list(range(self.diff_range[0], self.diff_range[1]))
        self.delta_choices = list(range(self.delta_range[0], self.delta_range[1]))
        self.sign_choices = [-1, 1]
        self.choose_numbers()
        if self.median_choice - self.min_number == 1 or self.diff_choice == 1:
            # If the difference between the median and min or max is only 1, then
            # this type of problem is too easy and so let us choose again if
            # flipping a coin yields tails.
            if random.random() < 0.5:
                self.choose_numbers()
        while self.min_number < 1 or self.min_number >= self.median_choice:
            self.choose_numbers()
            #if self.median_choice - self.min_number == 1 or self.diff_choice == 1:
            #    if random.random() < 0.5:
            #        self.choose_numbers()
        number_options = [self.min_number,
                          self.median_choice,
                          self.median_choice + self.diff_choice]
        
        # The answer choices must appear in random order.
        random.shuffle(number_options)
        self.question_str = 'Choose the number farthest from the median.'
        self.button_texts = [str(number_option) for number_option in number_options]
        num_with_largest_diff_from_median = number_options[0]
        for i in range(len(number_options)):
            if abs(number_options[i] - self.median_choice) > abs(num_with_largest_diff_from_median - self.median_choice):
                num_with_largest_diff_from_median = number_options[i]
        correct_idx = number_options.index(num_with_largest_diff_from_median)
        self.correct_answers.append(correct_idx)
    
    
class Reasoning(Thomas_GIA):
    def __init__(self):
        # User Input
        self.seconds_per_question = config.get_value('Reasoning', 'seconds_per_question', desired_type=float, default_value=8.0)
        self.total_number_of_questions = config.get_value('Reasoning', 'total_number_of_questions', desired_type=int, default_value=20)
        super().__init__()
        # Constants
        self.num_buttons = 2
        # Setup
        self.root.title("Perceptual Speed Section")
        for b_id in range(self.num_buttons):
            self.buttons.append(tk.Button(self.root, text='Go', command=lambda b_id=b_id: self.on_button_press(b_id), width=15, height=2))
            if b_id == 0:
                self.buttons[b_id].place(relx=0.5 - 0.025, rely=0.5, anchor=tk.E)
            else:
                self.buttons[b_id].place(relx=0.5 + 0.025, rely=0.5, anchor=tk.W)
        self.button_texts = [str(i) for i in range(self.num_buttons)]
        self.names = ['Brooks', 'Chloe', 'Cooper', 'Walker', 'Henry', 'Penelope',
'Isabella', 'Iris', 'Caleb', 'Aiden', 'James', 'Lucas', 'Mia', 'Claire', 'Ruby', 
'Cameron', 'Asher', 'Ariana', 'Levi', 'Gabriel', 'Mateo', 'Stella', 'Grayson', 
'Adam', 'Quinn', 'Nicholas', 'Easton', 'Daniel', 'Eliana', 'Matthew', 'Ella', 
'Jose', 'Elias', 'Aaliyah', 'Beau', 'Leilani', 'Leah', 'Maria', 'Cora', 'Sofia', 
'Silas', 'Jacob', 'Ethan', 'Noah', 'Everett', 'Paisley', 'Xavier', 'Hailey', 
'Logan', 'Landon', 'Michael', 'Nova', 'Madelyn', 'Theo', 'Jaxon', 'Leonardo', 
'Emery', 'Olivia', 'Bennett', 'Mila', 'Eloise', 'Joseph', 'Liam', 'Harper', 
'Layla', 'Raelynn', 'Abigail', 'Parker', 'Luca', 'Luna', 'Samuel', 'Jayden', 
'Willow', 'Kennedy', 'Sebastian', 'Serenity', 'Ryan', 'Emilia', 'Christian', 
'Aaron', 'Isaiah', 'Micah', 'Aurora', 'Skylar', 'Jonathan', 'Gianna', 'Luke', 
'Aubrey', 'Colton', 'Jackson', 'Anthony', 'Eleanor', 'Lucy', 'Adrian', 
'Christopher', 'Eli', 'Audrey', 'Weston', 'Gabriella', 'Roman', 'Mason', 
'Carter', 'Natalia', 'Amelia', 'Camila', 'Genesis', 'Hannah', 'Grace', 'Avery', 
'Theodore', 'Nolan', 'Emily', 'Ellie', 'Waylon', 'William', 'Kinsley', 'Kai', 
'Delilah', 'Robert', 'Leo', 'Dylan', 'Sadie', 'Elena', 'Victoria', 'Alexander', 
'Riley', 'Ezra', 'Liliana', 'Wyatt', 'Lillian', 'David', 'Miles', 'Santiago', 
'Jordan', 'Adeline', 'Sarah', 'Scarlett', 'Elizabeth', 'Naomi', 'Natalie', 
'Jade', 'Everleigh', 'Thomas', 'Anna', 'Valentina', 'Elijah', 'Ayla', 'Josiah', 
'Emma', 'Lincoln', 'Oliver', 'Rowan', 'Greyson', 'Josephine', 'Ezekiel', 
'Everly', 'Andrew', 'Caroline', 'Bella', 'Madison', 'Joshua', 'Wesley', 
'Charlotte', 'Sophia', 'Axel', 'Addison', 'Autumn', 'Maverick', 'Nevaeh', 
'Violet', 'Jameson', 'Charles', 'Zoe', 'Isaac', 'Benjamin', 'Alice', 'Aria', 
'Julian', 'Isla', 'Hudson', 'Lily', 'Nora', 'Evelyn', 'Owen', 'John', 'Athena', 
'Brooklyn', 'Angel', 'Ian', 'Jack', 'Jeremiah', 'Sophie', 'Lydia', 'Nathan', 
'Maya', 'Savannah', 'Hazel', 'Ava', 'Zoey', 'Ivy']

        heavier_options = ['heavier', 'weighs more', 'more heavy', 'less light', 
'fatter','lighter', 'weighs less', 'more light', 'less heavy', 'thinner']
        
        brighter_options = ['brighter', 'smarter', 'more competent', 
'less stupid', 'better educated','duller', 'stupider', 'more incompetent', 
'less smart', 'less intelligent']
        
        stronger_options = ['stronger', 'fitter', 'more fit', 'less weak', 
'better toned', 'weaker', 'not fitter', 'more weak', 'less strong', 'less able']
        
        happier_options = ['happier', 'more joyful', 'more happy', 'less sad', 
'less unhappy', 'sadder', 'more sad', 'in greater lamentation', 'less happy', 
'less joyful']
        
        self.options = {
 'heavier': heavier_options,
'lighter': heavier_options[::-1], 
'not heavier': heavier_options[::-1], 
'not lighter': heavier_options,
'more massive': heavier_options,
'less massive': heavier_options[::-1],
'brighter': brighter_options,
'duller': brighter_options[::-1],
'not brighter': brighter_options[::-1],
'not duller': brighter_options,
'smarter': brighter_options,
'dumber': brighter_options[::-1],
'stronger': stronger_options,
'weaker': stronger_options[::-1],
'not stronger': stronger_options[::-1],
'not weaker': stronger_options,
'fitter': stronger_options,
'not fitter': stronger_options[::-1],
'happier': happier_options,
'sadder': happier_options[::-1],
'not happier': happier_options[::-1],
'not sadder': happier_options,
'more joyful': happier_options,
'less joyful': happier_options[::-1]
 }
        # Run
        self.root.mainloop()


    def new_question(self):
        self.question_number = 1 + len(self.selections) // 2
        if self.question_number > self.total_number_of_questions:
            return
        names_sampled = random.sample(self.names, self.num_buttons)
        problem_str = random.choice(list(self.options.keys()))
        answer_str = random.choice(self.options[problem_str])
        self.statement_str = names_sampled[0] + ' is ' + problem_str + ' than ' + names_sampled[1] + '.'
        self.question_str = 'Who is ' + answer_str + '?'
        left_answer_choice = random.choice(names_sampled)
        right_answer_choice = list(set(names_sampled) - set([left_answer_choice]))[0]
        self.button_texts = [left_answer_choice, right_answer_choice]
        correct_answer_index_of_names = int(self.options[problem_str].index(answer_str) >= len(self.options[problem_str]) / 2)
        correct_name = names_sampled[correct_answer_index_of_names]
        self.correct_answers.append(self.button_texts.index(correct_name))
        
    
    def update_textbox(self):
        if len(self.selections) % 2 == 0:
            self.new_question()
            if self.question_number <= self.total_number_of_questions:
                self.label.config(text=self.statement_str)
                for b in range(self.num_buttons):
                    self.buttons[b].config(text="        ")
        else:
            self.label.config(text=self.question_str)
            for b in range(self.num_buttons):
                self.buttons[b].config(text=self.button_texts[b])
        self.question_number = 1 + len(self.selections) // 2
        if self.question_number <= self.total_number_of_questions:
            self.root.title(str(self.question_number))
        else:
            for index in list(range(len(self.selections) - 2, -2, -2)):
                del self.selections[index]
            self.results_textbox()
            
            
def main():
    section_lst = config.config_dct['main']['sections_lst']
    for section in section_lst:
        if section == 'Reasoning':
            Reasoning()
        elif section == 'Number_Speed':
            Number_Speed()
        elif section == 'Perceptual_Speed':
            Perceptual_Speed()
            
    
if __name__ == '__main__':
    main()