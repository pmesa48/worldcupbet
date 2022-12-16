import numpy as np
import pandas as pd

class GroupBetProcess():

    def __init__(self, multiplier, multiplier_range) -> None:
        self.multiplier = multiplier
        self.multiplier_range = multiplier_range
        self.columns = ['SENEGAL VS PAISESBAJOS', 'QATAR VS ECUADOR', 'SENEGAL VS QATAR', 'PAISESBAJOS VS ECUADOR', 'SENEGAL VS ECUADOR', 'PAISESBAJOS VS QATAR', \
                    'INGLATERRA VS IRAN', 'USA VS GALES', 'INGLATERRA VS USA', 'IRAN VS GALES', 'INGLATERRA VS GALES', 'IRAN VS USA', \
                    'ARGENTINA VS ARABIASAUDITA', 'MEXICO VS POLONIA', 'ARGENTINA VS MEXICO', 'ARABIASAUDITA VS POLONIA', 'ARGENTINA VS POLONIA', 'ARABIA SAUDITA VS MEXICO', \
                    'DINAMARCA VS TUNEZ', 'FRANCIA VS AUSTRALIA', 'DINAMARCA VS FRANCIA', 'TUNEZ VS AUSTRALIA', 'DINAMARCA VS AUSTRALIA', 'TUNEZ VS FRANCIA', \
                    'ALEMANIA VS JAPON', 'ESPAÑA VS COSTARICA', 'ALEMANIA VS ESPAÑA', 'JAPON VS COSTARICA', 'ALEMANIA VS COSTARICA', 'JAPON VS ESPAÑA', \
                    'MARRUECOS VS CROACIA', 'BELGICA VS CANADA', 'MARRUECOS VS BELGICA', 'CROACIA VS CANADA', 'MARRUECOS VS CANADA', 'CROACIA VS BELGICA', \
                    'SUIZA VS CAMERUN', 'BRASIL VS SERBIA', 'SUIZA VS BRASIL', 'CAMERUN VS SERBIA', 'SUIZA VS SERBIA', 'CAMERUN VS BRASIL', \
                    'URUGUAY VS COREA', 'PORTUGAL VS GHANA', 'URUGUAY VS PORTUGAL', 'COREA VS GHANA', 'URUGUAY VS GHANA', 'COREA VS PORTUGAL']
          

    def guessed_draw(self, goals_team_home, goals_team_away, real_goals_home, real_goals_team_away) -> bool:
        return goals_team_home == goals_team_away and real_goals_home == real_goals_team_away

    def guessed_home_victory(self, goals_team_home, goals_team_away, real_goals_home, real_goals_team_away) -> bool:
        return goals_team_home > goals_team_away and real_goals_home > real_goals_team_away

    def guessed_away_victory(self, goals_team_home, goals_team_away, real_goals_home, real_goals_team_away) -> bool:
        return goals_team_home < goals_team_away and real_goals_home < real_goals_team_away

    def guessed_exact_result(self, goals_team_home, goals_team_away, real_goals_home, real_goals_team_away) -> bool:
        return goals_team_home == real_goals_home and goals_team_away == real_goals_team_away

    def guessed_result(self, goals_team_home, goals_team_away, real_goals_home, real_goals_team_away) -> bool:
        return self.guessed_draw(goals_team_home, goals_team_away, real_goals_home, real_goals_team_away) \
             or self.guessed_home_victory(goals_team_home, goals_team_away, real_goals_home, real_goals_team_away) \
             or self.guessed_away_victory(goals_team_home, goals_team_away, real_goals_home, real_goals_team_away)

    def guessed_number_of_goals(self, goals_team_home, goals_team_away, real_goals_home, real_goals_team_away) -> bool:
        return goals_team_home + goals_team_away == real_goals_home + real_goals_team_away

    def get_number_of_points(self, goals_team_home, goals_team_away, real_goals_home, real_goals_team_away, multiplier=1) -> bool:
        if self.guessed_exact_result(goals_team_home, goals_team_away, real_goals_home, real_goals_team_away):
            return 3 * multiplier

        points = 0
        if self.guessed_result(goals_team_home, goals_team_away, real_goals_home, real_goals_team_away):
            points += 1
        if self.guessed_number_of_goals(goals_team_home, goals_team_away, real_goals_home, real_goals_team_away):
            points += 1
        return points * multiplier

    def get_multiplier(self, column) -> int:
        if (column > self.multiplier_range[0] and column < self.multiplier_range[1]):
            return self.multiplier
        return 1

    def isNaN(self, num) -> bool:
        if float('-inf') < float(num) < float('inf'):
            return False 
        else:
            return True

    def load_data(self, data_frame) -> pd.DataFrame:
        results = np.zeros(shape=(len(data_frame), len(self.columns)))

        for participant_index in range(1, len(data_frame)):
            for team_index, match_index in enumerate(range(0, len(data_frame.iloc[participant_index]), 2)):
                    real_home_goals = data_frame.iloc[0][match_index]
                    real_away_goals = data_frame.iloc[0][match_index + 1]

                    predicted_home_goals = data_frame.iloc[participant_index][match_index]
                    predicted_away_goals = data_frame.iloc[participant_index][match_index + 1]

                    if(self.isNaN(real_home_goals) or self.isNaN(real_away_goals)):
                        continue

                    multiplier = self.get_multiplier(match_index)
                    results[participant_index - 1][team_index] = self.get_number_of_points(predicted_home_goals, predicted_away_goals, real_home_goals, real_away_goals, multiplier)

        return self.add_columns(data_frame, results)

    def add_columns(self, data_frame, results) -> pd.DataFrame:
        results_frame = pd.DataFrame(data=results, columns=self.columns)
        participants_frame = pd.DataFrame(data=data_frame.index.values[1:], columns=['Participante'])
        participants_frame = participants_frame.join(results_frame)
        return participants_frame