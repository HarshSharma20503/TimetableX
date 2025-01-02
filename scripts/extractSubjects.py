

import pandas as pd

def extract_paired_data(file_path, start_row, end_row):
    data = pd.read_excel(file_path)
    data = data.iloc[start_row:end_row]
    
    # Extract codes (from column 1 onwards) and subjects (from column 3 onwards)
    codes_df = data.iloc[:, 1:]
    subjects_df = data.iloc[:, 3:]
    
    codes = []
    subjects = []
    
    # Process each column pair
    for code_col, subj_col in zip(codes_df.columns, subjects_df.columns):
        code_data = codes_df[code_col].dropna()
        subj_data = subjects_df[subj_col].dropna()
        
        # Only process if we have both a code and a subject
        for i in range(min(len(code_data), len(subj_data))):
            code = code_data.iloc[i]
            subject = subj_data.iloc[i]
            
            # Clean up code if it contains a forward slash
            if '/' in str(code):
                code = code.split('/')[0].strip()
                
            codes.append(code)
            subjects.append(subject)
    
    return codes, subjects

def create_course_subject_dict(file_path, start_row, end_row):
    course_codes, subject_names = extract_paired_data(file_path, start_row, end_row)
    return dict(zip(course_codes, subject_names))

def main():
    file_path = "../timetables/year2.xls"
    start_row, end_row = 131, 144
    
    course_subject_dict = create_course_subject_dict(file_path, start_row, end_row)
    
    print("\nCourse-Subject Dictionary:")
    for course_code, subject_name in course_subject_dict.items():
        print(f"{course_code}: {subject_name}")

if __name__ == "__main__":
    main()