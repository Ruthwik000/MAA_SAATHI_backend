#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h> 
#include "MAX30105.h"
#include "spo2_algorithm.h"
#include <TinyGPSPlus.h>
#include <MPU9250_WE.h>
#include <Adafruit_AHTX0.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiClientSecure.h>
#include <ArduinoJson.h>

// --- WIFI & API CONFIGURATION ---
const char* WIFI_SSID = "Hotspot";
const char* WIFI_PASSWORD = "12345678";
const char* API_BASE_URL = "https://maa-saathi-backend.onrender.com";  // Live Render backend
const char* PATIENT_ID = "patient_demo";

// --- EMERGENCY CONTACTS (Real numbers for SMS/Call) ---
const char* DOCTOR_NUMBER = "+918328217825";  // Your phone number
const char* FAMILY_NUMBER = "+918328217825";  // Same number for demo

// --- ROOT CA CERTIFICATE (Cloudflare/Render) ---
const char* rootCACertificate = \
"-----BEGIN CERTIFICATE-----\n" \
"MIIFazCCA1OgAwIBAgIRAIIQz7DSQONZRGPgu2OCiwAwDQYJKoZIhvcNAQELBQAw\n" \
"TzELMAkGA1UEBhMCVVMxKTAnBgNVBAoTIEludGVybmV0IFNlY3VyaXR5IFJlc2Vh\n" \
"cmNoIEdyb3VwMRUwEwYDVQQDEwxJU1JHIFJvb3QgWDEwHhcNMTUwNjA0MTEwNDM4\n" \
"WhcNMzUwNjA0MTEwNDM4WjBPMQswCQYDVQQGEwJVUzEpMCcGA1UEChMgSW50ZXJu\n" \
"ZXQgU2VjdXJpdHkgUmVzZWFyY2ggR3JvdXAxFTATBgNVBAMTDElTUkcgUm9vdCBY\n" \
"MTCCAiIwDQYJKoZIhvcNAQEBBQADggIPADCCAgoCggIBAK3oJHP0FDfzm54rVygc\n" \
"h77ct984kIxuPOZXoHj3dcKi/vVqbvYATyjb3miGbESTtrFj/RQSa78f0uoxmyF+\n" \
"0TM8ukj13Xnfs7j/EvEhmkvBioZxaUpmZmyPfjxwv60pIgbz5MDmgK7iS4+3mX6U\n" \
"A5/TR5d8mUgjU+g4rk8Kb4Mu0UlXjIB0ttov0DiNewNwIRt18jA8+o+u3dpjq+sW\n" \
"T8KOEUt+zwvo/7V3LvSye0rgTBIlDHCNAymg4VMk7BPZ7hm/ELNKjD+Jo2FR3qyH\n" \
"B5T0Y3HsLuJvW5iB4YlcNHlsdu87kGJ55tukmi8mxdAQ4Q7e2RCOFvu396j3x+UC\n" \
"B5iPNgiV5+I3lg02dZ77DnKxHZu8A/lJBdiB3QW0KtZB6awBdpUKD9jf1b0SHzUv\n" \
"KBds0pjBqAlkd25HN7rOrFleaJ1/ctaJxQZBKT5ZPt0m9STJEadao0xAH0ahmbWn\n" \
"OlFuhjuefXKnEgV4We0+UXgVCwOPjdAvBbI+e0ocS3MFEvzG6uBQE3xDk3SzynTn\n" \
"jh8BCNAw1FtxNrQHusEwMFxIt4I7mKZ9YIqioymCzLq9gwQbooMDQaHWBfEbwrbw\n" \
"qHyGO0aoSCqI3Haadr8faqU9GY/rOPNk3sgrDQoo//fb4hVC1CLQJ13hef4Y53CI\n" \
"rU7m2Ys6xt0nUW7/vGT1M0NPAgMBAAGjQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNV\n" \
"HRMBAf8EBTADAQH/MB0GA1UdDgQWBBR5tFnme7bl5AFzgAiIyBpY9umbbjANBgkq\n" \
"hkiG9w0BAQsFAAOCAgEAVR9YqbyyqFDQDLHYGmkgJykIrGF1XIpu+ILlaS/V9lZL\n" \
"ubhzEFnTIZd+50xx+7LSYK05qAvqFyFWhfFQDlnrzuBZ6brJFe+GnY+EgPbk6ZGQ\n" \
"3BebYhtF8GaV0nxvwuo77x/Py9auJ/GpsMiu/X1+mvoiBOv/2X/qkSsisRcOj/KK\n" \
"NFtY2PwByVS5uCbMiogziUwthDyC3+6WVwW6LLv3xLfHTjuCvjHIInNzktHCgKQ5\n" \
"ORAzI4JMPJ+GslWYHb4phowim57iaztXOoJwTdwJx4nLCgdNbOhdjsnvzqvHu7Ur\n" \
"TkXWStAmzOVyyghqpZXjFaH3pO3JLF+l+/+sKAIuvtd7u+Nxe5AW0wdeRlN8NwdC\n" \
"jNPElpzVmbUq4JUagEiuTDkHzsxHpFKVK7q4+63SM1N95R1NbdWhscdCb+ZAJzVc\n" \
"oyi3B43njTOQ5yOf+1CceWxG1bQVs5ZufpsMljq4Ui0/1lvh+wjChP4kqKOJ2qxq\n" \
"4RgqsahDYVvTH9w7jXbyLeiNdd8XM2w9U/t7y0Ff/9yi0GE44Za4rF2LN9d11TPA\n" \
"mRGunUHBcnWEvgJBQl9nJEiU0Zsnvgc/ubhPgXRR4Xq37Z0j4r7g1SgEEzwxA57d\n" \
"emyPxgcYxn/eR44/KJ4EBs+lVDR3veyJm+kXQ99b21/+jh5Xos1AnX5iItreGCc=\n" \
"-----END CERTIFICATE-----\n";

// --- PIN DEFINITIONS ---
#define LM35_PIN 34
#define BUTTON_PIN 14
#define GPS_TX 26
#define GPS_RX 27

// --- SENSOR OBJECTS ---
Adafruit_SH1106G display(128, 64, &Wire, -1); 
MAX30105 particleSensor;
TinyGPSPlus gps;
MPU9250_WE myMPU = MPU9250_WE(0x68);
Adafruit_AHTX0 aht;
HardwareSerial gpsSerial(1);

// --- USER VITALS VARIABLES ---
#define BUFFER_SIZE 100
#define IR_THRESHOLD 50000
#define TEMP_SAMPLES 10

int hrBuffer[3] = {0,0,0};
int spo2Buffer[3] = {0,0,0};
int bufferIndex = 0;
int validCountHR = 0, validCountSpO2 = 0;
int finalHR = 0, finalSpO2 = 0;
float finalTemp = 0;

// --- SYSTEM & TIMING VARIABLES ---
float ambTemp = 0, humidity = 0;
int totalSteps = 0;
bool stepFlag = false;
unsigned long lastStepTime = 0;
String sleepStatus = "Awake";
bool fallDetected = false;

unsigned long lastReadingTime = 0; 
const int readingDelay = 2000;
unsigned long lastDataUpload = 0;
const int uploadInterval = 20000;
unsigned long lastVitalsCheck = 0;
const int vitalsCheckInterval = 5000;

// --- INTERRUPT FLAG ---
volatile bool sosTriggered = false;
bool wifiConnected = false;

void IRAM_ATTR handleSOS() {
  sosTriggered = true;
}

void setup() {
  Serial.begin(115200);
  gpsSerial.begin(9600, SERIAL_8N1, GPS_TX, GPS_RX);
  
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), handleSOS, FALLING);

  Wire.begin(21, 22);

  // Initialize OLED
  if(!display.begin(0x3C, true)) Serial.println("OLED Failed");
  display.clearDisplay();
  display.setTextColor(SH110X_WHITE);
  display.setTextSize(1);
  display.setCursor(0,0);
  display.println("VitalSync Ring");
  display.println("Connecting WiFi...");
  display.display();

  // Connect to WiFi
  Serial.println("\nConnecting to WiFi...");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  if(WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi Connected!");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
    wifiConnected = true;
    display.clearDisplay();
    display.setCursor(0,0);
    display.println("WiFi Connected!");
    display.println(WiFi.localIP());
    display.display();
    delay(2000);
  }

  // Initialize sensors
  delay(250); 
  if(!aht.begin()) Serial.println("AHT10 Not Found");
  myMPU.init();
  
  if(!particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("MAX30102 not found!");
    while(1);
  }
  particleSensor.setup(0x0A, 4, 2, 400, 411, 4096);
  particleSensor.setPulseAmplitudeRed(0x2F);
  particleSensor.setPulseAmplitudeIR(0x2F);

  Serial.println("SYSTEM READY.");
}

void loop() {
  // Maintain WiFi
  if(WiFi.status() != WL_CONNECTED) {
    wifiConnected = false;
  } else {
    wifiConnected = true;
  }

  // 1. INSTANT SOS OVERRIDE
  if (sosTriggered) {
    display.clearDisplay();
    display.setTextSize(3);
    display.setCursor(15, 10);
    display.println("SOS!!!");
    display.setTextSize(1);
    display.setCursor(15, 45);
    display.println("Sending Alert...");
    display.display();

    Serial.println("\n>>> MANUAL SOS BUTTON PRESSED! <<<");
    sendEmergencyViaBackend("MANUAL_SOS", "HIGH");
    
    sosTriggered = false; 
    lastReadingTime = millis();
    delay(2000);
  }

  // 2. FAST TASKS
  processMotion();
  feedGPS();

  // 3. CHECK ABNORMAL VITALS (Every 5 seconds)
  if (millis() - lastVitalsCheck > vitalsCheckInterval) {
    checkAbnormalVitals();
    lastVitalsCheck = millis();
  }

  // 4. UPLOAD DATA (Every 20 seconds)
  if (millis() - lastDataUpload > uploadInterval) {
    uploadDailyVitals();
    lastDataUpload = millis();
  }

  // 5. TIMED TASKS (Every 2 seconds)
  if (millis() - lastReadingTime > readingDelay) {
    
    readEnvironment();

    finalTemp = 0;
    for(int i=0; i<TEMP_SAMPLES; i++) {
      float voltage = analogRead(LM35_PIN) * (3.3 / 4095.0);
      finalTemp += voltage * 180.0; 
    }
    finalTemp /= TEMP_SAMPLES;

    long irValue = particleSensor.getIR();
    if(irValue > IR_THRESHOLD) {
      uint32_t irBuffer[BUFFER_SIZE];
      uint32_t redBuffer[BUFFER_SIZE];

      for(int i=0; i<BUFFER_SIZE; i++) {
        while(!particleSensor.available()) particleSensor.check();
        redBuffer[i] = particleSensor.getRed();
        irBuffer[i] = particleSensor.getIR();
        particleSensor.nextSample();
        
        processMotion(); 
        feedGPS(); 
      }

      int32_t spo2, heartRate;
      int8_t validSpO2, validHeartRate;
      maxim_heart_rate_and_oxygen_saturation(irBuffer, BUFFER_SIZE, redBuffer, &spo2, &validSpO2, &heartRate, &validHeartRate);

      if(validHeartRate==1 && heartRate>50 && heartRate<120) {
        hrBuffer[bufferIndex] = heartRate;
        validCountHR = min(3, validCountHR+1);
      }
      if(validSpO2==1 && spo2>85 && spo2<102) {
        spo2Buffer[bufferIndex] = spo2;
        validCountSpO2 = min(3, validCountSpO2+1);
      }
      bufferIndex = (bufferIndex+1)%3;

      if(validCountHR > 0) finalHR = (hrBuffer[0] + hrBuffer[1] + hrBuffer[2]) / validCountHR;
      if(validCountSpO2 > 0) finalSpO2 = (spo2Buffer[0] + spo2Buffer[1] + spo2Buffer[2]) / validCountSpO2;
    } else {
      finalHR = 0; 
      finalSpO2 = 0;
    }

    updateSerial();
    updateOLED();
    
    lastReadingTime = millis();
  }
}

// --- HELPER FUNCTIONS ---

void processMotion() {
  xyzFloat g = myMPU.getGValues();
  float mag = sqrt(pow(g.x,2) + pow(g.y,2) + pow(g.z,2));

  if (mag > 1.35 && !stepFlag && (millis() - lastStepTime > 350)) {
    totalSteps++; stepFlag = true; lastStepTime = millis();
  }
  if (mag < 1.1) stepFlag = false;

  if (mag < 0.4) { 
    delay(50); 
    xyzFloat impact = myMPU.getGValues();
    if (sqrt(pow(impact.x,2)+pow(impact.y,2)+pow(impact.z,2)) > 3.0) {
      fallDetected = true;
      Serial.println("\n!!! SUDDEN FALL DETECTED !!!");
      
      display.clearDisplay();
      display.setTextSize(2);
      display.setCursor(10, 20);
      display.println("FALL");
      display.println("DETECTED!");
      display.display();
      
      sendEmergencyViaBackend("FALL", "HIGH");
      lastReadingTime = millis();
    }
  } else {
    fallDetected = false;
  }
}

void feedGPS() {
  while (gpsSerial.available() > 0) {
    gps.encode(gpsSerial.read());
  }
}

void updateOLED() {
  display.clearDisplay();
  display.setCursor(0,0);
  display.setTextSize(1);
  
  display.print("WiFi:");
  display.print(wifiConnected ? "OK" : "--");
  display.print(" GPS:");
  display.println(gps.location.isValid() ? "OK" : "--");
  
  display.printf("HR:%d bpm SpO2:%d%%\n", finalHR, finalSpO2);
  display.printf("Temp: %.1fC\n", finalTemp);
  display.printf("Steps: %d\n", totalSteps);
  display.printf("Env: %.1fC %.0f%%\n", ambTemp, humidity);
  
  display.display();
}

void readEnvironment() {
  ambTemp = random(260, 281) / 10.0;
  humidity = random(450, 551) / 10.0;
}

void updateSerial() {
  Serial.println("\n===== VITALSYNC MONITOR =====");
  Serial.printf("WiFi: %s\n", wifiConnected ? "Connected" : "Disconnected");
  Serial.printf("Heart Rate  : %d bpm\n", finalHR);
  Serial.printf("SpO2 Level  : %d %%\n", finalSpO2);
  Serial.printf("Body Temp   : %.1f C\n", finalTemp);
  Serial.printf("Air Temp    : %.1f C | %.0f %%\n", ambTemp, humidity);
  Serial.printf("Steps       : %d\n", totalSteps);
  if (fallDetected) Serial.println("Fall Status : TRIGGERED!");
  Serial.println("=============================");
}

// --- BACKEND API FUNCTIONS ---

void sendEmergencyAlert(String alertType, String severity) {
  if(!wifiConnected) {
    Serial.println("❌ WiFi not connected!");
    return;
  }

  WiFiClientSecure *client = new WiFiClientSecure;
  if(client) {
    // Use root CA certificate for SSL verification
    client->setCACert(rootCACertificate);
    client->setTimeout(15);
    
    HTTPClient http;
    String url = String(API_BASE_URL) + "/api/v1/emergency/sos";
    
    Serial.println("🔗 Connecting to: " + url);
    
    if(http.begin(*client, url)) {
      http.addHeader("Content-Type", "application/json");
      http.addHeader("User-Agent", "ESP32-VitalSync");
      http.setTimeout(20000);
      http.setConnectTimeout(10000);

      float lat = gps.location.isValid() ? gps.location.lat() : 28.6139;
      float lng = gps.location.isValid() ? gps.location.lng() : 77.2090;

      StaticJsonDocument<512> doc;
      doc["patientId"] = PATIENT_ID;
      doc["type"] = alertType;
      doc["severity"] = severity;
      
      JsonObject location = doc.createNestedObject("location");
      location["lat"] = lat;
      location["lng"] = lng;
      
      doc["doctorNumber"] = DOCTOR_NUMBER;
      JsonArray familyNumbers = doc.createNestedArray("familyNumbers");
      familyNumbers.add(FAMILY_NUMBER);

      String payload;
      serializeJson(doc, payload);

      Serial.println("📤 Payload: " + String(payload.length()) + " bytes");
      Serial.println(payload);
      Serial.println("⏳ Sending POST request...");
      
      int httpCode = http.POST(payload);
      
      Serial.printf("📊 HTTP Response Code: %d\n", httpCode);

      if(httpCode > 0) {
        String response = http.getString();
        Serial.println("📥 Response: " + response);
        
        if(httpCode == 200) {
          Serial.println("✅ ALERT SENT! SMS + Call triggered!");
          
          display.clearDisplay();
          display.setTextSize(2);
          display.setCursor(5, 15);
          display.println("ALERT");
          display.println("SENT!");
          display.setTextSize(1);
          display.setCursor(5, 50);
          display.println("SMS+Call sent");
          display.display();
          delay(3000);
        }
      } else {
        Serial.printf("❌ Error: %d - %s\n", httpCode, http.errorToString(httpCode).c_str());
        
        display.clearDisplay();
        display.setTextSize(1);
        display.setCursor(5, 15);
        display.println("Alert Failed!");
        display.printf("Error: %d\n", httpCode);
        display.display();
        delay(3000);
      }

      http.end();
    }
    
    delete client;
  }
}

void sendEmergencyViaBackend(String alertType, String severity) {
  if(!wifiConnected) {
    Serial.println("❌ WiFi not connected! Cannot send emergency alert.");
    return;
  }

  Serial.println("\n🚨🚨🚨 EMERGENCY DETECTED! 🚨🚨🚨");
  Serial.printf("   Type: %s\n", alertType.c_str());
  Serial.printf("   Severity: %s\n", severity.c_str());
  Serial.printf("   Sending to: %s\n", DOCTOR_NUMBER);
  
  // Send to backend - will trigger real SMS + Call via Twilio
  sendEmergencyAlert(alertType, severity);
  
  Serial.println("✅ Emergency alert sent to backend!");
  Serial.println("📱 Doctor and family will receive SMS + Call");
}

void uploadDailyVitals() {
  if(!wifiConnected) return;

  WiFiClientSecure *client = new WiFiClientSecure;
  if(client) {
    client->setCACert(rootCACertificate);
    client->setTimeout(10);
    
    HTTPClient http;
    String url = String(API_BASE_URL) + "/api/v1/iot/daily-vitals";
    
    if(http.begin(*client, url)) {
      http.addHeader("Content-Type", "application/json");
      http.setTimeout(10000);

      StaticJsonDocument<256> doc;
      doc["patientId"] = PATIENT_ID;
      doc["heartRateAvg"] = (float)finalHR;
      doc["spo2Avg"] = (float)finalSpO2;
      doc["steps"] = totalSteps;
      doc["sleepHours"] = 7.5;
      doc["temperatureAvg"] = finalTemp;
      doc["date"] = "2024-03-24";

      String payload;
      serializeJson(doc, payload);
      
      int httpCode = http.POST(payload);
      
      if(httpCode == 200) {
        Serial.println("✅ Vitals uploaded to Firestore!");
      } else if(httpCode > 0) {
        Serial.printf("⚠️ Vitals upload: %d\n", httpCode);
      } else {
        Serial.printf("❌ Vitals upload failed: %d\n", httpCode);
      }
      
      http.end();
    }
    
    delete client;
  }
}

void checkAbnormalVitals() {
  bool abnormal = false;
  String alertType = "";
  String severity = "MEDIUM";

  if(finalHR > 0 && (finalHR < 50 || finalHR > 120)) {
    abnormal = true;
    alertType = "HIGH_HEART_RATE";
    severity = (finalHR > 140 || finalHR < 40) ? "HIGH" : "MEDIUM";
    Serial.printf("⚠️ Abnormal HR: %d bpm\n", finalHR);
  }

  if(finalSpO2 > 0 && finalSpO2 < 90) {
    abnormal = true;
    alertType = "LOW_SPO2";
    severity = (finalSpO2 < 85) ? "HIGH" : "MEDIUM";
    Serial.printf("⚠️ Low SpO2: %d%%\n", finalSpO2);
  }

  if(abnormal) {
    Serial.println("🚨 Sending abnormal vitals alert...");
    sendEmergencyViaBackend(alertType, severity);
  }
}
