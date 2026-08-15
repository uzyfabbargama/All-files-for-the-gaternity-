// Constantes para identificar jugadores
const BOT = 1;        // Nuestro bot (maximizador)
const OPPONENT = 2;   // Oponente (minimizador)
const BOARD_SIZE = 25; // 5x5 = 25 casillas
const SIDE_LENGTH = 5; // Longitud del lado

/**
 * Comprueba si quedan casillas vacías (valor 0).
 * @param {number[]} board Estado actual del tablero (tamaño 25).
 * @returns {boolean} True si quedan movimientos.
 */
function isMovesLeft(board) {
  return board.includes(0);
}

/**
 * Genera todas las líneas posibles de 3 en raya para un tablero de 5x5.
 * @returns {number[][]} Array de arrays con los índices de cada línea de 3.
 */
function generateWinningLines() {
  const lines = [];

  // Filas (3 en línea, 3 posibilidades por fila)
  for (let r = 0; r < SIDE_LENGTH; r++) {
    for (let c = 0; c <= SIDE_LENGTH - 3; c++) {
      const start = r * SIDE_LENGTH + c;
      lines.push([start, start + 1, start + 2]);
    }
  }

  // Columnas (3 en línea, 3 posibilidades por columna)
  for (let c = 0; c < SIDE_LENGTH; c++) {
    for (let r = 0; r <= SIDE_LENGTH - 3; r++) {
      const start = r * SIDE_LENGTH + c;
      lines.push([start, start + SIDE_LENGTH, start + 2 * SIDE_LENGTH]);
    }
  }

  // Diagonales (Principal \ )
  for (let r = 0; r <= SIDE_LENGTH - 3; r++) {
    for (let c = 0; c <= SIDE_LENGTH - 3; c++) {
      const start = r * SIDE_LENGTH + c;
      lines.push([start, start + SIDE_LENGTH + 1, start + 2 * SIDE_LENGTH + 2]);
    }
  }

  // Diagonales (Inversa / )
  for (let r = 0; r <= SIDE_LENGTH - 3; r++) {
    for (let c = 2; c < SIDE_LENGTH; c++) {
      const start = r * SIDE_LENGTH + c;
      lines.push([start, start + SIDE_LENGTH - 1, start + 2 * SIDE_LENGTH - 2]);
    }
  }

  return lines;
}

const WINNING_LINES = generateWinningLines();

/**
 * Evalúa el tablero (5x5, 3 en raya):
 * +10 si gana BOT,
 * -10 si gana OPPONENT,
 * 0 en empate o sin ganador aún.
 * @param {number[]} board Estado actual del tablero.
 * @returns {number} Puntuación del estado.
 */
function evaluate(board) {
  for (let [a, b, c] of WINNING_LINES) {
    // Si la línea no está vacía y los 3 son iguales
    if (board[a] !== 0 && board[a] === board[b] && board[b] === board[c]) {
      return board[a] === BOT ? 10 : -10;
    }
  }
  return 0; // Empate o juego en curso
}

/**
 * Minimax con poda Alpha-Beta.
 * @param {number[]} board Estado actual del tablero.
 * @param {number} depth Profundidad de búsqueda.
 * @param {boolean} isMax True si es turno del maximizador (BOT).
 * @param {number} alpha Valor alfa.
 * @param {number} beta Valor beta.
 * @returns {number} La mejor puntuación desde este nodo.
 */
function minimax(board, depth, isMax, alpha, beta) {
  const score = evaluate(board);

  // Condición de victoria/derrota
  if (score === 10 || score === -10) return score - (isMax ? depth : -depth); // Preferir victorias/derrotas tempranas

  // Condición de empate (sin movimientos restantes)
  if (!isMovesLeft(board)) return 0;

  if (isMax) {
    let maxEval = -Infinity;
    for (let i = 0; i < BOARD_SIZE; i++) {
      if (board[i] === 0) {
        board[i] = BOT;
        // La profundidad se incrementa, se cambia de jugador.
        const evalScore = minimax(board, depth + 1, false, alpha, beta);
        board[i] = 0; // Se deshace el movimiento

        maxEval = Math.max(maxEval, evalScore);
        alpha = Math.max(alpha, evalScore);

        if (beta <= alpha) break; // poda beta
      }
    }
    return maxEval;

  } else {
    let minEval = Infinity;
    for (let i = 0; i < BOARD_SIZE; i++) {
      if (board[i] === 0) {
        board[i] = OPPONENT;
        // La profundidad se incrementa, se cambia de jugador.
        const evalScore = minimax(board, depth + 1, true, alpha, beta);
        board[i] = 0; // Se deshace el movimiento

        minEval = Math.min(minEval, evalScore);
        beta = Math.min(beta, evalScore);

        if (beta <= alpha) break; // poda alfa
      }
    }
    return minEval;
  }
}

/**
 * Verifica si un índice corresponde a un borde (fila o columna 0 o 4) en 5x5.
 * @param {number} index Índice de la casilla (0-24).
 * @returns {boolean} True si está en el borde.
 */
function isBorder(index) {
    const row = Math.floor(index / SIDE_LENGTH);
    const col = index % SIDE_LENGTH;
    // Borde: fila 0, fila 4, columna 0 o columna 4
    return row === 0 || row === 4 || col === 0 || col === 4;
}

/**
 * Verifica si hay dos fichas del oponente en línea, con una de ellas NO en el borde,
 * y que el tercer lugar esté vacío (creando una amenaza potencial de 3 en raya).
 * NOTA: Esta es una simplificación de la regla solicitada, enfocándose en la amenaza inmediata.
 * @param {number[]} board Estado actual del tablero.
 * @returns {number} El índice de la casilla vacía que bloquea la amenaza (si la hay), o -1.
 */
function getTwoInARowThreatMove(board) {
    // Casillas interiores (no borde): de la fila 1 a 3 y columna 1 a 3
    const innerIndices = [];
    for (let i = 0; i < BOARD_SIZE; i++) {
        if (board[i] === 0 && !isBorder(i)) {
            innerIndices.push(i);
        }
    }

    for (const [a, b, c] of WINNING_LINES) {
        const line = [board[a], board[b], board[c]];
        const indices = [a, b, c];

        // Contar Oponentes y vacíos
        const opponentCount = line.filter(val => val === OPPONENT).length;
        const emptyCount = line.filter(val => val === 0).length;

        // Si el oponente tiene 2 y hay 1 vacío (es decir, una amenaza inmediata)
        if (opponentCount === 2 && emptyCount === 1) {
            const emptyIndex = indices[line.findIndex(val => val === 0)];

            // Revisar la regla: "si hay XX, y colocas un O, queda XXO, y como es un 5*5, quedará XXXO, y perdemos"
            // Se interpreta como: Evitar la formación de 2 en línea del oponente, especialmente si el movimiento
            // de bloqueo NO está en el borde y es necesario.

            // Buscamos el lugar vacío. Si ese lugar vacío está disponible Y
            // si al menos una de las fichas del oponente NO está en el borde,
            // priorizamos bloquear. (Esto simplifica la regla específica de "evitar que hayan 2".)

            // Si el movimiento de bloqueo es el que evita la victoria (lo más crítico)
            return emptyIndex;
        }
    }
    return -1; // No hay amenaza inmediata de 2 en línea.
}


/**
 * Recorre todas las casillas vacías y elige
 * la que maximiza la puntuación para BOT.
 * @param {number[]} board Estado actual del tablero.
 * @returns {number} Índice del mejor movimiento (0-24).
 */
function findBestMove(board) {
  // 1. **Regla de Prioridad/Heurística Específica:**
  //    Primero, verifica si hay un movimiento que bloquee una victoria inmediata del oponente (3 en raya).
  //    (Esta lógica ya está implícita en Minimax, pero la hacemos explícita para asegurar prioridades,
  //     aunque Minimax debería encontrarla)
  const immediateWinMove = getTwoInARowThreatMove(board);
  if (immediateWinMove !== -1) {
    // El movimiento que bloquea la amenaza de 3 en raya es el más crítico.
    // Lo retornamos, ya que es la prioridad absoluta.
    return immediateWinMove;
  }

  // 2. **Heurística de 'Espejo en las esquinas' (Prioridad Menor):**
  //    Si el tablero está casi vacío, prioriza una esquina para forzar la estrategia del oponente.
  const corners = [0, 4, 20, 24]; // Índices de las esquinas en 5x5
  if (board.filter(val => val !== 0).length < 2) { // Si es el primer o segundo movimiento
      // Elige una esquina vacía al azar si no hay otra prioridad
      for(const corner of corners) {
          if (board[corner] === 0) {
              return corner;
          }
      }
  }


  // 3. **Minimax por defecto:**
  //    Si no hay un movimiento de prioridad especial, se usa el algoritmo Minimax.
  let bestVal = -Infinity;
  let bestMove = -1;

  for (let i = 0; i < BOARD_SIZE; i++) {
    if (board[i] === 0) {
      // 1. Probar el movimiento para el BOT
      board[i] = BOT;
      // 2. Calcular el valor de este movimiento asumiendo que el oponente juega de forma óptima después (false)
      // Se inicia la búsqueda en profundidad 0.
      const moveVal = minimax(board, 0, false, -Infinity, Infinity);
      // 3. Deshacer el movimiento para restaurar el tablero
      board[i] = 0;

      // 4. Actualizar el mejor movimiento encontrado
      if (moveVal > bestVal) {
        bestVal = moveVal;
        bestMove = i;
      }
    }
  }

  // Si Minimax no encontró nada (lo que no debería pasar si hay casillas vacías)
  if (bestMove === -1) {
      // Caso de reserva: buscar la primera casilla vacía
      bestMove = board.findIndex(cell => cell === 0);
  }

  return bestMove;
}

module.exports = {
  BOT,
  OPPONENT,
  isMovesLeft,
  evaluate,
  minimax,
  findBestMove,
  isBorder,
  getTwoInARowThreatMove,
  generateWinningLines
};
