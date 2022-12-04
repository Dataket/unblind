#!/usr/bin/env python3

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import pandas as pd
import numpy as np
import seaborn as sns

sns.set_theme(context='talk', style='darkgrid', palette='colorblind')

class DataViz:
    def __init__(self, pdn_system: str, root_path: str = './') -> None:
        self.pdn_system = pdn_system
        self.root_path = root_path
        return None

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------
    # PRIVATE METHODS
    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------
    def __featureSanityCheck(self, input_table: pd.DataFrame,
                             thresh: int = 10) -> list:

        non_constant_columns = []
        for column in input_table:
            if len(input_table[column].value_counts()) >= thresh:
                non_constant_columns.append(column)

        return non_constant_columns

    def __bivariatePlot(self, group_data: list,
                        file_path: str, variables: list) -> object:
        input_table = pd.read_csv(
            self.root_path+self.pdn_system+'/'+file_path+'_data.csv', usecols=variables)

        if group_data[0] and group_data[1]:
            # Stacked countplot
            df_plot = input_table.groupby(variables).size().reset_index().pivot(
                columns=variables[0], index=variables[1], values=0)
            output_graph = df_plot.plot(kind='bar', stacked=True)

        elif not (group_data[0] or group_data[1]):
            # Scatter plot
            temp_input_table = input_table.copy()

            # Add noise to avoid overlapping points

            # Check if the variable is categorical
            if len(temp_input_table[variables[0]].value_counts()) < 10:
                temp_input_table[variables[0]] = temp_input_table[variables[0]] + \
                    np.random.normal(0, 0.1, len(temp_input_table))
            if len(temp_input_table[variables[1]].value_counts()) < 10:
                temp_input_table[variables[1]] = temp_input_table[variables[1]] + \
                    np.random.normal(0, 0.1, len(temp_input_table))

            # Check if any of the variables is categorical
            if len(input_table[variables[0]].value_counts()) < 10 or len(input_table[variables[1]].value_counts()) < 10:
                output_graph = sns.scatterplot(
                    data=temp_input_table, x=variables[0], y=variables[1], alpha=0.2, size = 0.2)
            else:
                output_graph = sns.scatterplot(
                    data=temp_input_table, x=variables[0], y=variables[1], alpha =0.7)
        else:
            # Boxplot
            if group_data[0]:
                df_plot = input_table.groupby(variables[0])
            else:
                df_plot = input_table.groupby(variables[1])
            output_graph = df_plot.boxplot(subplots=False)

        return output_graph

    def __univariatePlot(self, group_data: bool,
                         file_path: str, variable: str) -> object:
        input_series = pd.read_csv(
            self.root_path+self.pdn_system+'/'+file_path+'_data.csv', usecols=[variable])
        if group_data:
            # Pie chart with counts
            output_graph = input_series.value_counts().plot(kind='pie')
        else:
            # Histogram
            output_graph = sns.histplot(input_series)
        return output_graph

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------
    # PUBLIC METHODS
    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------
    def availableFeatures(self, path_list:list, thresh:int=10) -> None:

        path_available_features = dict()
        for path in path_list:
            path_table = pd.read_csv(
                self.root_path+self.pdn_system+'/'+path+'_data.csv')
            path_available_features[path] = self.__featureSanityCheck(
                path_table, thresh)

        self.path_available_features = path_available_features

        return None

    def createGraph(self, group_data: list, file_path: str, variables: list) -> object:

        if len(variables) == 2:
            output_graph = self.__bivariatePlot(
                group_data, file_path, variables)
        elif len(variables) == 1:
            output_graph = self.__univariatePlot(
                group_data[0], file_path, variables[0])
        else:
            raise Exception(
                'Error on createGraph method:   Input variables must be a list of strings with length 1 or 2')
        output_graph.set_xticklabels(output_graph.get_xticklabels(), rotation=90)
        return output_graph


# This function is for recommending a list of features
# (On stramlit app, it can show the displayed features to select)
def give_viable_features(root_path: str, system: str, aggregated_data: bool, thresh: int) -> tuple:
    system_paths = {'s1': ['ut_ug_m', 'ut_g_m'],
                    's2': ['ut_ug_m'],
                    's3s': ['ut_ug_m'],
                    's3p': ['ut_ug_m']}

    if system != 's1':
        aggregated_data = False

    path = 'ut_ug_m'
    if aggregated_data:
        path = 'ut_g_m'

    data_visualizer = DataViz(pdn_system=system, root_path=root_path)
    data_visualizer.availableFeatures(system_paths[system], thresh)

    # NOTE: THE FEATURES MIGHT NEED SOME TREATMENT IN ORDER TO PROPERLY SHOW THEM
    return path, data_visualizer.path_available_features[path]


# Based on the selected features and path, it makes the optimal graph
def graph_features(root_path: str, system: str, group_data: list, file_path: str, variables: list) -> object:
    # NOTE: group_data IS A LIST OF BOOLEANS
    data_visualizer = DataViz(pdn_system=system, root_path=root_path)

    return data_visualizer.createGraph(group_data, file_path, variables)

if __name__=='__main__':
    print('This is a module for data visualization of the PDN system data 🙌🏽')
