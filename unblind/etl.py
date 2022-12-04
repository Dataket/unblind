class DataTreatment:
    def __init__(self, pdn_system: str, root_path: str,
                 keywords: list = [], metadata_columns: list = []) -> None:
        '''
          This object recieves the root path where all systems data is located
          as well as the PDN system, the it is able to append multiple paths into
          a single dataset.

          Parameters:
            root_path (str): The main location where every system data library is
            pdn_system (str): The PDN system you wish to work with:
                                's1', 's2', 's3p' or 's3s'
            keywords (list): The columns to keep during extraction
            metadata_columns (list): The columns to ignore when doing Machine Learning
        '''
        # TODO: ADD A FUNCTIONALITY TO ALSO WORKS WITH URLS

        # Define the system
        if type(pdn_system) == str:
            if pdn_system in ['s1', 's2', 's3p', 's3s']:
                self.pdn_system = pdn_system
            else:
                raise TypeError(
                    'Error on __init__ method:   Only values allowed for pdn_system are "s1", "s2", "s3p" or "s3s"')
        else:
            raise TypeError(
                'Error on __init__ method:   Only string type is allowed for pdn_system')

        # Define the root path
        if type(root_path) == str:
            self.root_path = root_path
        else:
            raise TypeError(
                'Error on __init__ method:   Only string type is allowed for root_path')

        self.metadata_columns = metadata_columns.copy()
        # list(set(keywords.copy() + metadata_columns.copy()))
        self.keywords = keywords.copy()

        self.last_data = pd.DataFrame({})
        self.tables = dict()
        self.table_history = []

        return None

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------
    # PRIVATE METHODS
    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------
    def __getPaths(self, main_path: str) -> list:
        return glob(main_path+'/*', recursive=False)

    def __readJson(self, path: str) -> dict:
        with open(path, 'r') as f:
            dictionary = json.load(f)
        return dictionary

    def __normalizeStateName(self, string: str) -> str:
        return string.replace('SESNA', '').replace('_', '').replace(' ', '').lower()

    def __execTableMethod(self, method: str, input: list, output: str) -> None:
        self.tables[output] = eval("""self._{0}__{1}({2})""".format(
            __class__.__name__, method, input))
        self.last_data = self.tables[output].copy()
        self.table_history.append(output)
        return None

    def __filterKeywords(self, dictionary: dict) -> dict:
        keywords = list(self.keywords.copy()) + \
            list(self.metadata_columns.copy())
        filtered_keys = []
        for keyword in keywords:
            filtered_keys += list(filter(lambda x: (keyword in x)
                                  or (keyword == x), list(dictionary.keys())))
        filtered_keys = list(set(filtered_keys))
        return {k: dictionary[k] for k in filtered_keys}

    def __flattenDictionary(self, dictionary: dict,
                            separator: str = '_', prefix: str = '') -> dict:
        # Source: https://www.geeksforgeeks.org/python-convert-nested-dictionary-into-flattened-dictionary/
        return {prefix + separator + str(k) if prefix else str(k): v
                for kk, vv in dictionary.items()
                for k, v in self.__flattenDictionary(vv, separator, str(kk)).items()
                } if isinstance(dictionary, dict) else {prefix: dictionary}

    def __flattenStatesData(self, state_paths: list) -> pd.DataFrame:
        # TODO: REFACTOR AND MODULARIZE THIS CODE
        flattened_data = pd.DataFrame({})

        for state_path in state_paths:
            # Get the state name and normalize it
            state = self.__normalizeStateName(state_path.split('/')[-1])

            # Get every data file on the state
            single_files = self.__getPaths(state_path)
            state_list = []
            for single_file in single_files:

                # Read the json as a dictionary
                dictionary_file = self.__readJson(single_file)

                # Flatten the dictionary and add it to the whole states' list
                state_list += [self.__filterKeywords(self.__flattenDictionary(item))
                               for item in dictionary_file]

            # Normalize the state data
            state_data = pd.DataFrame(state_list)
            state_data['estado_declarante'] = state
            flattened_data = flattened_data.append(
                state_data, ignore_index=True)

        return flattened_data

    def __normalizeData(self, input_name: list) -> pd.DataFrame:
        # TODO: MAKE THIS CODE TO AUTOMATICALLY ITERATE UNTIL THERE'S NO INCREASE IN
        # COLUMN COUNT
        # Source: https://stackoverflow.com/questions/35491274/split-a-pandas-column-of-lists-into-multiple-columns
        input_table = self.tables[input_name[0]]

        output_table = pd.DataFrame({})
        for column in input_table.columns:
            # Check if any element in the column is a list
            if any(isinstance(item, list) for item in input_table[column].to_list()) or any(isinstance(item, np.ndarray) for item in input_table[column].to_list()):
                # Extend the list in a single column into multiple columns with a single element
                df_dummy = pd.DataFrame([pd.Series(x)
                                        for x in input_table[column]])
                df_dummy.columns = [
                    column+'_{}'.format(i+1) for i in df_dummy.columns]

                # If there are nested dictionaries inside the elements, it flattens them
                df_dummy_list = df_dummy.to_dict('records')
                for i in range(len(df_dummy_list)):
                    df_dummy_list[i] = self.__flattenDictionary(
                        df_dummy_list[i])
                df_dummy = pd.DataFrame(df_dummy_list)

            # If there's no list in the dataframe column, read the column
            else:
                df_dummy = input_table[column]

            # Concat the treated columns into the output
            output_table = pd.concat([output_table, df_dummy], axis=1)
        return output_table

    def __missingTreatment(self, input_name: list) -> pd.DataFrame:
        # TODO: INCLUDE PERSONALIZED MISSING TREATMENT WITH MORE INTERPRETABILITY
        input_table = self.tables[input_name[0]]
        return input_table.fillna(self.missing_input)

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------
    # PUBLIC METHODS
    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------
    def extractData(self, output_table: str = 'flattened_data') -> None:
        # The main path of the PDN system
        system_root_path = os.path.join(self.root_path, self.pdn_system)

        # The list of every state on the PDN system
        state_paths = self.__getPaths(system_root_path)

        # Flatten all the states' data and append it into a single dataframe
        self.__execTableMethod(method='flattenStatesData',
                               input=state_paths, output=output_table)

        return None

    def defineId(self, id_columns: list = ['CURP'], input_table: str = 'last_data',
                 output_table: str = 'id_data') -> None:
        # This method takes a list of columns from which to make an unique id

        # TODO: DELETE THIS DISCLAIMER WHEN RAN ON AN ENVIRONMENT WITH DATAT THAT
        #        SHOWS THE CURP,SUCH AS INSIDE THE PLATAFORMA DIGITAL NACIONAL
        print('''Note on defineId method
    NOTE: IDEALLY, THIS FUNCTION SHOULD TAKE THE CURP OF EACH PUBLIC SERVANT
    THIS IS IN ORDER TO HAVE A TRULY UNIQUE AND TRACEABLE IDENTIFIER
    FOR EVERYONE. HOWEVER, IN THIS EXERCISE WE'LL TAKE A COMBINATION OF FULL NAME
    PLUS THE RESPECTIVE GOVERNMENT ORGANISATION THE PERSON WORKS FOR
    PLUS THE STATE THAT REPORTED THE DATA.''')

        # Create a unique string for each public servant
        df = self.tables[input_table].copy()
        df[id_columns] = df[id_columns].astype(str)
        df['unique_id'] = df[id_columns].agg('-'.join, axis=1)
        df['unique_id'] = df['unique_id'].apply(
            lambda x: x.lower().replace(' ', '_'))

        self.tables[output_table] = df.copy()
        self.metadata_columns += id_columns

        return None

    def normalizeData(self, input_table: str = 'last_data',
                      output_table: str = 'normalized_data') -> None:
        # This method extends every element  with a list within the dataframe
        # into multiple columns in the same dataframe
        self.__execTableMethod(method='normalizeData',
                               input=[input_table], output=output_table)
        return None

    def missingData(self, input: any = 0, input_table: str = 'last_data',
                    output_table: str = 'missing_data') -> None:
        # This method turns all missing data into a value
        self.missing_input = input
        self.__execTableMethod(method='missingTreatment',
                               input=[input_table], output=output_table)
        return None


class FeatureEngineering(DataTreatment):

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------
    # PRIVATE METHODS
    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def _tokenize_tfidf(self, corpus: list) -> object:
        # To tokenize with tfidf

        # Define and fit the tokenizer
        tokenizer = TfidfVectorizer()
        tokenizer.fit(corpus)

        return tokenizer

    # TODO: CORRECTLY FIX THIS CLASS INHERITANCE PROBLEM
    def __execTableMethod(self, method: str, input: list, output: str) -> None:
        self.tables[output] = eval("""self._{0}__{1}({2})""".format(
            __class__.__name__, method, input))
        self.last_data = self.tables[output].copy()
        self.table_history.append(output)
        return None

    def __tokenizeData(self, input_name: list):
        # TODO: BASED UPON THE WORD VARIETY, THE ALGORITHM DETERMINES TO TOKENIZE
        # WITH A DICTIONARY OR WITH TF-IDF

        # le paso el nombre de las columnas con las que voy a armar el id
        # -> de hecho, el id se puede armar desde el extract

        # la tokenizacion si debe ser sobre todas las palabras del dataset

        # Read the table, define the features to ignore and the date_column to sort by
        input_table = self.tables[input_name[0]]
        output_table = input_table.copy()
        ignore_features = self.metadata_columns.copy() + ['unique_id']

        # Get the non-ignorable features
        iterable_features = [
            column for column in input_table.columns if column not in ignore_features]

        # Construct the word corpus over all strings on each column
        if self.column_corpus:
            for column in iterable_features:
                word_corpus = [
                    item for item in input_table[column] if type(item) == str]

                try:
                    # Fit the tokenizer
                    self.tokenizers[column] = self._tokenize_tfidf(word_corpus)

                    # Apply element-wise tokenization on all iterable_features
                    output_table[column] = input_table[column].apply(lambda x: list(
                        self.tokenizers[column].transform([x]).toarray()[0]) if type(x) == str else x)
                except:
                    self.metadata_columns.append(column)

        # Construct the word corpus over all strings found on the dataframe
        #     (a good approach if you have A LOT of computing power and storage)
        else:
            word_corpus = []
            for column in iterable_features:
                filtered_list = [
                    item for item in input_table[column] if type(item) == str]
                word_corpus += filtered_list

            try:
                # Fit the tokenizer
                self.tokenizers['all'] = self._tokenize_tfidf(word_corpus)

                # Apply element-wise tokenization on all iterable_features
                output_table[iterable_features] = input_table[iterable_features].applymap(
                    lambda x: self.tokenizers[column].transform([x]).toarray()[0] if type(x) == str else x)
            except:
                self.metadata_columns += iterable_features

        return output_table

    def __groupData(self, input_name: list):
        # Read the table, define the features to ignore and the date_column to sort by
        input_table = self.tables[input_name[0]]
        ignore_features = self.metadata_columns.copy()
        date_column = grouping_date_dictionary[self.pdn_system]

        # Get the non-ignorable features
        iterable_features = [
            column for column in input_table.columns if column not in ignore_features]

        # Sort the table and then group by unique_id
        sorted_table = input_table[iterable_features+[date_column]
                                   ].sort_values(by=date_column, ascending=True)
        grouped_table = sorted_table.groupby('unique_id').agg(
            ['min', 'max', 'median', 'mean', 'prod', 'sum', 'std', 'var', 'sem', 'count'])

        # Flatten index on columns
        new_columns = ['_'.join(t) for t in grouped_table.columns]
        grouped_table.columns = new_columns
        grouped_table.reset_index(inplace=True)

        return grouped_table.rename(columns={'index': 'unique_id'})

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------
    # PUBLIC METHODS
    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def tokenizeData(self, column_corpus: bool = True, input_table: str = 'last_data', output_table: str = 'tokenized_data') -> None:
        # This method tokenizes text data based on the bag of words of each column
        self.tokenizers = dict()
        self.column_corpus = column_corpus
        self.__execTableMethod(method='tokenizeData',
                               input=[input_table], output=output_table)
        return None

    def groupData(self, input_table: str = 'last_data', output_table: str = 'grouped_data') -> None:
        # This method groups data into multiple features
        self.__execTableMethod(method='groupData',
                               input=[input_table], output=output_table)
        return None


def main():
    # LIBRARIES
    import os
    import json
    from glob import glob
    import pandas as pd
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    import pickle

    # The metadata column for every system
    metadata_columns = ['id']

    # For system 1
    metadata_items = ["tipo", "declaracionCompleta",
                      "actualizacionConflictoInteres", "actualizacion",
                      "institucion"]
    declaracion_items = ["nombre", "primerApellido", "segundoApellido",
                         "correoElectronico_institucional"]

    metadata_columns += ['metadata_'+item for item in metadata_items]
    metadata_columns += ['declaracion_situacionPatrimonial_datosGenerales_' +
                         item for item in declaracion_items]

    # For system 2
    metadata_columns += declaracion_items

    # For system 3s
    servidor_items = ["nombres", "primerApellido", "segundoApellido",
                      "genero_clave", "genero_valor"]

    metadata_columns += ["fechaCaptura",
                         "expediente", "fechaCaptura", "expediente"]
    metadata_columns += ['servidorPublicoSancionado_' +
                         item for item in servidor_items]

    # The unique build for ids in each system (at least in this exercise, without CURP)

    # For system 1, it will be the full name plus the delcaring institution plus estado_declarante
    declaracion_items = ["nombre", "primerApellido", "segundoApellido"]
    s1_id = ['declaracion_situacionPatrimonial_datosGenerales_' +
             item for item in declaracion_items]
    s1_id += ['estado_declarante', 'metadata_institucion']

    # For system 2, it will be similar
    s2_id = ["nombres", "primerApellido", "segundoApellido"]
    s2_id += ['estado_declarante', 'institucionDependencia_siglas']

    # For system 3, it is only the full name and estado_declarante because there's
    # no info about the institution the server works for
    servidor_items = ["nombres", "primerApellido", "segundoApellido"]

    s3s_id = ['servidorPublicoSancionado_'+item for item in servidor_items]
    s3s_id += ['estado_declarante']

    # Put every list into a single dictionary
    systems_id_dictionary = {'s1': s1_id, 's2': s2_id, 's3s': s3s_id}

    grouping_date_dictionary = {'s1': 'metadata_actualizacion',
                                's2': 'fechaCaptura', 's3s': 'fechaCaptura', 's3p': 'fechaCaptura'}

    # SINCE THERE'S A LOT OF RAM REQUIREMENTS, WE DROP HIGH NAN COLUMNS AND LOW VARIANCE ONES
    for system in ['s1', 's2', 's3s', 's3p']:
        if system == 's1':
            etl = FeatureEngineering(pdn_system=system, root_path='./',
                                     keywords=['escolaridad', 'ingreso', 'inversion'], metadata_columns=metadata_columns)

            # Initial extraction and normalization
            etl.extractData('ext_data')

            # Define the unique id of each servant
            etl.defineId(systems_id_dictionary[system], 'ext_data', 'ext_data')

            etl.normalizeData('ext_data', 'norm_data_inter_1')
            etl.normalizeData('norm_data_inter_1', 'norm_data_inter_2')
            etl.normalizeData('norm_data_inter_2', 'norm_data_1')

            # Treat all missing data
            etl.missingData(0, 'norm_data_1', 'miss_data_1')

            # Save this untokenized ungrouped data
            etl.last_data.to_csv('./'+system+'/ut_ug_m_data.csv', index=False)

            # Group the historic data
            etl.groupData('miss_data_1', 'group_data_1')

            # Save this untokenized grouped data
            etl.last_data.to_csv('./'+system+'/ut_g_um_data.csv', index=False)

            # Missing treatment for new NaNs (it has a different missing input because the origin is different)
            etl.missingData(-1, 'group_data_1', 'miss_data_2')

            # Save this untokenized grouped data
            etl.last_data.to_csv('./'+system+'/ut_g_m_data.csv', index=False)

            # Tokenize the text data and then normalize the newly created vectors
            etl.tokenizeData(True, 'miss_data_1', 'tok_data')
            etl.normalizeData('tok_data', 'norm_data_2')
            etl.missingData(0, 'norm_data_2', 'miss_data_3')
            etl.last_data.to_csv('./'+system+'/t_ug_m_data.csv', index=False)

        else:
            etl = FeatureEngineering(pdn_system=system, root_path='./',
                                     keywords=['nivel', 'tipo', 'nombre', 'clave', 'siglas', 'valor', 'superior', 'expediente', 'objeto', 'acto', 'causa', 'responsable', 'resolucion', 'multa', 'observacion', 'documento'], metadata_columns=metadata_columns)

            # Initial extraction and normalization
            etl.extractData('ext_data')

            # Define the unique id of each servant
            if system != 's3p':
                etl.defineId(
                    systems_id_dictionary[system], 'ext_data', 'ext_data')

            etl.normalizeData('ext_data', 'norm_data_inter_1')

            etl.normalizeData('norm_data_inter_1', 'norm_data_inter_2')

            etl.normalizeData('norm_data_inter_2', 'norm_data_1')

            # Treat all missing data
            etl.missingData(0, 'norm_data_1', 'miss_data_1')

            # Save this untokenized ungrouped data
            etl.last_data.to_csv('./'+system+'/ut_ug_m_data.csv', index=False)

            # Tokenize the text data and then normalize the newly created vectors
            etl.tokenizeData(True, 'miss_data_1', 'tok_data')

            etl.normalizeData('tok_data', 'norm_data_2')

            etl.missingData(0, 'norm_data_2', 'miss_data_3')

            # Save this tokenized ungrouped data
            etl.last_data.to_csv('./'+system+'/t_ug_m_data.csv', index=False)

        with open('./'+system+'/etl.pkl', 'wb') as f:
            pickle.dump(etl, f)


if __name__ == '__main__':
    main()
