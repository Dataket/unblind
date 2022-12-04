import pandas as pd

# TODO: WORK ON OTHER FEATURE SELECTION METHODS
class FeatureSelection:
  
  def __init__(self, root_path:str, dataset_name:str) -> None:
    self.root_path = root_path
    self.dataset_name = dataset_name

    self.final_features = list(pd.read_csv(root_path+dataset_name, nrows=1).columns)
    return None
  
  def dropNullFeatures(self, thresh:float=0.99) -> None:
    non_null_columns = []
    column_list = self.final_features.copy()

    input_table = pd.read_csv(root_path+dataset_name, usecols=column_list)

    for column in column_list:
      if 1-len(input_table[column].value_counts())/len(input_table)>=thresh:
        non_constant_columns.append(column)

    del input_table
    self.final_features = non_constant_features)

    return None
  
  def dropConstantFeatures(self, thresh:float=0.9) -> None:
    non_constant_columns = []
    column_list = self.final_features.copy()

    input_table = pd.read_csv(root_path+dataset_name, usecols=column_list)

    for column in column_list:
      if 1-len(input_table[column].value_counts())/len(input_table)>=thresh:
        non_constant_columns.append(column)

    del input_table
    self.final_features = non_constant_features)

    return None
    
class AnomalyDetection(FeatureSelection):
  # NOTE: THE ANOMALY SCORE CURRENTLY ONLY EXISTS FOR SYSTEM 1

  # These ones define a model, an instance variable to which one can use method fit and predict
  def anomalyBenchmark(self, load_path:str=None) -> None:
    pass
  def anomalyChallenger(self, load_path:str=None) -> None:
    pass
    
class NetworkDetection(AnomalyDetection):
  # NOTE: THE ANOMALY SCORE WORKS WITH ALL THE SYSTEMS INTEGRATED ON PDN

  # La network detection va a funconar a nivel institución en el caso del sistema 1+sistema 1
  #   va a funcionar a nivel estado en el caso del sistema 1+sistema 3 asímismo
  #   hay un boost al peso del nodo si id_sistema1 = id_sistema2 (a nivel dependencia+estado) o id_sistema2=id_sistema_3 (a nivel estado)
