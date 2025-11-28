#include "Adafruit_MCP23X17.h"

Adafruit_MCP23X17 mcp;
Adafruit_MCP23X17 mcp2;

char texto[32] = {0};   // array para guardar os caracteres recebidos
const int num_carac = 4; // máximo de caracteres que o dispositivo consegue mostrar
int progresso = 0, cortes = 0, resto = 0;
String lastMeg = "";

//const int letras[num_carac][6] = { {2, 3, 4, 5, 6, 7}, {8, 9, 10, 0, 12, 13},{2, 3, 4, 5, 6, 7}, {8, 9, 10, 11, 12, 13} };
const int letras[num_carac][6] = {{7, 6, 5, 4, 3, 2}, {8, 9, 10, 11, 12, 13}, {8,11,10,9,12,13},  {2, 3, 4, 5, 6, 7}};

void setup() {
	Serial.begin(9600);

	if (!mcp.begin_I2C(0x24)) {
		Serial.println("Falha ao inicializar o MCP23017 1!");
		while (1);
	}
	Serial.println("MCP23017 1 inicializado com sucesso.");

	if (!mcp2.begin_I2C(0x20)) {
		Serial.println("Falha ao inicializar o MCP23017 2!");
		while (1);
	}
	Serial.println("MCP23017 2 inicializado com sucesso.");

	for (int p = 2; p <= 13; p++) {
		mcp.pinMode(p, OUTPUT);
		 mcp2.pinMode(p, OUTPUT);
	}
	pinMode(2, INPUT);

	// desliga os pinos do caractere
	for (int i = 0; i < num_carac; i++) {
		for (int j = 0; j < 6; j++) {
			mcp.digitalWrite(letras[i][j], LOW);
			mcp2.digitalWrite(letras[i][j], LOW);
		}
	}
}

void loop() {
	if (Serial.available()) {
		
		String msgRecebida = Serial.readStringUntil('\n');
		if(msgRecebida != ""){
			
// aaaaaaaaaaaaaaaaaaa
		// LIMPAR espaços/brancos
		msgRecebida.trim();

		if (msgRecebida == lastMeg) {
			Serial.println("DESCARTADO (mensagem repetida)");
			return;
		}

		// VERIFICAR parecidas (ex: aberto ~ aberta)
		if (saoParecidas(msgRecebida, lastMeg)) {
			Serial.println("DESCARTADO (mensagem parecida demais)");
			return;
		}
//aaaaaaaaaaaaaaa

		Serial.print("Recebido: ");
		Serial.println(msgRecebida);
		msgRecebida.toCharArray(texto, sizeof(texto));

		cortes = msgRecebida.length() / num_carac; //quantos grupos de 4 letra existem na palavras
		resto = msgRecebida.length() % 4; // resto das letra que não fecha um grupo de 4 letras

			if (msgRecebida.length() > 0) {
				lastMeg = msgRecebida; //armazena a última mensagem
				if(msgRecebida.length() <= 4){
					for (int i = 0; i < msgRecebida.length(); i++) {
						char c = texto[i];
						Serial.print("Letra atual: ");
						Serial.println(c);
						switchMcp(c, i);
						}
						memset(texto, 0, sizeof(texto));				
				}
				else{
					for(int j = 0; j < cortes; j++){
						for (int i = 0; i < 4; i++) {
						char c = texto[i + (4*j)];
						Serial.print("Letra atual: ");
						Serial.println(c);
						switchMcp(c, i);
						}
					}	
					for (int i = 0; i < resto; i++) {
						char c = texto[i + (4*cortes)];
						Serial.print("Letra atual: ");
						Serial.println(c);
						switchMcp(c, i);
					}
						memset(texto, 0, sizeof(texto));		
				}
			}

		
		}
		else{
			Serial.print("Nada recebido/erro no serial");
			delay(1000);
		}

	}else{
	Serial.print("Erro na conexão raspberry");
  }

	if(digitalRead(2) == HIGH && lastMeg != ""){
      lastMeg.toCharArray(texto, sizeof(texto));

				cortes = lastMeg.length() / num_carac; //quantos grupos de 4 letra existem na palavras
				resto = lastMeg.length() % 4; // resto das letra que não fecha um grupo de 4 letras

					if(lastMeg.length() <= 4){
					for (int i = 0; i < lastMeg.length(); i++) {
						char c = texto[i];
						Serial.print("Letra atual: ");
						Serial.println(c);
						switchMcp(c, i);
						}
						memset(texto, 0, sizeof(texto));				
				}
				else{
					for(int j = 0; j < cortes; j++){
						for (int i = 0; i < 4; i++) {
						char c = texto[i + (4*j)];
						Serial.print("Letra atual: ");
						Serial.println(c);
						switchMcp(c, i);
						}
					}	
					for (int i = 0; i < resto; i++) {
						char c = texto[i + (4*cortes)];
						Serial.print("Letra atual: ");
						Serial.println(c);
						switchMcp(c, i);
					}
						memset(texto, 0, sizeof(texto));		
				}
  }
  else{ 
      Serial.println("Calma");
			delay(1000);
  }	
	
}

// 333333
bool saoParecidas(String a, String b) {
  if (abs((int)a.length() - (int)b.length()) > 1) return false;

  int dif = 0;
  int n = min(a.length(), b.length());

  for (int i = 0; i < n; i++) {
    if (a[i] != b[i]) dif++;
    if (dif > 1) return false;
  }

  return true;
}
// e333333

void switchMcp(char c, int f) {
	int i = f%4;
	if(f < 2){
		
				switch (c) {
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
					mcp.digitalWrite(letras[i][3], HIGH);
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
				default:
					break;
			}

			delay(2000); // tempo entre caracteres

			// desliga os pinos do caractere
			for (int j = 0; j < 6; j++) {
				mcp.digitalWrite(letras[i][j], LOW);
			}
			}else{
				switch (c) {
				case 'a':
					mcp2.digitalWrite(letras[i][0], HIGH);
					break;

				case 'b':
					mcp2.digitalWrite(letras[i][0], HIGH);
					mcp2.digitalWrite(letras[i][2], HIGH);
					break;

				case 'c':
					mcp2.digitalWrite(letras[i][0], HIGH);
					mcp2.digitalWrite(letras[i][1], HIGH);
					break;

				case 'd':
					mcp2.digitalWrite(letras[i][0], HIGH);
					mcp2.digitalWrite(letras[i][1], HIGH);
					mcp2.digitalWrite(letras[i][3], HIGH);
					break;

				case 'e':
					mcp2.digitalWrite(letras[i][0], HIGH);
					mcp2.digitalWrite(letras[i][3], HIGH);
					break;

				case 'f':
					mcp2.digitalWrite(letras[i][0], HIGH);
					mcp2.digitalWrite(letras[i][1], HIGH);
					mcp2.digitalWrite(letras[i][2], HIGH);
					break;

				case 'g':
					mcp2.digitalWrite(letras[i][0], HIGH);
					mcp2.digitalWrite(letras[i][1], HIGH);
					mcp2.digitalWrite(letras[i][2], HIGH);
					mcp2.digitalWrite(letras[i][3], HIGH);
					break;

				case 'h':
					mcp2.digitalWrite(letras[i][0], HIGH);
					mcp2.digitalWrite(letras[i][2], HIGH);
					mcp2.digitalWrite(letras[i][3], HIGH);
					break;

				case 'i':
					mcp2.digitalWrite(letras[i][1], HIGH);
					mcp2.digitalWrite(letras[i][2], HIGH);
					break;

				case 'j':
					mcp2.digitalWrite(letras[i][1], HIGH);
					mcp2.digitalWrite(letras[i][2], HIGH);
					mcp2.digitalWrite(letras[i][3], HIGH);
					break;

				case 'k':
					mcp2.digitalWrite(letras[i][0], HIGH);
					mcp2.digitalWrite(letras[i][4], HIGH);
					break;

				case 'l':
					mcp2.digitalWrite(letras[i][0], HIGH);
					mcp2.digitalWrite(letras[i][2], HIGH);
					mcp2.digitalWrite(letras[i][4], HIGH);
					break;

				case 'm':
					mcp2.digitalWrite(letras[i][0], HIGH);
					mcp2.digitalWrite(letras[i][1], HIGH);
					mcp2.digitalWrite(letras[i][4], HIGH);
					break;

				case 'n':
					mcp2.digitalWrite(letras[i][0], HIGH);
					mcp2.digitalWrite(letras[i][1], HIGH);
					mcp2.digitalWrite(letras[i][3], HIGH);
					mcp2.digitalWrite(letras[i][4], HIGH);
					break;

				case 'o':
					mcp2.digitalWrite(letras[i][0], HIGH);
					mcp2.digitalWrite(letras[i][3], HIGH);
					mcp2.digitalWrite(letras[i][4], HIGH);
					break;

				case 'p':
					mcp2.digitalWrite(letras[i][0], HIGH);
					mcp2.digitalWrite(letras[i][1], HIGH);
					mcp2.digitalWrite(letras[i][2], HIGH);
					mcp2.digitalWrite(letras[i][4], HIGH);
					break;

				case 'q':
					mcp2.digitalWrite(letras[i][0], HIGH);
					mcp2.digitalWrite(letras[i][1], HIGH);
					mcp2.digitalWrite(letras[i][2], HIGH);
					mcp2.digitalWrite(letras[i][3], HIGH);
					mcp2.digitalWrite(letras[i][4], HIGH);
					break;

				case 'r':
					mcp2.digitalWrite(letras[i][0], HIGH);
					mcp2.digitalWrite(letras[i][2], HIGH);
					mcp2.digitalWrite(letras[i][3], HIGH);
					mcp2.digitalWrite(letras[i][4], HIGH);
					break;

				case 's':
					mcp2.digitalWrite(letras[i][1], HIGH);
					mcp2.digitalWrite(letras[i][2], HIGH);
					mcp2.digitalWrite(letras[i][4], HIGH);
					break;

				case 't':
					mcp2.digitalWrite(letras[i][1], HIGH);
					mcp2.digitalWrite(letras[i][2], HIGH);
					mcp2.digitalWrite(letras[i][3], HIGH);
					mcp2.digitalWrite(letras[i][4], HIGH);
					break;

				case 'u':
					mcp2.digitalWrite(letras[i][0], HIGH);
					mcp2.digitalWrite(letras[i][4], HIGH);
					mcp2.digitalWrite(letras[i][5], HIGH);
					break;

				case 'v':
					mcp2.digitalWrite(letras[i][0], HIGH);
					mcp2.digitalWrite(letras[i][2], HIGH);
					mcp2.digitalWrite(letras[i][4], HIGH);
					mcp2.digitalWrite(letras[i][5], HIGH);
					break;

				case 'x':
					mcp2.digitalWrite(letras[i][0], HIGH);
					mcp2.digitalWrite(letras[i][1], HIGH);
					mcp2.digitalWrite(letras[i][4], HIGH);
					mcp2.digitalWrite(letras[i][5], HIGH);
					break;

				case 'y':
					mcp2.digitalWrite(letras[i][0], HIGH);
					mcp2.digitalWrite(letras[i][1], HIGH);
					mcp2.digitalWrite(letras[i][3], HIGH);
					mcp2.digitalWrite(letras[i][4], HIGH);
					mcp2.digitalWrite(letras[i][5], HIGH);
					break;

				case 'z':
					mcp2.digitalWrite(letras[i][0], HIGH);
					mcp2.digitalWrite(letras[i][3], HIGH);
					mcp2.digitalWrite(letras[i][4], HIGH);
					mcp2.digitalWrite(letras[i][5], HIGH);
					break;
				default:
					break;
			}

			delay(2000); // tempo entre caracteres

			// desliga os pinos do caractere
			for (int j = 0; j < 6; j++) {
				mcp2.digitalWrite(letras[i][j], LOW);
			}
		}
}