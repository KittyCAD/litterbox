// Needs two env variables: GITHUB_TOKEN and KITTYCAD_TOKEN
import fs from 'fs';
import fsp from 'fs/promises'
import { file } from '@kittycad/lib'
import { Octokit } from "@octokit/rest"
import fetch from "node-fetch"
import util from "util"
import path from "path"
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

async function makeViewable(source, srcFormat, outputFormat = "stl") {
    const body = await fsp.readFile(source, 'base64')

    const response = await file.create_file_conversion({
        output_format: outputFormat,
        src_format: srcFormat,
        body,
    })
    if ('error_code' in response) console.log(response)
    const { status, id, output } = response
    console.log(`File conversion id: ${id}`)
    console.log(`File conversion status: ${status}`)

    await fsp.writeFile(source, output, 'base64')
}

async function getDiff(octokit, owner, repo, changedFiles, sha, parentSha, destination) {
    const beforeDir = path.join(destination, "before")
    const afterDir = path.join(destination, "after")
    await fsp.mkdir(beforeDir, { recursive: true })
    await fsp.mkdir(afterDir, { recursive: true })
    const supportedSrcFormats = new Set([
        "dae",
        "dxf",
        "fbx",
        "obj_zip",
        "obj",
        "obj_nomtl",
        "ply",
        "step",
        "stl",
    ]);

    for (const file of changedFiles) {
        const { filename, status } = file
        const extension = filename.split(".").pop()
        if (!supportedSrcFormats.has(extension)) {
            continue;
        }

        // Supporting nested files
        const beforeFilePath = path.join(beforeDir, filename)
        await fsp.mkdir(path.join(beforeFilePath, ".."), { recursive: true })
        const afterFilePath = path.join(afterDir, filename)
        await fsp.mkdir(path.join(afterFilePath, ".."), { recursive: true })

        if (status == "modified") {
            await downloadFile(octokit, owner, repo, parentSha, filename, beforeFilePath)
            await makeViewable(beforeFilePath, extension)
            await downloadFile(octokit, owner, repo, sha, filename, afterFilePath)
            await makeViewable(afterFilePath, extension)
        } else if (status == "added") {
            await downloadFile(octokit, owner, repo, sha, filename, afterFilePath)
            await makeViewable(afterFilePath, extension)
        } else if (status == "removed") {
            await downloadFile(octokit, owner, repo, parentSha, filename, beforeFilePath)
            await makeViewable(beforeFilePath, extension)
        } else {
            console.error(`Unsupported file status (${status}), skipping.`)
        }
    }
}

async function main() {
    const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });
    const { data: { login } } = await octokit.rest.users.getAuthenticated();
    console.log(`Hello, @${login}`);

    const owner = "KittyCAD"
    const repo = "litterbox"

    // Get files from a Pull Request
    const pullNumber = 95
    const pull = await octokit.rest.pulls.get({ owner, repo, pull_number: pullNumber })
    let changedFiles = (await octokit.rest.pulls.listFiles({ owner, repo, pull_number: pullNumber })).data
    let sha = pull.data.head.sha
    let parentSha = pull.data.base.sha
    await getDiff(octokit, owner, repo, changedFiles, sha, parentSha, `diff/#${pullNumber}`)

    // Get files from a commit
    sha = "b697e3fc1c7f1be203ceb37928adbe423ffa25ac"
    const commit = await octokit.rest.repos.getCommit({ owner, repo, ref: sha })
    changedFiles = commit.data.files || []
    parentSha = commit.data.parents[0].sha
    await getDiff(octokit, owner, repo, changedFiles, sha, parentSha, `diff/${sha}`)
}

main()
