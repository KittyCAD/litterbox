import fsp from 'fs/promises'
import { exec } from 'child_process'
import { promisify } from 'util'
import { file } from '@kittycad/lib/import'

async function main() {
    const body = await fsp.readFile('./seesaw.obj', 'base64')
    // LITTERBOX-END-NON-EDITABLE-SECTION

    const response = await file.create_file_center_of_mass({
        material_density: 7,
        src_format: 'obj',
        body,
    })
    if ('error_code' in response) throw response
    const { center_of_mass } = response
    console.log(`File center of mass: ${center_of_mass}`)
    const partInfo = {
        title: 'output.json',
        center_of_mass,
    }

    // LITTERBOX-START-NON-EDITABLE-SECTION
    await promisify(exec)('cp ./seesaw.obj ./output.obj')
    await fsp.writeFile('./output.json', JSON.stringify(partInfo, null, 2), 'utf8')
}

main()
