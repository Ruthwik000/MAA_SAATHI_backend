// Simple ESP32 HTTPS Test for Render Backend
#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiClientSecure.h>

const char* ssid = "Hotspot";
const char* password = "12345678";
const char* serverUrl = "https://maa-saathi-backend.onrender.com/health";

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("\n\n=== ESP32 HTTPS Connection Test ===\n");
  
  // Connect to WiFi
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\n✅ WiFi Connected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
  
  // Test HTTPS connection
  Serial.println("\n--- Testing HTTPS Connection ---");
  testHTTPS();
}

void loop() {
  // Test every 30 seconds
  delay(30000);
  testHTTPS();
}

void testHTTPS() {
  WiFiClientSecure *client = new WiFiClientSecure;
  
  if(client) {
    // Skip certificate validation
    client->setInsecure();
    client->setTimeout(15);
    
    HTTPClient https;
    
    Serial.println("🔗 Connecting to: " + String(serverUrl));
    
    if (https.begin(*client, serverUrl)) {
      https.setTimeout(20000);
      https.setConnectTimeout(10000);
      
      Serial.println("⏳ Sending GET request...");
      int httpCode = https.GET();
      
      Serial.printf("📊 HTTP Response Code: %d\n", httpCode);
      
      if (httpCode > 0) {
        String payload = https.getString();
        Serial.println("📥 Response:");
        Serial.println(payload);
        
        if(httpCode == 200) {
          Serial.println("✅ SUCCESS! Backend is reachable!");
        }
      } else {
        Serial.printf("❌ Error: %d - %s\n", httpCode, https.errorToString(httpCode).c_str());
        
        if(httpCode == -1) {
          Serial.println("\n💡 Troubleshooting:");
          Serial.println("   1. Check if backend is awake (visit URL in browser)");
          Serial.println("   2. ESP32 may need root CA certificate");
          Serial.println("   3. Try updating ESP32 WiFi library");
        }
      }
      
      https.end();
    } else {
      Serial.println("❌ Unable to begin HTTPS connection");
    }
    
    delete client;
  }
  
  Serial.println("\n" + String("=").substring(0, 40) + "\n");
}
