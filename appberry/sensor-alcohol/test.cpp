// #include <pic18f2550.h>
#fuses xt, nowdt
#use delay(crystal = 4000000)

// #use rs232(baud = 9600, xmit = PIN_c6, rcv = PIN_c7, stream = ZIGBEE, parity = N, bits = 8)
#use rs232(baud = 9600, xmit = PIN_D0, rcv = PIN_D1, stream = SENSOR, parity = N, bits = 8)

void main()
{
    char status[] =
        "\xFF\x01\x85\x00\x00\x00\x00\x00\x7A";
    fprintf(SENSOR, "%x", status); // Muestra el Caracter recibido en el PC
}