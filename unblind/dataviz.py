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
            self.root_path+self.pdn_system+'/'+path+'_data.csv', usecols=variables)

        if group_data[0] and group_data[1]:
            # Stacked countplot
            df_plot = input_table.groupby(variables).size().reset_index().pivot(
                columns=variable[0], index=variable[1], values=0)
            output_graph = df_plot.plot(kind='bar', stacked=True)

        elif not (group_data[0] or group_data[1]):
            # Scatter plot
            output_graph = sns.scatterplot(
                data=input_table, x=variable[0], y=variable[1])
        else:
            # Boxplot
            if group_data[0]:
                df_plot = input_table.groupby(variables[0])
            else:
                df_plot = input_table.groupby(variables[1])
            output_graph = df_plot.plot(kind='bar', stacked=True)

        return output_graph

    def __univariatePlot(self, group_data: bool,
                         file_path: str, variable: str) -> object:
        input_series = pd.read_csv(
            self.root_path+self.pdn_system+'/'+path+'_data.csv', usecols=[variable])
        if group_data:
            # Pie chart with counts
            output_graph = input_series.value_counts().plot(kind='pie')
        else:
            # Histogram
            ourput_graph = sns.histplot(input_series)
        return output_graph

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------
    # PUBLIC METHODS
    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------
    def availableFeatures(self, path, thresh: int = 10) -> None:

        path_available_features = dict()
        for path in system_paths[self.pdn_system]:
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
    data_visualizer.availableFeatures(system_dictionary[system], thresh)

    # NOTE: THE FEATURES MIGHT NEED SOME TREATMENT IN ORDER TO PROPERLY SHOW THEM
    return path, data_visualizer.path_available_features[path]


# Based on the selected features and path, it makes the optimal graph
def graph_features(root_path: str, system: str, group_data: list, file_path: str, variables: list) -> object:
    # NOTE: group_data IS A LIST OF BOOLEANS
    data_visualizer = DataViz(pdn_system=system, root_path=root_path)

    return data_visualizer.createGraph(group_data, file_path, variables)
