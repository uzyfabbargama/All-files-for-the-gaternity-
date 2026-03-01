//lógica completa de la nuanot

module nuanot_sumador_completo(
    input [7:0] a, // Entrada de 8 bits
    input [7:0] b, // Entrada de 8 bits
    input [2:0] i, // La nitenle de 3 bits
    output [7:0] sum, // Salida de 8 bits
    output carry_out // Salida de acarreo (carry out),
    output carry_memory,
    input eraser
);
    // Declaración de los cables de acarreo (carry wires)
    // El tamaño del array es 7, ya que hay 7 acarreos entre los 8 bits.
    wire [10:0] carry;

    // ----- Lógica del sumador bit a bit (conectada en cadena) -----
    // Bit 0 (el bit menos significativo)
    // El acarreo de entrada (carry_in) es 0 para el primer bit.
    assign sum[0] = a[0] ^ b[0];
    assign carry[0] = a[0] & b[0];

    // Bit 1
    // La suma es el XOR de los dos bits y el acarreo de entrada.
    // El acarreo de salida es el OR de los ANDs.
    assign sum[1] = a[1] ^ b[1] ^ carry[0];
    assign carry[1] = (a[1] & b[1]) | (a[1] & carry[0]) | (b[1] & carry[0]);

    // Bit 2
    assign sum[2] = a[2] ^ b[2] ^ carry[1];
    assign carry[2] = (a[2] & b[2]) | (a[2] & carry[1]) | (b[2] & carry[1]);
    
    // Bit 3
    assign sum[3] = a[3] ^ b[3] ^ carry[2];
    assign carry[3] = (a[3] & b[3]) | (a[3] & carry[2]) | (b[3] & carry[2]);

    // Bit 4
    assign sum[4] = a[4] ^ b[4] ^ carry[3];
    assign carry[4] = (a[4] & b[4]) | (a[4] & carry[3]) | (b[4] & carry[3]);

    // Bit 5
    assign sum[5] = a[5] ^ b[5] ^ carry[4];
    assign carry[5] = (a[5] & b[5]) | (a[5] & carry[4]) | (b[5] & carry[4]);

    // Bit 6
    assign sum[6] = a[6] ^ b[6] ^ carry[5];
    assign carry[6] = (a[6] & b[6]) | (a[6] & carry[5]) | (b[6] & carry[5]);

    // Bit 7 (el bit más significativo)
    assign sum[7] = a[7] ^ b[7] ^ carry[6];
    assign carry[7] = (a[7] & b[7]) | (a[7] & carry[6]) | (b[7] & carry[6]);

    // Bit 8 (comenzamos los Nitenles)
    assign sum[8] = i[0] ^ carry[7];
    assign carry[8] = i[0] & carry[7];

    //Bit 9 (ahora colocamos la memoria)
    assign sum[9] = i[1] ^ carry[8]
    assign carry[9] = i[1] & carry[8];
    assign carry_memory = (~sum[9] ^ sum[9]) | ((~sum[9] ^ sum[9]) ^ eraser);

    //Bit 10 (último bit)
    assign sum[10] = i[2] ^ carry[9];
    assign carry[10] = 1[2] & carry[9];

    // El acarreo final del sumador de 11 bits es el acarreo del último bit.
    assign carry_out = carry[10];
endmodule

// ----- Módulo de prueba (Testbench) para el sumador de 8 bits -----
module nuanot_sumador_tb;

    // Declaración de las señales de entrada y salida
    reg [7:0] a, b;
    reg [2:0] i;
    reg eraser;
    wire [7:0] sum;
    wire carry_out;
    mire carry_memory

    // Instancia del sumador completo (Unit Under Test)
    nuanot_sumador_completo UUT (
        .a(a),
        .b(b),
        .i(i),
        .sum(sum),
        .carry_out(carry_out),
        .carry_memory(carry_memory)
    );

    // Bloque de inicialización para la simulación
    initial begin
        // Inicializar las entradas
        a = 8'b00000000;
        b = 8'b00000000;
        i = 3'b000;
        eraser = 1'b0;
        // Mostrar el encabezado de la simulación
        $monitor("Tiempo=%t, a=%b, b=%b, suma=%b, acarreo_salida=%b", $time, a, b, sum, carry_out);

        // Casos de prueba
        //comparar dos números, ¿20 < 50?
        #10 a = 8'b11101011; b = 8'b00110010; i = 3'b011 //esto redirecciona la comparación a la memoria
    end

endmodule