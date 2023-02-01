// Needs two env variables: GITHUB_TOKEN and KITTYCAD_TOKEN
import fs from 'fs';
import fsp from 'fs/promises'
import { file } from '@kittycad/lib'
import fetch from "node-fetch"
import util from "util"
import { pipeline } from "stream"
const streamPipeline = util.promisify(pipeline)

async function downloadFile(repo, ref, filename, destination) {
    const token = process.env.GITHUB_TOKEN
    const headers = token ? { "authorization": `token ${token}` } : {}
    // First get some info on the blob with the Contents api
    const contentsUrl = `https://api.github.com/repos/${repo}/contents/${filename}?ref=${ref}`
    console.log("fetch:", contentsUrl, headers)
    const contentsResponse = await fetch(contentsUrl, { headers })
    if (!contentsResponse.ok) throw new Error(`unexpected response ${contentsResponse.statusText}`)
    const contentsJson = await contentsResponse.json()

    // Then actually use the download url (that supports LFS files) to write the file
    const downloadUrl = contentsJson["download_url"]
    const downloadResponse = await fetch(downloadUrl, { headers })
    console.log("fetch:", downloadUrl, headers)
    if (!downloadResponse.ok) throw new Error(`unexpected response ${downloadResponse.statusText}`)
    await streamPipeline(downloadResponse.body, fs.createWriteStream(destination))
}

async function convertToViewable(source) {
    const viewableFormat = "stl"
    const body = await fsp.readFile(source, 'base64')
    
    const response = await file.create_file_conversion({
        output_format: viewableFormat,
        src_format: 'obj',
        body,
    })
    if ('error_code' in response) throw response
    const { status, id, output } = response
    console.log(`File conversion id: ${id}`)
    console.log(`File conversion status: ${status}`)
    
    await fsp.writeFile(`${source}.${viewableFormat}`, output, 'base64')
}

async function main() {
    const repo = "KittyCAD/litterbox"
    const beforeCommit = "ab5d712acd156741f020c7b242c29189ae9bcf9e"
    const afterCommit = "4ddf899550addf41d6bf1b790ce79e46501411b3"
    const filename = "seesaw.obj"
    const beforePath = "seesaw_diff_before.obj"
    const afterPath = "seesaw_diff_after.obj"
    await downloadFile(repo, beforeCommit, filename, beforePath)
    await convertToViewable(beforePath)
    await downloadFile(repo, afterCommit, filename, afterPath)
    await convertToViewable(afterPath)
}

main()
