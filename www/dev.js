import { readdirSync, readFileSync, writeFileSync } from 'fs';
import { resolve } from 'path';
import { execSync } from "child_process";

const profiles_folder = resolve(process.cwd(), "../profiles");
const index_path = resolve(process.cwd(), "index.html");
const index = readFileSync(index_path, "utf-8");

const result = {};
let r = index.matchAll(/class=\"profile\">(.*)\.ini/g)
for (const re of r) {
    const f = re[1] + ".ini"
    const file = resolve(profiles_folder, f)
    result[f] = readFileSync(file, { encoding: "utf-8" }).replace(/\r/g, "")
}
writeFileSync(resolve(process.cwd(), "ts", "config.ts"), "export const profiles=" + JSON.stringify(result, undefined, 2) + `
export const build_info={
    'time':"${new Date().toUTCString()}",
    'time_now':${Date.now()},
    'commit_info':"${execSync(`git log -1 --pretty=format:"%ci | %H | %ae | %s"`).toString().replace(/\r/g, "")}",
    'commit_hash':"${execSync(`git rev-parse --short HEAD`).toString().replace(/\r/g, "").trim()}"
}
`)