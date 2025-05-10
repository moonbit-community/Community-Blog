import chokidar from "chokidar";
import internal_build from "./scripts/build.js";
import fs from "node:fs";

const watched_path = fs
  .readdirSync("trees", {
    withFileTypes: true,
  })
  .filter((dir) => dir.name !== "publish" && dir.name !== "trees")
  .map((dir) => `trees/${dir.name}`);

let isBuilding = false;
let pendingBuild = false;

function build() {
  if (isBuilding) {
    pendingBuild = true;
    return;
  }

  isBuilding = true;
  try {
    internal_build();
  } finally {
    isBuilding = false;
    if (pendingBuild) {
      pendingBuild = false;
      build();
    }
  }
}

build();

chokidar.watch(watched_path, { ignoreInitial: true }).on("all", (_, path) => {
  console.log(path);
  build();
});
