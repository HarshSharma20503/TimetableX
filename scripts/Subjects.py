import pandas as pd
import json

# Function to extract subject names
def extract_subject_data(file_path, start_row, end_row, subject_col_start):
    data = pd.read_excel(file_path)
    data = data.iloc[start_row:end_row]
    data = data.iloc[:, subject_col_start:]  # Using configurable column start

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
    return subject_data

# Function to extract course codes
def course_codes(file_path, start_row, end_row, code_col):
    data = pd.read_excel(file_path)
    data = data.iloc[start_row:end_row]
    data = data.iloc[:, code_col:code_col+1]  # Using configurable column for course codes

    course_codes = []

    for col in data.columns:
        for idx, cell in data[col].items():
            if pd.notna(cell):
                valid_indices = data[col].index
                current_position = valid_indices.get_loc(idx)

                for i in valid_indices[current_position + 1:]:
                    if pd.notna(data[col][i]):
                        course_codes.append(data[col][i])
                break
    return course_codes

# Function to refine course codes
def extract_course_codes(course_codes):
    course_codes_new = []
    for subject in course_codes:
        if '/' in subject:
            i = subject.split('/')[0].strip()
            course_codes_new.append(i)
        else:
            # Append the code directly if '/' is not present
            course_codes_new.append(subject)
    return course_codes_new

# Function to combine course codes and subject names into a dictionary
def create_course_subject_dict(file_path, start_row, end_row, code_col, subject_col_start):
    # Extract course codes and subject names
    raw_course_codes = course_codes(file_path, start_row, end_row, code_col)
    refined_course_codes = extract_course_codes(raw_course_codes)
    subject_names = extract_subject_data(file_path, start_row, end_row, subject_col_start)

    # Create dictionary by combining the two tuples
    course_subject_dict = dict(zip(refined_course_codes, subject_names))

    # # If there are leftover course codes without subject names
    # if len(refined_course_codes) > len(subject_names):
    #     print("\nCourse codes without subject names:")
    #     for extra_code in refined_course_codes[len(subject_names):]:
    #         print(extra_code)

    return course_subject_dict

# Main function
def main():
    # Define file paths and configurations for each year
    year_configs = {
        'Year 1': {
            'file_path': "../timetables/year1.xlsx",
            'start_row': 148,
            'end_row': 163,
            'code_col': 7,         # Column index for course codes
            'subject_col_start': 8 # Starting column index for subject names
        },
        'Year 2': {
            'file_path': "../timetables/year2.xls",
            'start_row': 133,        # Update with actual row numbers
            'end_row': 144,          # Update with actual row numbers
            'code_col': 1,         # Update with actual column index
            'subject_col_start': 3 # Update with actual column index
        },
        'Year 3': {
            'file_path': "../timetables/year3.xls",
            'start_row': 116,        # Update with actual row numbers
            'end_row': 145,          # Update with actual row numbers
            'code_col': 1,         # Update with actual column index
            'subject_col_start': 3 # Update with actual column index
        },
        'Year 4': {
            'file_path': "../timetables/year4.xls",
            'start_row': 69,        # Update with actual row numbers
            'end_row': 109,          # Update with actual row numbers
            'code_col': 1,         # Update with actual column index
            'subject_col_start': 3 # Update with actual column index
        }
    }

    # Process each year
    all_year_data = {}

    for year, config in year_configs.items():
        try:
            course_subject_dict = create_course_subject_dict(
                config['file_path'],
                config['start_row'],
                config['end_row'],
                config['code_col'],
                config['subject_col_start']
            )
            all_year_data[year] = course_subject_dict

            # Print results for each year
            print(f"\n{year} Course-Subject Dictionary:")
            for course_code, subject_name in course_subject_dict.items():
                print(f"{course_code}: {subject_name}")

        except Exception as e:
            print(f"Error processing {year}: {str(e)}")
        with open("year_wise_data.json", "w") as json_file:
            json.dump(all_year_data, json_file, indent=4)

    print("\nYear-wise data has been written to 'year_wise_data.json'.")
    return all_year_data

if __name__ == "__main__":
    main()
