# Create your views here.
# csvhandler/views.py
import json
from csvhandler.processor.forced_data_conversion import forced_to_bool
from csvhandler.processor.main import infer_and_convert_data_types
import pandas as pd
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
import io
from csvhandler.process_functions import map_user_friendly_names_to_dtypes, get_differences
from csvhandler.process_functions import map_dtypes_to_user_friendly_names
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


"""
CSVUploadView: Django APIView to handle the upload of a CSV file, process its data types, 
and allow the user to download the processed CSV file.

Description:
This view is responsible for receiving a CSV file uploaded by the user. It processes 
the file using a custom function to infer and convert the data types of the columns. 
The processed DataFrame is then converted back into a CSV format, and the user can 
download the resulting file.

Key Functionalities:
- Accept an uploaded CSV file from the client.
- Process the CSV file to infer and convert data types using a custom function.
- Convert the processed DataFrame back into a CSV file.
- Return the processed CSV file as a downloadable HTTP response.

Returns:
- A CSV file (processed_data) for download in the response with the filename "processed_file.csv".

Note:
- This functionality is currently not used in the active workflow but remains operational for file processing and download.

Example Usage:
- A user uploads a CSV file, and the server processes the file, converting data types.
- The server returns the processed CSV file for the user to download.
"""


class CSVUploadView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        # Receive and process the uploaded file
        file = request.FILES['file']
        df = pd.read_csv(file)

        # Use a custom processing function to process the DataFrame
        processed_data = infer_and_convert_data_types(df)

        # Convert the processed DataFrame back to CSV format
        buffer = io.StringIO()
        processed_data.to_csv(buffer, index=False)
        buffer.seek(0)

        # Return the CSV file as an HTTP response
        response = HttpResponse(buffer, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="processed_file.csv"'
        return response

"""
CSVTypesView: Django APIView to process an uploaded CSV file, infer and store data types, 
and return a dict of column names to user-friendly data types.

Description:
This view handles the initial processing of an uploaded CSV file. It infers the data types 
of each column in the file using a custom processing function and generates a dict 
between column names and their data types. The processed data and its data type dict 
are saved on the server for subsequent operations. Finally, it returns the data type 
dict in a user-friendly format to the front-end as a JSON response.

Key Functionalities:
- Accept a CSV file upload from the client.
- Infer and convert column data types using a custom function.
- Save the processed data as a CSV file on the server.
- Create and save a JSON file representing the dict of column names to data types.
- Convert inferred data types to user-friendly names for front-end display.
- Return the user-friendly data type dict as a JSON response.

Returns:
- A JSON object containing a dict of column names to user-friendly data types.

Example Usage:
- A user uploads a CSV file, and the back-end processes the file to infer and convert data types.
- The processed data and its data type dict are stored for future operations.
- The front-end receives a user-friendly dict of the inferred data types for display or further editing.
"""

class CSVTypesView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        # Receive and process the uploaded file
        file = request.FILES['file']
        df = pd.read_csv(file)

        # Use a custom function to process data and infer data types
        processed_data = infer_and_convert_data_types(df)

        # Save the processed data to a CSV file
        processed_data.to_csv("csvhandler/files/output.csv", index=False)

        # Create a map of column names to their data types
        dtype_map = {col: str(dtype) for col, dtype in processed_data.dtypes.items()}

        # Save the data type map to a JSON file for later use
        with open('csvhandler/files/dtype_map.json', 'w') as f:
            json.dump(dtype_map, f)

        # Map the inferred data types to user-friendly names
        dtype_map = map_dtypes_to_user_friendly_names(dtype_map)

        # Return the data type map as a JSON response
        return JsonResponse(dtype_map)

"""
CSVSaveViewAndDownload: Django APIView to process updated data type dict, 
coerce data types in a DataFrame accordingly, and provide the updated data as a downloadable CSV.

Description:
This view receives a JSON string from the front-end representing the updated relationships 
between column attributes and their desired data types (as modified by the user). 
It compares this dict with the original data type dict stored on the server. If there are differences:
1. Coerces the affected columns to the specified data types.
2. Saves the updated DataFrame to a file.
3. Sends the updated CSV file back to the user as an HTTP response for download.

Key Functionalities:
- Retrieve and parse the updated data type dict from the front-end.
- Load the previously processed CSV and its original data type dict.
- Compare the updated dict with the original and identify differences.
- Coerce columns to the specified types where changes are detected.
- Save the updated data and send it as a downloadable CSV to the client.

Error Handling:
- Handles cases where the original data type dict file is missing with an appropriate JSON response.

Returns:
- A downloadable CSV file containing the updated data.

Example Usage:
- User modifies column data types via a front-end UI and submits the changes.
- The back-end processes these changes, updates the DataFrame, and provides the modified CSV for download.
"""


class CSVSaveViewAndDownload(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        # Retrieve the updated data type dict as a JSON string from the request
        updated_map_str = request.data['data']  # `data` is expected to be a JSON string

        # Parse the JSON string into a Python dictionary
        updated_map = json.loads(updated_map_str)

        # Load the previously processed DataFrame from the saved file
        df = pd.read_csv("csvhandler/files/output.csv")

        # Load the original data type dict from the JSON file
        try:
            with open('csvhandler/files/dtype_map.json', 'r') as f:
                dtype_map = json.load(f)
        except FileNotFoundError:
            # Handle missing JSON file with an error response
            return JsonResponse({'error': 'dtype_map file is missing. Please re-upload and save again.'}, status=400)

        # Map user-friendly data type names back to the original data types
        updated_map = map_user_friendly_names_to_dtypes(updated_map)

        if updated_map != dtype_map:
            # Detect differences between the original and updated data type dict
            difference_map = get_differences(updated_map, dtype_map)

            # Perform specific type coercion based on the differences
            df = forced_to_bool(df, difference_map)

            # Save the updated DataFrame back to the same file
            df.to_csv("csvhandler/files/output.csv", index=False)

        # Convert the DataFrame to a CSV string
        csv_file = io.StringIO()
        df.to_csv(csv_file, index=False)
        csv_file.seek(0)  # Reset the file pointer

        # Create an HTTP response containing the CSV file for download
        response = HttpResponse(csv_file.getvalue(), content_type='text/csv')

        # Set the file name for the download prompt in the browser
        response['Content-Disposition'] = 'attachment; filename="output.csv"'
        return response



