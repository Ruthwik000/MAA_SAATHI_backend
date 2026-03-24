// TEST VERSION - Use local backend first to verify everything works
// Then we'll fix the HTTPS issue

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* WIFI_SSID = "Hotspot";
const char* WIFI_PASSWORD = "12345678";

// TEST WITH LOCAL BACKEND FIRST
const char* API_BASE_URL = "http://192.168.43.1:8000";  // Your local backend
const char* PATIENT_ID = "patient_demo";
const char* DOCTOR_NUMBER = "+918328217825";
const char* FAMILY_NUMBER = "+918328217825";

#define BUTTON_PIN 14
volatile bool sosTriggered = false;

void IRAM_ATTR handleSOS() {
  sosTriggered = true;
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), handleSOS, FALLING);
  
  Serial.println("\n=== VitalSync Ring - Local Test ===\n");
  
  // Connect to WiFi
  Serial.print("Connecting to WiFi");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\n✅ WiFi Connected!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
  Serial.println("\nPress SOS button to test...\n");
}

void loop() {
  if (sosTriggered) {
    Serial.println("\n🚨 SOS BUTTON PRESSED!");
    sendEmergencyAlert();
    sosTriggered = false;
    delay(2000);
  }
  delay(100);
}

void sendEmergencyAlert() {
  HTTPClient http;
  String url = String(API_BASE_URL) + "/api/v1/emergency/sos";
  
  Serial.println("🔗 URL: " + url);
  
  http.begin(url);
  http.addHeader("Content-Type", "application/json");
  http.setTimeout(10000);
  
  StaticJsonDocument<512> doc;
  doc["patientId"] = PATIENT_ID;
  doc["type"] = "MANUAL_SOS";
  doc["severity"] = "HIGH";
  
  JsonObject location = doc.createNestedObject("location");
  location["lat"] = 28.6139;
  location["lng"] = 77.2090;
  
  doc["doctorNumber"] = DOCTOR_NUMBER;
  JsonArray familyNumbers = doc.createNestedArray("familyNumbers");
  familyNumbers.add(FAMILY_NUMBER);
  
  String payload;
  serializeJson(doc, payload);
  
  Serial.println("📤 Sending:");
  Serial.println(payload);
  
  int httpCode = http.POST(payload);
  
  Serial.printf("\n📊 Response Code: %d\n", httpCode);
  
  if(httpCode > 0) {
    String response = http.getString();
    Serial.println("📥 Response:");
    Serial.println(response);
    
    if(httpCode == 200) {
      Serial.println("\n✅✅✅ SUCCESS! Alert sent!");
      Serial.println("📱 Check your phone for SMS + Call!");
    }
  } else {
    Serial.printf("❌ Error: %d - %s\n", httpCode, http.errorToString(httpCode).c_str());
  }
  
  http.end();
}
