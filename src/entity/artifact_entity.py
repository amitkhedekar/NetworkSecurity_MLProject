from dataclasses import dataclass

@dataclass
class DataIngestionArtifact: ##data that will get returned from Ingestion stage
    trained_file_path : str
    test_file_path : str

@dataclass
class DataValidationArtifact:  ##data that will get returned from Validation stage
    validation_status : bool
    valid_train_file_path : str
    valid_test_file_path : str
    invalid_train_file_path : str
    invalid_test_file_path : str
    drift_report_file_path : str
