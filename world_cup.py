import pandas as pd
import numpy as np

from bet_parser import ExcelParser
from group_bet_process import GroupBetProcess
from knockout_bet_process import KnockoutBetProcess
from finals_bet_process import FinalsBetProcess

class WorldCup():
    def __init__(self, bet_path, save_path) -> None:
        self.save_path = save_path
        self.excel_parser = ExcelParser(bet_path)
        self.group_bet_process = GroupBetProcess(multiplier=2, multiplier_range=[46, 59])
        self.last_sixteen_process = KnockoutBetProcess(points=2, columns=[f"16avos Equipo {i+1}" for i in range(0, 16)])
        self.quarter_finals_process = KnockoutBetProcess(points=3, columns=[f"8avos Equipo {i+1}" for i in range(0, 8)])
        self.semi_finals_process = KnockoutBetProcess(points=4, columns=[f"Semifinales Equipo {i+1}" for i in range(0, 4)])
        self.finals_bet_process = KnockoutBetProcess(points=5, columns=[f"Finalista Equipo {i+1}" for i in range(0, 2)])
        self.finals_results_bet_process = FinalsBetProcess(points=[3, 5, 10])

    def process(self) -> pd.DataFrame:
        group_results = self.group_bet_process.load_data(self.excel_parser.groups)
        last_sixteen_results = self.last_sixteen_process.load_data(self.excel_parser.last_sixteen)
        quarter_finals_results = self.quarter_finals_process.load_data(self.excel_parser.quarter_finals)
        semi_finals_results = self.semi_finals_process.load_data(self.excel_parser.semi_finals)
        finals_results = self.finals_bet_process.load_data(self.excel_parser.finals)
        finals_matches_results = self.finals_results_bet_process.load_data(self.excel_parser.finals_results)

        world_cup_results = group_results.join(last_sixteen_results)
        world_cup_results = world_cup_results.join(quarter_finals_results)
        world_cup_results = world_cup_results.join(semi_finals_results)
        world_cup_results = world_cup_results.join(finals_results)
        world_cup_results = world_cup_results.join(finals_matches_results)

        return self.order_by_points(world_cup_results)

    def save(self, results) -> None:
        results.to_excel(self.save_path, index=False)
        
    def order_by_points(self, results) -> pd.DataFrame:
        results['Puntos'] = results.sum(axis=1)
        results = results.sort_values('Puntos', ascending=False)
        return results

    def calculate_results(self) -> None:
        results = self.process()
        self.save(results)