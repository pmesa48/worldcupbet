import pandas as pd
import numpy as np

class KnockoutBetProcess():
    def __init__(self, points, columns) -> None:
        self.points = points
        self.columns = columns

    def load_data(self, round_data) -> pd.DataFrame:
        round_results = np.zeros(shape=(len(round_data), len(round_data.iloc[0])))
        real_results = round_data.iloc[0].to_numpy()
        for participant_index in range(1, len(round_data)):
            for team_index in range(len(round_data.iloc[participant_index])):
                team_guess = round_data.iloc[participant_index][team_index]
                if(team_guess in real_results):
                    round_results[participant_index - 1][team_index] = self.points
        round_results_frame = pd.DataFrame(data=round_results, columns=self.columns)
        return round_results_frame