import sys
import helpers.printer
import helpers.parser
import helpers.config
import program.obfuscation
import program.bypass

modes = helpers.config.Modes
bypass_methods = helpers.config.BypassMethods
obfuscation_methods = helpers.config.ObfuscationMethods

printer = helpers.printer.Printer()
parser = helpers.parser.Parser(
    printer, modes, bypass_methods, obfuscation_methods)

bypass = program.bypass.Bypass()
obfuscation = program.obfuscation.Obfuscation()


def execute_program(options):
    try:
        print(options)
        mode = options[0]
        bypass_type = options[1]
        obfuscation_type = options[2]
        input = options[3]
        output = options[4]
        if mode == modes.bypass:
            code = bypass.execute_bypass(bypass_type)
            obfuscation.execute_ofuscation_code(
                obfuscation_type, code, output)
        elif mode == modes.obfuscate:
            obfuscation.execute_obfuscation_file(
                obfuscation_type, input, output)
        else:
            raise SystemExit("Not supported mode")
        print("The file " + output + " has been created succesfully")

    except:
        raise SystemError("Options are not valid")


def main(args=None):
    # Get command line arguments
    if args is None:
        try:
            args = sys.argv[1:]
        except IndexError:
            printer.print_help()

    if ("-h" in args or "--help" in args):
        if len(args) == 1:
            printer.print_help()
        else:
            raise SystemExit(
                "Help option (-h or --help) must be run without arguments")
    elif ("-v" in args or "--version" in args):
        if len(args) == 1:
            printer.print_version()
        else:
            raise SystemExit(
                "Version option (-v or --version) must be run without arguments")
    else:
        if (len(args) == 0):
            printer.print_help()
        else:
            # Mode - Bypass type - Obfuscation type - Input file to obfuscate - Output file to generate
            options = parser.parse_command_line(args)
            execute_program(options)


if __name__ == "__main__":
    main()
