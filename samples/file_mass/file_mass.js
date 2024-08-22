import fsp from 'fs/promises'
import { exec } from 'child_process'
import { promisify } from 'util'
import { file } from '@kittycad/lib/import'

async function main() {
    const body = await fsp.readFile('./ORIGINALVOXEL-3.obj', 'base64')
    // LITTERBOX-END-NON-EDITABLE-SECTION

    const steelDensityPerCubicMillimeter = 0.00785
    const response = await file.create_file_mass({
        material_density: steelDensityPerCubicMillimeter,
        src_format: 'obj',
        body,
    })
    if ('error_code' in response) throw response
    const { mass } = response
    console.log(`File mass: ${mass}`)
    const partInfo = {
        title: 'output.json',
        mass,
    }

    // LITTERBOX-START-NON-EDITABLE-SECTION
    await promisify(exec)('cp ./ORIGINALVOXEL-3.obj ./output.obj')
    await fsp.writeFile('./output.json', JSON.stringify(partInfo, null, 2), 'utf8')
}

main()
