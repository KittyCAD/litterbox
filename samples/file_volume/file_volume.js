import fsp from 'fs/promises'
import { exec } from 'child_process'
import { promisify } from 'util'
import { file } from '@kittycad/lib'

async function main() {
    const body = await fsp.readFile('./ORIGINALVOXEL-3.obj', 'base64')
    // LITTERBOX-END-NON-EDITABLE-SECTION

    const response = await file.create_file_volume({
        output_unit: 'm3',
        src_format: 'obj',
        body,
    })
    if ('error_code' in response) throw response
    const { volume } = response
    console.log(`File volume: ${volume}`)
    const partInfo = {
        title: 'output.json',
        volume,
    }

    // LITTERBOX-START-NON-EDITABLE-SECTION
    await promisify(exec)('cp ./ORIGINALVOXEL-3.obj ./output.obj')
    await fsp.writeFile('./output.json', JSON.stringify(partInfo, null, 2), 'utf8')
}

main()
