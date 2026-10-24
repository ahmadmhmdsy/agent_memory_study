// A smolagents-ts ContainerRuntime over the docker CLI. It replaces the library's dockerode
// runtime only to add what the study needs: our own image and the task workspace mounted at /work.
import { execFile } from "node:child_process";
import { promisify } from "node:util";

const run = promisify(execFile);

export const IMAGE = "r013-sandbox:1";

async function docker(args) {
  const { stdout } = await run("docker", args, { windowsHide: true, maxBuffer: 16 * 1024 * 1024 });
  return stdout.trim();
}

/** One runtime per session: it knows the workspace to mount. */
// `session` labels every container of one session, so cleanup can find a container whose create
// finished after the session was aborted (the budget abort can race a pending `docker create`).
export function cliRuntime({ workspace, created, pending, session }) {
  return {
    // The library asks to build its default Dockerfile; the study image is built once, beforehand.
    async buildImage() {
      return IMAGE;
    },
    async createContainer(request) {
      const args = ["create", "--memory", "1g", "--cpus", "1", "--label", "r013=1",
        ...(session ? ["--label", `r013.session=${session}`] : []),
        "-v", `${workspace}:/work`, "-w", "/work"];
      for (const e of request.env) args.push("-e", e);
      for (const port of Object.keys(request.portBindings ?? {})) {
        args.push("-p", `127.0.0.1::${port.split("/")[0]}`);
      }
      args.push(request.image);
      const p = docker(args);
      pending?.push(p);
      const id = await p;
      created?.push(id);
      return id;
    },
    async startContainer(id) {
      await docker(["start", id]);
    },
    async endpoint(id, port) {
      // "127.0.0.1:49153" (one line per address family; take the IPv4 one).
      const out = await docker(["port", id, `${port}/tcp`]);
      const line = out.split(/\r?\n/).find((l) => l.startsWith("127.0.0.1:")) ?? out.split(/\r?\n/)[0];
      const at = line.lastIndexOf(":");
      return { host: line.slice(0, at), port: Number(line.slice(at + 1)) };
    },
    async stopContainer(id) {
      await docker(["stop", "-t", "2", id]);
    },
    async removeContainer(id) {
      await docker(["rm", "-f", id]);
    },
  };
}

/** Hidden tests: no network, workspace read-only, tests mounted beside it. */
export async function runHiddenTests(workspace, hiddenDir) {
  const args = ["run", "--rm", "--network", "none", "--memory", "1g",
    "-v", `${workspace}:/work:ro`, "-v", `${hiddenDir}:/hidden:ro`, "-w", "/work",
    "-e", "PYTHONPATH=/work", "-e", "PYTHONDONTWRITEBYTECODE=1",
    IMAGE, "python", "-m", "pytest", "/hidden", "-q", "-rA", "-p", "no:cacheprovider"];
  try {
    const { stdout } = await run("docker", args, { windowsHide: true, timeout: 180_000, maxBuffer: 16 * 1024 * 1024 });
    return parsePytest(stdout, 0);
  } catch (err) {
    return parsePytest(String(err.stdout ?? ""), err.code ?? 1, String(err.stderr ?? "").slice(0, 2000));
  }
}

function parsePytest(stdout, code, stderr = "") {
  const results = {};
  for (const m of stdout.matchAll(/^(PASSED|FAILED|ERROR)\s+\S*::(\S+)/gm)) results[m[2]] = m[1];
  return { exitCode: code, results, tail: stdout.slice(-3000), stderr };
}

/** Remove study containers left behind: all of them, or only one session's (by its label). */
export async function sweepContainers(session) {
  const label = session ? `label=r013.session=${session}` : "label=r013=1";
  const ids = (await docker(["ps", "-aq", "--filter", label])).split(/\s+/).filter(Boolean);
  for (const id of ids) await docker(["rm", "-f", id]).catch(() => {});
  return ids.length;
}
