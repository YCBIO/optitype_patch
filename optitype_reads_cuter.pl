#! /usr/bin/perl

#use FindBin qw($RealBin);
use Getopt::Long;

our %seqhash;
our ($bam, $outprefix, $cutoff);
GetOptions(
    "c:f" => \$cutoff,
    "b=s" => \$bam,
    "o=s" => \$outprefix,
    "help|?" => \$help,
);
if (!defined $bam || !defined $outprefix ||$help){&usage;exit(0);}

$cutoff ||= 300000;

&main($bam, $cutoff,$outprefix);

sub usage{
print "
	Usage: $0  < -b bam >  < -o outprefix >  [ -c 300000 ] 
	Options:
        -o:<file>     the output file (Require)
        -b:<file>     the input bam file (Require)
        -c:[int]    the reads num cutoff(default 300000)
        -help:   show this infomation\n";
}

sub main{
    ($bam,$cutoff,$outprefix) =  @_;
    ## count reads save fractionr
    $reads1_num = `samtools view -f 64 -F 256 $bam|wc -l`;
    chomp($reads1_num);
    $random_num = int(($cutoff/$reads1_num)*10);

    $fq1 = $outprefix."_R1.hla.fq.gz";
    $fq2 = $outprefix."_R2.hla.fq.gz";
    if($random_num >=10){
        &printreads($bam,$fq1,$random_num,'r1');
        &printreads($bam,$fq2,$random_num,'r2');
    }else{
        &cutreads($bam,$fq1,$random_num,'r1');
        &cutreads($bam,$fq2,$random_num,'r2');
    }
}


sub cutreads{
    ($bam,$outfq,$random_num,$end) = @_;
    if($end eq "r1"){
        open BAM,"samtools view -f 64 -F 256 $bam|" or die $!;
    }else{
        open BAM,"samtools view -f 128 -F 256 $bam|" or die $!;
    }
    open FQ,"| gzip >$outfq" or die $!;
    while(<BAM>){
        @arr = split/\t/;
        $line = "\@$arr[0]/2\n$arr[9]\n+\n$arr[10]\n";
        if($seqhash{$arr[9]}){
            if($random_num >rand(10)){
                print FQ $line;
            }
        }else{
            $seqhash{$arr[9]} = 1;
            print FQ $line;
        }
    }
}

sub printreads{
    ($bam,$outfq,$random_num,$end) = @_;
    if($end eq "r1"){
        open BAM,"samtools view -f 64 -F 256 $bam|" or die $!;
    }else{
        open BAM,"samtools view -f 128 -F 256 $bam|" or die $!;
    }
    open FQ,"| gzip >$outfq" or die $!;
    while(<BAM>){
        @arr = split/\t/;
        $line = "\@$arr[0]/2\n$arr[9]\n+\n$arr[10]\n";
        print FQ $line;
    }
    close BAM;
    close FQ;
}
