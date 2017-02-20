#!/bin/bash
files=./Examples/Simple/*
output=time.txt
echo "||OCamL|Cython|Python">$output
echo "-|-|-|-">>$output
for f in $files
do
  echo "Processing $f file..."
  ocaml="$( TIMEFORMAT='%lR';time ( ./OCamL/DPLL $f ) 2>&1 1>/dev/null )"
  cython="$( TIMEFORMAT='%lR';time ( ./Cython/DPLL_compiled $f ) 2>&1 1>/dev/null )"
  python="$( TIMEFORMAT='%lR';time ( python ./Python/DPLL.py $f ) 2>&1 1>/dev/null )"
  echo "${f#$files}|$ocaml|$cython|$python">>$output
done
