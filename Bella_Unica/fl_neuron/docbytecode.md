# NeuralScript Bytecode Reference

## Instrucciones

### var
`var nombre, valor`
- Crea una neurona con un valor inicial.

### proc
`proc destino, origen`
- Procesa la neurona `origen` y guarda el resultado en `destino`.
- Fórmula: `destino = (origen * proc) + ...`

### conv
`conv destino, kernel, bias`
- Convolución: `destino = (destino * kernel) + bias`.

### norm
`norm n1, n2`
- Normaliza `n1` y `n2` usando una resta branchless.

### decay / growth
`decay neurona, valor`
- Reduce o aumenta el valor de una neurona.

### logic cmp
`logic cmp cond, n1, n2`
- Compara `n1` y `n2`, guarda el resultado en `cond`.

### logic loop / endloop
- Bucles anidados.

## Ejemplos
...
