import fsp from 'fs/promises'
import { file } from '@kittycad/lib'

async function main() {
    const body = await fsp.readFile('./ORIGINALVOXEL-3.obj', 'base64')
    // LITTERBOX-END-NON-EDITABLE-SECTION
    
    const response = await file.create_file_conversion({
        output_format: 'stl',
        src_format: 'obj',
        body,
    })
    if ('error_code' in response) throw response
    const { status, id, output } = response
    console.log(`File conversion id: ${id}`)
    console.log(`File conversion status: ${status}`)
    
    // LITTERBOX-START-NON-EDITABLE-SECTION
    await fsp.writeFile('./output.stl' , output, 'base64')
}

main()
