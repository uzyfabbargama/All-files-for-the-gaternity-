const { 
    BOT, 
    OPPONENT, 
    isMovesLeft, 
    evaluate, 
    minimax, 
    findBestMove 
} = require('./MinimaxLogic'); // Asume que la lógica está en MinimaxLogic.js

describe('isMovesLeft', () => {
    test('Debería retornar true si hay casillas vacías (0)', () => {
        const board = [1, 2, 0, 1, 2, 0, 0, 0, 0];
        expect(isMovesLeft(board)).toBe(true);
    });

    test('Debería retornar false si el tablero está lleno', () => {
        const board = [1, 2, 1, 2, 1, 2, 1, 2, 1];
        expect(isMovesLeft(board)).toBe(false);
    });

    test('Debería retornar true en un tablero vacío', () => {
        const board = [0, 0, 0, 0, 0, 0, 0, 0, 0];
        expect(isMovesLeft(board)).toBe(true);
    });
});

describe('evaluate', () => {
    // Escenarios de victoria para el BOT (1)
    test('Debería retornar 10 si BOT gana en la primera fila', () => {
        const board = [BOT, BOT, BOT, 0, OPPONENT, 0, OPPONENT, 0, 0];
        expect(evaluate(board)).toBe(10);
    });

    test('Debería retornar 10 si BOT gana en la diagonal', () => {
        const board = [BOT, OPPONENT, 0, 0, BOT, 0, OPPONENT, OPPONENT, BOT];
        expect(evaluate(board)).toBe(10);
    });

    // Escenarios de victoria para el OPPONENT (2)
    test('Debería retornar -10 si OPPONENT gana en la segunda columna', () => {
        const board = [BOT, OPPONENT, BOT, BOT, OPPONENT, 0, 0, OPPONENT, 0];
        expect(evaluate(board)).toBe(-10);
    });

    test('Debería retornar -10 si OPPONENT gana en la otra diagonal', () => {
        const board = [BOT, 0, OPPONENT, BOT, OPPONENT, 0, OPPONENT, 0, 0];
        expect(evaluate(board)).toBe(-10);
    });

    // Escenario de empate o sin ganador aún
    test('Debería retornar 0 si no hay ganador ni empate (juego en curso)', () => {
        const board = [BOT, OPPONENT, BOT, 0, 0, 0, 0, 0, 0];
        expect(evaluate(board)).toBe(0);
    });

    test('Debería retornar 0 en caso de empate (tablero lleno sin línea)', () => {
        const board = [BOT, OPPONENT, BOT, OPPONENT, BOT, BOT, OPPONENT, BOT, OPPONENT];
        expect(evaluate(board)).toBe(0);
    });
});

describe('findBestMove', () => {
    // 1. Prueba de movimiento ganador inmediato
    test('Debería elegir el movimiento que le da la victoria inmediata (índice 2)', () => {
        // BOT (1) puede ganar poniendo en 2
        const board = [BOT, BOT, 0, OPPONENT, OPPONENT, 0, 0, 0, 0];
        expect(findBestMove(board)).toBe(2);
    });

    // 2. Prueba de bloqueo (el oponente ganaría en el siguiente turno)
    test('Debería bloquear la victoria inminente del oponente (índice 8)', () => {
        // OPPONENT (2) ganaría poniendo en 8
        const board = [BOT, BOT, 0, 2, 2, 0, 0, 0, 0];
        // El BOT debe bloquear en el índice 8, o al menos en 5
        const bestMove = findBestMove(board);
        // Dado que el algoritmo es Minimax óptimo, se espera un movimiento de bloqueo (que maximice el resultado a 0 si no puede ganar)
        expect(bestMove).toBe(5); // El 5 también bloquea y mantiene el empate
    });

    // 3. Prueba de inicio (tablero vacío)
    test('Debería elegir el centro (4) si el tablero está vacío', () => {
        const board = [0, 0, 0, 0, 0, 0, 0, 0, 0];
        expect(findBestMove(board)).toBe(4);
    });

    // 4. Prueba de centro ocupado, tomar una esquina
    test('Debería elegir una esquina si el centro está ocupado por el oponente', () => {
        const board = [0, 0, 0, 0, OPPONENT, 0, 0, 0, 0];
        // Los mejores movimientos son 0, 2, 6, 8 (las esquinas)
        const validCorners = [0, 2, 6, 8];
        expect(validCorners).toContain(findBestMove(board));
    });

    // 5. Prueba de estado avanzado: BOT (1) va a ganar
    test('Debería predecir la victoria en un tablero avanzado (índice 7)', () => {
        const board = [BOT, OPPONENT, BOT, BOT, OPPONENT, OPPONENT, 0, 0, 0];
        // BOT debe jugar en 7, forzando la victoria.
        expect(findBestMove(board)).toBe(7);
    });

    // 6. Prueba de estado avanzado: el oponente (2) gana si no se bloquea correctamente
    test('Debería bloquear una amenaza doble (índice 2)', () => {
        const board = [
            BOT, 0, 0, 
            OPPONENT, BOT, 0, 
            0, OPPONENT, 0
        ];
        // El oponente tiene doble amenaza: 0-1-2 y 2-5-8. El BOT debe jugar en 2
        expect(findBestMove(board)).toBe(2);
    });
});
