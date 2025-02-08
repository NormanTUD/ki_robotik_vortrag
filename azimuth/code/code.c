int motorPin = 9;  // Beispiel Pin für den Motor

void setup() {
	pinMode(motorPin, OUTPUT);
	Serial.begin(9600);
}

void loop() {
	int angle = stroke_here();

	// Bewege den Motor, bis stroke_here() 0 zurückgibt
	if (angle != 0) {
		if (angle > 0) {
			// Motor nach links bewegen (positive Winkel)
			analogWrite(motorPin, 255);
		} else {
			// Motor nach rechts bewegen (negative Winkel)
			analogWrite(motorPin, 0);
		}
	} else {
		stroke();
	}

	delay(500);  // Kurze Pause
}
