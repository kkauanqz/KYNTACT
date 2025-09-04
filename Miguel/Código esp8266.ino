#include "Adafruit_MCP23X17.h"
Adafruit_MCP23X17 mcp;

String frase = "du";  //Armazena a mensagem
//d = 2 5 6 (pinos 23, 26, 27)
//u = 8 10 13 (pinos 1, 3, 6)
char* carac;  // Guarda os caracteres da mensagem

const int num_carac = 2;  //Armazena o número de caracters do dispositivo

const int letras[num_carac][6] = { { 2, 5, 3, 6, 4, 7 }, { 8, 11, 9, 12, 10, 13 } };  //Armazenas as portas digitais dos solenoides que formam os caracteres em braille

uint16_t estado = 0;  // representa os 16 pinos do MCP (A0..A7, B0..B7)

void setup() {
  Serial.begin(9600);
  if (!mcp.begin_I2C(0x20)) {
    Serial.println("Falha ao inicializar o MCP23017!");
    while (1)
      ;
  }
  Serial.println("MCP23017 inicializado com sucesso.");

  //Declaração dos pinos do mcp
  mcp.pinMode(2, OUTPUT);
  mcp.pinMode(3, OUTPUT);
  mcp.pinMode(4, OUTPUT);
  mcp.pinMode(5, OUTPUT);
  mcp.pinMode(6, OUTPUT);
  mcp.pinMode(7, OUTPUT);
  mcp.pinMode(8, OUTPUT);
  mcp.pinMode(9, OUTPUT);
  mcp.pinMode(10, OUTPUT);
  mcp.pinMode(11, OUTPUT);
  mcp.pinMode(12, OUTPUT);
  mcp.pinMode(13, OUTPUT);

  // Aloca dinamicamente um array de char com o tamanho da String
  // O +1 é para o caractere nulo ('\0') que indica o fim da string
  carac = new char[frase.length() + 1];

  //Transforma a Strign "frase" em um array de caracteres e salva em carac
  strcpy(carac, frase.c_str());
}

void loop() {
  //mcp.digitalWrite(letras[0][0],HIGH);
  // delay(10000);
  //mcp.digitalWrite(letras[0][0],LOW);
  /*
  mcp.digitalWrite(3,HIGH);
  mcp.digitalWrite(2,HIGH);
  delay(1000);
  mcp.digitalWrite(3,LOW);
  mcp.digitalWrite(2,LOW);
  delay(1000);
  */


  for (int i = 0; i < num_carac; i++) {
    switch (carac[i]) {

      case 'a':
        mcp.digitalWrite(letras[i][0], HIGH);
        break;

      case 'b':
        mcp.digitalWrite(letras[i][0], HIGH);
        mcp.digitalWrite(letras[i][2], HIGH);
        break;

      case 'c':
        mcp.digitalWrite(letras[i][0], HIGH);
        mcp.digitalWrite(letras[i][1], HIGH);
        break;

      case 'd':
        mcp.digitalWrite(letras[i][0], HIGH);
        mcp.digitalWrite(letras[i][1], HIGH);
        mcp.digitalWrite(letras[i][3], HIGH);
        break;

      case 'e':
        mcp.digitalWrite(letras[i][0], HIGH);
        mcp.digitalWrite(letras[i][2], HIGH);
        break;

      case 'f':
        mcp.digitalWrite(letras[i][0], HIGH);
        mcp.digitalWrite(letras[i][1], HIGH);
        mcp.digitalWrite(letras[i][2], HIGH);
        break;

      case 'g':
        mcp.digitalWrite(letras[i][0], HIGH);
        mcp.digitalWrite(letras[i][1], HIGH);
        mcp.digitalWrite(letras[i][2], HIGH);
        mcp.digitalWrite(letras[i][3], HIGH);
        break;

      case 'h':
        mcp.digitalWrite(letras[i][0], HIGH);
        mcp.digitalWrite(letras[i][2], HIGH);
        mcp.digitalWrite(letras[i][3], HIGH);
        break;

      case 'i':
        mcp.digitalWrite(letras[i][1], HIGH);
        mcp.digitalWrite(letras[i][2], HIGH);
        break;

      case 'j':
        mcp.digitalWrite(letras[i][1], HIGH);
        mcp.digitalWrite(letras[i][2], HIGH);
        mcp.digitalWrite(letras[i][3], HIGH);
        break;

      case 'k':
        mcp.digitalWrite(letras[i][0], HIGH);
        mcp.digitalWrite(letras[i][4], HIGH);
        break;

      case 'l':
        mcp.digitalWrite(letras[i][0], HIGH);
        mcp.digitalWrite(letras[i][2], HIGH);
        mcp.digitalWrite(letras[i][4], HIGH);
        break;

      case 'm':
        mcp.digitalWrite(letras[i][0], HIGH);
        mcp.digitalWrite(letras[i][1], HIGH);
        mcp.digitalWrite(letras[i][4], HIGH);
        break;

      case 'n':
        mcp.digitalWrite(letras[i][0], HIGH);
        mcp.digitalWrite(letras[i][1], HIGH);
        mcp.digitalWrite(letras[i][3], HIGH);
        mcp.digitalWrite(letras[i][4], HIGH);
        break;

      case 'o':
        mcp.digitalWrite(letras[i][0], HIGH);
        mcp.digitalWrite(letras[i][3], HIGH);
        mcp.digitalWrite(letras[i][4], HIGH);
        break;

      case 'p':
        mcp.digitalWrite(letras[i][0], HIGH);
        mcp.digitalWrite(letras[i][1], HIGH);
        mcp.digitalWrite(letras[i][2], HIGH);
        mcp.digitalWrite(letras[i][4], HIGH);
        break;

      case 'q':
        mcp.digitalWrite(letras[i][0], HIGH);
        mcp.digitalWrite(letras[i][1], HIGH);
        mcp.digitalWrite(letras[i][2], HIGH);
        mcp.digitalWrite(letras[i][3], HIGH);
        mcp.digitalWrite(letras[i][4], HIGH);
        break;

      case 'r':
        mcp.digitalWrite(letras[i][0], HIGH);
        mcp.digitalWrite(letras[i][2], HIGH);
        mcp.digitalWrite(letras[i][3], HIGH);
        mcp.digitalWrite(letras[i][4], HIGH);
        break;

      case 's':
        mcp.digitalWrite(letras[i][1], HIGH);
        mcp.digitalWrite(letras[i][2], HIGH);
        mcp.digitalWrite(letras[i][4], HIGH);
        break;

      case 't':
        mcp.digitalWrite(letras[i][1], HIGH);
        mcp.digitalWrite(letras[i][2], HIGH);
        mcp.digitalWrite(letras[i][3], HIGH);
        mcp.digitalWrite(letras[i][4], HIGH);
        break;

      case 'u':
        mcp.digitalWrite(letras[i][0], HIGH);
        mcp.digitalWrite(letras[i][4], HIGH);
        mcp.digitalWrite(letras[i][5], HIGH);
        break;

      case 'v':
        mcp.digitalWrite(letras[i][0], HIGH);
        mcp.digitalWrite(letras[i][2], HIGH);
        mcp.digitalWrite(letras[i][4], HIGH);
        mcp.digitalWrite(letras[i][5], HIGH);
        break;

      case 'x':
        mcp.digitalWrite(letras[i][0], HIGH);
        mcp.digitalWrite(letras[i][1], HIGH);
        mcp.digitalWrite(letras[i][4], HIGH);
        mcp.digitalWrite(letras[i][5], HIGH);
        break;

      case 'y':
        mcp.digitalWrite(letras[i][0], HIGH);
        mcp.digitalWrite(letras[i][1], HIGH);
        mcp.digitalWrite(letras[i][3], HIGH);
        mcp.digitalWrite(letras[i][4], HIGH);
        mcp.digitalWrite(letras[i][5], HIGH);
        break;

      case 'z':
        mcp.digitalWrite(letras[i][0], HIGH);
        mcp.digitalWrite(letras[i][3], HIGH);
        mcp.digitalWrite(letras[i][4], HIGH);
        mcp.digitalWrite(letras[i][5], HIGH);
        break;
    }
    Serial.print("Ligando led ");
    Serial.println(i + 1);
    delay(2000);

    Serial.print("Desligando led ");
    Serial.println(i + 1);
    // desliga os 6 pinos do caractere
    for (int j = 0; j < 6; j++) {
      mcp.digitalWrite(letras[i][j], LOW);
    }

    delay(1000);
  }
}
