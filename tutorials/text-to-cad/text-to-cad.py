import time
from typing import Any, List, Optional, Tuple, Union

from kittycad.api.ai import create_text_to_cad, get_text_to_cad_model_for_user
from kittycad.client import ClientFromEnv
from kittycad.models import Error, TextToCad
from kittycad.models.file_export_format import FileExportFormat
from kittycad.models.text_to_cad_create_body import TextToCadCreateBody
from kittycad.types import Response


def text_to_cad_gen():

    # Create our client.
    client = ClientFromEnv()

    # Call the ML-ephant API to generate a 3D model from text.
    result: Optional[Union[TextToCad, Error]] = create_text_to_cad.sync(
        client=client,
        output_format=FileExportFormat.GLTF,
        body=TextToCadCreateBody(
            prompt="design a 40 tooth gear", # The prompt to use for generating the model
        ),
    )

    # Check if the response is an error
    if isinstance(result, Error) or result == None:
        print(result)
        raise Exception("Error in response")

    # Print the response
    body: TextToCad = result
    print(body)
 
    # Get the ID from the response
    task_id = body.id

    # Polling to check if the task is complete
    while True:
        # Check the status of the task
        check_result: Optional[
            Union[TextToCad, Error]
        ] = get_text_to_cad_model_for_user.sync(
        client=client,
        id=task_id,
    )

        if isinstance(check_result, Error):
            print(check_result)
            raise Exception("Error checking task status")

        if check_result.completed_at != None:  # Check to see if completed_at is not None (meaning, it's done)
            break

        # Wait for 5 seconds before checking again
        time.sleep(5) 

    # Retrieve the final result
    final_result = check_result.outputs["source.gltf"] # Get the GLTF file from the outputs

    output_file_path = "./text-to-cad-output.gltf"
    print(f"Saving output to {output_file_path}")
    output_file = open(output_file_path, "wb") 

    output_file.write(final_result.get_decoded()) # Write the GLTF information to the text-to-cad-output.gltf file
    output_file.close()

text_to_cad_gen()