import pandas as pd
import json


def extract_subject_data(file_path, start_row, end_row):
    data = pd.read_excel(file_path)

    data = data.iloc[start_row:end_row]

    data = data.iloc[:, 8:]


    subject_data = []

    for col in data.columns:
        for idx, cell in data[col].items():
            if pd.notna(cell):
                valid_indices = data[col].index
                current_position = valid_indices.get_loc(idx)

                for i in valid_indices[current_position + 1:]:
                    if pd.notna(data[col][i]):
                        subject_data.append(data[col][i])
                break
    print(subject_data)
    return subject_data


def main():
    # Extract the raw subject data
    subject_data = extract_subject_data("../timetables/year1.xlsx", 148, 163)
    
    # Print the raw subject data
    print("\nRaw Subject Data:")
    for subject in subject_data:
        print(subject)

if __name__ == "__main__":
    main()