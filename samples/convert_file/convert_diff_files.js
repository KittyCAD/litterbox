// Needs two env variables: GITHUB_TOKEN and KITTYCAD_TOKEN
import fs from 'fs';
import fsp from 'fs/promises'
import { file } from '@kittycad/lib'
import { Octokit } from "@octokit/rest"
import fetch from "node-fetch"
import util from "util"
import { pipeline } from "stream"
const streamPipeline = util.promisify(pipeline)

async function downloadFile(octokit, owner, repo, ref, path, destination) {
    // First get some info on the blob with the Contents api
    const content = await octokit.rest.repos.getContent({ owner, repo, path, ref })

    // Then actually use the download_url (that supports LFS files and has a direct download token) to write the file
    console.log(`Downloading ${path}...`)
    const response = await fetch(content.data.download_url)
    if (!response.ok) throw new Error(`unexpected response ${response.statusText}`)
    await streamPipeline(response.body, fs.createWriteStream(destination))
}

async function convertToViewable(source, viewableFormat = "stl") {
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
    const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });
    const { data: { login } } = await octokit.rest.users.getAuthenticated();
    console.log(`Hello, @${login}`);

    const owner = "KittyCAD"
    const repo = "litterbox"
    const beforeCommit = "ab5d712acd156741f020c7b242c29189ae9bcf9e"
    const afterCommit = "4ddf899550addf41d6bf1b790ce79e46501411b3"
    const filename = "seesaw.obj"
    const beforePath = "seesaw_diff_before.obj"
    const afterPath = "seesaw_diff_after.obj"

    await downloadFile(octokit, owner, repo, beforeCommit, filename, beforePath)
    await convertToViewable(beforePath)
    await downloadFile(octokit, owner, repo, afterCommit, filename, afterPath)
    await convertToViewable(afterPath)
}

main()
