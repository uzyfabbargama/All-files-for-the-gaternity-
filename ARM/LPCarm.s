//lsl 1 = 10
//lsr 10 = 1
//constantes
.set contador, 0
.macro def_kw nombre
    .equ \nombre, contador
    .set contador, contador + 1
.endm

.macro def_slot nombre
    .equ \nombre, contador
    .set contador, contador + 8
.endm
//VAR
def_kw kw_var                   //0
//CTRL
def_kw kw_ctrl                  //1
//CLASS
def_kw kw_class                 //2
//"("
def_slot kw_parenthesis_open    //3
//")"
def_kw kw_parenthesis           //11
//","
def_kw kw_comma                 //12
//"{
def_slot kw_key_open            //13
//"}
def_kw kw_key_close             //21
//";
def_kw kw_semicolon             //22
//"=
def_kw kw_equal                 //23
//"+"
def_kw kw_add                   //24
//"-"
def_kw kw_sub                   //25
//"/"
def_kw kw_div                   //26
//"*
def_kw kw_                      //27
//"**
def_kw kw_                      //28
//"0"
def_kw kw_                      //29
//"1"
def_kw kw_                      //30
//"2"
def_kw kw_                      //31
//"3"
def_kw kw_                      //32
//"4"
def_kw kw_                      //33
//"5"
def_kw kw_                      //34
//"6"
def_kw kw_                      //35
//"7"
def_kw kw_                      //36
//"8"
def_kw kw_                      //37
//"9"
def_kw kw_                      //38
//"#"
def_kw kw_                      //39
//"\n"
def_kw kw_                      //40
//" "
def_kw kw_                      //41
//ERROR
def_kw kw_                      //42
//"."
def_kw kw_                      //43
//"["
def_kw kw_                      //51
//"]"
def_kw kw_                      //52
//":"
def_kw kw_                      //53
//&
def_kw kw_                      //54
//^
def_kw kw_                      //55
//|
def_kw kw_                      //56
//!
def_kw kw_                      //57
//<
def_kw kw_                      //58
//>
def_kw kw_                      //59
//"'"
def_kw kw_                      //60
//'"'
def_kw kw_                      //61

.macro if condition, position
    mov x1, INPUT
    eor x1, \condition
    cset x1, eq
    