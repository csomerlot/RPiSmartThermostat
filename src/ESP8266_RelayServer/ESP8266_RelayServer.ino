#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

const char* ssid = "linksys";
const char* password = "somerlotsomerlot";
MDNSResponder mdns;
ESP8266WebServer server(80);

int myPins[] = {0,2,4,5,12,13,14,15,16};
int i;
String webString="";     // String to display

void handleRoot() {
  server.send(200, "text/plain", "hello from esp8266!");
}

void handleNotFound(){
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET)?"GET":"POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i=0; i<server.args(); i++){
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);
}
 
void setup(void){

  for (i = 0; i < 10; i = i + 1) {
    pinMode(myPins[i],  OUTPUT);
  }
  
  Serial.begin(9600);
  WiFi.begin(ssid, password);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    for (i = 0; i < 10; i = i + 1) {
      digitalWrite(myPins[i], 1);
    }
    
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  
  if (mdns.begin("esp8266", WiFi.localIP())) {
    Serial.println("MDNS responder started");
  }
  
  server.on("/", handleRoot);
  
  server.on("/relay0Off", [](){
    server.send(200, "text/plain", "Relay 0 is off");
    digitalWrite(myPins[0], 1);
  });
  server.on("/relay1Off", [](){
    server.send(200, "text/plain", "Relay 1 is off");
    digitalWrite(myPins[1], 1);
  });
  server.on("/relay2Off", [](){
    server.send(200, "text/plain", "Relay 2 is off");
    digitalWrite(myPins[2], 1);
  });
  server.on("/relay3Off", [](){
    server.send(200, "text/plain", "Relay 3 is off");
    digitalWrite(myPins[3], 1);
  });
  server.on("/relay4Off", [](){
    server.send(200, "text/plain", "Relay 4 is off");
    digitalWrite(myPins[4], 1);
  });
  server.on("/relay5Off", [](){
    server.send(200, "text/plain", "Relay 5 is off");
    digitalWrite(myPins[5], 1);
  });
  server.on("/relay6Off", [](){
    server.send(200, "text/plain", "Relay 6 is off");
    digitalWrite(myPins[6], 1);
  });
  server.on("/relay7Off", [](){
    server.send(200, "text/plain", "Relay 7 is off");
    digitalWrite(myPins[7], 1);
  });
  server.on("/relay8Off", [](){
    server.send(200, "text/plain", "Relay 8 is off");
    digitalWrite(myPins[8], 1);
  });

  server.on("/relay0On", [](){
    server.send(200, "text/plain", "Relay 0 is on");
    digitalWrite(myPins[0], 0);
  });
  server.on("/relay1On", [](){
    server.send(200, "text/plain", "Relay 1 is on");
    digitalWrite(myPins[1], 0);
  });
  server.on("/relay2On", [](){
    server.send(200, "text/plain", "Relay 2 is on");
    digitalWrite(myPins[2], 0);
  });
  server.on("/relay3On", [](){
    server.send(200, "text/plain", "Relay 3 is on");
    digitalWrite(myPins[3], 0);
  });
  server.on("/relay4On", [](){
    server.send(200, "text/plain", "Relay 4 is on");
    digitalWrite(myPins[4], 0);
  });
  server.on("/relay5On", [](){
    server.send(200, "text/plain", "Relay 5 is on");
    digitalWrite(myPins[5], 0);
  });
  server.on("/relay6On", [](){
    server.send(200, "text/plain", "Relay 6 is on");
    digitalWrite(myPins[6], 0);
  });
  server.on("/relay7On", [](){
    server.send(200, "text/plain", "Relay 7 is on");
    digitalWrite(myPins[7], 0);
  });
  server.on("/relay8On", [](){
    server.send(200, "text/plain", "Relay 8 is on");
    digitalWrite(myPins[8], 0);
  });

  server.onNotFound(handleNotFound);
  
  server.begin();
  Serial.println("HTTP server started");
}
 
void loop(void){
  server.handleClient();
}

