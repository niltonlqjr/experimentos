#! /usr/bin/python3

import random
import argparse

LLVM_FLAGS = [
    '-adce', '-always-inline', '-argpromotion', '-bb-vectorize', '-block-placement',
    '-break-crit-edges', '-codegenprepare', '-constmerge', '-dce', '-deadargelim',
    '-deadtypeelim', '-die', '-dse', '-function-attrs', '-globaldce',
    '-globalopt', '-gvn', '-indvars', '-inline', '-instcombine',
    '-aggressive-instcombine', '-internalize', '-ipsccp', '-jump-threading', '-lcssa',
    '-licm', '-loop-deletion', '-loop-extract', '-loop-extract-single', '-loop-reduce',
    '-loop-rotate', '-loop-simplify', '-loop-unroll', '-loop-unroll-and-jam', '-loop-unswitch',
    '-lower-global-dtors', '-loweratomic', '-lowerinvoke', '-lowerswitch', '-mem2reg',
    '-memcpyopt', '-mergefunc', '-mergereturn', '-partial-inliner', '-prune-eh',
    '-reassociate', '-rel-lookup-table-converter', '-reg2mem', '-sroa', '-sccp',
    '-simplifycfg', '-sink', '-strip', '-strip-dead-debug-info', '-strip-dead-prototypes',
    '-strip-debug-declare', '-strip-nondebug', '-tailcallelim'
]

default_len_min = 1
default_len_max = 37
default_seqs_total = 100

def generate_seqs(seed, lmin, lmax, total):
    random.seed(seed)
    generated_seqs = dict()
    while len(generated_seqs) < total:
        N = random.randint(lmin, lmax)
        new_seq = dict() # Don't repeat the flags.
        while len(new_seq) < N:
            new_seq[LLVM_FLAGS[random.randint(0, len(LLVM_FLAGS) - 1)]] = None
        seq_str = ''
        for seq in new_seq: # Concatenate seqs from dict into single string.
            seq_str += seq + ' '
        generated_seqs[seq_str] = None # Add new generated sequence.
    for seq in generated_seqs.keys(): # Print generated sequences to stdout.
        print(seq)


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [--min VAL] [--max VAL] [--seed VAL] [--total VAL]",
        description="Generate random sequences of optimizations."
    )
    parser.add_argument('--min', dest='len_min', default=default_len_min)
    parser.add_argument('--max', dest='len_max', default=default_len_max)
    parser.add_argument('--total', dest='total', default=default_seqs_total)
    parser.add_argument('--seed', dest='seed')
    return parser

args = init_argparse().parse_args()
generate_seqs(args.seed, int(args.len_min), int(args.len_max), int(args.total))
