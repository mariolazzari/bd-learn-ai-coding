import { Plugin } from "@opencode/plugin";
import { appendFile, mkdir } from "node:fs/promises";
import path from "node:path";

// This file lives at <project root>/.opencode/plugins/playground-log.ts
const PROJECT_ROOT = path.resolve(import.meta.dir, "../..");
const LOG_PATH = path.join(PROJECT_ROOT, "logs", "plugin-playground.log");
const MARKER = "playground/server.py";

export default Plugin.define({
  id: "sloperator.playground-log",
  setup: async (ctx) => {
    await ctx.shell.hook("create.before", async ({ command }) => {
      if (!command.includes(MARKER)) return;
      await mkdir(path.dirname(LOG_PATH), { recursive: true });
      await appendFile(LOG_PATH, "playground shell request\n", "utf8");
    });
  },
});
