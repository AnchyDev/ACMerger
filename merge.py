import sys
import io
import re

def main(args):
    if len(args) < 3:
        print("You must supply the input file and destination file.")
        print("Ex: merge.py my-worldserver.conf worldserver.conf")
        return

    path_file_in = args[1]
    path_file_out = args[2]

    with open(path_file_in, "rt") as file_in:
        with open(path_file_out, "rt") as file_out:
            lines = file_in.readlines()
            config_current = file_out.read()
            for line in lines:
                # Ignore empty lines
                if not line.strip():
                    continue

                key = line.split('=')[0].strip()
                value = line.split('=')[1].strip()

                config_modified = re.sub(f"{key}\s*=\s*.+", f"{key} = {value}", config_current)

                if config_modified == config_current:
                    print(f"Failed to find key '{key}' in `{path_file_out}`, make sure your config is up-to-date.")
                    continue
                else:
                    print(f"Merging key '{key}' into '{path_file_out}'.")
                    config_current = config_modified

    with open(path_file_out, "wt") as file_out:
        file_out.write(config_current)

if __name__ == "__main__":
    main(sys.argv)