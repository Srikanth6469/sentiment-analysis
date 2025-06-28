import csv
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# Function to read data from CSV file, predict labels, and write input and output to a new CSV file
def process_csv_with_prediction(input_file, output_file):
    try:
        # Open the input CSV file for reading
        with open(input_file, 'r') as csv_input:
            # Create a CSV reader
            csv_reader = csv.DictReader(csv_input)
            
            # Get the header names
            headers = csv_reader.fieldnames
            
            # Assuming the last column is the label to be predicted
            feature_columns = headers[:-1]
            label_column = headers[-1]
            
            # Read the data into lists
            features = []
            labels = []
            for row in csv_reader:
                feature_values = [float(row[column]) for column in feature_columns]
                label_value = float(row[label_column])
                features.append(feature_values)
                labels.append(label_value)
            
            # Split the data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
            
            # Create a Decision Tree Classifier (you can replace this with another algorithm)
            classifier = DecisionTreeClassifier()
            
            # Fit the model on the training data
            classifier.fit(X_train, y_train)
            
            # Predict labels for the test data
            predictions = classifier.predict(X_test)
            
            # Open the output CSV file for writing
            with open(output_file, 'w', newline='') as csv_output:
                # Create a CSV writer
                csv_writer = csv.writer(csv_output)
                
                # Write the header to the output CSV file
                csv_writer.writerow(headers + ['PredictedLabel'])
                
                # Write input features, actual labels, and predicted labels to the output CSV file
                for features, actual_label, predicted_label in zip(X_test, y_test, predictions):
                    csv_writer.writerow(features + [actual_label, predicted_label])
                
                print(f"Input and output written to '{output_file}'.")
    
    except FileNotFoundError:
        print(f"File '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
input_csv_file = 'input_data.csv'
output_csv_file = 'output_predictions.csv'

process_csv_with_prediction(input_csv_file, output_csv_file)