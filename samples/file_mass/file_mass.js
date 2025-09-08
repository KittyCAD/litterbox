import fsp from 'fs/promises'
import { exec } from 'child_process'
import { promisify } from 'util'
import { file } from '@kittycad/lib'

async function main() {
    const body = await fsp.readFile('./ORIGINALVOXEL-3.obj', 'base64')
    // LITTERBOX-END-NON-EDITABLE-SECTION

    // Steel density ≈ 7850 kg/m^3
    const steelDensityKgPerM3 = 7850
    const response = await file.create_file_mass({
        material_density: steelDensityKgPerM3,
        material_density_unit: 'kg:m3',
        output_unit: 'g',
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
