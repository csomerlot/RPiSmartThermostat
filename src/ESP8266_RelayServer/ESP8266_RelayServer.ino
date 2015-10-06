#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

const char* ssid = "linksys";
const char* password = "somerlotsomerlot";
MDNSResponder mdns;
ESP8266WebServer server(80);

int myPins[] = {0,2,4,5,12,13,14,15,16};
const char* pathOn[] = {"/r0on", "/r1on", "/r2on", "/r3on", "/r4on", "/r5on", "/r6on", "/r7on", "/r8on" };
const char* pathOff[] = {"/r0off", "/r1off", "/r2off", "/r3off", "/r4off", "/r5off", "/r6off", "/r7off", "/r8off" };

int i;
String sPin;

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

  for (i = 0; i < 9; i = i + 1) {
    pinMode(myPins[i],  OUTPUT);
  }
  
  Serial.begin(9600);
  WiFi.begin(ssid, password);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    for (i = 0; i < 9; i = i + 1) {
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

  for (i = 0; i < 9; i = i + 1) {
    sPin = String(i);
    Serial.println(sPin);
    Serial.println(myPins[i]);
    Serial.println(pathOn[i]);
    Serial.println(pathOff[i]);
    Serial.println("\n");
    
    server.on(pathOn[i], [](){
      server.send(200, "text/plain", "Relay " + sPin + " is on");
      digitalWrite(myPins[i], 0);
    });

    server.on(pathOff[i], [](){
      server.send(200, "text/plain", "Relay " + sPin + " is off");
      digitalWrite(myPins[i], 1);
    });
  }

  server.onNotFound(handleNotFound);
  
  server.begin();
  Serial.println("HTTP server started");
}
 
void loop(void){
  server.handleClient();
}

