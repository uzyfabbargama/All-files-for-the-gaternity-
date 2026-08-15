// Constantes para identificar jugadores
const BOT = 1;        // Nuestro bot (maximizador)
const OPPONENT = 2;   // Oponente (minimizador)

/**
 * Comprueba si quedan casillas vacías (valor 0).
 * @param {number[]} board Estado actual del tablero.
 * @returns {boolean} True si quedan movimientos.
 */
function isMovesLeft(board) {
  return board.includes(0);
}

/**
 * Evalúa el tablero:
 * +10 si gana BOT,
 * -10 si gana OPPONENT,
 * 0 en empate o sin ganador aún.
 * @param {number[]} board Estado actual del tablero.
 * @returns {number} Puntuación del estado.
 */
function evaluate(board) {
  const lines = [
    [0,1,2], [3,4,5], [6,7,8],  // filas
    [0,3,6], [1,4,7], [2,5,8],  // columnas
    [0,4,8], [2,4,6]            // diagonales
  ];

  for (let [a, b, c] of lines) {
    if (board[a] !== 0 && board[a] === board[b] && board[b] === board[c]) {
      return board[a] === BOT ? 10 : -10;
    }
  }
  return 0;
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
  if (score === 10 || score === -10) return score;
  
  // Condición de empate (sin movimientos restantes)
  if (!isMovesLeft(board)) return 0;

  if (isMax) {
    let maxEval = -Infinity;
    for (let i = 0; i < 9; i++) {
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
    for (let i = 0; i < 9; i++) {
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
 * Recorre todas las casillas vacías y elige
 * la que maximiza la puntuación para BOT.
 * @param {number[]} board Estado actual del tablero.
 * @returns {number} Índice del mejor movimiento (0-8).
 */
function findBestMove(board) {
  let bestVal = -Infinity;
  let bestMove = -1;

  for (let i = 0; i < 9; i++) {
    if (board[i] === 0) {
      // 1. Probar el movimiento para el BOT
      board[i] = BOT;
      // 2. Calcular el valor de este movimiento asumiendo que el oponente juega de forma óptima después (false)
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

  return bestMove;
}

module.exports = {
  BOT,
  OPPONENT,
  isMovesLeft,
  evaluate,
  minimax,
  findBestMove
};
