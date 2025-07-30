# ERPNext Student Applicant File Transfer App

A Flask-based web application that helps transfer files from ERPNext sites to a local directory, specifically designed for managing student applicant files.

## Features

- Upload Excel files containing file information from ERPNext
- Automatically copy files from ERPNext site directories (private/public)
- Organize files in output directories based on student information
- User-friendly web interface
- Detailed logging of file operations
- Support for both private and public file locations

## Prerequisites

- Python 3.x
- ERPNext installation
- Access to ERPNext site files

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ransikerandeni/ERPNext_STAPP_File_Transfer_APP.git
cd ERPNext_STAPP_File_Transfer_APP
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. **Start the Application**
```bash
cd app
python app.py
```
The application will start on `http://0.0.0.0:5001`

2. **Prepare Your Excel File**
   - Your Excel file should contain these columns:
     - `Attached To Name`: The folder name where files will be copied to
     - `File URL`: The path to the file in ERPNext

3. **Using the Web Interface**
   - Open your browser and go to `http://localhost:5001`
   - Enter your ERPNext site name (e.g., `ucsctest_site.com`)
   - Upload your Excel file
   - Submit the form
   - Check the logs displayed on the page for file operation details

4. **Check Results**
   - Copied files will be in the `output` directory
   - Files are organized in subfolders based on the `Attached To Name` column
   - Check the web interface logs for detailed operation information

## Directory Structure

```
ERPNext_STAPP_File_Transfer_APP/
├── app/
│   ├── app.py            # Main application file
│   ├── templates/        # HTML templates
│   ├── uploads/         # Temporary storage for uploaded Excel files
│   └── output/          # Output directory for copied files
└── requirements.txt     # Python dependencies
```

## Troubleshooting

1. **Files Not Found**
   - Verify the ERPNext site name is correct
   - Check if files exist in both private and public directories
   - Ensure file paths in Excel file are correct
   - Check the logs for exact paths being searched

2. **Permission Issues**
   - Ensure the application has read access to ERPNext site directories
   - Ensure write permissions for uploads and output directories

## Security Considerations

- The app runs on localhost by default
- Only .xlsx files are allowed for upload
- File paths are sanitized before processing
- Keep your ERPNext file access secure

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
