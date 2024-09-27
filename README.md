# README.md
# GAMDL Web UI

This is a simple web interface for the GAMDL (Glomatico's Apple Music Downloader) library.

## Setup

1. Ensure you have installed the gamdl library and all its dependencies.

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Make sure your gamdl configuration files (like cookies.txt) are in the correct location.

## Usage

1. Run the Flask application:
   ```
   python app.py [--port PORT]
   ```
   By default, the application will run on port 5000. You can specify a different port using the `--port` argument.

2. Open a web browser and navigate to `http://localhost:PORT`, where PORT is the port number you specified (or 5000 if you didn't specify one).

3. Fill in the form with the following information:
   - Apple Music URL
   - Output Path
   - Template File Playlist
   - Check the boxes for Print Exceptions and Save Playlist if needed

4. Click "Download" to start the download process. You will see real-time logs and progress in the log window below the form.

Downloaded files will be saved in the specified output path.

Note: This implementation includes real-time logging and progress updates.
