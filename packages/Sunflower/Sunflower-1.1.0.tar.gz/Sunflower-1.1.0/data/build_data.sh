#!/usr/bin/env bash

### This shows how the contents of sunflower.data are built.
###
### End-users should not need to run this file, so it's not included
### in the sunflower distribution

WORK=/lustre/work1/ensembl/mh5
PWMDIR="${WORK}/pwm/JASPAR_CORE"
GENOME=/data/blastdb/Ensembl

mkdir -p build/data
command cd build/data

## 0) compile
${CC:-gcc} ${CFLAGS:--O} -o fastacomp ../../data/fastacomp.c

## 1) build models
for SYSGROUP in vertebrate insect plant; do
    pwm2sfl --revcom --sysgroup ${SYSGROUP} \
        -o ../../sunflower/data/jaspar/core/${SYSGROUP}.sfl "${PWMDIR}"
done

## 2) get composition
calc_comp ()
{
    cat "${2}" | ./fastacomp "${1}" >> all.fastacomposition
}

calc_comp "aedes jaspar/core/insect" \
    ${GENOME}/Aedes/aedes_1_softmasked_supercontig.fa
calc_comp "anopheles jaspar/core/insect" \
    ${GENOME}/Anopheles/genome/agamP3/chromosomes_agamP3_rm_dust_soft/*.fa
calc_comp "chicken jaspar/core/vertebrate" \
    ${GENOME}/Large/Gallus_gallus/WASHUC2/Gallus_gallus.WASHUC2.softmasked.fa
calc_comp "chimp jaspar/core/vertebrate" \
    ${GENOME}/Chimp/2.1/genome/softmasked_dusted.fa
calc_comp "dog jaspar/core/vertebrate" \
    ${GENOME}/Dog/BROADD2/genome/softmasked_dusted/toplevel.fa
calc_comp "fruitfly jaspar/core/insect" \
    ${GENOME}/Drosophila/bdgp4.3/drosophila_melanogaster_bdgp43_softmask_dusted_chr.fasta
calc_comp "human jaspar/core/vertebrate" \
    ${GENOME}/Human/NCBI36/genome/unmasked/*.fa
calc_comp "fugu jaspar/core/vertebrate" \
    ${GENOME}/Fugu/v3/fugu.v3.mask.trf.dust.fa
calc_comp "medaka jaspar/core/vertebrate" \
    ${GENOME}/Oryzias_latipes/MEDAKA1/oryzias_latipes.MEDAKA1.norep.fa
calc_comp "mouse jaspar/core/vertebrate" \
    ${GENOME}/Mouse/NCBIM37/genome/unmasked/toplevel.fa
calc_comp "rat jaspar/core/vertebrate" \
    ${GENOME}/Rat/RGSC3_4/softmasked_dusted/*.fa
calc_comp "rhesus jaspar/core/vertebrate" \
    ${GENOME}/Rmacaque/MMUL_2/genome/softmasked_dusted.fa
calc_comp "zebrafish jaspar/core/vertebrate" \
    /data/blastdb/Fish/Zv7/genome/zv7_softmasked_dusted.fa

## 3) make_species_info
../../data/make_species_info.py
