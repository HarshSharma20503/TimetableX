import pandas as pd
import json

def extract_faculty_data(file_path, start_row, end_row):
    data = pd.read_excel(file_path)

    data = data.iloc[start_row:end_row]

    data = data.iloc[:, 1:]

    data = data.dropna(axis=1, how='all')

    faculty_data = []

    for col in data.columns:
        for idx, cell in data[col].items():
            if pd.notna(cell) and cell == "Faculty Abbreviation with Names":

                valid_indices = data[col].index
                current_position = valid_indices.get_loc(idx)

                for i in valid_indices[current_position + 1:]:
                    if pd.notna(data[col][i]):
                        faculty_data.append(data[col][i])
                break

    return faculty_data

def process_faculty_data(faculty_data):
    teacher_dict = {}
    
    for entry in faculty_data:
        # Handle both '-' and ':' separators
        separator_index = max(entry.find('-'), entry.find(':'), entry.find(';'))
        
        if separator_index != -1:
            # Extract code (left part) and name (right part)
            code = entry[:separator_index].strip()
            name = entry[separator_index + 1:].strip()
            
            # Add to dictionary with name as key and code as value
            teacher_dict[code] = name
        else:
            print("Separator not found in entry: ", entry)
    
    return teacher_dict

def main():
    faculty_data = extract_faculty_data("../timetables/year1.xlsx", 149, 168)

    teacher_dict = process_faculty_data(faculty_data)

    with open('../data/teachers.json', 'w') as json_file:
        json.dump(teacher_dict, json_file, indent=2)

if __name__ == "__main__":
    main()
