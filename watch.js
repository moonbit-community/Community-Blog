import chokidar from "chokidar";
import cp from "node:child_process";
import fs from "node:fs";

let watched_path = fs
  .readdirSync("trees", {
    withFileTypes: true,
  })
  .filter((dir) => dir.name !== "publish" && dir.name !== "trees")
  .map((dir) => `trees/${dir.name}`);

function build() {
  cp.execSync("kodama c -r trees");
  cp.execSync("node scripts/highlight.js");
}
build();

chokidar.watch(watched_path, { ignoreInitial: true }).on("all", (_, path) => {
  console.log(path);
  build();
});
