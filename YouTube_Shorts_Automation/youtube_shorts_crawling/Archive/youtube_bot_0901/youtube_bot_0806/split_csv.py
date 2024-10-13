import csv
import os
def split_csv(input_file, output_folder, max_records):

    with open(input_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Read the header

        count = 0
        file_index = 1
        os.makedirs(output_folder, exist_ok=True)
        output_file = os.path.join(output_folder, f'split_{file_index}.csv')
        with open(output_file, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(header)  # Write the header to each split file
            for row in reader:
                writer.writerow(row)
                count += 1
                if count == max_records:
                    count = 0
                    file_index += 1
                    output_file = os.path.join(output_folder, f'split_{file_index}.csv')
                    outfile.close()  # Close the current file
                    outfile = open(output_file, 'w', newline='')  # Reopen the file
                    writer = csv.writer(outfile)
                    writer.writerow(header)
        print("split-csv files are created")
# Example usage:
input_file = 'links.csv'  # Replace 'input.csv' with your CSV file path
output_folder = 'split-csv'  # Folder where split CSV files will be saved
split_csv(input_file, output_folder, max_records=40)