import time

from kittycad.api.ml import create_text_to_cad, get_text_to_cad_model_for_user
from kittycad.client import ClientFromEnv
from kittycad.models import (
    ApiCallStatus,
    Error,
    FileExportFormat,
    TextToCad,
    TextToCadCreateBody,
)

# Create our client.
client = ClientFromEnv()

# Prompt the API to generate a 3D model from text.
response = create_text_to_cad.sync(
    client=client,
    output_format=FileExportFormat.STEP,
    body=TextToCadCreateBody(
        prompt="Design a gear with 40 teeth",
    ),
)

if isinstance(response, Error) or response is None:
    print(f"Error: {response}")
    exit(1)

result: TextToCad = response

# Polling to check if the task is complete
while result.completed_at is None:
    # Wait for 5 seconds before checking again
    time.sleep(5)

    # Check the status of the task
    response = get_text_to_cad_model_for_user.sync(
        client=client,
        id=result.id,
    )

    if isinstance(response, Error) or response is None:
        print(f"Error: {response}")
        exit(1)

    result = response

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
