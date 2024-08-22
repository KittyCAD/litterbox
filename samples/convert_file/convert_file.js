import fsp from 'fs/promises'
import { file } from '@kittycad/lib/import'

async function main() {
    const body = await fsp.readFile('./ORIGINALVOXEL-3.obj', 'base64')
    // LITTERBOX-END-NON-EDITABLE-SECTION

    const fc = await file.create_file_conversion({
        output_format: 'stl',
        src_format: 'obj',
        body,
    })
    if ('error_code' in fc) throw fc
    console.log(`File conversion id: ${fc.id}`)
    console.log(`File conversion status: ${fc.status}`)

    const outputs = Object.entries(fc.outputs)
    if (outputs.length !== 1) throw Error("Expected one output file")

    // LITTERBOX-START-NON-EDITABLE-SECTION
    for (const [_, output] of outputs) {
        const outputFilePath = './output.stl'
        await fsp.writeFile(outputFilePath, output, 'base64')
    }
}

main()
