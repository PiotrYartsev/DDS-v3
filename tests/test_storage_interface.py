import unittest
import os
from src.storage_interface import load_files_dump_from_RSE,generate_SQLite_database_for_temporal_check,temporal_check
from tests.test_log_config import logger

class TestStorageInterfaceLoadingData(unittest.TestCase):
    def setUp(self):
        # This will print before each test method
        test_id = self.id()
        test_name = test_id.split('.')[-1]
        print(f"\nRunning test: {test_name}")

    def test_positive_load(self):
        #test a positive testcase where test file is loaded correctly
        loading_data=load_files_dump_from_RSE("tests/rsedumptest","LUND_GRIDFTP",logger)
        expected_set=set(['/projects/hep/fs9/shared/ldmx/ldcs/gridftp/mc20/v9/8.0GeV/v1.7.1_targetPN_reco_tskim_subrun10-batch5/mc_v9-8GeV-1e-target_photonuclear_run1892_t1639389153.root','/projects/hep/fs9/shared/ldmx/ldcs/gridftp/mc20/v9/8.0GeV/v1.7.1_targetPN_reco_tskim_subrun4-batch2/mc_v9-8GeV-1e-target_photonuclear_run1618_t1638539490.root','/projects/hep/fs9/shared/ldmx/ldcs/gridftp/mc21/v12/4.0GeV/v3.0.0_overlayEcalPN-batch10/mc_v12-4GeV-2e-ecal_photonuclear_run828_t1637173197.root','/projects/hep/fs9/shared/ldmx/ldcs/gridftp/mc20/v12/4.0GeV/v2.3.0-1e-pileup/mc_v12-4GeV-1e-inclusive_pileup_run4157_t1615836801.root','/projects/hep/fs9/shared/ldmx/ldcs/gridftp/mc20/v9/8.0GeV/v1.7.1_target_gammamumu_8gev_reco-batch8/mc_v9-8GeV-1e-target_gammamumu_run524_t1651202103.root','/projects/hep/fs9/shared/ldmx/ldcs/gridftp/mc21/v12/4.0GeV/v3.0.0_overlayEcalPN-batch46/mc_v12-4GeV-2e-ecal_photonuclear_run4963_t1639406505.root','/projects/hep/fs9/shared/ldmx/ldcs/gridftp/mc20/v9/8.0GeV/v1.7.1_target_gammamumu-batch20/mc_v9-8GeV-1e-target_gammamumu_run192094_t1646266728.root','/projects/hep/fs9/shared/ldmx/ldcs/gridftp/mc20/v9/4.0GeV/v1.7.1_ecal_photonuclear-batch7/mc_v9-4.0GeV-1e-ecal_photonuclear_run16620_t1651730368.root','/projects/hep/fs9/shared/ldmx/ldcs/gridftp/validation/v12/4.0GeV/v2.3.0-testPileup-large/mc_v12-4GeV-2e-ecal_photonuclear_run1706_t1616546764.root','/projects/hep/fs9/shared/ldmx/ldcs/gridftp/mc20/v9/8.0GeV/v1.7.1_target_gammamumu-batch2/mc_v9-8GeV-1e-target_gammamumu_run10868_t1645738858.root','/projects/hep/fs9/shared/ldmx/ldcs/gridftp/mc20/v9/8.0GeV/v1.7.1_targetPN_reco_tskim_subrun6-batch2/mc_v9-8GeV-1e-target_photonuclear_run1615_t1639052210.root','/projects/hep/fs9/shared/ldmx/ldcs/gridftp/mc20/v9/8.0GeV/v1.7.1_targetPN_reco_tskim_subrun1-batch2/mc_v9-8GeV-1e-target_photonuclear_run242_t1631843043.root','/projects/hep/fs9/shared/ldmx/ldcs/gridftp/mc20/v9/8.0GeV/v1.7.1_targetPN_reco_tskim_subrun8-batch4/mc_v9-8GeV-1e-target_photonuclear_run95_t1639246068.root','/projects/hep/fs9/shared/ldmx/ldcs/gridftp/mc20/v9/8.0GeV/v1.7.1_target_gammamumu-batch4/mc_v9-8GeV-1e-target_gammamumu_run34082_t1645777315.root','/projects/hep/fs9/shared/ldmx/ldcs/gridftp/mc20/v9/8.0GeV/v1.7.1_target_gammamumu_8gev_reco-batch30/mc_v9-8GeV-1e-target_gammamumu_run1697_t1651281178.root','/projects/hep/fs9/shared/ldmx/ldcs/gridftp/validation/v9/8.0GeV/v1.7.1_ecal_gammamumu_reco-batch4/mc_v9-8GeV-1e-ecal_gammamumu_run1846_t1626175020.root','/projects/hep/fs9/shared/ldmx/ldcs/gridftp/mc20/v9/8.0GeV/v1.7.1_target_gammamumu-batch18/mc_v9-8GeV-1e-target_gammamumu_run171012_t1646226794.root','/projects/hep/fs9/shared/ldmx/ldcs/gridftp/mc20/v9/8.0GeV/v1.7.1_target_gammamumu_8gev_reco-batch4/mc_v9-8GeV-1e-target_gammamumu_run1602_t1651190610.root','/projects/hep/fs9/shared/ldmx/ldcs/gridftp/mc20/v9/8.0GeV/v1.7.1_target_gammamumu-batch16/mc_v9-8GeV-1e-target_gammamumu_run152388_t1646196709.root','/projects/hep/fs9/shared/ldmx/ldcs/gridftp/mc20/v9/8.0GeV/v1.7.1_target_gammamumu_8gev_reco-batch3/mc_v9-8GeV-1e-target_gammamumu_run533_t1651186035.root'])
        self.assertEqual(loading_data,expected_set,"The set does not contain the expected output of files")
    
    def test_negative_load_empty_directory(self):
        #test a negative testcase where the directory provided is empty, not containing any dump
        directory = "tests/empty_directory"
        # If directory does not exist, create it
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        with self.assertRaises(SystemExit) as cm:
            load_files_dump_from_RSE(directory, "LUND_GRIDFTP", logger)
        
        self.assertEqual(str(cm.exception), "Error: Expected 1 dump file in tests/empty_directory, found 0.")
        
        # Delete the empty_directory after the test
        os.rmdir(directory)

    def test_negative_no_rse_in_filename(self):
        #test the negative testcase if the filename does not match the rse
        with self.assertRaises(SystemExit) as cm:
            load_files_dump_from_RSE("tests/rsedumptest","WRONG",logger)
        self.assertEqual(str(cm.exception),"Error: Dump file LUND_GRIDFTP-RUCIO-2023_10_06.txt does not match RSE name WRONG.")
    
    def test_negative_not_a_txt_file(self):
        # Define the directory path
        directory = "tests/check_directory"
        # If directory does not exist, create it
        if not os.path.exists(directory):
            os.makedirs(directory)
        # Define the CSV file path
        csv_file_path = os.path.join(directory, "LUND_GRIDFTP-RUCIO-2023_10_06.csv")
        # If there is no file there called LUND_GRIDFTP-RUCIO-2023_10_06.csv, create an empty csv file named such
        if not os.path.exists(csv_file_path):
            with open(csv_file_path, 'w') as f:
                pass  # Create an empty CSV file
        # Test that the correct exception is raised for a non-txt file
        with self.assertRaises(SystemExit) as cm:
            load_files_dump_from_RSE(directory, "LUND_GRIDFTP", logger)
        self.assertEqual(str(cm.exception), "Error: Dump file LUND_GRIDFTP-RUCIO-2023_10_06.csv is not in TXT format.")
        # Cleanup: Remove the CSV file and then the directory
        os.remove(csv_file_path)
        os.rmdir(directory)
    
# Define a class for testing the generation of SQLite database for temporal checks
class TestGenerationSQliteDatabaseForTemporalCheck(unittest.TestCase):
    def setUp(self):
        # Print the name of the test before each test method
        test_id = self.id()
        test_name = test_id.split('.')[-1]
        print(f"\nRunning test: {test_name}")
        
    def test_generate_SQLite_database_for_temporal_check(self):
        # Test generating an SQLite database
        database_file = "tests/test_database"
        generate_SQLite_database_for_temporal_check(database_file)
        # Assert that the database file exists
        self.assertTrue(os.path.exists(database_file + '.db'))
        # Cleanup: Remove the database file
        os.remove(database_file + '.db')
class TestTemporalCheck(unittest.TestCase):
    def setUp(self):
        # This will print before each test method
        test_id = self.id()
        test_name = test_id.split('.')[-1]
        print(f"\nRunning test: {test_name}")
        
    def test_generate_SQLite_database_for_temporal_check_not_an_integer_days_between_checks(self):
        with self.assertRaises(ValueError) as cm:
            temporal_check("tests/temporal_check/temporal_bad_data_database","LUND_GRIDFTP",set(),set(),"hello")
        self.assertEqual(str(cm.exception),"Error occurred while handling days_between_checks, hello not a positive integer")
    
    def test_generate_SQLite_database_for_temporal_check_not_an_existing_database(self):
        with self.assertRaises(FileNotFoundError) as cm:
            temporal_check("tests/rsedumptest","LUND_GRIDFTP",set(),set(),1)
        self.assertEqual(str(cm.exception),"The database file tests/rsedumptest.db does not exist")
    


# Run the tests if the script is executed directly
if __name__ == '__main__':
    unittest.main()