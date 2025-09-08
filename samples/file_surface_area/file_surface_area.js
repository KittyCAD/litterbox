import fsp from 'fs/promises'
import { exec } from 'child_process'
import { promisify } from 'util'
import { file } from '@kittycad/lib'

async function main() {
    const body = await fsp.readFile('./ORIGINALVOXEL-3.obj', 'base64')
    // LITTERBOX-END-NON-EDITABLE-SECTION

    const response = await file.create_file_surface_area({
        src_format: 'obj',
        body,
    })
    if ('error_code' in response) throw response
    const { surface_area } = response
    console.log(`File surface area: ${surface_area}`)
    const partInfo = {
        title: 'output.json',
        surface_area,
    }

    // LITTERBOX-START-NON-EDITABLE-SECTION
    await promisify(exec)('cp ./ORIGINALVOXEL-3.obj ./output.obj')
    await fsp.writeFile('./output.json', JSON.stringify(partInfo, null, 2), 'utf8')
}

main()
