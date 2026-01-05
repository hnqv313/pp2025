import shlex
import subprocess
import sys


def parse_command(command):
    pipeline = [seg.strip() for seg in command.split("|")]
    commands = []

    for segment in pipeline:
        tokens = shlex.split(segment)

        cmd = []
        stdin = None
        stdout = None
        append = False

        i = 0
        while i < len(tokens):
            if tokens[i] == "<":
                stdin = tokens[i + 1]
                i += 2
            elif tokens[i] == ">":
                stdout = tokens[i + 1]
                append = False
                i += 2
            elif tokens[i] == ">>":
                stdout = tokens[i + 1]
                append = True
                i += 2
            else:
                cmd.append(tokens[i])
                i += 1

        commands.append(
            {"cmd": cmd, "stdin": stdin, "stdout": stdout, "append": append}
        )

    return commands


def execute_pipeline(commands):
    processes = []
    prev_pipe = None

    for i, command in enumerate(commands):
        stdin = None
        stdout = None

        if command["stdin"]:
            stdin = open(command["stdin"], "r")
        elif prev_pipe:
            stdin = prev_pipe

        if command["stdout"]:
            mode = "a" if command["append"] else "w"
            stdout = open(command["stdout"], mode)
        elif i < len(commands) - 1:
            stdout = subprocess.PIPE

        process = subprocess.Popen(
            command["cmd"],
            stdin=stdin,
            stdout=stdout,
            stderr=subprocess.PIPE,
            text=True,
        )

        if prev_pipe:
            prev_pipe.close()

        prev_pipe = process.stdout
        processes.append(process)

    out, err = processes[-1].communicate()

    if out:
        print(out, end="")
    if err:
        print(err, file=sys.stderr)

    for p in processes[:-1]:
        p.wait()


def shell():
    while True:
        try:
            command = input("7.shell> ").strip()
            if not command:
                continue
            if command in ("exit", "quit"):
                break

            commands = parse_command(command)
            execute_pipeline(commands)

        except KeyboardInterrupt:
            print()
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)


if __name__ == "__main__":
    shell()
