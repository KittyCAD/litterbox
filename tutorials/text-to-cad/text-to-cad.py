import time

from kittycad import KittyCAD, KittyCADAPIError
from kittycad.models import (
    ApiCallStatus,
    FileExportFormat,
    TextToCad,
    TextToCadCreateBody,
)

# Create our client.
client = KittyCAD()

# Prompt the API to generate a 3D model from text.
try:
    response = client.ml.create_text_to_cad(
        output_format=FileExportFormat.STEP,
        body=TextToCadCreateBody(
            prompt="Design a gear with 40 teeth",
        ),
    )
except KittyCADAPIError as e:
    print(f"Error: {e}")
    exit(1)

result = response

# Polling to check if the task is complete
while result.completed_at is None:
    # Wait for 5 seconds before checking again
    time.sleep(5)

    # Check the status of the task
    try:
        status_response = client.ml.get_text_to_cad_model_for_user(
            id=result.id,
        )
    except KittyCADAPIError as e:
        print(f"Error: {e}")
        exit(1)

    # The response is a TextToCadResponse, extract the actual data
    response_data = status_response.root
    # For this example, we expect it to be a TextToCad instance
    if isinstance(response_data, TextToCad):
        result = response_data
    else:
        print(f"Unexpected response type: {type(response_data)}")
        exit(1)

if result.status == ApiCallStatus.FAILED:
    # Print out the error message
    print(f"Text-to-CAD failed: {result.error}")

elif result.status == ApiCallStatus.COMPLETED:
    if result.outputs is None:
        print("Text-to-CAD completed but returned no files.")
        exit(0)

    # Print out the names of the generated files
    print(f"Text-to-CAD completed and returned {len(result.outputs)} files:")
    for name in result.outputs:
        print(f"  * {name}")

    # Save the STEP data as text-to-cad-output.step
    final_result = result.outputs["source.step"]
    with open("text-to-cad-output.step", "w", encoding="utf-8") as output_file:
        output_file.write(final_result.decode("utf-8"))
        print(f"Saved output to {output_file.name}")
