#!/bin/bash

mkdir -p compiled images

for i in sources/*.txt tests/*.txt; do
	echo "Compiling: $i"
    fstcompile --isymbols=syms.txt --osymbols=syms.txt $i | fstarcsort > compiled/$(basename $i ".txt").fst
done

# TODO
echo "text2num"
fstconcat compiled/horas.fst compiled/e2dot.fst > compiled/a.fst
fstconcat compiled/a.fst compiled/minutos.fst > compiled/text2num.fst

echo "lazy2num"
fstconcat compiled/e2dot.fst compiled/minutos.fst > compiled/a.fst
fstunion compiled/zeros.fst compiled/a.fst > compiled/b.fst
fstconcat compiled/horas.fst compiled/b.fst > compiled/lazy2num.fst

echo "rich2text"
fstproject --project_type=input compiled/horas.fst > compiled/a.fst
fstproject --project_type=input compiled/e2dot.fst > compiled/b.fst
fstconcat compiled/a.fst compiled/b.fst > compiled/c.fst
fstunion compiled/meias.fst compiled/quartos.fst > compiled/d.fst
fstconcat compiled/c.fst compiled/d.fst > compiled/rich2text.fst

echo "rich2num"
fstcompose <(fstarcsort --sort_type=olabel compiled/rich2text.fst) compiled/text2num.fst > compiled/a.fst
fstunion compiled/a.fst compiled/lazy2num.fst > compiled/rich2num.fst

echo "num2text"
fstinvert compiled/text2num.fst > compiled/num2text.fst

for i in compiled/*.fst; do
	echo "Creating image: images/$(basename $i '.fst').pdf"
    fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt $i | dot -Tpdf > images/$(basename $i '.fst').pdf
done

echo "Testing the transducer 'converter' with the input 'tests/numero.txt'"
fstcompose compiled/horas_test.fst compiled/horas.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
fstcompose compiled/minutos_test.fst compiled/minutos.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
fstcompose compiled/quartos_test.fst compiled/quartos.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
fstcompose compiled/text2num_test.fst compiled/text2num.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
fstcompose compiled/lazy2num_test.fst compiled/lazy2num.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
fstcompose compiled/rich2text_test.fst compiled/rich2text.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
fstcompose compiled/rich2num_test.fst compiled/rich2num.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
fstcompose compiled/num2text_test.fst compiled/num2text.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
