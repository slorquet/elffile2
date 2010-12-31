#!/usr/bin/env python -3
# -*- coding: utf-8 -*-
#
# Copyright 2010 K. Richard Pixley.
# See LICENSE for details.
#
# Time-stamp: <30-Dec-2010 19:06:06 PST by rich@noir.com>

"""
Elffile is a library which reads and writes `ELF format object files
<http://en.wikipedia.org/wiki/Executable_and_Linkable_Format>`_.
Elffile is pure `python <http://python.org>`_ so installation is easy.

.. todo:: loosely like tarfile

.. todo:: need a "copy" method

.. todo:: need an equality method

.. todo:: need a reverse write method, (for testing)

"""

from __future__ import unicode_literals, print_function

__docformat__ = 'restructuredtext en'

#__all__ = []

import mmap
import struct

import coding

class ElfClass(coding.Coding):
    """
    Encodes the word size of the elf file as from the elf file header.
    This is a subclass of :py:class:`coding.Coding`.
    """
    bycode = byname = {}

ElfClass('ELFCLASSNONE', 0, 'Invalid class')
ElfClass('ELFCLASS32', 1, '32-bit objects')
ElfClass('ELFCLASS64', 2, '64-bit objects')

class ElfData(coding.Coding):
    """

    Encodes the byte-wise endianness of the elf file as from the elf
    file header.  This is a subclass of :py:class:`coding.Coding`.

    """
    bycode = byname = {}

ElfData('ELFDATANONE', 0, 'Invalid data encoding')
ElfData('ELFDATA2LSB', 1, 'least significant byte first')
ElfData('ELFDATA2MSB', 2, 'most significant byte first')

class EV(coding.Coding):
    """
    Encodes the elf file format version of this elf file as from the
    elf file header.  This is a subclass of :py:class:`coding.Coding`.
    """
    bycode = byname = {}

EV('EV_NONE', 0, 'Invalid version')
EV('EV_CURRENT', 1, 'Current version')

class ElfOsabi(coding.Coding):
    """
    Encodes OSABI values which roughly represent operating systems as
    from the elf file header.  This is a subclass of
    :py:class:`coding.Coding`.
    """
    bycode = byname = {}

ElfOsabi('ELFOSABI_NONE', 0, 'No extensions or unspecified')
ElfOsabi('ELFOSABI_HPUX', 1, 'Hewlett-Packard HP-UX')
ElfOsabi('ELFOSABI_NETBSD', 2, 'NetBSD')
ElfOsabi('ELFOSABI_LINUX', 3, 'Linux')
ElfOsabi('ELFOSABI_SOLARIS', 6, 'Sun Solaris')
ElfOsabi('ELFOSABI_AIX', 7, 'AIX')
ElfOsabi('ELFOSABI_IRIX', 8, 'IRIX')
ElfOsabi('ELFOSABI_FREEBSD', 9, 'FreeBSD')
ElfOsabi('ELFOSABI_TRU64', 10, 'Compaq TRU64 UNIX')
ElfOsabi('ELFOSABI_MODESTO', 11, 'Novell Modesto')
ElfOsabi('ELFOSABI_OPENBSD', 12, 'Open BSD')
ElfOsabi('ELFOSABI_OPENVMS', 13, 'Open VMS')
ElfOsabi('ELFOSABI_NSK', 14, 'Hewlett-Packard Non-Stop Kernel')
ElfOsabi('ELFOSABI_AROS', 15, 'Amiga Research OS')
ElfOsabi('ELFOSABI_FENIXOS', 16, 'The FenixOS highly scalable multi-core OS')

class ET(coding.Coding):
    """
    Encodes the type of this elf file, (relocatable, executable,
    shared library, etc.)
    """
    bycode = byname = {}

ET('ET_NONE', 0, 'No file type')
ET('ET_REL', 1, 'Relocatable file')
ET('ET_EXEC', 2, 'Executable file')
ET('ET_DYN', 3, 'Shared object file')
ET('ET_CORE', 4, 'Core file')
ET('ET_LOOS', 0xfe00, 'Operating system-specific')
ET('ET_HIOS', 0xfeff, 'Operating system-specific')
ET('ET_LOPROC', 0xff00, 'Processor-specific')
ET('ET_HIPROC', 0xffff, 'Processor-specific')

class EM(coding.Coding):
    """
    Encodes the processor type represented in this elf file.
    """
    bycode = byname = {}
    overload_codes = True

EM('EM_NONE', 0, 'No machine')
EM('EM_M32', 1, 'AT&T WE 32100')
EM('EM_SPARC', 2, 'SPARC')
EM('EM_386', 3, 'Intel 80386')
EM('EM_68K', 4, 'Motorola 68000')
EM('EM_88K', 5, 'Motorola 88000')
EM('EM_486', 6, 'Reserved for future use (was EM_486)')
EM('EM_860', 7, 'Intel 80860')
EM('EM_MIPS', 8, 'MIPS I Architecture')
EM('EM_S370', 9, 'IBM System/370 Processor')
EM('EM_MIPS_RS3_LE', 10, 'MIPS RS3000 Little-endian')
# 11 - 14 reserved
EM('EM_PARISC', 15, 'Hewlett-Packard PA-RISC')
# 16 reserved
EM('EM_VPP500', 17, 'Fujitsu VPP500')
EM('EM_SPARC32PLUS', 18, 'Enhanced instruction set SPARC')
EM('EM_960', 19, 'Intel 80960')
EM('EM_PPC', 20, 'PowerPC')
EM('EM_PPC64', 21, '64-bit PowerPC')
EM('EM_S390', 22, 'IBM System/390 Processor')
EM('EM_SPU', 23, 'IBM SPU/SPC')
# 24 - 35 reserved
EM('EM_V800', 36, 'NEC V800')
EM('EM_FR20', 37, 'Fujitsu FR20')
EM('EM_RH32', 38, 'TRW RH-32')
EM('EM_RCE', 39, 'Motorola RCE')
EM('EM_ARM', 40, 'Advanced RISC Machines ARM')
EM('EM_ALPHA', 41, 'Digital Alpha')
EM('EM_SH', 42, 'Hitachi SH')
EM('EM_SPARCV9', 43, 'SPARC Version 9')
EM('EM_TRICORE', 44, 'Siemens TriCore embedded processor')
EM('EM_ARC', 45, 'Argonaut RISC Core, Argonaut Technologies Inc.')
EM('EM_H8_300', 46, 'Hitachi H8/300')
EM('EM_H8_300H', 47, 'Hitachi H8/300H')
EM('EM_H8S', 48, 'Hitachi H8S')
EM('EM_H8_500', 49, 'Hitachi H8/500')
EM('EM_IA_64', 50, 'Intel IA-64 processor architecture')
EM('EM_MIPS_X', 51, 'Stanford MIPS-X')
EM('EM_COLDFIRE', 52, 'Motorola ColdFire')
EM('EM_68HC12', 53, 'Motorola M68HC12')
EM('EM_MMA', 54, 'Fujitsu MMA Multimedia Accelerator')
EM('EM_PCP', 55, 'Siemens PCP')
EM('EM_NCPU', 56, 'Sony nCPU embedded RISC processor')
EM('EM_NDR1', 57, 'Denso NDR1 microprocessor')
EM('EM_STARCORE', 58, 'Motorola Star*Core processor')
EM('EM_ME16', 59, 'Toyota ME16 processor')
EM('EM_ST100', 60, 'STMicroelectronics ST100 processor')
EM('EM_TINYJ', 61, 'Advanced Logic Corp. TinyJ embedded processor family')
EM('EM_X86_64', 62, 'AMD x86-64 architecture')
EM('EM_PDSP', 63, 'Sony DSP Processor')
EM('EM_PDP10', 64, 'Digital Equipment Corp. PDP-10')
EM('EM_PDP11', 65, 'Digital Equipment Corp. PDP-11')
EM('EM_FX66', 66, 'Siemens FX66 microcontroller')
EM('EM_ST9PLUS', 67, 'STMicroelectronics ST9+ 8/16 bit microcontroller')
EM('EM_ST7', 68, 'STMicroelectronics ST7 8-bit microcontroller')
EM('EM_68HC16', 69, 'Motorola MC68HC16 Microcontroller')
EM('EM_68HC11', 70, 'Motorola MC68HC11 Microcontroller')
EM('EM_68HC08', 71, 'Motorola MC68HC08 Microcontroller')
EM('EM_68HC05', 72, 'Motorola MC68HC05 Microcontroller')
EM('EM_SVX', 73, 'Silicon Graphics SVx')
EM('EM_ST19', 74, 'STMicroelectronics ST19 8-bit microcontroller')
EM('EM_VAX', 75, 'Digital VAX')
EM('EM_CRIS', 76, 'Axis Communications 32-bit embedded processor')
EM('EM_JAVELIN', 77, 'Infineon Technologies 32-bit embedded processor')
EM('EM_FIREPATH', 78, 'Element 14 64-bit DSP Processor')
EM('EM_ZSP', 79, 'LSI Logic 16-bit DSP Processor')
EM('EM_MMIX', 80, 'Donald Knuth\'s educational 64-bit processor')
EM('EM_HUANY', 81, 'Harvard University machine-independent object files')
EM('EM_PRISM', 82, 'SiTera Prism')
EM('EM_AVR', 83, 'Atmel AVR 8-bit microcontroller')
EM('EM_FR30', 84, 'Fujitsu FR30')
EM('EM_D10V', 85, 'Mitsubishi D10V')
EM('EM_D30V', 86, 'Mitsubishi D30V')
EM('EM_V850', 87, 'NEC v850')
EM('EM_M32R', 88, 'Mitsubishi M32R')
EM('EM_MN10300', 89, 'Matsushita MN10300')
EM('EM_MN10200', 90, 'Matsushita MN10200')
EM('EM_PJ', 91, 'picoJava')
EM('EM_OPENRISC', 92, 'OpenRISC 32-bit embedded processor')
EM('EM_ARC_COMPACT', 93, 'ARC International ARCompact processor (old spelling/synonym: EM_ARC_A5)')
EM('EM_XTENSA', 94, 'Tensilica Xtensa Architecture')
EM('EM_VIDEOCORE', 95, 'Alphamosaic VideoCore processor')
EM('EM_TMM_GPP', 96, 'Thompson Multimedia General Purpose Processor')
EM('EM_NS32K', 97, 'National Semiconductor 32000 series')
EM('EM_TPC', 98, 'Tenor Network TPC processor')
EM('EM_SNP1K', 99, 'Trebia SNP 1000 processor')
EM('EM_ST200', 100, 'STMicroelectronics (www.st.com) ST200 microcontroller')
EM('EM_IP2K', 101, 'Ubicom IP2xxx microcontroller family')
EM('EM_MAX', 102, 'MAX Processor')
EM('EM_CR', 103, 'National Semiconductor CompactRISC microprocessor')
EM('EM_F2MC16', 104, 'Fujitsu F2MC16')
EM('EM_MSP430', 105, 'Texas Instruments embedded microcontroller msp430')
EM('EM_BLACKFIN', 106, 'Analog Devices Blackfin (DSP) processor')
EM('EM_SE_C33', 107, 'S1C33 Family of Seiko Epson processors')
EM('EM_SEP', 108, 'Sharp embedded microprocessor')
EM('EM_ARCA', 109, 'Arca RISC Microprocessor')
EM('EM_UNICORE', 110, 'Microprocessor series from PKU-Unity Ltd. and MPRC of Peking University')
EM('EM_EXCESS', 111, 'eXcess: 16/32/64-bit configurable embedded CPU')
EM('EM_DXP', 112, 'Icera Semiconductor Inc. Deep Execution Processor')
EM('EM_ALTERA_NIOS2', 113, 'Altera Nios II soft-core processor')
EM('EM_CRX', 114, 'National Semiconductor CompactRISC CRX microprocessor')
EM('EM_XGATE', 115, 'Motorola XGATE embedded processor')
EM('EM_C166', 116, 'Infineon C16x/XC16x processor')
EM('EM_M16C', 117, 'Renesas M16C series microprocessors')
EM('EM_DSPIC30F', 118, 'Microchip Technology dsPIC30F Digital Signal Controller')
EM('EM_CE', 119, 'Freescale Communication Engine RISC core')
EM('EM_M32C', 120, 'Renesas M32C series microprocessors')
# 121 - 130 reserved
EM('EM_TSK3000', 131, 'Altium TSK3000 core')
EM('EM_RS08', 132, 'Freescale RS08 embedded processor')
# 133 reserved
EM('EM_ECOG2', 134, 'Cyan Technology eCOG2 microprocessor')
EM('EM_SCORE7', 135, 'Sunplus S+core7 RISC processor')
EM('EM_DSP24', 136, 'New Japan Radio (NJR) 24-bit DSP Processor')
EM('EM_VIDEOCORE3', 137, 'Broadcom VideoCore III processor')
EM('EM_LATTICEMICO32', 138, 'RISC processor for Lattice FPGA architecture')
EM('EM_SE_C17', 139, 'Seiko Epson C17 family')
EM('EM_TI_C6000', 140, 'The Texas Instruments TMS320C6000 DSP family')
EM('EM_TI_C2000', 141, 'The Texas Instruments TMS320C2000 DSP family')
EM('EM_TI_C5500', 142, 'The Texas Instruments TMS320C55x DSP family')
# 143 - 159 reserved
EM('EM_MMDSP_PLUS', 160, 'STMicroelectronics 64bit VLIW Data Signal Processor')
EM('EM_CYPRESS_M8C', 161, 'Cypress M8C microprocessor')
EM('EM_R32C', 162, 'Renesas R32C series microprocessors')
EM('EM_TRIMEDIA', 163, 'NXP Semiconductors TriMedia architecture family')
EM('EM_QDSP6', 164, 'QUALCOMM DSP6 Processor')
EM('EM_8051', 165, 'Intel 8051 and variants')
EM('EM_STXP7X', 166, 'STMicroelectronics STxP7x family of configurable and extensible RISC processors')
EM('EM_NDS32', 167, 'Andes Technology compact code size embedded RISC processor family')
EM('EM_ECOG1', 168, 'Cyan Technology eCOG1X family')
EM('EM_ECOG1X', 168, 'Cyan Technology eCOG1X family')
EM('EM_MAXQ30', 169, 'Dallas Semiconductor MAXQ30 Core Micro-controllers')
EM('EM_XIMO16', 170, 'New Japan Radio (NJR) 16-bit DSP Processor')
EM('EM_MANIK', 171, 'M2000 Reconfigurable RISC Microprocessor')
EM('EM_CRAYNV2', 172, 'Cray Inc. NV2 vector architecture')
EM('EM_RX', 173, 'Renesas RX family')
EM('EM_METAG', 174, 'Imagination Technologies META processor architecture')
EM('EM_MCST_ELBRUS', 175, 'MCST Elbrus general purpose hardware architecture')
EM('EM_ECOG16', 176, 'Cyan Technology eCOG16 family')
EM('EM_CR16', 177, 'National Semiconductor CompactRISC CR16 16-bit microprocessor')
EM('EM_ETPU', 178, 'Freescale Extended Time Processing Unit')
EM('EM_SLE9X', 179, 'Infineon Technologies SLE9X core')
# 180-182 Reserved for future Intel use
# 183-184 Reserved for future ARM use
EM('EM_AVR32', 185, 'Atmel Corporation 32-bit microprocessor family')
EM('EM_STM8', 186, 'STMicroeletronics STM8 8-bit microcontroller')
EM('EM_TILE64', 187, 'Tilera TILE64 multicore architecture family')
EM('EM_TILEPRO', 188, 'Tilera TILEPro multicore architecture family')
EM('EM_MICROBLAZE', 189, 'Xilinx MicroBlaze 32-bit RISC soft processor core')
EM('EM_CUDA', 190, 'NVIDIA CUDA architecture')
EM('EM_TILEGX', 191, 'Tilera TILE-Gx multicore architecture family')
EM('EM_CLOUDSHIELD', 192, 'CloudShield architecture family')
EM('EM_COREA_1ST', 193, 'KIPO-KAIST Core-A 1st generation processor family')
EM('EM_COREA_2ND', 194, 'KIPO-KAIST Core-A 2nd generation processor family')

class SHN(coding.Coding):
    bycode = byname = {}
    overload_codes = True

SHN('SHN_UNDEF', 0, 'marks an undefined, missing, irrelevant, or otherwise meaningless section reference')
SHN('SHN_LORESERVE', 0xff00, 'specifies the lower bound of the range of reserved indexes')
SHN('SHN_LOPROC', 0xff00, '')
SHN('SHN_HIPROC', 0xff1f, '')
SHN('SHN_LOOS', 0xff20, '')
SHN('SHN_HIOS', 0xff3f, '')
SHN('SHN_ABS', 0xfff1, 'specifies absolute values for the corresponding reference')
SHN('SHN_COMMON', 0xfff2, 'symbols defined relative to this section are common symbols, such as FORTRAN COMMON or unallocated C external variables.')
SHN('SHN_XINDEX', 0xffff, 'This value is an escape value. It indicates that the actual section header index is too large to fit in the containing field and is to be found in another location (specific to the structure where it appears). ')
SHN('SHN_HIRESERVE', 0xffff, 'specifies the upper bound of the range of reserved indexes')

class SHT(coding.Coding):
    bycode = byname = {}

SHT('SHT_NULL', 0, 'marks the section header as inactive; it does not have an associated section. Other members of the section header have undefined values.')
SHT('SHT_PROGBITS', 1, 'The section holds information defined by the program, whose format and meaning are determined solely by the program.')
SHT('SHT_SYMTAB', 2, 'provides symbols for link editing, though it may also be used for dynamic linking.')
SHT('SHT_STRTAB', 3, 'section holds a string table. An object file may have multiple string table sections.')
SHT('SHT_RELA', 4, 'section holds relocation entries with explicit addends, such as type Elf32_Rela for the 32-bit class of object files or type Elf64_Rela for the 64-bit class of object files.')
SHT('SHT_HASH', 5, 'section holds a symbol hash table')
SHT('SHT_DYNAMIC', 6, 'section holds information for dynamic linking')
SHT('SHT_NOTE', 7, 'section holds information that marks the file in some way')
SHT('SHT_NOBITS', 8, 'A section of this type occupies no space in the file but otherwise resembles SHT_PROGBITS')
SHT('SHT_REL', 9, 'section holds relocation entries without explicit addends')
SHT('SHT_SHLIB', 10, 'section type is reserved but has unspecified semantics')
SHT('SHT_DYNSYM', 11, 'holds a minimal set of dynamic linking symbols,')
SHT('SHT_INIT_ARRAY', 14, 'section contains an array of pointers to initialization functions')
SHT('SHT_FINI_ARRAY', 15, 'section contains an array of pointers to termination functions')
SHT('SHT_PREINIT_ARRAY', 16, 'section contains an array of pointers to functions that are invoked before all other initialization functions')
SHT('SHT_GROUP', 17, 'section defines a section group')
SHT('SHT_SYMTAB_SHNDX', 18, 'section is associated with a section of type SHT_SYMTAB and is required if any of the section header indexes referenced by that symbol table contain the escape value SHN_XINDEX')
SHT('SHT_LOOS', 0x60000000, '')
SHT('SHT_HIOS', 0x6fffffff, '')
SHT('SHT_LOPROC', 0x70000000, '')
SHT('SHT_HIPROC', 0x7fffffff, '')
SHT('SHT_LOUSER', 0x80000000, '')
SHT('SHT_HIUSER', 0xffffffff, '')

class SHF(coding.Coding):
    bycode = byname = {}

SHF('SHF_WRITE', 0x1, 'section contains data that should be writable during process execution')
SHF('SHF_ALLOC', 0x2, 'section occupies memory during process execution')
SHF('SHF_EXECINSTR', 0x4, 'section contains executable machine instructions')
SHF('SHF_MERGE', 0x10, 'data in the section may be merged to eliminate duplication')
SHF('SHF_STRINGS', 0x20, 'data elements in the section consist of null-terminated character strings')
SHF('SHF_INFO_LINK', 0x40, 'The sh_info field of this section header holds a section header table index')
SHF('SHF_LINK_ORDER', 0x80, 'adds special ordering requirements for link editors')
SHF('SHF_OS_NONCONFORMING', 0x100, 'section requires special OS-specific processing')
SHF('SHF_GROUP', 0x200, 'section is a member of a section group')
SHF('SHF_TLS', 0x400, 'section holds Thread-Local Storage')
SHF('SHF_MASKOS', 0x0ff00000, 'All bits included in this mask are reserved for operating system-specific semantics')
SHF('SHF_MASKPROC', 0xf0000000, 'All bits included in this mask are reserved for processor-specific semantics')

class GRP(coding.Coding):
    bycode = byname = {}

GRP('GRP_COMDAT', 0x1, 'This is a COMDAT group')
GRP('GRP_MASKOS', 0x0ff00000, 'All bits included in this mask are reserved for operating system-specific semantics')
GRP('GRP_MASKPROC', 0xf0000000, 'All bits included in this mask are reserved for processor-specific semantics')

class PT(coding.Coding):
    bycode = byname = {}

PT('PT_NULL', 0, 'array element is unused')
PT('PT_LOAD', 1, 'array element specifies a loadable segment')
PT('PT_DYNAMIC', 2, 'array element specifies dynamic linking information')
PT('PT_INTERP', 3, 'array element specifies the location and size of a null-terminated path name to invoke as an interpreter')
PT('PT_NOTE', 4, 'array element specifies the location and size of auxiliary information')
PT('PT_SHLIB', 5, 'segment type is reserved')
PT('PT_PHDR', 6, 'specifies the location and size of the program header table itself')
PT('PT_TLS', 7, 'array element specifies the Thread-Local Storage template')
PT('PT_LOOS', 0x60000000, '')
PT('PT_HIOS', 0x6fffffff, '')
PT('PT_LOPROC', 0x70000000, '')
PT('PT_HIPROC', 0x7fffffff, '')

class PF(coding.Coding):
    bycode = byname = {}

PF('PF_X', 0x1, 'Execute')
PF('PF_W', 0x2, 'Write')
PF('PF_R', 0x4, 'Read')
PF('PF_MASKOS', 0x0ff00000, 'Unspecified')
PF('PF_MASKPROC', 0xf0000000, 'Unspecified')

EI_NIDENT = 16

class ElfFileIdent(object):
    """
    This class corresponds to the first, byte-endian-independent,
    values in an elf file.  These tell us about the encodings for the
    rest of the file.  This is the *e_ident* field of the elf file
    header in the format specifications.
    """

    coder = struct.Struct(b'=4sBBBBBxxxxxxx')
    """
    The (de)coder for this struct involves six fields:
    * '\x1fELF', (Elf file magic number)
    * ElfClass (32 vs 64-bit)
    * ElfData (endianness)
    * EV (file version)
    * ElfOsabi (operating system)
    * abiversion
    """

    # size is EI_IDENT
    assert (coder.size == EI_NIDENT), 'coder.size = {0}({0}), EI_NIDENT = {0}({0})'.format(coder.size, type(coder.size),
                                                                                           EI_NIDENT, type(EI_NIDENT))

    def __init__(self):
        self.magic = None
        self.elfClass = None
        self.elfData = None
        self.fileVersion = None
        self.osabi = None
        self.abiversion = None

    def unpack(self, block, offset=0):
        (self.magic, self.elfClass, self.elfData, self.fileVersion, self.osabi,
         self.abiversion) = identCoder.unpack_from(block, offset)

    def pack(self, block, offset=0):
        identCoder.pack_into(block, offset, self.magic, self.elfClass, self.elfData, self.fileVersion, self.osabi, self.abiversion)

class ElfFileHeader(object):
    coder = None

    def __init__(self):
        self.type = None
        self.machine = None
        self.version = None
        self.entry = None
        self.phoff = None
        self.shoff = None
        self.flags = None
        self.ehsize = None
        self.phentsize = None
        self.phnum = None
        self.shentsize = None
        self.shnum = None
        self.shstrndx = None

    def unpack(self, block, offset=0):
        (self.type, self.machine, self.version, self.entry,
         self.phoff, self.shoff, self.flags, self.ehsize,
         self.phentsize, self.phnum, self,shentsize, self.shnm,
         self.shstrndx) = self.coder.unpack_from(buffer, offset)

    def pack(self, block, offset=0):
        self.coder.pack_into(block, offset,
                             self.type, self.machine, self.version, self.entry,
                             self.phoff, self.shoff, self.flags, self.ehsize,
                             self.phentsize, self.phnum, self,shentsize, self.shnm,
                             self.shstrndx)

# 13 items
class ElfFileHeader32b(ElfFileHeader):
    coder = struct.Struct(b'>HHIIIIIHHHHHH')

class ElfFileHeader32l(ElfFileHeader):
    coder = struct.Struct(b'<HHIIIIIHHHHHH')

class ElfFileHeader64b(ElfFileHeader):
    coder = struct.Struct(b'>HHIQQQIHHHHHH')

class ElfFileHeader64l(ElfFileHeader):
    coder = struct.Struct(b'<HHIQQQIHHHHHH')


class ElfSectionHeader(object):
    coder = None

    def __init__(self):
        self.name = None
        self.type = None
        self.flags = None
        self.addr = None
        self.offset = None
        self.size = None
        self.link = None
        self.info = None
        self.addralign = None
        self.entsize = None

    def unpack(self, block, offset=0):
        (self.name, self.type, self.flags, self.addr,
         self.offset, self.size, self.link, self.info,
         self.addralign, self.entsize) = self.coder.unpack_from(block, offset)

    def pack(self, block, offset=0):
        self.coder.pack_into(block, offset,
                             self.name, self.type, self.flags, self.addr,
                             self.offset, self.size, self.link, self.info,
                             self.addralign, self.entsize)

# 10 items
class ElfSectionHeader32b(ElfSectionHeader):
    coder = struct.Struct(b'>IIIIIIIIII')

class ElfSectionHeader32l(ElfSectionHeader):
    coder = struct.Struct(b'<IIIIIIIIII')

class ElfSectionHeader64b(ElfSectionHeader):
    coder = struct.Struct(b'>IIQQQQIIQQ')

class ElfSectionHeader64l(ElfSectionHeader):
    coder = struct.Struct(b'<IIQQQQIIQQ')


class ElfProgramHeader(object):
    coder = None

    def __init__(self):
        self.type = None
        self.offset = None
        self.vaddr = None
        self.paddr = None
        self.filesz = None
        self.memsz = None
        self.flags = None
        self.align = None

    def unpack(self, block, offset=0):
        raise NotImplentedError

    def pack(self, block, offset=0):
        raise NotImplementedError

# 32 vs 64 have differing element orders.
class ElfProgramHeader32(ElfProgramHeader):
    def unpack(self, block, offset=0):
        (self.type, self.offset, self.vaddr, self.paddr,
         self.filesz, self.memsz, self.flags, self.align) = self.coder.unpack_from(block, offset)

    def pack(self, block, offset=0):
        self.coder.pack_into(block, offset,
                             self.type, self.offset, self.vaddr, self.paddr,
                             self.filesz, self.memsz, self.flags, self.align)

class ElfProgramHeader64(ElfProgramHeader):
    def unpack(self, block, offset=0):
        (self.type, self.flags, self.offset, self.vaddr,
         self.paddr, self.filesz, self.memsz, self.align) = self.coder.unpack_from(block, offset)

    def pack(self, block, offset=0):
        self.coder.pack_into(block, offset,
                             self.type, self.flags, self.offset, self.vaddr,
                             self.paddr, self.filesz, self.memsz, self.align)

# 8 items
class ElfProgramHeader32b(ElfProgramHeader32):
    coder = struct.Struct(b'>IIIIIIII')

class ElfProgramHeader32l(ElfProgramHeader32):
    coder = struct.Struct(b'<IIIIIIII')

class ElfProgramHeader64b(ElfProgramHeader64):
    coder = struct.Struct(b'>IIQQQQQQ')

class ElfProgramHeader64l(ElfProgramHeader64):
    coder = struct.Struct(b'<IIQQQQQQ')

def open(name=None, fileobj=None, map=None, block=None, mode='r', use_map=True):
    """
    :param string name: a file name
    :param file fileobj: a file object, (if given, this overrides *name*)
    :param mmap.mmap map: a :py:class:`mmap.mmap`, (if given, this overrides *fileobj*)
    :param string block: file info in a block of memory, (if given, this overrides *map*)
    :param string mode: must be 'r' for read
    :param bool use_mmap: if True, then use map in place.  If False, the copy the file contents from map to block.

    The open function takes some form of file identifier, reads the
    first few bytes, (:py:class:`ElfFileIdent`), to determine whether
    the file is 32-bit or 64-bit encoded and whether it is big or
    little endian.  Based on this information it initializes an
    instance of the appropriate class, :py:class:`ElfFile32b`,
    :py:class:`ElfFile32l`, :py:class:`ElfFile64b`,
    :py:class:`ElfFile64l`, respectively, each of which are subclasses
    of the :py:class:`ElfFile` class.

    The file to be opened can be specified in any of four different forms:

    #. a file name
    #. :py:class:`file` object
    #. :py:mod:`mmap.mmap`, or
    #. a block of memory

    If an :py:class:`mmap.mmap` object is specified then any file
    object or file name specified are ignored.  Instead, those values
    are initialized from the :py:class:`mmap.mmap` object.

    If no :py:class:`mmap.mmap` object is specified and a file object
    is specified then any file name specified is ignored.  Instead,
    that value is initialized from the :py:class:`file` object and mmap'd.

    IF no :py:class:`mmap.mmap` object and no :py:class:`file` object
    are specified then the file name will be opened and mapped.

    If use_mmap is :py:const:`True`, then we will use the mmap object
    as our memory block.  This uses a file descriptor but is faster as
    it eliminates an extra memory-to-memory copy.  If *use_mmap* is
    :py:const:`False`, the mmap content is copied into process memory
    and the file descriptor is closed.

    In all read cases except when *use_mmap* is :py:const:`True` the
    file is copied into memory and the descriptor closed before this
    function returns.
    
    .. todo:: add write support.
    """

    assert use_mmap
    assert mode == 'r'

    if block:
        fileIdent = ElfFileIdent().unpack(block)
        return ElfFile.encodedClass(fileIdent)(name, fileobj, map, block, mode, fileIdent)

    if map:
        if use_map:
            block = map
        else:
            block = map[:]
            map.close()

    elif fileobj:
        map = mmap.mmap(fileobj.fd.fileno(), 0, mmap.MAP_SHARED, mmap.PROT_READ)

    elif name:
        fileobj = open(name, 'rb')

    else:
        assert False
        
    return __name__.open(name, fileobj, map, block, mode, use_map)

### MARKER

class ElfFile(object):
    @staticmethod
    def encodedClass(ident):
        classcode = ident.elfClass.code
        if classcode in encodingDict:
            elfclass = encodingDict[classcode]
        else:
            raise NO_CLASS

        endiancode = ident.elfData.code
        if endiancode in elfclass:
            return elfclass[endiancode]
        else:
            raise NO_ENCODING

    fileHeaderClass = None

    def __init__(self, name, fileobj, map, block, mode, fileIdent=None):
        self.name = name
        self.fileobj = fileobj
        self.map = map
        self.block = block
        self.mode = mode

        self.fileIdent = fileIdent
        self.fileHeader = None
        self.sectionHeaders = None
        self.programHeaders = None

    def unpack(self):
        self.fileHeader = fileHeaderClass().unpack(self.block, EI_NIDENT)

        # section headers
        if self.fileHeader.shoff == 0:
            self.sectionHeaders = []
        else:
            sectionCount = self.fileHeader.shnum

            self.sectionHeaders.append(sectionHeaderClass().unpack(self.block, self.fileHeader.shoff))

            if sectionCount == 0:
                sectionCount = self.sectionHeaders[0].size
                
            for i in xrange(1, sectionCount):
                self.sectionHeaders.append(sectionHeaderClass().unpack(self.block,
                                                                       self.fileHeader.shoff + (i * self.fileHeader.shentsize)))

        # program headers
        if self.fileHeader.phoff == 0:
            self.programHeaders == []
        else:
            for i in xrange(self.fileHeader.phnum):
                self.programHeaders.append(programHeaderClass().unpack(self.block,
                                                                       self.fileHeader.phoff + (i * self.fileHeader.phentsize)))

class ElfFile32b(ElfFile):
    fileHeaderClass = ElfFileHeader32b
    sectionHeaderClass = ElfSectionHeader32b
    programHeaderClass = ElfSectionHeader32b

class ElfFile32l(ElfFile):
    fileHeaderClass = ElfFileHeader32l
    sectionHeaderClass = ElfSectionHeader32l
    programHeaderClass = ElfSectionHeader32l

class ElfFile64b(ElfFile):
    fileHeaderClass = ElfFileHeader64b
    sectionHeaderClass = ElfSectionHeader64b
    programHeaderClass = ElfSectionHeader64b

class ElfFile64l(ElfFile):
    fileHeaderClass = ElfFileHeader64l
    sectionHeaderClass = ElfSectionHeader64l
    programHeaderClass = ElfSectionHeader64l

encodingDict = {
    1: {
        1: ElfFile32l,
        2: ElfFile32b,
        },
    2: {
        1: ElfFile64l,
        2: ElfFile32b,
        },
    }

