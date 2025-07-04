#include WiFi.h
#include ESPAsyncWebServer.h
#include DHT.h

#define DHTPIN 13           Pin connected to the DATA pin of DHT22
#define DHTTYPE DHT22       Define the type of DHT sensor

DHT dht(DHTPIN, DHTTYPE);

const char ssid = ITD-AI;
const char password = ITD#RInno;

AsyncWebServer server(80);

void setup() {
  Serial.begin(115200);
  dht.begin();

   Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print(Connecting to WiFi);
  
  int retries = 0;
  while (WiFi.status() != WL_CONNECTED && retries  20) {  retry for about 10 seconds
    delay(500);
    Serial.print(.);
    retries++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println(nConnected to WiFi);
    Serial.print(IP Address );
    Serial.println(WiFi.localIP());
  } else {
    Serial.println(nFailed to connect to WiFi);
    return;  Exit setup if the connection fails
  }

   Serve the web page
  server.on(, HTTP_GET, [](AsyncWebServerRequest request){
    String html = htmlbody;
    html += h1ESP32 DHT22 Web Serverh1;
    html += pTemperature  + String(dht.readTemperature()) +  &deg;Cp;
    html += pHumidity  + String(dht.readHumidity()) +  %p;
    html += bodyhtml;
    request-send(200, texthtml, html);
  });

   Start server
  server.begin();
}

void loop() {
   Nothing needed here, the server is asynchronous
}