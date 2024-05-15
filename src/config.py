import os


class Config:
    def __init__(self):
        self.data_folder = "_1_data_prepared_input"
        self.data_file = "test.csv"
        self.txt_label = "text"
        self.target_label = "label"
        self.data_out_folder = "output"#"_2_preproc_pipeline_de/data_preprocessed"
        self.data_out_file = "test_preproc.csv"
        
    def get_data_path(self):
        return os.path.join(self.data_folder, self.data_file)
    
    def get_data_out_path(self):
        return os.path.join(self.data_out_folder, self.data_out_file)