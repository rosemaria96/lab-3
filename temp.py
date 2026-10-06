#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

// WiFi credentials
const char* ssid = ""; 
const char* password = "";

// MQTT Broker settings
const char* mqtt_server = "broker.hivemq.com";  // e.g., "192.168.1.100" or "broker.hivemq.com"
const int mqtt_port = 1883;  // Standard MQTT port (1883 for non-encrypted, 8883 for encrypted)

// DHT sensor setup
#define DHTPIN 4          // GPIO4 (D4 pin on ESP32)
#define DHTTYPE DHT22     // DHT22 (AM2302) or DHT11
DHT dht(DHTPIN, DHTTYPE);

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to WiFi: ");
  Serial.println(ssid);
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 30) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  Serial.println();
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("WiFi connected!");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
    Serial.print("Signal strength (RSSI): ");
    Serial.println(WiFi.RSSI());
  } else {
    Serial.println("WiFi connection FAILED!");
    Serial.print("Status: ");
    Serial.println(WiFi.status());
  }
}

// void setup_wifi() {
//   delay(10);
//   Serial.println();
//   Serial.print("Connecting to WiFi: ");
//   Serial.println(ssid);
  
//   WiFi.begin(ssid, password);
  
//   int attempts = 0;
//   while (WiFi.status() != WL_CONNECTED && attempts < 20) {
//     delay(500);
//     Serial.print(".");
//     attempts++;
//   }
  
//   Serial.println();
//   Serial.println("WiFi connected");
//   Serial.print("IP address: ");
//   Serial.println(WiFi.localIP());
// }

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    
    // Create a random client ID
    String clientId = "ESP32-";
    clientId += String(random(0xffff), HEX);
    
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  dht.begin();
  
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  
  // Read sensor data every 2 seconds
  delay(2000);
  
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  
  // Check if readings are valid
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  
  // Convert to strings
  String temp_str = String(temperature, 2);
  String humidity_str = String(humidity, 2);
  
  // Publish to MQTT topics
  client.publish("home/sensors/temperature", temp_str.c_str());
  client.publish("home/sensors/humidity", humidity_str.c_str());
  
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print("°C, Humidity: ");
  Serial.print(humidity);
  Serial.println("%");
}