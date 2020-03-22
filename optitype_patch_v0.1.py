#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, os, argparse, re, math, glob,subprocess
import getopt,configparser
basepath = os.path.dirname(__file__)
sys.path.append(basepath)

def USAGE(script):
    helpMess = '''
     ProgramName:\t%s
         Version:\tv0.1
         Contact:\tyijian@yucebio.com
    Program Date:\t2019.10.14
          Modify:\t-
     Description:\tThis program is used to filter HLA related reads before run optitype.
           Usage:\tpython3 %s --f1 <fastq1> --f2 <fastq2> -o <outdir>
         Options:
            -h              Show this help message.
            --f1            Fastq file 1.
            --f2            Fastq file 2.  
            -t --type       Sequence type [DNA|RNA].
            -p --prefix     Prefix for result file.
            -o --outdir     Optional outdir.Default=[./].
            -c --config     Config file.
    ''' %(script,script)
    return helpMess


def read_config(arguFile):
    arg_ini = configparser.ConfigParser()
    arg_ini.read(arguFile)
    return arg_ini

def run_patch(argDict,arg_ini):
    print("INFO: Start write work shell.")
    ref_dna = "%s/bwa_index_dna/hla_reference_dna.fasta" % (arg_ini.get("data","bwa_index"))
    ref_rna = "%s/bwa_index_rna/hla_reference_rna.fasta" % (arg_ini.get("data","bwa_index"))
    bwa = arg_ini.get("tools","bwa")
    samtools = arg_ini.get("tools","samtools")
    python = arg_ini.get("tools","python")
    optitype = arg_ini.get("tools","optitype")
    bwa_path = os.path.join(argDict['outdir'],'bwa')
    if not os.path.exists(bwa_path):
        os.mkdir(bwa_path)
    hla_reads = os.path.join(argDict['outdir'],'hla_reads')
    if not os.path.exists(hla_reads):
        os.mkdir(hla_reads)
    optitype_path =  os.path.join(argDict['outdir'],'optitype')
    if not os.path.exists(optitype_path):
        os.mkdir(optitype_path)
    shellpath = os.path.join(argDict['outdir'],'shell')
    if not os.path.exists(shellpath):
        os.mkdir(shellpath)
    sampleshellpath = "%s/%s.sh" % (shellpath,argDict['prefix'])
    
    f1 = argDict['f1']
    f2 = argDict['f2']
    bam = "%s/%s.bam" % (argDict['outdir'],argDict['prefix'])
    shellstr = ""
    res
    if argDict['seq_type'] == "RNA":
        ref = ref_rna
        ref_type = "rna"
    else:
        ref = ref_dna
        ref_type = "dna"

    shellstr += "%s mem -M -t 8  %s  %s %s   |%s view -1 -b -S -F 256 -F 4 - > %s &&\n" % (bwa,samtools,ref,f1,f2,bam)
    shellstr += "perl %s/optitype_reads_cuter.pl -b %s -o %s/%s  &&\n" % (basepath,bam,argDict['outdir'],argDict['prefix'])
    shellstr += "%s %s -i  %s/%s_R1.hla.fq.gz %s/%s_R2.hla.fq.gz --%s -v -o %s -p %s \n" % (python,optitype,hla_reads,argDict['prefix'],hla_reads,argDict['prefix'],ref_type,optitype_path,argDict['prefix'])
    samShell = open(sampleshellpath,"w")
    samShell.write(shellstr)
    samShell.close()
    ##run

    print("INFO: Finished.")

if __name__ == '__main__':
    argv = sys.argv[1:]
    argDict = {}
    argDict['outdir'] = os.getcwd()
    try:
        opts, args = getopt.getopt(argv,"ho:t:p:c:",["f1=","f2=","outdir=","type=","prefix=","config"])
    except getopt.GetoptError:
        print(USAGE(sys.argv[0]))
        sys.exit(2)
    if len(opts) == 0:
        print(USAGE(sys.argv[0]))
        sys.exit()
    for opt, arg in opts:
        if opt in ('-h','--help'):
            print(USAGE(sys.argv[0],Version))
            sys.exit()
        elif opt in ('--f1'):
            argDict['f1']  = arg
            if not os.path.exists(argDict['f1'] ):
                print("Error: FASTQ file 1 not exists.")
                sys.exit(0)
            argDict['f1']  = os.path.abspath(argDict['f1'] )
        elif opt in ('--f2'):
            argDict['f2']  = arg
            if not os.path.exists(argDict['f1'] ):
                print("Error: FASTQ file 2 not exists.")
                sys.exit(0)
            argDict['f2']  = os.path.abspath(argDict['f2'] )
        elif opt in ("-t","--type"):
            argDict['f2']  = arg
            if not os.path.exists(argDict['f1'] ):
                print("Error: FASTQ file 2 not exists.")
                sys.exit(0)
            argDict['f2']  = os.path.abspath(argDict['f2'] )
        elif opt in ("-o", "--outdir"):
            argDict['outdir'] = arg
            if not os.path.exists(argDict['outdir'] ):
                os.mkdir(argDict['outdir'] )
            argDict['outdir']  = os.path.abspath(argDict['outdir'] )
        elif opt in ("-p","--prefix"):
            argDict['prefix'] = arg
         elif opt in ("-c","--config"):
            argDict['config'] = arg
    
    arg_ini = read_config(argDict['config'])
    run_patch(argDict,arg_ini)

