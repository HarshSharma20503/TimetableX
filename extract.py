import pandas as pd

class ExcelExtractor:
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_and_print(self):
        if self.file_path.endswith('.xls'):
            data = pd.read_excel(self.file_path)
            print(data)
        else:
            print("The file is not an .xls file")

# Example usage:
# extractor = ExcelExtractor('/path/to/your/file.xls')
# extractor.extract_and_print()