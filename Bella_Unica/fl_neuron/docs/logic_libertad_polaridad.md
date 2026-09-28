
# Libertad de polaridad en `logic`

## Nota técnica sobre la asimetría `if`/`else` y su ausencia en NS

### Contexto

Todos los lenguajes imperativos clásicos (C, Python, Java, etc.)
imponen una **polaridad** a las estructuras condicionales:

- El caso **positivo** (`if`) es el "normal".
- El caso **negativo** (`else`) es el "excepcional".

Esa asimetría está tan interiorizada que nadie la cuestiona. NS la
rompe: `logic yes` y `logic no` son **ramas de una misma estructura**,
y el orden lo decide el programador.

---

## 1. La asimetría clásica

### Python

```python
if cond:
    # caso verdadero (normal)
else:
    # caso falso (excepcional)
```

### C

```c
if (cond) {
    // caso verdadero (normal)
} else {
    // caso falso (excepcional)
}
```

### Java

```java
if (cond) {
    // caso verdadero (normal)
} else {
    // caso falso (excepcional)
}
```

En todos los casos, el **caso positivo va primero**. El negativo es
el "else", el "si no". Es una convención universal.

---

## 2. El problema de la asimetría

Imagina que tienes una condición que normalmente es **falsa**, y solo
raramente es verdadera. En Python:

```python
if not cond:
    # caso normal (raro de escribir)
else:
    # caso excepcional
```

Eso es **antinatural**. El caso normal está en el `else`, y el
excepcional en el `if`. La lógica está invertida respecto a la
frecuencia.

Y si tienes **múltiples condiciones** que pueden ser verdaderas o
falsas independientemente:

```python
if not c1:
    # transición 1
if not c2:
    # transición 2
if c3:
    # transición 3
if c4:
    # transición 4
```

Eso es **feo, confuso y propenso a errores**. No hay `endcond` que
agrupe las ramas. Cada `if` es independiente. El lector no sabe si
están relacionados o no.

---

## 3. La solución de NS

```
logic no c1
    $ transición 1
logic no c2
    $ transición 2
logic yes c3
    $ transición 3
logic yes c4
    $ transición 4
logic endcond
```

Eso se lee como **"primero transición 1, luego transición 2, luego
transición 3, luego transición 4"**. El orden es el flujo. Y no hay
que invertir nada mentalmente.

También es válido:

```
logic yes c1
    $ transición 1
logic no c2
    $ transición 2
logic yes c3
    $ transición 3
logic no c4
    $ transición 4
logic endcond
```

**Ambos son válidos.** No hay un "caso normal". No hay un "caso
excepcional". Hay **ramas de una misma estructura**, y el orden lo
decides tú.

---

## 4. Lógica sin polaridad

NS no impone una polaridad a la lógica. No hay un "caso positivo" y
un "caso negativo". Hay **ramas**, y tú decides el orden.

Eso es **libertad de polaridad**, y no lo tiene ningún lenguaje
imperativo. Todos empiezan por el `if` positivo, y el `else` es el
negativo. NS empieza por donde tú quieras.

### La filosofía de NS

> "lógica: no cond make this"

Eso no es "si no cond, haz esto". Es **"lógica: la rama no-cond hace
esto"**. La rama es una **unidad**, no un caso. Y tú decides si esa
rama va primero o después.

Eso es **lógica sin polaridad**, y es coherente con la idea de que
`logic` es el intérprete del estado, no un `if` disfrazado.

---

## 5. Comparación con `switch` y `if/elif/else`

| Estructura        | Múltiples ramas | Excluyentes | Orden libre |
|-------------------|-----------------|-------------|-------------|
| `if/else`         | 2               | Sí          | No          |
| `if/elif/else`    | N               | Sí          | No          |
| `switch`          | N               | Sí          | No          |
| **NS `logic`**    | **N**           | **No**      | **Sí**      |

NS `logic` es **un `switch` no excluyente con orden libre**. No
existe en ningún lenguaje imperativo clásico.

---

## 6. Lo que esto permite

### Máquinas de estado compactas

```
logic no c1
    $ transición 1
logic no c2
    $ transición 2
logic yes c3
    $ transición 3
logic yes c4
    $ transición 4
logic endcond
```

Se lee como una secuencia de transiciones. El orden es el flujo. No
hay que invertir nada.

### Sistemas de reglas

```
logic cmpv c1, n1, 0.1
logic cmpv c2, n2, 0.2
logic cmpv c3, n3, 0.3

logic yes c1
    growth n2, 0.1
logic yes c2
    decay n3, 0.05
logic yes c3
    proc n1, n2
logic endcond
```

Si se cumple c1, haz algo; si se cumple c2, haz otra cosa; si se
cumple c3, haz otra. **Pueden cumplirse varias a la vez**, y se
ejecutan en orden.

Eso es **un sistema de producción**, no un `if/elif/else`.

---

## 7. Por qué no se agregó antes

La asimetría `if`/`else` es una **convención histórica**, no una
necesidad técnica. Los lenguajes clásicos la impusieron porque:

1. **Simplicidad de implementación**: un solo `if` positivo es más
   fácil de compilar que múltiples ramas no excluyentes.
2. **Tradición**: los lenguajes se copian unos a otros.
3. **Cognición**: el caso positivo es el "normal", el negativo es el
   "excepcional".
4. **Falta de necesidad**: la mayoría de programas no requieren
   múltiples ramas no excluyentes.

NS no tiene esas restricciones porque:

1. **`logic` es un intérprete del estado**, no un `if` disfrazado.
2. **Las ramas son unidades**, no casos.
3. **El orden es el flujo**, no una imposición del lenguaje.
4. **Las ramas pueden ser no excluyentes**, porque el estado puede
   cambiar entre ellas.

Eso significa que NS puede hacer cosas que los lenguajes clásicos no
pueden hacer de forma natural. Y no es porque sea más complicado, sino
porque **no arrastra la convención histórica**.

---

## 8. Conclusión

NS tiene **libertad de polaridad** en `logic`:

- Puedes empezar con `logic yes` o `logic no`.
- Las ramas son unidades, no casos.
- El orden es el flujo, no una imposición.
- Las ramas pueden ser no excluyentes.

Eso es **un `switch` no excluyente con orden libre**, y no existe en
ningún lenguaje imperativo clásico.

La asimetría `if`/`else` es una convención, no una necesidad. NS la
rompe, y el resultado es más flexible.

---

## Referencias

- Documentación interna: `docs/dispatch_jerarquico_branchless.md`.
- Documentación interna: `docs/memoria_y_localidad.md`.
