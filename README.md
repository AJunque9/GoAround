# GoAround

A tool that allows the generation of AMSI bypasses and the automatic obfuscation of PowerShell scripts using three different obfuscation methods.

- [GoAround](#goaround)
  - [Installation](#installation)
  - [User's guide](#users-guide)
    - [How to use it](#how-to-use-it)
    - [Operation modes](#operation-modes)
    - [Bypass types](#bypass-types)
    - [Obfuscation methods](#obfuscation-methods)
    - [Examples](#examples)

## Installation

You only need to download the code from Github and run the tool from the Windows command line or PowerShell console.

## User's guide

With GoAround you are able to do two different things:
- Generate PowerShell scripts with the necessary code to make an AMSI bypass. The generated code can be automatically obfuscated.
- Automatic obfuscation of PowerShell scripts, using different techniques.
  
The user can chose between two different AMSI bypasses and three different obfuscation techniques.

### How to use it

To be able to use this tool it is necessary to have Python installed in the machine. The following paths should be added to the PATH environment variable:

- C:\Users\{Usuario}\AppData\Local\Programs\Python\Python39
- C:\Users\{Usuario}\AppData\Local\Programs\Python\Python39\Scripts

Once this is done, you would be able to run the tool from the command line, in either of these two ways:
1. From the tool's folder: python goaround.py {options}
2. From any other folder: python {complete path to GoAround folder} {options}

The command structure is the following:

` python goaround.py -m [mode] (-t [type]) (-f [type_obfuscation]) (-i [input_file]) (-o [output_file]) `

Where all the options between brackets are optional. The values for these options are:

- **-m or --mode**: the only mandatory option. It indicates the operation mode in which the tool must run. Go to section [Operation modes](#operation-modes) for more info.
- **-t or --type**: it indicates the type of bypass that is going to be used when the mode is *bypass* or the type of obfuscation method when the mode is *obfuscate*. See section [Bypass types](#bypass-types) to know the different bypass types and section [Obfuscation methods](#obfuscation-methods) to know the available obfuscation methods.
- **-f or --obfuscation**: when the operation mode is *bypass*, this option is used to select the obfuscation type for the bypass. This option is not available in the *obfuscate* mode, use "-t" or "--type" instead. To know the different obfuscation methods pleasee read section [Obfuscation methods](#obfuscation-methods) .
- **-i or --input**: only used in *obfuscate* mode. It allows the user to select the file to obfuscate.
- **-o or --output**: this option allows the user to select the name of the generated script. The name must end in ".ps1". By default, the output file name will be "output.ps1".
  
Furthermore, thw following options are also supported and must be run alone (without any other option):
- **-h or --help**: shows the user the tool's usage guide.
- **-v or --version**: shows the tool's version number.

### Operation modes

There are two operation modes, *bypass* and *obfuscate*, and they are selected with the option "-m" or "--mode":

- **bypass**: to indicate that the tool must run in bypass mode. In this case, a PS1 file will be generated with the code of the AMSI bypass.
- **obfuscate**: to indicate that the tool must run in obfuscation mode. In this case, the tool will obfuscate the file provided by the user with the option "-i" or "--input" (mandatory in this operation mode). A PS1 file will be generated with the obfuscated code. The obfuscation is only functional for PowerShell scripts.

### Bypass types

In *bypass* mode (-m bypass), the bypass type can be indicated with the option "-t" or "--type".

At this moment, these are the supported bypass types:
- **reflection**: Matt Graeber's reflection bypass.
- **scan_buffer_laine**: Paul Laîné's AmsiScanBuffer patch bypass.

If no type is specified, the reflection one will be used by default.

### Obfuscation methods

At this moment, the tool supports three different PowerShell obfuscation techniques. 

To select the type of obfuscation in *bypass* mode, the option "-f" or "--obfuscation" is used (if none is specified, the bypass won't be obfuscated). To select the type of obfuscation in *obfuscate* mode, the option "-t" or "--type" is used (if none is specified, the concatenation technique will be used).

The name of the obfuscation types are the following:

- **mayus**: it will change the PowerShell code using randomcase technique. This will not affect the strings present in the code. This method will change the hash of the file.
- **concatenation**: method used by default in *obfuscate* mode. It will change the strings present in the code for concatenation of smaller strings. The strings will be splitted randomly, so each time the code will be different for the same input file.
- **insertion**: it will change the strings present in the code for combinations of string and variable. For example, if the code has the stringa “amsiutils”, it could be replaced by “am$var_tfm0”, where *var_tfm0 = “siutils”*. The strings are splitted randomly, so each time the code will be different for the same input file. The vairables will hava a name of the format “var_tfm{número}”, so, if the original code has variables with these names, they should be changed before the obfuscation phase. 

### Examples

Here you can see some usage examples:

**Show help menu**

`python main.py -h`

`python main.py --help`

**Show tool's version number**

`python main.py -v`

`python main.py --version`

**Generate reflection bypass obfuscated using variables insertion**

`python main.py -m bypass -t reflection -f insertion`

**Generate Paul Laîné's bypass changing the output file name**

`python main.py -m bypass -t scan_buffer_laine -o "output_name.ps1"`

**Obfuscate file using strings concatenation method**

`python main.py -m obfuscate -t concatenation -i "input_required.ps1"`
