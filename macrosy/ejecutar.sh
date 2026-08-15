cd $HOME/macrosy
echo "ingresa tipo (1-5)"
read a
python3 macrosy11.py test_parsing/test_parse$a.asm let.asm
cat let.asm
