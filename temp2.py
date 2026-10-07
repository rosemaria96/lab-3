#include <DHT.h>
 
#define DHT_PIN 18
#define DHT_TYPE DHT22
 
DHT dht(DHT_PIN, DHT_TYPE);
 
void setup() {
  Serial.begin(115200);
  dht.begin();
}
 
void loop() {
 
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" °C");
 
  delay(2000);
}

