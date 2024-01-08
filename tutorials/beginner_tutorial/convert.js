import { file } from '@kittycad/lib'
import fsp from 'fs/promises'

async function convertOBJtoSTEP() {
    // Use KittyCAD client library to output base64 string from OBJ to STEP
    const response = await file.create_file_conversion({
        output_format: 'step',
        src_format: 'obj',
        body: await fsp.readFile('./gear.obj', 'base64'),
    })
  
  
    for (const key in response.outputs) {
        if (response.outputs.hasOwnProperty(key)) {
          const output = response.outputs[key];
          const outputFilePath = "./output.step";
        
          console.log(`Saving output to ${outputFilePath}`);
        
          const decodedData = Buffer.from(output, "base64").toString("utf-8");
          fsp.writeFile(outputFilePath, decodedData);
        }
    }
}

convertOBJtoSTEP()