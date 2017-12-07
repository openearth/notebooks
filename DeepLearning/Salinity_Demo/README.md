## Files explanation
This demo contains five notebooks which together can be used to train and test a neural network on the provided salinity data:
 * Data_Preprocessing: used to get the relevant data from the original files and merge it into a single dataset which is then written to a csv files
 * Correlation_Analysis: used to analyse the correlation between the input parameters (the salinity and discharge in Lobith and water level at Hoek van Holland) and the output parameter (the salinity in Capelle aan de IJssel)
 * Preprocess_NN_Data: used to take the raw data and convert it to input ready to be put into the neural network, this notebook randomly divides the resulting batches among train, test and validation data.
 * Train_Model: trains a model on the training data provided
 * Test_Model: tests a trained model on the test data provided

The first three notebooks should be run in the order they are listed to generate a database on which models can be trained and tested. In order to run the Preprocess_NN_Data notebook there needs to be three folder 'train', 'test', and 'validate' in the 'data' folder. The notebook will use the 'data/shuffle' file to divide the batches among train, test and validation data. Note that if any change is made to this file, the batches will be ordered differently and using a previously trained model in the Test_Model notebook could then result in mixing the test and training data for a model. Similarly, if the data preprocessing scripts are changed the resulting data will of course also differ from those used by previously trained models. 

The model created in the Train_Model notebook can be adapted each time a new NN is desired, don't forget to change the output filename in the last cell to make sure the newly trained model is saved in a different file (the notebook will test whether the provided filename exists and refuse to write the model to file if it does). This saved model can then be read by the Test_Model notebook. 

In addition to the notebooks there should already be a folder 'data' present containing the following files:
 * Cl_KadIJ_Merge_dt1h.tek
 * Cl_Lobith_Merge_dt1h.lss
 * Q_Lobith_Merge_dt1h.lss
 * h_HvH_Merge_dt1h.tek
 * shuffle
