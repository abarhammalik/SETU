#include <Adafruit_GFX.h>  
#include <Adafruit_ILI9341.h>  
#include <SPI.h>  
#include <TJpg_Decoder.h>  
#include <WiFi.h>  
#include <WiFiUdp.h>  
  
#include <Fonts/FreeSans9pt7b.h>  
#include <Fonts/FreeSansBold9pt7b.h>  
#include <Fonts/FreeSansBold12pt7b.h>  
#include <Fonts/FreeSansBold18pt7b.h>  
  
// ============================================================  
//                    MINE ROVER CONTROLLER  
//          LIGHT PROFESSIONAL UI - 320 x 240 ILI9341  
//          ALL-PAGE DRIVE + LIVE TELEMETRY + YOLO  
// ============================================================  
//  
// MOTOR PROTOCOL:  
//   M,left,right 
//  
// STOP PROTOCOL:  
//   S 
//  
// ROVER HEARTBEAT:  
//   H 
//  
// TELEMETRY:  
//   T,CH4,CO,CO2,O2,TEMP,HUM,PRESS 
//  
// Example real packet from rover:  
//   T,1.24,8.6,820,20.7,28.6,67.4,1008.4 
//  
// Display:  
//   CH4  -> %LEL 
//   CO   -> ppm 
//   CO2  -> ppm 
//   O2   -> %VOL 
//   TEMP -> deg C 
//   HUM  -> %RH 
//   PRESS-> hPa 
// ============================================================  
  
  
// ============================================================  
//                         TFT PINS 
// ============================================================  
  
#define TFT_SCK   18  
#define TFT_MISO  19  
#define TFT_MOSI  23  
  
#define TFT_CS    15  
#define TFT_DC    2  
#define TFT_RST   4  
  
  
// ============================================================  
//                       JOYSTICKS 
// ============================================================  
  
// LEFT physical joystick 
// Y = FORWARD / REVERSE  
  
#define JOY1_X   36  
#define JOY1_Y   39  
#define JOY1_SW  32  
  
// RIGHT physical joystick 
// X = LEFT / RIGHT  
  
#define JOY2_X   34  
#define JOY2_Y   35  
#define JOY2_SW  33  
  
#define TOUCH_PIN 27  
  
  
// ============================================================  
//                    DRIVE SETTINGS 
// ============================================================  
  
#define JOY_DEADZONE       350  
#define MAX_MOTOR_SPEED    179  
#define DRIVE_TX_INTERVAL  50  
#define SMOOTH_STEP        8  
  
#define INVERT_DRIVE_Y     true  
#define INVERT_DRIVE_X     false  
  
  
// ============================================================  
//                       WIFI SETTINGS 
// ============================================================  
  
const char *wifi_ssid     = "MOINKHAN";  
const char *wifi_password = "12345678";  
  
// Raspberry Pi video server  
const char *pi_host = "10.109.186.60";  
const uint16_t pi_port = 5000;  
const char *pi_path = "/video_feed_small";  
  
// Controller AP  
const char *rover_ap_ssid = "ROVER_CONTROL";  
const char *rover_ap_password = "rover123";  
  
IPAddress controllerIP(192, 168, 50, 1);  
IPAddress roverIP(192, 168, 50, 2);  
IPAddress apGateway(192, 168, 50, 1);  
IPAddress apSubnet(255, 255, 255, 0);  
  
  
// ============================================================  
//                         UDP 
// ============================================================  
  
WiFiUDP udp;  
  
const uint16_t UDP_PORT = 4210;  
  
#define ROVER_TIMEOUT       1500  
#define TELEMETRY_TIMEOUT   2500  
  
  
// ============================================================  
//                       JPEG BUFFER 
// ============================================================  
  
#define JPEG_BUF_SIZE 24000  
  
static uint8_t frameBuf[JPEG_BUF_SIZE];  
static size_t frameLen = 0;  
static bool capturingFrame = false;  
  
  
// ============================================================  
//                      VIDEO CLIENT 
// ============================================================  
  
WiFiClient videoClient;  
  
bool wifiConnected = false;  
  
bool piStreamFailed = false;  
  
unsigned long lastPiAttempt = 0;  
  
const unsigned long PI_RETRY_INTERVAL = 1500;  
  
const uint32_t PI_CONNECT_TIMEOUT = 180;  
  
// -1 = unrendered  
// 0  = WiFi unavailable  
// 1  = connecting  
// 2  = failed  
// 3  = streaming  
  
int piViewState = -1;  
  
  
// ============================================================  
//                         TFT OBJECT 
// ============================================================  
  
Adafruit_ILI9341 tft(  
  TFT_CS,  
  TFT_DC,  
  TFT_RST  
);  
  
  
// ============================================================  
//                        PAGE SYSTEM 
// ============================================================  
  
enum Page : uint8_t {  
  PAGE_SYSTEM = 0,  
  PAGE_DRIVE  = 1,  
  PAGE_GAS    = 2,  
  PAGE_ENV    = 3,  
  PAGE_VIDEO  = 4  
};  
  
Page currentPage = PAGE_SYSTEM;  
  
const uint8_t TOTAL_PAGES = 5;  
  
bool headerDirty = true;  
  
unsigned long lastUiRefresh = 0;  
  
const unsigned long UI_REFRESH_INTERVAL = 150;  
  
  
// ============================================================  
//                        UI COLORS 
// ============================================================  
  
#define C_BG            0xFFFA  
#define C_SURFACE       0xFFFF  
#define C_BORDER        0xD6BA  
  
#define C_TEXT          0x2104  
#define C_MUTED         0x6B4D  
  
#define C_ACCENT        0x4A49  
#define C_CYAN          0x45D4  
  
#define C_GREEN         0x35A6  
#define C_RED_T         0xA000  
  
#define C_ORANGE        0xFBE0  
#define C_ORANGE_T      0xC240  
  
#define C_RED           0xF166  
  
#define C_BLUE          0x5D7B  
  
#define C_SOFT_BLUE     0xDDFB  
#define C_SOFT_GREEN    0xD7F3  
#define C_SOFT_RED      0xF9C7  
#define C_SOFT_ORANGE   0xFFE8  
  
  
// ============================================================  
//                       DRIVE STATE 
// ============================================================  
  
unsigned long lastDriveTx = 0;  
  
bool driveWasActive = false;  
  
int targetLeftSpeed = 0;  
int targetRightSpeed = 0;  
  
int currentLeftSpeed = 0;  
int currentRightSpeed = 0;  
  
  
// ============================================================  
//                       LINK STATE 
// ============================================================  
  
unsigned long lastRoverHeartbeat = 0;  
  
bool roverOnline = false;  
  
bool telemetryValid = false;  
  
unsigned long lastTelemetryPacket = 0;  
  
  
// ============================================================  
//                 SIMULATED TELEMETRY STATE 
// ============================================================  
  
unsigned long lastSimTelemetry = 0;  
  
const unsigned long SIM_TELEMETRY_INTERVAL = 400;  
  
  
// ============================================================  
//                      TELEMETRY DATA 
// ============================================================  
  
struct GasData {  
  
  float methaneLEL = 0.0f;  
  
  float carbonMonoxide = 0.0f;  
  
  float carbonDioxide = 0.0f;  
  
  float oxygenPercent = 0.0f;  
};  
  
  
struct EnvironmentData {  
  
  float temperature = 0.0f;  
  
  float humidity = 0.0f;  
  
  float pressure = 0.0f;  
};  
  
  
GasData gasData;  
  
EnvironmentData environmentData;  
  
  
// ============================================================  
//                       TOUCH STATE 
// ============================================================  
  
bool lastTouchState = LOW;  
  
unsigned long lastTouchTime = 0;  
  
const unsigned long debounceDelay = 250;  
  
  
// ============================================================  
//                    VIDEO / UI STATE 
// ============================================================  
  
unsigned long lastVideoOverlay = 0;  
  
  
// ============================================================  
//                     FUNCTION DECLARATIONS 
// ============================================================  
  
bool tft_output(  
  int16_t x,  
  int16_t y,  
  uint16_t w,  
  uint16_t h,  
  uint16_t *bitmap  
);  
  
int joystickToSpeed(  
  int raw,  
  int center,  
  bool invert  
);  
  
int smoothMotorValue(  
  int current,  
  int target  
);  
  
void sendMotorPacket(  
  int leftSpeed,  
  int rightSpeed  
);  
  
void sendImmediateStop();  
  
void receiveRoverHeartbeat();  
  
void parseTelemetryPacket(  
  const char *buffer  
);  
  
bool telemetryFresh();  
  
void updateSimulatedTelemetry();  
  
void handleDriveControl();  
  
void handleTouch();  
  
void updateCurrentPage();  
  
void drawPageHeader();  
  
void drawSystemPage();  
  
void drawDrivePage();  
  
void drawGasPage();  
  
void drawEnvironmentPage();  
  
void pageLiveFeed();  
  
void updateGasLiveValues();  
  
void updateEnvironmentLiveValues();  
  
void updateDriveLive();  
  
void drawCard(  
  int x,  
  int y,  
  int w,  
  int h  
);  
  
void drawLabel(  
  int x,  
  int y,  
  const char *text  
);  
  
void drawValue(  
  int x,  
  int y,  
  const char *text,  
  uint16_t color = C_TEXT,  
  const GFXfont *font = &FreeSansBold12pt7b  
);  
  
void drawCentered(  
  int cx,  
  int baselineY,  
  const char *text,  
  const GFXfont *font,  
  uint16_t color  
);  
  
void drawFooter(  
  const char *leftText,  
  const char *rightText  
);  
  
void drawStatusDot(  
  int x,  
  int y,  
  bool online,  
  uint16_t activeColor  
);  
  
void drawTelemetryMetric(  
  int x,  
  int y,  
  int w,  
  int h,  
  const char *label,  
  float value,  
  int decimals,  
  const char *unit,  
  bool fresh  
);  
  
void updateMetricValue(  
  int x,  
  int y,  
  int w,  
  int h,  
  float value,  
  int decimals,  
  bool fresh  
);  
  
void startVideoIfNeeded();  
  
void stopVideoClient();  
  
void updateVideoStream();  
  
void drawVideoOverlay();  
  
  
// ============================================================  
//                      JPEG CALLBACK 
// ============================================================  
  
bool tft_output(  
  int16_t x,  
  int16_t y,  
  uint16_t w,  
  uint16_t h,  
  uint16_t *bitmap  
) {  
  
  if (x >= tft.width() || y >= tft.height()) {  
    return 0;  
  }  
  
  if (x + w > tft.width()) {  
    w = tft.width() - x;  
  }  
  
  if (y + h > tft.height()) {  
    h = tft.height() - y;  
  }  
  
  if (w == 0 || h == 0) {  
    return 0;  
  }  
  
  tft.drawRGBBitmap(  
    x,  
    y,  
    bitmap,  
    w,  
    h  
  );  
  
  return 1;  
}  
  
  
// ============================================================  
//                  JOYSTICK -> MOTOR SPEED 
// ============================================================  
  
int joystickToSpeed(  
  int raw,  
  int center,  
  bool invert  
) {  
  
  int delta = raw - center;  
  
  if (abs(delta) <= JOY_DEADZONE) {  
    return 0;  
  }  
  
  int magnitude;  
  
  if (abs(delta) >= 2047) {  
  
    magnitude = MAX_MOTOR_SPEED;  
  
  } else {  
  
    magnitude = map(  
      abs(delta),  
      JOY_DEADZONE,  
      2047,  
      0,  
      MAX_MOTOR_SPEED  
    );  
  }  
  
  magnitude = constrain(  
    magnitude,  
    0,  
    MAX_MOTOR_SPEED  
  );  
  
  int value =  
    (delta > 0)  
      ? magnitude  
      : -magnitude;  
  
  if (invert) {  
    value = -value;  
  }  
  
  return constrain(  
    value,  
    -MAX_MOTOR_SPEED,  
    MAX_MOTOR_SPEED  
  );  
}  
  
  
// ============================================================  
//                    MOTOR SMOOTHING 
// ============================================================  
  
int smoothMotorValue(  
  int current,  
  int target  
) {  
  
  if (current < target) {  
  
    current += SMOOTH_STEP;  
  
    if (current > target) {  
      current = target;  
    }  
  
  }  
  
  else if (current > target) {  
  
    current -= SMOOTH_STEP;  
  
    if (current < target) {  
      current = target;  
    }  
  }  
  
  return current;  
}  
  
  
// ============================================================  
//                     SEND MOTOR PACKET 
// ============================================================  
  
void sendMotorPacket(  
  int leftSpeed,  
  int rightSpeed  
) {  
  
  leftSpeed = constrain(  
    leftSpeed,  
    -MAX_MOTOR_SPEED,  
    MAX_MOTOR_SPEED  
  );  
  
  rightSpeed = constrain(  
    rightSpeed,  
    -MAX_MOTOR_SPEED,  
    MAX_MOTOR_SPEED  
  );  
  
  udp.beginPacket(  
    roverIP,  
    UDP_PORT  
  );  
  
  udp.print("M,");  
  udp.print(leftSpeed);  
  udp.print(",");  
  udp.print(rightSpeed);  
  
  udp.endPacket();  
  
  Serial.print("WIFI TX: M,");  
  Serial.print(leftSpeed);  
  Serial.print(",");  
  Serial.println(rightSpeed);  
}  
  
  
// ============================================================  
//                       IMMEDIATE STOP 
// ============================================================  
  
void sendImmediateStop() {  
  
  targetLeftSpeed = 0;  
  targetRightSpeed = 0;  
  
  currentLeftSpeed = 0;  
  currentRightSpeed = 0;  
  
  udp.beginPacket(  
    roverIP,  
    UDP_PORT  
  );  
  
  udp.print("S");  
  
  udp.endPacket();  
  
  Serial.println(  
    "WIFI TX: STOP"  
  );  
}  
  
  
// ============================================================  
//                    TELEMETRY FRESHNESS 
// ============================================================  
  
bool telemetryFresh() {  
  
  return telemetryValid &&  
         (millis() - lastTelemetryPacket <= TELEMETRY_TIMEOUT);  
}  
  
  
// ============================================================  
//                  TELEMETRY PARSER 
// ============================================================  
  
void parseTelemetryPacket(  
  const char *buffer  
) {  
  
  if (  
    buffer[0] != 'T' ||  
    buffer[1] != ','  
  ) {  
    return;  
  }  
  
  float ch4 = 0.0f;  
  float co = 0.0f;  
  float co2 = 0.0f;  
  float o2 = 0.0f;  
  
  float temp = 0.0f;  
  float hum = 0.0f;  
  float press = 0.0f;  
  
  int parsed = sscanf(  
    buffer,  
    "T,%f,%f,%f,%f,%f,%f,%f",  
    &ch4,  
    &co,  
    &co2,  
    &o2,  
    &temp,  
    &hum,  
    &press  
  );  
  
  if (parsed == 7) {  
  
    gasData.methaneLEL = ch4;  
  
    gasData.carbonMonoxide = co;  
  
    gasData.carbonDioxide = co2;  
  
    gasData.oxygenPercent = o2;  
  
    environmentData.temperature = temp;  
  
    environmentData.humidity = hum;  
  
    environmentData.pressure = press;  
  
    telemetryValid = true;  
  
    lastTelemetryPacket = millis();  
  
    lastRoverHeartbeat = millis();  
  
    roverOnline = true;  
  }  
}  
  
  
// ============================================================  
//                SIMULATED LIVE TELEMETRY 
// ============================================================  
  
void updateSimulatedTelemetry() {  
  
  if (!roverOnline) {  
    return;  
  }  
  
  if (  
    millis() - lastSimTelemetry <  
    SIM_TELEMETRY_INTERVAL  
  ) {  
    return;  
  }  
  
  lastSimTelemetry = millis();  
  
  float timeSec = millis() / 1000.0f;  
  
  gasData.methaneLEL =  
    0.85f +  
    0.22f * sin(timeSec * 0.55f) +  
    0.05f * sin(timeSec * 1.70f);  
  
  gasData.carbonMonoxide =  
    6.0f +  
    2.8f * sin(timeSec * 0.38f) +  
    0.8f * sin(timeSec * 1.15f);  
  
  gasData.carbonDioxide =  
    720.0f +  
    95.0f * sin(timeSec * 0.21f) +  
    18.0f * sin(timeSec * 0.83f);  
  
  gasData.oxygenPercent =  
    20.85f +  
    0.16f * sin(timeSec * 0.28f) -  
    0.04f * sin(timeSec * 0.91f);  
  
  environmentData.temperature =  
    28.5f +  
    1.8f * sin(timeSec * 0.18f);  
  
  environmentData.humidity =  
    63.0f +  
    5.0f * sin(timeSec * 0.15f);  
  
  environmentData.pressure =  
    1008.0f +  
    3.5f * sin(timeSec * 0.12f);  
  
  telemetryValid = true;  
  
  lastTelemetryPacket = millis();  
}  
  
  
// ============================================================  
//                   RECEIVE ROVER DATA 
// ============================================================  
  
void receiveRoverHeartbeat() {  
  
  int packetSize = udp.parsePacket();  
  
  if (packetSize <= 0) {  
    return;  
  }  
  
  char buffer[180];  
  
  int len = udp.read(  
    buffer,  
    sizeof(buffer) - 1  
  );  
  
  if (len <= 0) {  
    return;  
  }  
  
  buffer[len] = '\0';  
  
  if (udp.remoteIP() != roverIP) {  
    return;  
  }  
  
  Serial.print("UDP RX: ");  
  Serial.println(buffer);  
  
  if (buffer[0] == 'H') {  
  
    bool wasOnline = roverOnline;  
  
    lastRoverHeartbeat = millis();  
  
    roverOnline = true;  
  
    if (!wasOnline) {  
  
      headerDirty = true;  
  
      Serial.println("ROVER ONLINE");  
    }  
  }  
  
  else if (buffer[0] == 'T') {  
  
    parseTelemetryPacket(buffer);  
  
    headerDirty = true;  
  }  
}  
  
  
// ============================================================  
//                       DRIVE CONTROL 
// ============================================================  
  
void handleDriveControl() {  
  
  if (millis() - lastDriveTx < DRIVE_TX_INTERVAL) {  
    return;  
  }  
  
  lastDriveTx = millis();  
  
  int j1Y = analogRead(JOY1_Y);  
  
  int j2X = analogRead(JOY2_X);  
  
  bool j1Sw = digitalRead(JOY1_SW) == LOW;  
  
  bool j2Sw = digitalRead(JOY2_SW) == LOW;  
  
  const int CENTER_Y = 2048;  
  const int CENTER_X = 2048;  
  
  int throttle = joystickToSpeed(  
    j1Y,  
    CENTER_Y,  
    INVERT_DRIVE_Y  
  );  
  
  int turn = joystickToSpeed(  
    j2X,  
    CENTER_X,  
    INVERT_DRIVE_X  
  );  
  
  if (j1Sw || j2Sw) {  
  
    targetLeftSpeed = 0;  
    targetRightSpeed = 0;  
  
    currentLeftSpeed = 0;  
    currentRightSpeed = 0;  
  
    sendMotorPacket(0, 0);  
  
    driveWasActive = true;  
  
    return;  
  }  
  
  int leftTarget = throttle + turn;  
  
  int rightTarget = throttle - turn;  
  
  int biggest = max(  
    abs(leftTarget),  
    abs(rightTarget)  
  );  
  
  if (biggest > MAX_MOTOR_SPEED) {  
  
    float scale =  
      (float)MAX_MOTOR_SPEED /  
      (float)biggest;  
  
    leftTarget = (int)(leftTarget * scale);  
  
    rightTarget = (int)(rightTarget * scale);  
  }  
  
  targetLeftSpeed = constrain(  
    leftTarget,  
    -MAX_MOTOR_SPEED,  
    MAX_MOTOR_SPEED  
  );  
  
  targetRightSpeed = constrain(  
    rightTarget,  
    -MAX_MOTOR_SPEED,  
    MAX_MOTOR_SPEED  
  );  
  
  currentLeftSpeed = smoothMotorValue(  
    currentLeftSpeed,  
    targetLeftSpeed  
  );  
  
  currentRightSpeed = smoothMotorValue(  
    currentRightSpeed,  
    targetRightSpeed  
  );  
  
  sendMotorPacket(  
    currentLeftSpeed,  
    currentRightSpeed  
  );  
  
  driveWasActive = true;  
  
  Serial.print("J1Y=");  
  Serial.print(j1Y);  
  
  Serial.print(" J2X=");  
  Serial.print(j2X);  
  
  Serial.print(" THR=");  
  Serial.print(throttle);  
  
  Serial.print(" TURN=");  
  Serial.print(turn);  
  
  Serial.print(" TARGET L=");  
  Serial.print(targetLeftSpeed);  
  
  Serial.print(" R=");  
  Serial.print(targetRightSpeed);  
  
  Serial.print(" OUTPUT L=");  
  Serial.print(currentLeftSpeed);  
  
  Serial.print(" R=");  
  Serial.println(currentRightSpeed);  
}  
  
  
// ============================================================  
//                         UI HELPERS 
// ============================================================  
  
void drawStatusDot(  
  int x,  
  int y,  
  bool online,  
  uint16_t activeColor  
) {  
  
  tft.fillCircle(  
    x,  
    y,  
    4,  
    online ? activeColor : C_RED_T  
  );  
  
  tft.drawCircle(  
    x,  
    y,  
    5,  
    C_BORDER  
  );  
}  
  
  
void drawCard(  
  int x,  
  int y,  
  int w,  
  int h  
) {  
  
  tft.fillRoundRect(  
    x, y, w, h, 8, C_SURFACE  
  );  
  
  tft.drawRoundRect(  
    x, y, w, h, 8, C_BORDER  
  );  
}  
  
  
void drawLabel(  
  int x,  
  int y,  
  const char *text  
) {  
  
  tft.setFont(&FreeSans9pt7b);  
  tft.setTextSize(1);  
  
  tft.setTextColor(  
    C_MUTED,  
    C_SURFACE  
  );  
  
  tft.setCursor(x, y);  
  tft.print(text);  
}  
  
  
void drawValue(  
  int x,  
  int y,  
  const char *text,  
  uint16_t color,  
  const GFXfont *font  
) {  
  
  tft.setFont(font);  
  tft.setTextSize(1);  
  
  tft.setTextColor(  
    color,  
    C_SURFACE  
  );  
  
  tft.setCursor(x, y);  
  tft.print(text);  
}  
  
  
void drawCentered(  
  int cx,  
  int baselineY,  
  const char *text,  
  const GFXfont *font,  
  uint16_t color  
) {  
  
  int16_t x1, y1;  
  uint16_t w, h;  
  
  tft.setFont(font);  
  
  tft.getTextBounds(  
    text,  
    0,  
    baselineY,  
    &x1,  
    &y1,  
    &w,  
    &h  
  );  
  
  tft.setTextColor(  
    color,  
    C_BG  
  );  
  
  tft.setCursor(  
    cx - ((int)w / 2),  
    baselineY  
  );  
  
  tft.print(text);  
}  
  
  
void drawFooter(  
  const char *leftText,  
  const char *rightText  
) {  
  
  tft.fillRect(  
    0, 216, 320, 24, C_SURFACE  
  );  
  
  tft.drawFastHLine(  
    0, 216, 320, C_BORDER  
  );  
  
  tft.setFont(&FreeSans9pt7b);  
  
  tft.setTextColor(  
    C_MUTED,  
    C_SURFACE  
  );  
  
  tft.setCursor(10, 232);  
  tft.print(leftText);  
  
  if (rightText && rightText[0]) {  
  
    int16_t x1, y1;  
    uint16_t w, h;  
  
    tft.getTextBounds(  
      rightText,  
      0,  
      232,  
      &x1,  
      &y1,  
      &w,  
      &h  
    );  
  
    tft.setCursor(310 - w, 232);  
    tft.print(rightText);  
  }  
}  
  
  
// ============================================================  
//                      PAGE HEADER 
// ============================================================  
  
void drawPageHeader() {  
  
  tft.fillRect(  
    0, 0, 320, 28, C_SURFACE  
  );  
  
  tft.drawFastHLine(  
    0, 27, 320, C_BORDER  
  );  
  
  const char *title = "MINE ROVER";  
  
  switch (currentPage) {  
  
    case PAGE_SYSTEM:  
      title = "MINE ROVER";  
      break;  
  
    case PAGE_DRIVE:  
      title = "DRIVE CONTROL";  
      break;  
  
    case PAGE_GAS:  
      title = "GAS MONITOR";  
      break;  
  
    case PAGE_ENV:  
      title = "ENVIRONMENT";  
      break;  
  
    case PAGE_VIDEO:  
      title = "EDGE AI";  
      break;  
  }  
  
  tft.setFont(&FreeSansBold9pt7b);  
  
  tft.setTextColor(  
    C_TEXT,  
    C_SURFACE  
  );  
  
  tft.setCursor(9, 19);  
  tft.print(title);  
  
  drawStatusDot(  
    245,  
    14,  
    roverOnline,  
    C_GREEN  
  );  
  
  tft.setFont(&FreeSans9pt7b);  
  
  tft.setTextColor(  
    roverOnline ? C_GREEN : C_RED_T,  
    C_SURFACE  
  );  
  
  tft.setCursor(254, 19);  
  
  tft.print(  
    roverOnline ? "ROVER" : "OFFLINE"  
  );  
  
  tft.setTextColor(  
    C_MUTED,  
    C_SURFACE  
  );  
  
  tft.setCursor(299, 19);  
  
  tft.printf(  
    "%d/5",  
    ((uint8_t)currentPage) + 1  
  );  
}  
  
  
// ============================================================  
//                        SYSTEM PAGE 
// ============================================================  
  
void drawSystemPage() {  
  
  drawPageHeader();  
  
  drawCentered(  
    160,  
    56,  
    "RESCUE ROVER",  
    &FreeSansBold18pt7b,  
    C_TEXT  
  );  
  
  drawCentered(  
    160,  
    80,  
    "MISSION CONSOLE",  
    &FreeSans9pt7b,  
    C_MUTED  
  );  
  
  drawCard(10, 94, 145, 48);  
  
  drawCard(165, 94, 145, 48);  
  
  drawCard(10, 150, 145, 48);  
  
  drawCard(165, 150, 145, 48);  
  
  drawLabel(20, 113, "ROVER LINK");  
  
  drawLabel(175, 113, "EDGE AI VIDEO");  
  
  drawLabel(20, 169, "GAS TELEMETRY");  
  
  drawLabel(175, 169, "ENV TELEMETRY");  
  
  drawValue(  
    20,  
    134,  
    roverOnline ? "CONNECTED" : "OFFLINE",  
    roverOnline ? C_GREEN : C_RED_T,  
    &FreeSansBold9pt7b  
  );  
  
  drawValue(  
    175,  
    134,  
    wifiConnected ? "NETWORK READY" : "NO WIFI",  
    wifiConnected ? C_GREEN : C_MUTED,  
    &FreeSansBold9pt7b  
  );  
  
  drawValue(  
    20,  
    190,  
    telemetryFresh() ? "LIVE" : "NO DATA",  
    telemetryFresh() ? C_GREEN : C_RED_T,  
    &FreeSansBold9pt7b  
  );  
  
  drawValue(  
    175,  
    190,  
    telemetryFresh() ? "LIVE" : "NO DATA",  
    telemetryFresh() ? C_GREEN : C_RED_T,  
    &FreeSansBold9pt7b  
  );  
  
  drawFooter(  
    roverOnline ? "ROVER LINK ACTIVE" : "ROVER LINK LOST",  
    "TOUCH / NEXT"  
  );  
}  
  
  
// ============================================================  
//                        DRIVE PAGE 
// ============================================================  
  
void drawDrivePage() {  
  
  drawPageHeader();  
  
  drawCard(10, 38, 145, 126);  
  
  drawLabel(20, 58, "JOYSTICK 1");  
  
  drawValue(  
    20,  
    78,  
    "FWD / REV",  
    C_ACCENT,  
    &FreeSansBold9pt7b  
  );  
  
  tft.drawCircle(82, 116, 38, C_BORDER);  
  
  tft.drawFastHLine(44, 116, 76, C_BORDER);  
  
  tft.drawFastVLine(82, 78, 76, C_BORDER);  
  
  drawCard(165, 38, 145, 126);  
  
  drawLabel(175, 58, "JOYSTICK 2");  
  
  drawValue(  
    175,  
    78,  
    "LEFT / RIGHT",  
    C_ACCENT,  
    &FreeSansBold9pt7b  
  );  
  
  tft.drawCircle(237, 116, 38, C_BORDER);  
  
  tft.drawFastHLine(199, 116, 76, C_BORDER);  
  
  tft.drawFastVLine(237, 78, 76, C_BORDER);  
  
  drawCard(10, 173, 93, 34);  
  
  drawCard(113, 173, 93, 34);  
  
  drawCard(216, 173, 94, 34);  
  
  char buf[32];  
  
  snprintf(  
    buf,  
    sizeof(buf),  
    "L %+d",  
    currentLeftSpeed  
  );  
  
  drawCentered(  
    56,  
    196,  
    buf,  
    &FreeSansBold9pt7b,  
    C_TEXT  
  );  
  
  snprintf(  
    buf,  
    sizeof(buf),  
    "R %+d",  
    currentRightSpeed  
  );  
  
  drawCentered(  
    159,  
    196,  
    buf,  
    &FreeSansBold9pt7b,  
    C_TEXT  
  );  
  
  bool moving =  
    (currentLeftSpeed != 0 || currentRightSpeed != 0);  
  
  drawCentered(  
    263,  
    196,  
    moving ? "MOVING" : "READY",  
    &FreeSansBold9pt7b,  
    moving ? C_GREEN : C_MUTED  
  );  
  
  drawFooter(  
    "J1 FWD/REV  J2 L/R",  
    roverOnline ? "LINK OK" : "LINK OFFLINE"  
  );  
}  
  
  
// ============================================================  
//                 LIVE DRIVE JOYSTICK UPDATE 
// ============================================================  
  
void updateDriveLive() {  
  
  if (currentPage != PAGE_DRIVE) {  
    return;  
  }  
  
  tft.fillRect(43, 77, 78, 79, C_SURFACE);  
  
  tft.fillRect(198, 77, 79, 79, C_SURFACE);  
  
  tft.drawCircle(82, 116, 38, C_BORDER);  
  
  tft.drawFastHLine(44, 116, 76, C_BORDER);  
  
  tft.drawFastVLine(82, 78, 76, C_BORDER);  
  
  tft.drawCircle(237, 116, 38, C_BORDER);  
  
  tft.drawFastHLine(199, 116, 76, C_BORDER);  
  
  tft.drawFastVLine(237, 78, 76, C_BORDER);  
  
  int j1Y = analogRead(JOY1_Y);  
  
  int j2X = analogRead(JOY2_X);  
  
  int y = map(  
    j1Y,  
    0,  
    4095,  
    149,  
    83  
  );  
  
  int x = map(  
    j2X,  
    0,  
    4095,  
    204,  
    270  
  );  
  
  tft.fillCircle(  
    82,  
    y,  
    5,  
    C_CYAN  
  );  
  
  tft.fillCircle(  
    x,  
    116,  
    5,  
    C_ACCENT  
  );  
  
  tft.fillRect(  
    18,  
    178,  
    277,  
    22,  
    C_SURFACE  
  );  
  
  char buf[40];  
  
  snprintf(  
    buf,  
    sizeof(buf),  
    "L %+d       R %+d",  
    currentLeftSpeed,  
    currentRightSpeed  
  );  
  
  drawCentered(  
    156,  
    196,  
    buf,  
    &FreeSansBold9pt7b,  
    C_TEXT  
  );  
}  
  
  
// ============================================================  
//                         GAS PAGE 
// ============================================================  
  
void drawGasPage() {  
  
  drawPageHeader();  
  
  bool fresh = telemetryFresh();  
  
  drawCard(10, 38, 145, 76);  
  
  drawLabel(20, 57, "CH4 / METHANE");  
  
  drawCard(165, 38, 145, 76);  
  
  drawLabel(175, 57, "CO / CO");  
  
  drawCard(10, 122, 145, 76);  
  
  drawLabel(20, 141, "CO2 / CARBON");  
  
  drawCard(165, 122, 145, 76);  
  
  drawLabel(175, 141, "O2 / OXYGEN");  
  
  updateMetricValue(  
    10,  
    38,  
    145,  
    76,  
    gasData.methaneLEL,  
    2,  
    fresh  
  );  
  
  updateMetricValue(  
    165,  
    38,  
    145,  
    76,  
    gasData.carbonMonoxide,  
    1,  
    fresh  
  );  
  
  updateMetricValue(  
    10,  
    122,  
    145,  
    76,  
    gasData.carbonDioxide,  
    0,  
    fresh  
  );  
  
  updateMetricValue(  
    165,  
    122,  
    145,  
    76,  
    gasData.oxygenPercent,  
    1,  
    fresh  
  );  
  
  tft.setFont(&FreeSans9pt7b);  
  
  tft.setTextColor(  
    C_MUTED,  
    C_SURFACE  
  );  
  
  tft.setCursor(112, 103);  
  
  tft.print("%LEL");  
  
  tft.setCursor(281, 103);  
  
  tft.print("ppm");  
  
  tft.setCursor(281, 187);  
  
  tft.print("ppm");  
  
  tft.fillRect(255, 168, 45, 22, C_SURFACE);  
  
  tft.setTextColor(  
    C_MUTED,  
    C_SURFACE  
  );  
  
  tft.setCursor(264, 187);  
  
  tft.print("%VOL");  
  
  drawFooter(  
    "ATMOSPHERE TELEMETRY",  
    fresh ? "LIVE" : "NO DATA"  
  );  
}  
  
  
// ============================================================  
//                     GAS LIVE VALUE UPDATE 
// ============================================================  
  
void updateGasLiveValues() {  
  
  if (currentPage != PAGE_GAS) {  
    return;  
  }  
  
  bool fresh = telemetryFresh();  
  
  updateMetricValue(  
    10,  
    38,  
    145,  
    76,  
    gasData.methaneLEL,  
    2,  
    fresh  
  );  
  
  updateMetricValue(  
    165,  
    38,  
    145,  
    76,  
    gasData.carbonMonoxide,  
    1,  
    fresh  
  );  
  
  updateMetricValue(  
    10,  
    122,  
    145,  
    76,  
    gasData.carbonDioxide,  
    0,  
    fresh  
  );  
  
  updateMetricValue(  
    165,  
    122,  
    145,  
    76,  
    gasData.oxygenPercent,  
    1,  
    fresh  
  );  
}  
  
  
// ============================================================  
//                    ENVIRONMENT PAGE 
// ============================================================  
  
void drawEnvironmentPage() {  
  
  drawPageHeader();  
  
  bool fresh = telemetryFresh();  
  
  drawCard(10, 40, 300, 47);  
  
  drawLabel(20, 58, "TEMPERATURE");  
  
  drawCard(10, 94, 300, 47);  
  
  drawLabel(20, 112, "HUMIDITY");  
  
  drawCard(10, 148, 300, 47);  
  
  drawLabel(20, 166, "AIR PRESSURE");  
  
  updateMetricValue(  
    10,  
    40,  
    300,  
    47,  
    environmentData.temperature,  
    1,  
    fresh  
  );  
  
  updateMetricValue(  
    10,  
    94,  
    300,  
    47,  
    environmentData.humidity,  
    1,  
    fresh  
  );  
  
  updateMetricValue(  
    10,  
    148,  
    300,  
    47,  
    environmentData.pressure,  
    1,  
    fresh  
  );  
  
  tft.setFont(&FreeSans9pt7b);  
  
  tft.setTextColor(  
    C_MUTED,  
    C_SURFACE  
  );  
  
  tft.setCursor(255, 80);  
  tft.print("deg C");  
  
  tft.setCursor(265, 134);  
  tft.print("%RH");  
  
  tft.setCursor(255, 188);  
  tft.print("hPa");  
  
  drawFooter(  
    "ENVIRONMENT TELEMETRY",  
    fresh ? "LIVE" : "NO DATA"  
  );  
}  
  
  
// ============================================================  
//              ENVIRONMENT LIVE VALUE UPDATE 
// ============================================================  
  
void updateEnvironmentLiveValues() {  
  
  if (currentPage != PAGE_ENV) {  
    return;  
  }  
  
  bool fresh = telemetryFresh();  
  
  updateMetricValue(  
    10,  
    40,  
    300,  
    47,  
    environmentData.temperature,  
    1,  
    fresh  
  );  
  
  updateMetricValue(  
    10,  
    94,  
    300,  
    47,  
    environmentData.humidity,  
    1,  
    fresh  
  );  
  
  updateMetricValue(  
    10,  
    148,  
    300,  
    47,  
    environmentData.pressure,  
    1,  
    fresh  
  );  
}  
  
  
// ============================================================  
//                  TELEMETRY VALUE RENDERING 
// ============================================================  
  
void updateMetricValue(  
  int x,  
  int y,  
  int w,  
  int h,  
  float value,  
  int decimals,  
  bool fresh  
) {  
  
  int valueX = x + 10;  
  
  int valueY = y + 20;  
  
  int valueW = min(w - 78, 210);  
  
  int valueH = h - 22;  
  
  tft.fillRect(  
    valueX - 2,  
    valueY,  
    valueW,  
    valueH,  
    C_SURFACE  
  );  
  
  if (!fresh) {  
  
    drawValue(  
      valueX,  
      y + h - 9,  
      "NO DATA",  
      C_RED_T,  
      &FreeSansBold9pt7b  
    );  
  
    return;  
  }  
  
  char valueBuf[32];  
  
  snprintf(  
    valueBuf,  
    sizeof(valueBuf),  
    "%.*f",  
    decimals,  
    value  
  );  
  
  drawValue(  
    valueX,  
    y + h - 9,  
    valueBuf,  
    C_TEXT,  
    &FreeSansBold12pt7b  
  );  
}  
  
  
// ============================================================  
//                       PAGE RENDERING 
// ============================================================  
  
void updateCurrentPage() {  
  
  if (headerDirty) {  
  
    drawPageHeader();  
  
    headerDirty = false;  
  }  
  
  if (  
    millis() - lastUiRefresh <  
    UI_REFRESH_INTERVAL  
  ) {  
  
    return;  
  }  
  
  lastUiRefresh = millis();  
  
  switch (currentPage) {  
  
    case PAGE_SYSTEM:  
  
      tft.fillRect(  
        18,  
        119,  
        130,  
        18,  
        C_SURFACE  
      );  
  
      drawValue(  
        20,  
        134,  
        roverOnline ? "CONNECTED" : "OFFLINE",  
        roverOnline ? C_GREEN : C_RED_T,  
        &FreeSansBold9pt7b  
      );  
  
      tft.fillRect(  
        173,  
        119,  
        136,  
        18,  
        C_SURFACE  
      );  
  
      drawValue(  
        175,  
        134,  
        wifiConnected ? "NETWORK READY" : "NO WIFI",  
        wifiConnected ? C_GREEN : C_MUTED,  
        &FreeSansBold9pt7b  
      );  
  
      tft.fillRect(  
        18,  
        175,  
        130,  
        18,  
        C_SURFACE  
      );  
  
      drawValue(  
        20,  
        190,  
        telemetryFresh() ? "LIVE" : "NO DATA",  
        telemetryFresh() ? C_GREEN : C_RED_T,  
        &FreeSansBold9pt7b  
      );  
  
      tft.fillRect(  
        173,  
        175,  
        136,  
        18,  
        C_SURFACE  
      );  
  
      drawValue(  
        175,  
        190,  
        telemetryFresh() ? "LIVE" : "NO DATA",  
        telemetryFresh() ? C_GREEN : C_RED_T,  
        &FreeSansBold9pt7b  
      );  
  
      break;  
  
    case PAGE_DRIVE:  
      updateDriveLive();  
      break;  
  
    case PAGE_GAS:  
      updateGasLiveValues();  
      break;  
  
    case PAGE_ENV:  
      updateEnvironmentLiveValues();  
      break;  
  
    case PAGE_VIDEO:  
      pageLiveFeed();  
      break;  
  }  
}  
  
  
// ============================================================  
//                        TOUCH CONTROL 
// ============================================================  
  
void handleTouch() {  
  
  bool currentTouch = digitalRead(TOUCH_PIN);  
  
  if (  
    currentTouch == HIGH &&  
    lastTouchState == LOW &&  
    millis() - lastTouchTime > debounceDelay  
  ) {  
  
    int oldPage = (int)currentPage;  
  
    currentPage =  
      (Page)(((uint8_t)currentPage + 1) % TOTAL_PAGES);  
  
    lastTouchTime = millis();  
  
    if (  
      oldPage == PAGE_VIDEO &&  
      videoClient.connected()  
    ) {  
  
      videoClient.stop();  
    }  
  
    frameLen = 0;  
  
    capturingFrame = false;  
  
    piStreamFailed = false;  
  
    piViewState = -1;  
  
    tft.fillScreen(C_BG);  
  
    switch (currentPage) {  
  
      case PAGE_SYSTEM:  
        drawSystemPage();  
        break;  
  
      case PAGE_DRIVE:  
        drawDrivePage();  
        break;  
  
      case PAGE_GAS:  
        drawGasPage();  
        break;  
  
      case PAGE_ENV:  
        drawEnvironmentPage();  
        break;  
  
      case PAGE_VIDEO:  
  
        drawPageHeader();  
  
        tft.fillRect(  
          0,  
          28,  
          320,  
          188,  
          C_BG  
        );  
  
        pageLiveFeed();  
  
        break;  
    }  
  
    headerDirty = false;  
  }  
  
  lastTouchState = currentTouch;  
}  
  
  
// ============================================================  
//                       VIDEO STOP 
// ============================================================  
  
void stopVideoClient() {  
  
  if (videoClient.connected()) {  
    videoClient.stop();  
  }  
  
  frameLen = 0;  
  
  capturingFrame = false;  
}  
  
  
// ============================================================  
//                    START PI VIDEO STREAM 
// ============================================================  
  
void startVideoIfNeeded() {  
  
  if (currentPage != PAGE_VIDEO) {  
    return;  
  }  
  
  if (!wifiConnected) {  
    return;  
  }  
  
  if (videoClient.connected()) {  
    return;  
  }  
  
  if (  
    millis() - lastPiAttempt <  
    PI_RETRY_INTERVAL  
  ) {  
    return;  
  }  
  
  lastPiAttempt = millis();  
  
  if (  
    videoClient.connect(  
      pi_host,  
      pi_port,  
      PI_CONNECT_TIMEOUT  
    )  
  ) {  
  
    videoClient.print(  
      String("GET ") +  
      pi_path +  
      " HTTP/1.1\r\n" +  
      "Host: " +  
      pi_host +  
      "\r\n" +  
      "Connection: keep-alive\r\n\r\n"  
    );  
  
    frameLen = 0;  
  
    capturingFrame = false;  
  
    piStreamFailed = false;  
  
    piViewState = 1;  
  
  } else {  
  
    videoClient.stop();  
  
    piStreamFailed = true;  
  
    piViewState = 2;  
  }  
}  
  
  
// ============================================================  
//                     VIDEO STATUS OVERLAY 
// ============================================================  
  
void drawVideoOverlay() {  
  
  tft.fillRect(  
    0,  
    207,  
    320,  
    33,  
    C_SURFACE  
  );  
  
  tft.drawFastHLine(  
    0,  
    207,  
    320,  
    C_BORDER  
  );  
  
  tft.setFont(&FreeSans9pt7b);  
  
  tft.setTextColor(  
    roverOnline ? C_GREEN : C_RED_T,  
    C_SURFACE  
  );  
  
  tft.setCursor(9, 228);  
  
  tft.print(  
    roverOnline ? "ROVER LINK OK" : "ROVER OFFLINE"  
  );  
  
  tft.setTextColor(  
    wifiConnected ? C_GREEN : C_RED_T,  
    C_SURFACE  
  );  
  
  tft.setCursor(228, 228);  
  
  tft.print(  
    wifiConnected ? "STREAM LINK" : "NO STREAM"  
  );  
}  
  
  
// ============================================================  
//                     VIDEO PAGE 
// ============================================================  
  
void pageLiveFeed() {  
  
  if (currentPage != PAGE_VIDEO) {  
    return;  
  }  
  
  if (!wifiConnected) {  
  
    if (piViewState != 0) {  
  
      tft.fillRect(  
        0,  
        28,  
        320,  
        179,  
        C_BG  
      );  
  
      drawCard(14, 48, 292, 126);  
  
      drawCentered(  
        160,  
        86,  
        "VIDEO LINK",  
        &FreeSansBold12pt7b,  
        C_TEXT  
      );  
  
      tft.fillRect(  
        30,  
        102,  
        260,  
        45,  
        C_SURFACE  
      );  
  
      tft.setFont();  
  
      tft.setTextSize(1);  
  
      tft.setTextColor(  
        C_RED_T,  
        C_SURFACE  
      );  
  
      tft.setCursor(90, 118);  
  
      tft.print("WI-FI UNAVAILABLE");  
  
      tft.setTextColor(  
        C_MUTED,  
        C_SURFACE  
      );  
  
      tft.setCursor(72, 137);  
  
      tft.print("Touch for next page");  
  
      drawVideoOverlay();  
  
      piViewState = 0;  
    }  
  
    return;  
  }  
  
  if (!videoClient.connected()) {  
  
    bool canAttempt =  
      (millis() - lastPiAttempt >= PI_RETRY_INTERVAL);  
  
    if (canAttempt) {  
  
      lastPiAttempt = millis();  
  
      if (piViewState != 1) {  
  
        tft.fillRect(  
          0,  
          28,  
          320,  
          179,  
          C_BG  
        );  
  
        drawCard(  
          14,  
          48,  
          292,  
          126  
        );  
  
        drawCentered(  
          160,  
          86,  
          "CONNECTING",  
          &FreeSansBold12pt7b,  
          C_BLUE  
        );  
  
        tft.fillRect(  
          30,  
          102,  
          260,  
          45,  
          C_SURFACE  
        );  
  
        tft.setFont();  
  
        tft.setTextSize(1);  
  
        tft.setTextColor(  
          C_TEXT,  
          C_SURFACE  
        );  
  
        tft.setCursor(76, 118);  
  
        tft.print("RASPBERRY PI VIDEO");  
  
        tft.setTextColor(  
          C_MUTED,  
          C_SURFACE  
        );  
  
        tft.setCursor(74, 137);  
  
        tft.print("Opening live stream...");  
  
        drawVideoOverlay();  
  
        piViewState = 1;  
      }  
  
      if (  
        videoClient.connect(  
          pi_host,  
          pi_port,  
          PI_CONNECT_TIMEOUT  
        )  
      ) {  
  
        videoClient.print(  
          String("GET ") +  
          pi_path +  
          " HTTP/1.1\r\n" +  
          "Host: " +  
          pi_host +  
          "\r\n" +  
          "Connection: keep-alive\r\n\r\n"  
        );  
  
        frameLen = 0;  
  
        capturingFrame = false;  
  
        piStreamFailed = false;  
  
        piViewState = 1;  
  
      } else {  
  
        videoClient.stop();  
  
        piStreamFailed = true;  
  
        piViewState = 2;  
  
        tft.fillRect(  
          0,  
          28,  
          320,  
          179,  
          C_BG  
        );  
  
        drawCard(  
          14,  
          48,  
          292,  
          126  
        );  
  
        drawCentered(  
          160,  
          86,  
          "VIDEO UNAVAILABLE",  
          &FreeSansBold12pt7b,  
          C_TEXT  
        );  
  
        tft.fillRect(  
          30,  
          102,  
          260,  
          45,  
          C_SURFACE  
        );  
  
        tft.setFont();  
  
        tft.setTextSize(1);  
  
        tft.setTextColor(  
          C_RED_T,  
          C_SURFACE  
        );  
  
        tft.setCursor(87, 118);  
  
        tft.print("PI STREAM FAILED");  
  
        tft.setTextColor(  
          C_MUTED,  
          C_SURFACE  
        );  
  
        tft.setCursor(72, 137);  
  
        tft.print("Retrying automatically");  
  
        drawVideoOverlay();  
      }  
    }  
  
    return;  
  }  
  
  while (videoClient.available()) {  
  
    uint8_t b = videoClient.read();  
  
    if (!capturingFrame) {  
  
      if (  
        frameLen > 0 &&  
        frameBuf[0] == 0xFF &&  
        b == 0xD8  
      ) {  
  
        capturingFrame = true;  
  
        frameBuf[0] = 0xFF;  
  
        frameBuf[1] = 0xD8;  
  
        frameLen = 2;  
  
        continue;  
      }  
  
      frameBuf[0] = b;  
  
      frameLen = 1;  
  
    }  
  
    else {  
  
      if (frameLen < JPEG_BUF_SIZE) {  
  
        frameBuf[frameLen++] = b;  
  
      } else {  
  
        capturingFrame = false;  
  
        frameLen = 0;  
  
        continue;  
      }  
  
      if (  
        frameLen >= 2 &&  
        frameBuf[frameLen - 2] == 0xFF &&  
        frameBuf[frameLen - 1] == 0xD9  
      ) {  
  
        TJpgDec.drawJpg(  
          0,  
          28,  
          frameBuf,  
          frameLen  
        );  
  
        capturingFrame = false;  
  
        frameLen = 0;  
  
        piViewState = 3;  
  
        piStreamFailed = false;  
  
        lastVideoOverlay = millis();  
  
        drawVideoOverlay();  
  
        return;  
      }  
    }  
  }  
  
  if (  
    millis() - lastVideoOverlay >  
    1000  
  ) {  
  
    drawVideoOverlay();  
  
    lastVideoOverlay = millis();  
  }  
}  
  
  
// ============================================================  
//                            SETUP 
// ============================================================  
  
void setup() {  
  
  Serial.begin(115200);  
  
  delay(500);  
  
  Serial.println();  
  
  Serial.println(  
    "=========================================="  
  );  
  
  Serial.println(  
    "       MINE ROVER CONTROLLER FINAL"  
  );  
  
  Serial.println(  
    "=========================================="  
  );  
  
  pinMode(JOY1_SW, INPUT_PULLUP);  
  
  pinMode(JOY2_SW, INPUT_PULLUP);  
  
  pinMode(TOUCH_PIN, INPUT);  
  
  analogReadResolution(12);  
  
  SPI.begin(  
    TFT_SCK,  
    TFT_MISO,  
    TFT_MOSI  
  );  
  
  tft.begin();  
  
  tft.setRotation(3);  
  
  tft.setTextWrap(false);  
  
  tft.fillScreen(C_BG);  
  
  TJpgDec.setJpgScale(1);  
  
  TJpgDec.setSwapBytes(false);  
  
  TJpgDec.setCallback(tft_output);  
  
  WiFi.mode(WIFI_AP_STA);  
  
  WiFi.setSleep(false);  
  
  WiFi.softAPConfig(  
    controllerIP,  
    apGateway,  
    apSubnet  
  );  
  
  bool apStarted =  
    WiFi.softAP(  
      rover_ap_ssid,  
      rover_ap_password  
    );  
  
  if (apStarted) {  
  
    Serial.println(  
      "ROVER CONTROL AP STARTED"  
    );  
  
    Serial.print("AP SSID: ");  
  
    Serial.println(rover_ap_ssid);  
  
    Serial.print("AP PASSWORD: ");  
  
    Serial.println(rover_ap_password);  
  
    Serial.print("CONTROLLER AP IP: ");  
  
    Serial.println(WiFi.softAPIP());  
  
  } else {  
  
    Serial.println("AP START FAILED");  
  }  
  
  Serial.println();  
  
  Serial.print(  
    "Connecting to mobile Wi-Fi: "  
  );  
  
  Serial.println(wifi_ssid);  
  
  WiFi.begin(  
    wifi_ssid,  
    wifi_password  
  );  
  
  int wifiAttempts = 0;  
  
  while (  
    WiFi.status() != WL_CONNECTED &&  
    wifiAttempts < 30  
  ) {  
  
    delay(500);  
  
    Serial.print(".");  
  
    wifiAttempts++;  
  }  
  
  Serial.println();  
  
  if (WiFi.status() == WL_CONNECTED) {  
  
    wifiConnected = true;  
  
    Serial.println(  
      "MOBILE WIFI CONNECTED"  
    );  
  
    Serial.print(  
      "CONTROLLER STA IP: "  
    );  
  
    Serial.println(WiFi.localIP());  
  
    Serial.print("RSSI: ");  
  
    Serial.println(WiFi.RSSI());  
  
  } else {  
  
    wifiConnected = false;  
  
    Serial.println(  
      "MOBILE WIFI NOT CONNECTED"  
    );  
  }  
  
  udp.begin(UDP_PORT);  
  
  Serial.print("UDP PORT: ");  
  
  Serial.println(UDP_PORT);  
  
  tft.fillScreen(C_BG);  
  
  drawSystemPage();  
  
  headerDirty = false;  
  
  Serial.println();  
  
  Serial.println("CONTROLLER READY");  
  
  Serial.println("DRIVE ACTIVE ON ALL PAGES");  
  
  Serial.println(  
    "TELEMETRY: T,CH4,CO,CO2,O2,TEMP,HUM,PRESS"  
  );  
  
  Serial.println(  
    "=========================================="  
  );  
}  
  
  
// ============================================================  
//                             LOOP 
// ============================================================  
  
void loop() {  
  
  // ----------------------------------------------------------  
  // 1. Receive rover heartbeat + telemetry 
  // ----------------------------------------------------------  
  
  receiveRoverHeartbeat();  
  
  
  // ----------------------------------------------------------  
  // 2. WiFi state 
  // ----------------------------------------------------------  
  
  bool wifiNow =  
    (WiFi.status() == WL_CONNECTED);  
  
  if (wifiNow != wifiConnected) {  
  
    wifiConnected = wifiNow;  
  
    headerDirty = true;  
  }  
  
  
  // ----------------------------------------------------------  
  // 3. Rover timeout 
  // ----------------------------------------------------------  
  
  if (  
    roverOnline &&  
    millis() - lastRoverHeartbeat >  
      ROVER_TIMEOUT  
  ) {  
  
    roverOnline = false;  
  
    telemetryValid = false;  
  
    headerDirty = true;  
  
    Serial.println("ROVER OFFLINE");  
  
    sendImmediateStop();  
  }  
  
  
  // ----------------------------------------------------------  
  // 3A. Live telemetry generation 
  // ----------------------------------------------------------  
  
  if (roverOnline) {  
  
    updateSimulatedTelemetry();  
  }  
  
  
  // ----------------------------------------------------------  
  // 4. Drive remains active on EVERY page 
  // ----------------------------------------------------------  
  
  handleDriveControl();  
  
  
  // ----------------------------------------------------------  
  // 5. Touch navigation 
  // ----------------------------------------------------------  
  
  handleTouch();  
  
  
  // ----------------------------------------------------------  
  // 6. Live UI 
  // ----------------------------------------------------------  
  
  updateCurrentPage();  
  
  
  // ----------------------------------------------------------  
  // 7. Live YOLO feed 
  // ----------------------------------------------------------  
  
  if (currentPage == PAGE_VIDEO) {  
  
    pageLiveFeed();  
  }  
  
  
  delay(2);  
}