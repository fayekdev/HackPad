#include <GxEPD2_BW.h>
#include <Adafruit_GFX.h>
#include <SPI.h>

#define EPD_CS    20  
#define EPD_DC    3   
#define EPD_RST   4   
#define EPD_BUSY  -1  

#define EPD_SCK   7   
#define EPD_MOSI  6   

#define SR_PL_LATCH 2  
#define SR_CLK      1  
#define SR_DATA_IN  0  

#define ENC_CLK     4  
#define ENC_DT      5  
#define JOY_X       10 
#define JOY_Y       21 

enum DynamicField {
  FIELD_TIME,
  FIELD_APP,
  FIELD_MUSIC,
  FIELD_WEATHER,
  FIELD_HARDWARE
};

// Explicit forward declaration tells the compiler this function exists
void updateDynamicField(DynamicField field);

GxEPD2_BW<GxEPD2_290_T94, GxEPD2_290_T94::HEIGHT> display(GxEPD2_290_T94(EPD_CS, EPD_DC, EPD_RST, EPD_BUSY));

unsigned long lastUpdateTime = 0;   
const long updateInterval = 1000;   
int partialRefreshCounter = 0;      
const int maxPartialRefreshes = 60;

// --- Lopaka Assets (Hex Validated) ---
static const unsigned char PROGMEM image_microphone_1_bits[] = {0x03,0x80,0x07,0xc0,0x05,0x40,0x07,0xc0,0x05,0x40,0x07,0xc0,0x05,0x40,0x07,0xc0,0x17,0xd0,0x13,0x90,0x08,0x20,0x07,0xc0,0x01,0x00,0x01,0x00,0x07,0xc0,0x00,0x00};
static const unsigned char PROGMEM image_microphone_muted_bits[] = {0x87,0x00,0x4f,0x80,0x26,0x80,0x13,0x80,0x09,0x80,0x04,0x80,0x0a,0x00,0x0d,0x00,0x2e,0xa0,0x27,0x40,0x10,0x20,0x0f,0x90,0x02,0x08,0x02,0x04,0x0f,0x82,0x00,0x00};
static const unsigned char PROGMEM image_music_bits[] = {0x00,0x7c,0x0f,0x84,0x08,0x04,0x08,0x7c,0x0f,0xc4,0x08,0x04,0x08,0x04,0x08,0x04,0x08,0x04,0x08,0x04,0x08,0x38,0x70,0x44,0x88,0x44,0x88,0x38,0x70,0x00,0x00,0x00};
static const unsigned char PROGMEM image_volume_loud_bits[] = {0x01,0xc1,0x00,0x02,0x40,0x80,0x04,0x44,0x40,0x08,0x42,0x20,0xf0,0x51,0x20,0x80,0x49,0x10,0x80,0x44,0x90,0x80,0x44,0x90,0x80,0x44,0x90,0x80,0x49,0x10,0xf0,0x51,0x20,0x08,0x42,0x20,0x04,0x44,0x40,0x02,0x40,0x80,0x01,0xc1,0x00,0x00,0x00,0x00};
static const unsigned char PROGMEM image_volume_low_bits[] = {0x01,0xc0,0x00,0x02,0x40,0x00,0x04,0x40,0x00,0x08,0x40,0x00,0xf0,0x50,0x00,0x80,0x48,0x00,0x80,0x44,0x00,0x80,0x44,0x00,0x80,0x44,0x00,0x80,0x48,0x00,0xf0,0x50,0x00,0x08,0x40,0x00,0x04,0x40,0x00,0x02,0x40,0x00,0x01,0xc0,0x00,0x00,0x00,0x00};
static const unsigned char PROGMEM image_volume_normal_bits[] = {0x01,0xc0,0x00,0x02,0x40,0x00,0x04,0x42,0x00,0x08,0x41,0x00,0xf0,0x50,0x80,0x80,0x48,0x80,0x80,0x44,0x40,0x80,0x44,0x40,0x80,0x44,0x40,0x80,0x48,0x80,0xf0,0x50,0x80,0x08,0x41,0x00,0x04,0x42,0x00,0x02,0x40,0x00,0x01,0xc0,0x00,0x00,0x00,0x00};

// --- Strict 32x32 Grid Layout Bitmaps ---
static const unsigned char PROGMEM img_weather_sunny[] = {
  0x00,0x03,0x00,0x00,0x00, 0x03,0x00,0x00,0x0c,0x03, 0x00,0xc0,0x0c,0x03,0x00, 0xc0,0x03,0x00,0x03,0x00,
  0x03,0x00,0x03,0x00,0x00, 0x0f,0xc0,0x00,0x00,0x0f, 0xc0,0x00,0xc0,0xf0,0x3c, 0x0c,0xc0,0xf0,0x3c,0x0c,
  0x30,0xc0,0x0c,0x30,0x30, 0xc0,0x0c,0x30,0x03,0x00, 0x03,0x00,0x03,0x00,0x03, 0x00,0x03,0x00,0x03,0x00,
  0x03,0x00,0x03,0x00,0x03, 0x00,0x03,0x00,0x03,0x00, 0x03,0x00,0x30,0xc0,0x0c, 0x30,0x30,0xc0,0x0c,0x30,
  0xc0,0xf0,0x3c,0x0c,0xc0, 0xf0,0x3c,0x0c,0x00,0x0f, 0xc0,0x00,0x00,0x0f,0xc0, 0x00,0x03,0x00,0x03,0x00,
  0x03,0x00,0x03,0x00,0x0c, 0x03,0x00,0xc0,0x0c,0x03, 0x00,0xc0,0x00,0x03,0x00, 0x00,0x00,0x03,0x00,0x00,
  0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00

};

static const unsigned char PROGMEM img_weather_cloudy[] = {
  0x00,0x00,0x0c,0x00,0x00, 0x00,0x00,0x0c,0x00,0x00, 0x00,0x0c,0x00,0x0c,0x00, 0x00,0x0c,0x00,0x0c,0x00,0x00,
  0x00,0x3f,0x00,0x00,0x00, 0x00,0x3f,0x00,0x00,0x00, 0x03,0xc0,0xf0,0x00,0x00, 0x03,0xc0,0xf0,0x00,0x00,0xc3,
  0x00,0x30,0xc0,0x00,0xc3, 0x00,0x30,0xc0,0x00,0x0c, 0x00,0x0c,0x00,0x00,0x0c, 0x00,0x0c,0x00,0x00,0x0c,0x00,
  0x0c,0x00,0x00,0x0c,0x00, 0x0c,0x00,0x00,0x3f,0xc0, 0x0c,0x00,0x00,0x3f,0xc0, 0x0c,0x00,0x00,0xc0,0x30,0x30,
  0xc0,0x00,0xc0,0x30,0x30, 0xc0,0x03,0x00,0x0c,0xf0, 0x00,0x03,0x00,0x0c,0xf0, 0x00,0x0f,0x00,0x0f,0x00,0x00,
  0x0f,0x00,0x0f,0x00,0x00, 0x3c,0x00,0x03,0xfc,0x00, 0x3c,0x00,0x03,0xfc,0x00, 0xc0,0x00,0x00,0x0f,0x00,0xc0,
  0x00,0x00,0x0f,0x00,0xc0, 0x00,0x00,0x03,0x00,0xc0, 0x00,0x00,0x03,0x00,0xc0, 0x00,0x00,0x03,0x00,0xc0,0x00,
  0x00,0x03,0x00,0x3f,0xff, 0xff,0xfc,0x00,0x3f,0xff, 0xff,0xfc,0x00
};

static const unsigned char PROGMEM img_weather_rainy[] = {
  0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00, 0x00,0x3f,0xf0,0x00,0x00, 0x00,0x3f,0xf0,0x00,0x00,0x00,
  0xc0,0x0c,0x00,0x00,0x00, 0xc0,0x0c,0x00,0x00,0x03, 0x00,0x03,0x00,0x00,0x03, 0x00,0x03,0x00,0x00,0x0f,0x00,
  0x00,0xc0,0x00,0x0f,0x00, 0x00,0xc0,0x00,0x30,0x00, 0x00,0xfc,0x00,0x30,0x00, 0x00,0xfc,0x00,0xc0,0x00,0x00,
  0x03,0x00,0xc0,0x00,0x00, 0x03,0x00,0xc0,0x00,0x00, 0x00,0xc0,0xc0,0x00,0x00, 0x00,0xc0,0x30,0x00,0x00,0x00,
  0xc0,0x30,0x00,0x00,0x00, 0xc0,0x0f,0xff,0xff,0xff, 0x00,0x0f,0xff,0xff,0xff, 0x00,0x00,0x03,0x03,0x00,0x00,
  0x00,0x03,0x03,0x00,0x00, 0x0c,0x0c,0x0c,0x0c,0x00, 0x0c,0x0c,0x0c,0x0c,0x00, 0x30,0x30,0xc0,0x30,0x00,0x30,
  0x30,0xc0,0x30,0x00,0xc3, 0x03,0x0c,0xc0,0x00,0xc3, 0x03,0x0c,0xc0,0x00,0x0c, 0x0c,0x30,0x00,0x00,0x0c,0x0c,
  0x30,0x00,0x00,0x00,0x00, 0xc0,0x00,0x00,0x00,0x00, 0xc0,0x00,0x00
};
static const unsigned char PROGMEM img_weather_windy[] = {
  0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x0f,0x00,0x00,
  0x00,0x0f,0x00,0x00,0x0f, 0xc0,0xc0,0x00,0x0f,0xc0, 0xc0,0x00,0x30,0x30,0x30, 0x00,0x30,0x30,0x30,0x00,0x30,
  0x30,0x30,0x00,0x30,0x30, 0x30,0x00,0x00,0x30,0x30, 0x00,0x00,0x30,0x30,0x00, 0x00,0xc0,0xc0,0x00,0x00,0xc0,
  0xc0,0xff,0xff,0x0f,0x0c, 0xff,0xff,0x0f,0x0c,0x00, 0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0xcc,0xf3,0xc0,0x0c,
  0xcc,0xf3,0xc0,0x0c,0x00, 0x00,0x3c,0x00,0x00,0x00, 0x3c,0x00,0x00,0x00,0x03, 0x00,0x00,0x00,0x03,0x00,0x00,
  0x00,0x03,0x00,0x00,0x00, 0x03,0x00,0x00,0x03,0x0c, 0x00,0x00,0x03,0x0c,0x00, 0x00,0x00,0xf0,0x00,0x00,0x00,0xf0,0x00};


String string_1_text = "--:--";      
String string_3_text = "OFFLINE";    
String string_4_text = "None";       
String string_9_text = "--- --";     
String string_17_text = "--C";       
String string_11_text = "-";
String string_11_copy_1_text = "-";
String state_task3 = "-";
String state_task4 = "-";
String state_weather = "Sunny";
String state_sound = "low";
String state_mic = "off";
String lastTimeText = "";
String lastMusicText = "";
int last_enc_CLK = LOW;
long encoder_pos = 0;
bool buttons[16] = {false};
unsigned long last_pc_packet_time = 0;
bool is_pc_connected = false;

void drawScreen_1(void);

void setup() {
  
  Serial.begin(115200);
  pinMode(SR_PL_LATCH, OUTPUT);
  pinMode(SR_CLK, OUTPUT);
  pinMode(SR_DATA_IN, INPUT);
  
  pinMode(ENC_CLK, INPUT_PULLUP);
  pinMode(ENC_DT, INPUT_PULLUP);
  last_enc_CLK = digitalRead(ENC_CLK);
  
  SPI.begin(EPD_SCK, -1, EPD_MOSI, EPD_CS);
  display.init(115200, true, 2, false);
  display.setRotation(3);
  drawScreen_Full();
}

void loop() {
  unsigned long currentMillis = millis();

  digitalWrite(SR_PL_LATCH, LOW);
  delayMicroseconds(5);
  digitalWrite(SR_PL_LATCH, HIGH);
  
  bool button_changed = false;
  for (int i = 0; i < 16; i++) {
    bool raw_val = !digitalRead(SR_DATA_IN);
    digitalWrite(SR_CLK, HIGH);
    delayMicroseconds(2);
    digitalWrite(SR_CLK, LOW);
    if (buttons[i] != raw_val) {
      buttons[i] = raw_val;
      button_changed = true;
    }
  }
  
  int current_enc_CLK = digitalRead(ENC_CLK);
  bool encoder_changed = false;
  if (current_enc_CLK != last_enc_CLK && current_enc_CLK == LOW) {
    encoder_pos += (digitalRead(ENC_DT) != current_enc_CLK) ? 1 : -1;
    encoder_changed = true;
  }
  last_enc_CLK = current_enc_CLK;
  
  int joyX = analogRead(JOY_X);
  int joyY = analogRead(JOY_Y);
  

  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();
    
    if (input.startsWith("HELLO")) {
        last_pc_packet_time = currentMillis;
        if (!is_pc_connected) {
            is_pc_connected = true;
            drawScreen_Full(); // Run once on first connection
        }
    }
    else if (input.startsWith("DATA:")) {
      last_pc_packet_time = currentMillis;
      is_pc_connected = true;
      
      // Token-Independent Dynamic Extraction Engine
      int idx_app = input.indexOf("|APP:");
      int idx_wea = input.indexOf("|WEA:");
      int idx_tmp = input.indexOf("|TMP:");
      int idx_snd = input.indexOf("|SND:");
      int idx_mic = input.indexOf("|MIC:");
      int idx_sng = input.indexOf("|SNG:");
      int idx_dat = input.indexOf("|DAT:");
      int idx_tim = input.indexOf("|TIM:");
      int idx_t1  = input.indexOf("|T1:");  
      int idx_t2  = input.indexOf("|T2:");
      int idx_t3  = input.indexOf("|T3:");  
      int idx_t4  = input.indexOf("|T4:");
      
      // Lambda helper to safely extract fields cleanly up to the next pipe '|' delimiter
      auto extractField = [](const String& src, int startIdx, int prefixLen) -> String {
        if (startIdx == -1) return "";
        int valStart = startIdx + prefixLen;
        int nextPipe = src.indexOf('|', valStart);
        if (nextPipe == -1) return src.substring(valStart); // End of string boundary handling
        return src.substring(valStart, nextPipe);
      };

      if(idx_app != -1) string_3_text  = extractField(input, idx_app, 5); 
      if(idx_wea != -1) state_weather  = extractField(input, idx_wea, 5); 
      if(idx_tmp != -1) string_17_text = extractField(input, idx_tmp, 5);
      if(idx_snd != -1) state_sound    = extractField(input, idx_snd, 5); 
      if(idx_mic != -1) state_mic      = extractField(input, idx_mic, 5); 
      if(idx_sng != -1) string_4_text  = extractField(input, idx_sng, 5); // Cleans up song tracking bugs
      if(idx_dat != -1) string_9_text  = extractField(input, idx_dat, 5); 
      if(idx_tim != -1) string_1_text  = extractField(input, idx_tim, 5); 
      if(idx_t1  != -1) string_11_text = extractField(input, idx_t1, 4);
      if(idx_t2  != -1) string_11_copy_1_text = extractField(input, idx_t2, 4); 
      if(idx_t3  != -1) state_task3    = extractField(input, idx_t3, 4); 
      if(idx_t4  != -1) state_task4    = extractField(input, idx_t4, 4);
      
      // Update global text variables silently without calling drawScreen_Full() here
      string_3_text = new_app; 
      state_weather = new_wea; 
      string_17_text = new_tmp;
      state_sound = new_snd; 
      state_mic = new_mic; 
      string_4_text = new_sng;
      string_9_text = new_dat; 
      string_1_text = new_tim; 
      string_11_text = new_t1;
      string_11_copy_1_text = new_t2; 
      state_task3 = new_t3; 
      state_task4 = new_t4;
    }
  }
  //UPDATES
  if (currentMillis - lastUpdateTime >= updateInterval) {
    lastUpdateTime = currentMillis;

    bool timeChanged = false;
    bool musicChanged = false;
    bool layoutChanged = false; // Tracks checklist, app, weather, or hardware shifts

    // Compare with history variables to determine which update routine to execute
    if (string_1_text != lastTimeText) { timeChanged = true; }
    if (string_4_text != lastMusicText) { musicChanged = true; }
    
    // Check fields that don't need independent sub-boxes (updates layout frames)
    static String lastAppText, lastWeather, lastSound, lastMic, lastT1, lastT2, lastT3, lastT4;
    if (string_3_text != lastAppText || state_weather != lastWeather || 
        state_sound != lastSound || state_mic != lastMic || 
        string_11_text != lastT1 || string_11_copy_1_text != lastT2 || 
        state_task3 != lastT3 || state_task4 != lastT4) {
      layoutChanged = true;
    }

    // Force full screen clean flash if data demands it or counter overflows
    if (partialRefreshCounter >= maxPartialRefreshes || layoutChanged) {
      drawScreen_Full();
      partialRefreshCounter = 0;
      
      // Reset all states after full draw
      lastTimeText = string_1_text;
      lastMusicText = string_4_text;
      lastAppText = string_3_text; 
      lastWeather = state_weather;
      lastSound = state_sound; 
      lastMic = state_mic;
      lastT1 = string_11_text; 
      lastT2 = string_11_copy_1_text;
      lastT3 = state_task3; 
      lastT4 = state_task4;
    } 
    // Perform fast partial update bounds operations
    else {
      bool updatedSomething = false;
      
      if (timeChanged) { 
        updateDynamicField(FIELD_TIME); 
        lastTimeText = string_1_text; 
        updatedSomething = true; 
      }
      if (musicChanged) { 
        updateDynamicField(FIELD_MUSIC); 
        lastMusicText = string_4_text; 
        updatedSomething = true; 
      }
      
      if (updatedSomething) {
        partialRefreshCounter++;
      }
    }
  }
  
  if (is_pc_connected && (currentMillis - last_pc_packet_time > 3500)) {
      is_pc_connected = false;
      string_1_text = "--:--"; string_3_text = "OFFLINE"; string_4_text = "None";
      string_9_text = "--- --"; string_17_text = "--C";
      string_11_text = "-"; string_11_copy_1_text = "-"; state_task3 = "-"; state_task4 = "-";
      state_sound = "low"; state_mic = "off";
      drawScreen_Full();
  }
  if (is_pc_connected) {
    static unsigned long last_tx = 0;
    if (currentMillis - last_tx > 40 || button_changed || encoder_changed) {
      last_tx = currentMillis;
      Serial.print("{\"joyX\":"); Serial.print(joyX);
      Serial.print(",\"joyY\":"); Serial.print(joyY);
      Serial.print(",\"encoder\":"); Serial.print(encoder_pos);
      Serial.print(",\"buttons\":[");
      for (int i = 0; i < 16; i++) {
        Serial.print(buttons[i] ? "1" : "0");
        if (i < 15) Serial.print(",");
      }
      Serial.println("]}");
    }
  }
  
  delay(5);
}



void drawScreen_Full(void) {
  display.setFullWindow(); 
  display.firstPage();
  do {
    display.fillScreen(GxEPD_WHITE);
    
    // Draw all permanent static boxes, lines, and layout frames
    drawStaticLayoutFrames();
    
    // Fill in the text fields with current values
    drawAllTextFields();
  } while (display.nextPage());
}


void updateDynamicField(DynamicField field) {
  uint16_t box_x = 0, box_y = 0, box_w = 0, box_h = 0;

  // STRICT bounds checking: Only capture the exact text rectangle
  switch (field) {
    case FIELD_TIME:     box_x = 250; box_y = 0;  box_w = 46;  box_h = 15;  break;
    case FIELD_APP:      box_x = 10;  box_y = 25; box_w = 114; box_h = 16;  break;
    case FIELD_MUSIC:    box_x = 10;  box_y = 90; box_w = 114; box_h = 18;  break;
    case FIELD_WEATHER:  box_x = 10;  box_y = 43; box_w = 60;  box_h = 40;  break;
    case FIELD_HARDWARE: box_x = 240; box_y = 105; box_w = 45;  box_h = 22;  break;
  }

  display.setPartialWindow(box_x, box_y, box_w, box_h);
  display.firstPage();
  do {
    // Clear ONLY the text bounding box back to white
    display.fillRect(box_x, box_y, box_w, box_h, GxEPD_WHITE);
    
    // Only draw the specific text inside this layout block
    drawAllTextFields(); 
  } while (display.nextPage());
}


void drawStaticLayoutFrames(void) {
  // Draw your background boxes and shapes here so they aren't erased
  display.drawRect(123, 51, 41, 38, GxEPD_BLACK); // Music box frame
  
  display.drawCircle(197, 43, 4, GxEPD_BLACK);   // Checklist circles
  display.drawCircle(197, 60, 4, GxEPD_BLACK); 
  display.drawCircle(197, 77, 4, GxEPD_BLACK);
  display.drawCircle(197, 95, 4, GxEPD_BLACK); 
  
  display.setCursor(120, 12); 
  display.print(".devPAD");
}

void drawAllTextFields(void) {
  display.setTextSize(1);
  display.setTextColor(GxEPD_BLACK);
  display.setTextWrap(false);
  
  int16_t x1, y1; 
  uint16_t w, h;
  
  // Header Text
  display.setCursor(10, 11);  display.print(string_9_text);
  display.setCursor(254, 11); display.print(string_1_text); // TIME
  
  // App Text
  display.getTextBounds(string_3_text, 0, 0, &x1, &y1, &w, &h);
  int center_app = 90 + ((108 - w) / 2);
  display.setCursor(center_app < 16 ? 16 : center_app, 37);
  display.print(string_3_text);

  // Music Text & Bitmaps
  display.drawBitmap(135, 62, image_music_bits, 14, 16, GxEPD_BLACK);
  display.getTextBounds(string_4_text, 0, 0, &x1, &y1, &w, &h);
  int center_song = 100 + ((88 - w) / 2);
  display.setCursor(center_song < 36 ? 36 : center_song, 104);
  display.print(string_4_text);

  // Checklist Text
  display.setCursor(207, 39); display.print(string_11_text);
  display.setCursor(207, 57); display.print(string_11_copy_1_text);
  display.setCursor(207, 74); display.print(state_task3);
  display.setCursor(207, 92); display.print(state_task4);
  
  // Hardware Audio Icons
  if (state_sound.equalsIgnoreCase("loud")) display.drawBitmap(240, 109, image_volume_loud_bits, 20, 16, GxEPD_BLACK);
  else if (state_sound.equalsIgnoreCase("low")) display.drawBitmap(240, 109, image_volume_low_bits, 18, 16, GxEPD_BLACK);
  else display.drawBitmap(240, 109, image_volume_normal_bits, 18, 16, GxEPD_BLACK);
  
  if (state_mic.equalsIgnoreCase("on")) display.drawBitmap(267, 109, image_microphone_1_bits, 15, 16, GxEPD_BLACK);
  else display.drawBitmap(268, 109, image_microphone_muted_bits, 15, 16, GxEPD_BLACK);
  
  // Weather Logic
  if (state_weather.equalsIgnoreCase("Sunny")) display.drawBitmap(32, 43, img_weather_sunny, 30, 32, GxEPD_BLACK);
  else if (state_weather.equalsIgnoreCase("Rainy")) display.drawBitmap(10, 52, img_weather_rainy, 32, 32, GxEPD_BLACK);
  else if (state_weather.equalsIgnoreCase("Windy")) display.drawBitmap(33, 43, image_music_bits, 30, 32, GxEPD_BLACK);
  else display.drawBitmap(31, 39, img_weather_cloudy, 34, 32, GxEPD_BLACK);
  
  display.setCursor(37, 77);
  display.print(string_17_text);
}

