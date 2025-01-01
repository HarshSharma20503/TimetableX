from extract import ExcelExtractor

# Create an object of the excelExtractor class and pass the file path to it

# logic to get the file path
file_path = 'timetables/year2.xls'


extractor = ExcelExtractor(file_path)

# Call the extract function
extractor.extract_and_print()