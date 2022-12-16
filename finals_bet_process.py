import numpy as np
import pandas as pd

class FinalsBetProcess():
    def __init__(self, points) -> None:
        if len(points) != 3:
            raise f"Must provide positive points for final bet stage invalid input: {points}"
        self.points = points
        self.columns = ['TERCERO', 'SUBCAMPEON', 'CAMPEON']

    def load_data(self, final_round) -> pd.DataFrame:
        final_round_results = np.zeros(shape=(len(final_round), len(final_round.iloc[0])))
        for participant_index in range(1, len(final_round)):
            for team_index in range(len(final_round.iloc[participant_index])):
                team_guess = final_round.iloc[participant_index][team_index]
                if team_index == 0 and team_guess == final_round.iloc[0][team_index]:
                    final_round_results[participant_index - 1][team_index] = self.points[0]
                elif team_index == 1 and team_guess == final_round.iloc[0][team_index]:
                    final_round_results[participant_index - 1][team_index] = self.points[1]
                elif team_index == 2 and team_guess == final_round.iloc[0][team_index]:
                    final_round_results[participant_index - 1][team_index] = self.points[2]

        return pd.DataFrame(data=final_round_results, columns=self.columns)