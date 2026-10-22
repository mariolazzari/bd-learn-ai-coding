import { Plugin } from "@opencode/plugin";
import { spawn } from "node:child_process";
import path from "node:path";

// This file lives at <project root>/.opencode/plugins/run-slop.ts
const PROJECT_ROOT = path.resolve(import.meta.dir, "../..");

type SlopResult = {
  stdout: string;
  stderr: string;
  exitCode: number;
};

function runSloperator(file: string): Promise<SlopResult> {
  const target = path.isAbsolute(file) ? file : path.resolve(PROJECT_ROOT, file);

  return new Promise((resolve, reject) => {
    const child = spawn("uv", ["run", "--no-active", "sloperator.py", target], {
      cwd: PROJECT_ROOT,
      env: process.env,
    });

    let stdout = "";
    let stderr = "";

    child.stdout?.setEncoding("utf8");
    child.stdout?.on("data", (chunk: string) => {
      stdout += chunk;
    });

    child.stderr?.setEncoding("utf8");
    child.stderr?.on("data", (chunk: string) => {
      stderr += chunk;
    });

    child.on("error", reject);
    child.on("close", (code) => {
      resolve({ stdout, stderr, exitCode: code ?? 1 });
    });
  });
}

export default Plugin.define({
  id: "sloperator.run-slop",
  setup: async (ctx) => {
    await ctx.tool.transform((tools) => {
      tools.add({
        name: "run_slop",
        description: "Run a SlopLang (.slop) file with Sloperator and return stdout, stderr, and exitCode as JSON",
        input: {
          type: "object",
          properties: {
            path: {
              type: "string",
              description: "Path to the .slop file, absolute or relative to the project root",
            },
          },
          required: ["path"],
          additionalProperties: false,
        },
        options: { codemode: false },
        execute: async (input) => {
          const { path: file } = input as { path: string };
          const result = await runSloperator(file);
          return { content: JSON.stringify(result, null, 2) };
        },
      });
    });
  },
});
