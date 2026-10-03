#include <WiFi.h>
#include <WiFiUdp.h>

// =====================================================
//                  ROVER WIFI
// =====================================================

const char* WIFI_SSID = "ROVER_CONTROL";
const char* WIFI_PASSWORD = "rover123";

IPAddress local_IP(192, 168, 50, 2);
IPAddress gateway(192, 168, 50, 1);
IPAddress subnet(255, 255, 255, 0);

IPAddress controller_IP(192, 168, 50, 1);

WiFiUDP udp;

const uint16_t UDP_PORT = 4210;


// =====================================================
//              LEFT BTS7960
// =====================================================

#define LEFT_RPWM 25
#define LEFT_LPWM 33
#define LEFT_REN  32
#define LEFT_LEN  27


// =====================================================
//              RIGHT BTS7960
// =====================================================

#define RIGHT_RPWM 26
#define RIGHT_LPWM 14
#define RIGHT_REN  12
#define RIGHT_LEN  13


// =====================================================
//                 PWM SETTINGS
// =====================================================

#define PWM_FREQ 20000
#define PWM_RESOLUTION 8


// =====================================================
//                   SPEED LIMIT
// =====================================================

// 30% lower than old 255
#define MAX_MOTOR_SPEED 179


// =====================================================
//                 FAILSAFE
// =====================================================

#define MOTOR_TIMEOUT 350

unsigned long lastMotorPacket = 0;

unsigned long lastHeartbeat = 0;

bool roverConnected = false;


// =====================================================
//                 PACKET BUFFER
// =====================================================

char packetBuffer[100];


// =====================================================
//                 STOP MOTORS
// =====================================================

void stopMotors() {

  ledcWrite(
    LEFT_RPWM,
    0
  );

  ledcWrite(
    LEFT_LPWM,
    0
  );


  ledcWrite(
    RIGHT_RPWM,
    0
  );

  ledcWrite(
    RIGHT_LPWM,
    0
  );


  digitalWrite(
    LEFT_REN,
    LOW
  );

  digitalWrite(
    LEFT_LEN,
    LOW
  );


  digitalWrite(
    RIGHT_REN,
    LOW
  );

  digitalWrite(
    RIGHT_LEN,
    LOW
  );
}


// =====================================================
//                 LEFT MOTOR
// =====================================================

void setLeftMotor(
  int speedValue
) {

  speedValue =
    constrain(
      speedValue,
      -MAX_MOTOR_SPEED,
      MAX_MOTOR_SPEED
    );


  if (speedValue == 0) {

    ledcWrite(
      LEFT_RPWM,
      0
    );

    ledcWrite(
      LEFT_LPWM,
      0
    );

    digitalWrite(
      LEFT_REN,
      LOW
    );

    digitalWrite(
      LEFT_LEN,
      LOW
    );

    return;
  }


  digitalWrite(
    LEFT_REN,
    HIGH
  );

  digitalWrite(
    LEFT_LEN,
    HIGH
  );


  if (speedValue > 0) {

    // FORWARD

    ledcWrite(
      LEFT_RPWM,
      speedValue
    );

    ledcWrite(
      LEFT_LPWM,
      0
    );

  } else {

    // BACKWARD

    ledcWrite(
      LEFT_RPWM,
      0
    );

    ledcWrite(
      LEFT_LPWM,
      abs(speedValue)
    );
  }
}


// =====================================================
//                 RIGHT MOTOR
// =====================================================

void setRightMotor(
  int speedValue
) {

  speedValue =
    constrain(
      speedValue,
      -MAX_MOTOR_SPEED,
      MAX_MOTOR_SPEED
    );


  if (speedValue == 0) {

    ledcWrite(
      RIGHT_RPWM,
      0
    );

    ledcWrite(
      RIGHT_LPWM,
      0
    );

    digitalWrite(
      RIGHT_REN,
      LOW
    );

    digitalWrite(
      RIGHT_LEN,
      LOW
    );

    return;
  }


  digitalWrite(
    RIGHT_REN,
    HIGH
  );

  digitalWrite(
    RIGHT_LEN,
    HIGH
  );


  if (speedValue > 0) {

    // FORWARD

    ledcWrite(
      RIGHT_RPWM,
      speedValue
    );

    ledcWrite(
      RIGHT_LPWM,
      0
    );

  } else {

    // BACKWARD

    ledcWrite(
      RIGHT_RPWM,
      0
    );

    ledcWrite(
      RIGHT_LPWM,
      abs(speedValue)
    );
  }
}


// =====================================================
//                 DRIVE MOTORS
// =====================================================

void driveMotors(
  int leftSpeed,
  int rightSpeed
) {

  leftSpeed =
    constrain(
      leftSpeed,
      -MAX_MOTOR_SPEED,
      MAX_MOTOR_SPEED
    );


  rightSpeed =
    constrain(
      rightSpeed,
      -MAX_MOTOR_SPEED,
      MAX_MOTOR_SPEED
    );


  setLeftMotor(
    leftSpeed
  );

  setRightMotor(
    rightSpeed
  );


  Serial.print(
    "MOTOR -> L:"
  );

  Serial.print(
    leftSpeed
  );

  Serial.print(
    " R:"
  );

  Serial.println(
    rightSpeed
  );
}


// =====================================================
//                 SEND HEARTBEAT
// =====================================================

void sendHeartbeat() {

  if (
    WiFi.status() !=
    WL_CONNECTED
  ) {

    return;
  }


  udp.beginPacket(
    controller_IP,
    UDP_PORT
  );


  udp.print(
    "H,"
  );

  udp.print(
    WiFi.localIP()
  );


  udp.endPacket();
}


// =====================================================
//                 RECEIVE PACKETS
// =====================================================

void receivePackets() {

  int packetSize =
    udp.parsePacket();


  if (packetSize <= 0) {

    return;
  }


  int len =
    udp.read(
      packetBuffer,
      sizeof(packetBuffer) - 1
    );


  if (len <= 0) {

    return;
  }


  packetBuffer[len] =
    '\0';


  Serial.print(
    "RX: "
  );

  Serial.println(
    packetBuffer
  );


  // ===================================================
  // MOTOR PACKET
  //
  // M,left,right
  // ===================================================

  if (
    packetBuffer[0] == 'M'
  ) {

    int leftSpeed = 0;

    int rightSpeed = 0;


    int result =
      sscanf(
        packetBuffer,
        "M,%d,%d",
        &leftSpeed,
        &rightSpeed
      );


    if (result == 2) {

      leftSpeed =
        constrain(
          leftSpeed,
          -MAX_MOTOR_SPEED,
          MAX_MOTOR_SPEED
        );


      rightSpeed =
        constrain(
          rightSpeed,
          -MAX_MOTOR_SPEED,
          MAX_MOTOR_SPEED
        );


      driveMotors(
        leftSpeed,
        rightSpeed
      );


      lastMotorPacket =
        millis();

      roverConnected =
        true;
    }
  }


  // ===================================================
  // STOP PACKET
  // ===================================================

  if (
    packetBuffer[0] == 'S'
  ) {

    stopMotors();

    lastMotorPacket =
      millis();

    Serial.println(
      "STOP COMMAND RECEIVED"
    );
  }
}


// =====================================================
//                     SETUP
// =====================================================

void setup() {

  Serial.begin(115200);

  delay(1000);


  Serial.println();

  Serial.println(
    "===================================="
  );

  Serial.println(
    "       MINE ROVER WIFI ROVER"
  );

  Serial.println(
    "===================================="
  );


  // ===================================================
  // MOTOR PIN SETUP
  // ===================================================

  pinMode(
    LEFT_REN,
    OUTPUT
  );

  pinMode(
    LEFT_LEN,
    OUTPUT
  );


  pinMode(
    RIGHT_REN,
    OUTPUT
  );

  pinMode(
    RIGHT_LEN,
    OUTPUT
  );


  // ===================================================
  // PWM SETUP
  // Arduino ESP32 Core 3.x
  // ===================================================

  ledcAttach(
    LEFT_RPWM,
    PWM_FREQ,
    PWM_RESOLUTION
  );


  ledcAttach(
    LEFT_LPWM,
    PWM_FREQ,
    PWM_RESOLUTION
  );


  ledcAttach(
    RIGHT_RPWM,
    PWM_FREQ,
    PWM_RESOLUTION
  );


  ledcAttach(
    RIGHT_LPWM,
    PWM_FREQ,
    PWM_RESOLUTION
  );


  // ===================================================
  // INITIAL MOTOR STOP
  // ===================================================

  stopMotors();


  // ===================================================
  // WIFI
  // ===================================================

  WiFi.mode(
    WIFI_STA
  );

  WiFi.setSleep(false);


  if (!WiFi.config(
        local_IP,
        gateway,
        subnet
      )) {

    Serial.println(
      "STATIC IP CONFIG FAILED"
    );
  }


  Serial.print(
    "Connecting to: "
  );

  Serial.println(
    WIFI_SSID
  );


  WiFi.begin(
    WIFI_SSID,
    WIFI_PASSWORD
  );


  int attempts = 0;


  while (
    WiFi.status() != WL_CONNECTED &&
    attempts < 30
  ) {

    delay(500);

    Serial.print(".");

    attempts++;
  }


  Serial.println();


  // ===================================================
  // WIFI STATUS
  // ===================================================

  if (
    WiFi.status() ==
    WL_CONNECTED
  ) {

    Serial.println(
      "===================================="
    );

    Serial.println(
      "       WIFI CONNECTED"
    );

    Serial.println(
      "===================================="
    );


    Serial.print(
      "SSID: "
    );

    Serial.println(
      WIFI_SSID
    );


    Serial.print(
      "ROVER IP: "
    );

    Serial.println(
      WiFi.localIP()
    );


    Serial.print(
      "GATEWAY: "
    );

    Serial.println(
      WiFi.gatewayIP()
    );


    Serial.print(
      "RSSI: "
    );

    Serial.println(
      WiFi.RSSI()
    );

  } else {

    Serial.println(
      "===================================="
    );

    Serial.println(
      "       WIFI CONNECTION FAILED"
    );

    Serial.println(
      "===================================="
    );


    stopMotors();
  }


  // ===================================================
  // UDP
  // ===================================================

  udp.begin(
    UDP_PORT
  );


  Serial.print(
    "UDP PORT: "
  );

  Serial.println(
    UDP_PORT
  );


  Serial.println();

  Serial.println(
    "ROVER READY"
  );
}


// =====================================================
//                     LOOP
// =====================================================

void loop() {


  // ===================================================
  // WIFI DISCONNECTED
  // ===================================================

  if (
    WiFi.status() !=
    WL_CONNECTED
  ) {

    if (roverConnected) {

      Serial.println(
        "WIFI LOST -> MOTOR STOP"
      );

      roverConnected = false;
    }


    stopMotors();

    delay(100);

    return;
  }


  // ===================================================
  // RECEIVE CONTROLLER DATA
  // ===================================================

  receivePackets();


  // ===================================================
  // MOTOR FAILSAFE
  // ===================================================

  if (
    millis() - lastMotorPacket >
    MOTOR_TIMEOUT
  ) {

    if (roverConnected) {

      Serial.println(
        "CONTROLLER TIMEOUT -> MOTOR STOP"
      );

      roverConnected = false;
    }


    stopMotors();
  }


  // ===================================================
  // HEARTBEAT
  // ===================================================

  if (
    millis() - lastHeartbeat >
    500
  ) {

    lastHeartbeat =
      millis();

    sendHeartbeat();
  }


  delay(5);
}