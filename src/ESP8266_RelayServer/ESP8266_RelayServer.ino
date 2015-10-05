#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

const char* ssid = "linksys";
const char* password = "somerlotsomerlot";
MDNSResponder mdns;
ESP8266WebServer server(80);

int myPins[] = {0,2,4,5,12,13,14,15,16};
int myPin;
int i;
String sPin;
String sUrl;
const char cUrl;

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
    myPin = myPins[i];
    sPin = String(i);
    
    sUrl = "/relay" + sPin + "On";
    cUrl = sUrl.c_str();
    
    server.on(&cUrl, [](){
      server.send(200, "text/plain", "Relay " + sPin + " is on");
      digitalWrite(myPin, 0);
    });

    sUrl = "/relay" + sPin + "Off";
    cUrl = sUrl.c_str();
    
    server.on(&cUrl, [](){
      server.send(200, "text/plain", "Relay " + sPin + " is off");
      digitalWrite(myPin, 1);
    });
  }

  server.onNotFound(handleNotFound);
  
  server.begin();
  Serial.println("HTTP server started");
}
 
void loop(void){
  server.handleClient();
}

