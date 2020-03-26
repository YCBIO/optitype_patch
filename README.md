# OptiType patch
Authors: Jian Yi
Date: Jan 2020
Version: 0.1

## Introduction
When running OptiType, if there are too many reads for typing, memory error will occur. The error message are 
1.
```bash
"/home/osboxes/seqan/include/seqan/basic/basic_exception.h:363 FAILED!". This error was frequently mentioned on [GitHub](https://github.com/FRED-2/OptiType/issues/71).
```
2.
```bash
  File "/mnt/cfs/project/test_freshman/yijian/HLA/lib/python2.7/site-packages/pandas/core/indexing.py", line 1869, in _getitem_axis
    return self._getbool_axis(key, axis=axis)
  File "/mnt/cfs/project/test_freshman/yijian/HLA/lib/python2.7/site-packages/pandas/core/indexing.py", line 1520, in _getbool_axis
    raise self._exception(detail)
KeyError: MemoryError()
```

Therefore, we wrote a patch to avoid these problem. Firstly, extracting the reads that can be aligned to the HLA sequence. Secondly, using OptiType to perform HLA typing on the extracted reads. For samples that can be analyzed normally, HLA typing results of with and without patches are the same. For the failed sample, it can do HLA typing successfully.

## Requirements
1.  [Python 3.7](https://www.python.org/)
2.  [SAMtools 1.2](http://www.htslib.org/)
3.  [BWA](https://github.com/lh3/bwa)


## Installation from Source

```bash
git clone https://github.com/YCBIO/optitype_patch.git
```


## Usage
Step1. make bwa index
```bash
bwa index -a bwtsw -p /path/to/bwa_index/hla_reference_dna.fasta  /path/to/optitype/data/hla_reference_dna.fasta

bwa index -a bwtsw -p /path/to/bwa_index/hla_reference_rna.fasta  /path/to/optitype/data/hla_reference_rna.fasta
```

Step2. edit config file(/path/to/optitype_patch/config.ini)
```bash
[tools]
bwa=/path/to/bwa
samtools=/path/to/samtools

[data]
bwa_index=/path/to/bwa_index/
```

Step2: filter reads
```bash
python3 /path/to/optitype_patch/optitype_patch_v0.1.py \
--f1 test.R1.fq.gz --f2  test.R2.fq.gz \
-t rna \
-c /path/to/optitype_patch/config.ini \
-o /path/to/outdir/ \
-p test
```


## Contact
Jian Yi
yijian@yucebio.com
YuceBio Technology Co., Ltd., Shenzhen, 518081, China

