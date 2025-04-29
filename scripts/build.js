import fs from "node:fs";
import cp from "node:child_process";

function build() {
  fs.cpSync("trees", "__trees", { recursive: true });
  cp.execSync("node scripts/index.js literal __trees");
  cp.execSync("kodama c -r __trees");
  cp.execSync("node scripts/index.js highlight __trees");
  fs.rmSync("trees/publish", { recursive: true, force: true });
  fs.cpSync("__trees/publish", "trees/publish", { recursive: true });
  fs.rmSync("__trees", { recursive: true, force: true });
}

export default build;
