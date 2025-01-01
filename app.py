

import streamlit as st
import pdfplumber
import pandas as pd
import io
from typing import Dict, List, Optional

class TimeTableFormatter:
    """Handles the formatting and display of timetable data in a structured way"""
    
    @staticmethod
    def create_time_slots():
        """Creates a list of standard time slots matching the PDF format"""
        return ['9-10', '10-11', '11-12', '12-1', '1-2', '2-3', '3-4', '4-5']
    
    @staticmethod
    def create_weekdays():
        """Creates a list of weekdays as shown in the timetable"""
        return ['MON', 'TUE', 'Wed', 'Thu', 'Fri', 'Sat']

class FlexibleTimetableExtractor:
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file
        self.timetable_data = None
        self.time_slots = TimeTableFormatter.create_time_slots()
        self.weekdays = TimeTableFormatter.create_weekdays()

    def extract_content(self):
        """
        Extracts and processes the timetable content from the PDF.
        Now specifically handling the format shown in the example image.
        """
        try:
            # Create an empty timetable DataFrame with the correct structure
            self.timetable_data = pd.DataFrame(
                index=self.weekdays,
                columns=self.time_slots,
                data=''
            )
            
            # Read the PDF file
            pdf_bytes = io.BytesIO(self.pdf_file.getvalue())
            
            with pdfplumber.open(pdf_bytes) as pdf:
                for page in pdf.pages:
                    # Extract tables with specific settings to match the PDF structure
                    tables = page.extract_tables(
                        table_settings={
                            "vertical_strategy": "text",
                            "horizontal_strategy": "text",
                            "intersection_y_tolerance": 10,
                            "intersection_x_tolerance": 10
                        }
                    )
                    
                    # Process each table found in the PDF
                    for table in tables:
                        self._process_table(table)
                        
        except Exception as e:
            raise Exception(f"PDF extraction failed: {str(e)}")

    def _process_table(self, table: List[List[str]]) -> None:
        """
        Processes each table from the PDF and maps it to our timetable structure.
        Now specifically handling the format shown in the example image.
        """
        # Clean the table data
        cleaned_table = [
            [str(cell).strip() if cell is not None else '' for cell in row]
            for row in table
        ]
        
        # Map the data to our timetable structure
        current_day = None
        for row in cleaned_table:
            # Find the day if present in the first column
            if row and row[0]:
                day_check = row[0].strip().upper()
                if day_check in [d.upper() for d in self.weekdays]:
                    current_day = day_check
            
            if current_day:
                # Map the cells to time slots
                for col_idx, time_slot in enumerate(self.time_slots):
                    if col_idx + 1 < len(row) and row[col_idx + 1]:  # +1 because first column is for days
                        content = row[col_idx + 1].strip()
                        if content and content.upper() != 'BREAK':
                            self.timetable_data.at[current_day, time_slot] = content

    def get_timetable(self) -> pd.DataFrame:
        """Returns the processed timetable"""
        if self.timetable_data is None:
            raise ValueError("Timetable has not been processed yet")
        return self.timetable_data

def main():
    st.set_page_config(page_title="Enhanced Batch Timetable Extractor", layout="wide")
    
    st.title("📚 Enhanced Batch Timetable Extractor")
    st.write("""
    Upload your timetable PDF and select your batch to view your schedule.
    """)
    
    uploaded_file = st.file_uploader("Upload your timetable PDF", type="pdf")
    
    if uploaded_file is not None:
        try:
            with st.spinner("Processing PDF... Please wait."):
                extractor = FlexibleTimetableExtractor(uploaded_file)
                extractor.extract_content()
            
            # Create batch options
            batch_prefixes = ['A', 'B', 'C']
            batch_options = []
            for prefix in batch_prefixes:
                max_num = 18 if prefix in ['A', 'B'] else 3
                batch_options.extend([f"{prefix}{i}" for i in range(1, max_num + 1)])
            
            # Batch selection
            selected_batch = st.selectbox(
                "Select your batch:",
                batch_options
            )
            
            # Simplified elective selection
            has_electives = st.radio(
                "Do you have elective subjects?",
                ["No", "Yes"]
            )
            
            if has_electives == "Yes":
                elective_subject = st.text_input("Enter your elective subject name:")
            
            if selected_batch:
                try:
                    timetable = extractor.get_timetable()
                    
                    if not timetable.empty:
                        st.success(f"Timetable for batch {selected_batch}")
                        
                        # Apply custom styling to the table
                        st.markdown("""
                        <style>
                        .stDataFrame {
                            font-size: 14px;
                        }
                        .stDataFrame td {
                            white-space: pre-wrap;
                            padding: 8px;
                        }
                        </style>
                        """, unsafe_allow_html=True)
                        
                        # Display the timetable
                        st.dataframe(
                            timetable,
                            use_container_width=True,
                            height=400
                        )
                        
                        # Download option
                        buffer = io.BytesIO()
                        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                            timetable.to_excel(writer, index=True)
                        
                        st.download_button(
                            label="📥 Download Timetable as Excel",
                            data=buffer.getvalue(),
                            file_name=f"timetable_{selected_batch}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    else:
                        st.warning("No data found in the timetable")
                        
                except Exception as e:
                    st.error(f"Error processing timetable: {str(e)}")
                    
        except Exception as e:
            st.error(f"Error processing the PDF: {str(e)}")
            st.info("""
            Troubleshooting tips:
            1. Ensure the PDF is not password protected
            2. Check if the PDF contains readable text (not scanned)
            3. Make sure the PDF format matches the expected timetable structure
            """)

if __name__ == "__main__":
    main()