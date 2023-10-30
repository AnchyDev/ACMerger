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
            line_number = 0
            for line in lines:
                line_number = line_number + 1

                # Ignore empty lines
                if not line.strip():
                    continue

                if line.strip().startswith("#"):
                    continue

                kvp = line.split('=')
                if len(kvp) < 2:
                    print(f"Invalid key-value-pair found on line {line_number}.")
                    continue

                key = line.split('=')[0].strip()
                value = line.split('=')[1].strip()

                if not key:
                    print(f"Invalid key (empty) found on line {line_number}.")
                    continue

                if not value:
                    print(f"Invalid value (empty) found on line {line_number}.")
                    continue

                pattern = f"{key}\s*=\s*.+"

                if not re.search(pattern, config_current):
                    print(f"Key '{key}' not found, appending to '{path_file_out}'..")
                    config_current = f"{config_current}\n{key} = {value}"
                    continue

                config_modified = re.sub(pattern, f"{key} = {value}", config_current)

                if config_modified == config_current:
                    print(f"No changes were made for '{key}', value is up-to-date.")
                    continue
                else:
                    print(f"Merging key '{key}' into '{path_file_out}'.")
                    config_current = config_modified

    with open(path_file_out, "wt") as file_out:
        file_out.write(config_current)

if __name__ == "__main__":
    main(sys.argv)