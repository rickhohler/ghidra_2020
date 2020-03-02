#!/usr/bin/env python2
# vim: tabstop=4:softtabstop=4:shiftwidth=4:expandtab:

import os
import requests
import sys

docs = {
    '68000': {
        'M68000PRM.pdf': 'https://www.nxp.com/files-static/archives/doc/ref_manual/M68000PRM.pdf',
    },

    '8051': {
        '8xc251sx_um.pdf': 'https://www.keil.com/dd/docs/datashts/intel/8xc251sx_um.pdf',
    },

    'ARM': {
        'Armv7AR_errata.pdf': 'https://www.cs.utexas.edu/~simon/378/resources/ARMv7-AR_TRM.pdf',
    },

    'Atmel': {
        'doc32000.pdf': 'https://ww1.microchip.com/downloads/en/devicedoc/doc32000.pdf',
    },

    'CR16': {
        'cr16.pdf': 'https://pubweb.eng.utah.edu/~cs3710/handouts/cr16.pdf',
        'prog16c.pdf': 'https://doc-0s-4s-docs.googleusercontent.com/docs/securesc/ha0ro937gcuc7l7deffksulhg5h7mbp1/tgcekhm1ilon5d6gp5v5c09mepm3b9fa/1551938400000/14157490643402214266/*/1QOkOiMNmoH_D0JEk62R4B4MdFhZR0il7?e=download',
    },

    'JVM': {
        'jvms8.pdf': 'https://docs.oracle.com/javase/specs/jvms/se8/jvms8.pdf',
    },

    'MIPS': {
        'mips64v2.pdf': 'https://www.ece.lsu.edu/ee4720/mips64v2.pdf',
        'MD00076-2B-MIPS1632-AFP-02.63.pdf': 'https://s3-eu-west-1.amazonaws.com/downloads-mips/documents/MD00076-2B-MIPS1632-AFP-02.63.pdf',
        'MD00087-2B-MIPS64BIS-AFP-06.03.pdf': 'https://s3-eu-west-1.amazonaws.com/downloads-mips/documents/MD00087-2B-MIPS64BIS-AFP-06.03.pdf',
        'MD00582-2B-microMIPS32-AFP-05.03.pdf': 'https://github.com/f47h3r/firmware_reversing/raw/master/docs/research/MD00582-2B-microMIPS32-AFP-05.03.pdf',
        'MD00582-2B-microMIPS32-AFP-05.04.pdf': 'https://s3-eu-west-1.amazonaws.com/downloads-mips/documents/MD00582-2B-microMIPS32-AFP-05.04.pdf',
        'MD000594-2B-microMIPS64-AFP-06.02.pdf': 'https://s3-eu-west-1.amazonaws.com/downloads-mips/documents/MD000594-2B-microMIPS64-AFP-06.02.pdf',
        'r4000.pdf': 'https://groups.csail.mit.edu/cag/raw/documents/R4400_Uman_book_Ed2.pdf',
    },

    'PA-RISC': {
        'pa11_acd.pdf': 'http://ftp.parisc-linux.org/docs/arch/pa11_acd.pdf',
    },

    'PIC': {
        'PIC12_40139e.pdf': 'https://ww1.microchip.com/downloads/en/devicedoc/40139e.pdf',
        'PIC17F_40001761E.pdf': 'https://ww1.microchip.com/downloads/en/DeviceDoc/40001761E.pdf',
        'PIC16_33023a.pdf': 'https://ww1.microchip.com/downloads/en/devicedoc/33023a.pdf',
        'PIC17_30289b.pdf': 'https://ww1.microchip.com/downloads/en/devicedoc/30289b.pdf',
        'PIC18_14702.pdf': 'https://www.farnell.com/datasheets/22241.pdf',
        'PIC24_70157D.pdf': 'https://ww1.microchip.com/downloads/en/DeviceDoc/70157D.pdf',
    },

    'PowerPC': {
        'POWERISA_V2.06_PUBLIC.pdf': 'http://kib.kiev.ua/x86docs/POWER/PowerISA_V2.06B_V2_PUBLIC.pdf',
        'PowerISA_V2.07B.pdf': 'http://kib.kiev.ua/x86docs/POWER/PowerISA_V2.07B.pdf',
        'PowerISA_V3.0.pdf': 'http://kib.kiev.ua/x86docs/POWER/PowerISA_V3.0.pdf', 
        'powerpc.pdf': 'https://wiki.alcf.anl.gov/images/f/fb/PowerPC_-_Assembly_-_IBM_Programming_Environment_2.3.pdf',
        'altivec.pdf': 'http://dec8.info/Apple/macos8pdfs/CD_MacOS_8_9_X_4D_Omnis/Apple/MPC7450/ALTIVECPEM.pdf',
    },

    'Sparc': {
        'SPARCV9.pdf': 'https://cr.yp.to/2005-590/sparcv9.pdf',
    },

    'TI_MSP430': {
        # 'MSP430.pdf': 'https://e2echina.ti.com/cfs-file/__key/telligent-evolution-components-attachments/00-55-01-00-00-00-61-61/MSP430x2xx-Family-User_26002300_39_3B00_s-Guide-_2800_Rev.-E_2900_.pdf', # Rev. E
        'MSP430.pdf': 'https://www.ti.com/lit/ug/slau144j/slau144j.pdf', # Rev. J
    },

    'x86': {
        'Intel64_IA32_SoftwareDevelopersManual_vol2a.pdf': 'http://kib.kiev.ua/x86docs/SDMs/253666-029.pdf', 
        'Intel64_IA32_SoftwareDevelopersManual_vol2b.pdf': 'http://kib.kiev.ua/x86docs/SDMs/253667-029.pdf', 
        'AMD64_ProgrammersManual_vol3.pdf': 'https://www.amd.com/system/files/TechDocs/24594.pdf', 
        'AMD64_ProgrammersManual_vol4.pdf': 'https://www.amd.com/system/files/TechDocs/26568.pdf', 
        'AMD64_ProgrammersManual_vol5.pdf': 'https://www.amd.com/system/files/TechDocs/26569_APM_V5.pdf', 
        'AMD64_128-bit_SSE5_Instructions.pdf': 'https://www.amd.com/system/files/TechDocs/43479.pdf', 
    },

    'Z80': {
        'UM0050.pdf': 'https://www.zilog.com/force_download.php?filepath=YUhSMGNEb3ZMM2QzZHk1NmFXeHZaeTVqYjIwdlpHOWpjeTk2TVRnd0wzVnRNREExTUM1d1pHWT0=',
        'UM0080.pdf': 'https://www.zilog.com/force_download.php?filepath=YUhSMGNEb3ZMM2QzZHk1NmFXeHZaeTVqYjIwdlpHOWpjeTk2T0RBdlZVMHdNRGd3TG5Ca1pnPT0=',
    }
}

if len(sys.argv) > 2 or sys.argv[1] == '-h':
    print "Usage: {} [</path/to/ghidra>]\n".format(os.path.basename(__file__))
    exit(1)
elif len(sys.argv):
    os.chdir(sys.argv[1])

headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}

for platform in docs:
    destdir = 'Ghidra/Processors/{}/data/manuals'.format(platform)
    if not os.path.exists(destdir):
        os.makedirs(destdir)
    for proc_doc in docs[platform]:
        destfile = '{}/{}'.format(destdir, proc_doc)
        print "{}:".format(destfile),
        if not os.path.exists(destfile):
            web_src = docs[platform][proc_doc]
            if web_src is None:
                print "no docs :-("
                continue
            print "download {}:".format(web_src),
            try:
                resp = requests.get(web_src, stream=True, headers=headers)
                if resp.ok:
                    with open(destfile, 'w') as fd:
                        for chunk in resp.iter_content(chunk_size=16384):
                            if not chunk:
                                break
                            fd.write(chunk)
                        print "OK!"
                else:
                    print "Failed! ({})".format(resp.status_code)
            except requests.exceptions.ConnectionError:
                print 'HTTP Exception :-('
        else:
            print "exists"
