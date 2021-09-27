import random


class Parser:
    def __init__(self, printer, modes, bypass_methods, obfuscation_methods) -> None:
        self.printer = printer
        self.modes = modes
        self.bypass_methods = bypass_methods
        self.obfuscation_methods = obfuscation_methods

    def get_mode(self, args):
        if ("-m" in args or "--mode" in args):
            index = -1
            if "-m" in args:
                index = args.index("-m")
            else:
                index = args.index("--mode")
            try:
                mode_string = args[index+1]
            except IndexError:
                raise SystemExit(
                    "Operation mode is required: -m obfuscate or -m bypass.")
            try:
                return self.modes[mode_string]
            except:
                raise SystemExit(
                    "The selected mode must be one of the following:\n" + self.printer.print_enum(self.modes))
        else:
            raise SystemExit("-m option is required")

    def get_bypass(self, args):
        if ("-t" in args or "--type" in args):
            index = -1
            if "-t" in args:
                index = args.index("-t")
            else:
                index = args.index("--type")

            try:
                bypass_string = args[index+1]
                return self.bypass_methods[bypass_string]
            except:
                raise SystemExit(
                    "The selected bypass type must be one of the following:\n" + self.printer.print_enum(self.bypass_methods))

        else:
            # Reflection bypass by default
            return self.bypass_methods.reflection

    def get_obfuscation(self, args):
        if ("-t" in args or "--type" in args):
            index = -1
            if "-t" in args:
                index = args.index("-t")
            else:
                index = args.index("--type")

            try:
                obfuscation_string = args[index+1]
                return self.obfuscation_methods[obfuscation_string]
            except:
                raise SystemExit(
                    "The selected obfuscation type must be one of the following:\n" + self.printer.print_enum(self.obfuscation_methods))
        else:
            # Concatenation obfuscation by default
            return self.obfuscation_methods.concatenation

    def get_obfuscation_for_bypass(self, args):
        if ("-f" in args or "--obfuscation" in args):
            index = -1
            if "-f" in args:
                index = args.index("-f")
            else:
                index = args.index("--obfuscation")

            try:
                obfuscation_string = args[index+1]
                return self.obfuscation_methods[obfuscation_string]
            except:
                raise SystemExit(
                    "The selected obfuscation type must be one of the following:\n" + self.printer.print_enum(self.obfuscation_methods))
        else:
            # Return code, do not obfuscate
            return None

    def get_input_file(self, args):
        if ("-i" in args or "--input" in args):
            index = -1
            if "-i" in args:
                index = args.index("-i")
            else:
                index = args.index("--input")

            try:
                return args[index+1]
            except:
                raise SystemExit(
                    "Input file is required. Please use -i or --input to specify the input file")
        else:
            raise SystemExit(
                "Input file is required. Please use -i or --input to specify the input file")

    def get_output_file(self, args):
        if ("-o" in args or "--output" in args):
            index = -1
            if "-o" in args:
                index = args.index("-o")
            else:
                index = args.index("--output")

            try:
                filename = args[index+1]
                if filename.endswith('.ps1'):
                    return filename
                else:
                    raise SystemExit(
                        "The output filename must be a PowerShell script, with extension '.ps1'")
            except:
                raise SystemExit(
                    "Output filename must be specified in option -o")
        else:
            return "output.ps1"

    def parse_command_line(self, args):
        options = []

        # Find non existing arguments
        for a in args:
            if ('--' in a):
                if (a != '--mode' and a != '--type' and a != '--obfuscation' and a != '--input' and a != '--output'):
                    raise SystemExit(
                        "Unknown option: " + a)
            elif ('-' in a):
                if (a != '-m' and a != '-t' and a != '-f' and a != '-i' and a != '-o'):
                    raise SystemExit(
                        "Unknown option: " + a)

        # Obtain mode
        mode = self.get_mode(args)
        options.append(mode)

        # Get bypass or obfuscation type
        if (mode == self.modes.bypass):
            bypass_type = self.get_bypass(args)
            options.append(bypass_type)
            obfuscation = self.get_obfuscation_for_bypass(args)
            options.append(obfuscation)
            # Input file
            options.append(None)
        elif (mode == self.modes.obfuscate):
            options.append(None)  # Bypass type -> none
            obfuscation_type = self.get_obfuscation(args)
            options.append(obfuscation_type)
            options.append(self.get_input_file(args))
        else:
            SystemExit("Not supported mode")

        options.append(self.get_output_file(args))

        # Mode - Bypass type - Obfuscation type - Input file to obfuscate - Output file to generate
        return options
