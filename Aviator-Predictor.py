import os
import pickle
import numpy as np
from termcolor import colored

class MultiplierPredictor:
    def __init__(self, data_file="multiplier_data.pkl"):
        self.data_file = data_file
        self.history = [] 
        self.max_multiplier = 100 
        self.min_multiplier = 1.1 

    def add_multiplier(self, multiplier):
        if multiplier > self.max_multiplier:
            multiplier = self.max_multiplier
        elif multiplier < self.min_multiplier:
            multiplier = self.min_multiplier
        self.history.append(multiplier)
        if len(self.history) > 10:
            self.history.pop(0)

    def save_data(self):
        with open(self.data_file, "wb") as file:
            pickle.dump(self.history, file)

    def calculate_statistics(self):
        if len(self.history) < 2:
            return 0, 0, 0
        mean = np.mean(self.history)
        std_dev = np.std(self.history)
        range_val = np.ptp(self.history)
        return mean, std_dev, range_val

    def predict_next_multiplier(self):
        if len(self.history) < 2:
            return None 

        mean, std_dev, _ = self.calculate_statistics()
        last_multiplier = self.history[-1]
        recent_impact = 0.1 * (last_multiplier - mean)
        prediction = mean + (std_dev * 0.5) + recent_impact
        prediction = max(self.min_multiplier, min(prediction, self.max_multiplier))
        return prediction

    def display_history(self):
        print(colored("\n       --- HISTORY OF LAST 10 MULTIPLIERS ---       ", "cyan", attrs=["bold", "underline"]))
        for i, multiplier in enumerate(self.history, start=1):
            print(f"{colored(f' {i}.', 'green')} {colored(f'{multiplier:.2f}', 'yellow')}")
        print(colored("-" * 40, "cyan", attrs=["bold"]))

def main():
    predictor = MultiplierPredictor()

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(colored("************** AVIATOR PREDICTOR **************", "red", attrs=["bold", "underline", "reverse"]))
        print(colored("                 By: SULTAN                 ", "yellow", attrs=["bold"]))
        print(colored(" PLZ READ DISCLIMER IN FOLDER BEFORE USING IT <3 ", "red", attrs=["bold"]))        
        print(colored("=" * 50, "blue", attrs=["bold"]))

        if len(predictor.history) >= 2:
            predicted_value = predictor.predict_next_multiplier()
            print(f"\n{colored('Predicted Next Multiplier:', 'blue', attrs=['bold'])} {colored(f'{predicted_value:.2f}', 'green', attrs=['bold'])}")
            try:
                actual_next_value = float(input(colored("\nEnter the actual next multiplier: ", "yellow", attrs=["bold"])))
                predictor.add_multiplier(actual_next_value)
                predictor.display_history()
            except ValueError:
                print(colored("\nInvalid input. Please enter a numeric value.", "red", attrs=["bold"]))
        else:
            print(colored("\nNot enough data for prediction. Add more multipliers.", "red", attrs=["bold"]))
            try:
                new_multiplier = float(input(colored("\nEnter a new multiplier to start: ", "yellow", attrs=["bold"])))
                predictor.add_multiplier(new_multiplier)
            except ValueError:
                print(colored("\nInvalid input. Please enter a numeric value.", "red", attrs=["bold"]))

        input(colored("\nPress Enter to continue or Ctrl+C to exit...", "green", attrs=["bold"]))

if __name__ == "__main__":
    main()
