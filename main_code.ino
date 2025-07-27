const int irPins[] = {3, 4, 5, 6, 7, 8, 9, 10, 11, 12};
const int numKeys = sizeof(irPins) / sizeof(irPins[0]);

const int buttonPin = 2;  
int instrumentIndex = 0;  
bool lastButtonState = HIGH;  
unsigned long lastDebounceTime = 0;
const unsigned long debounceDelay = 300;  

const int pianoNotes[] =   {60, 62, 64, 65, 67, 69, 71, 72, 74, 76};  // Piano (C4-E5)
const int guitarNotes[] =  {40, 42, 44, 45, 47, 49, 51, 52, 54, 56};  // Guitar (E2-G#3)
const int violinNotes[] =  {55, 57, 59, 60, 62, 64, 65, 67, 69, 71};  // Violin (G3-B4)
const int trumpetNotes[] = {108, 110, 112, 113, 115, 117, 119, 121, 122, 124};   // Trumpet (A#3-D5)
const int fluteNotes[] =   {72, 74, 76, 77, 79, 81, 83, 84, 86, 88};  // Flute (C5-E6)

const int* instruments[] = {pianoNotes, guitarNotes, violinNotes, trumpetNotes, fluteNotes};
const int totalInstruments = sizeof(instruments) / sizeof(instruments[0]);

bool lastState[numKeys] = {false}; 

void setup() {
    Serial.begin(115200); 

    for (int i = 0; i < numKeys; i++) {
        pinMode(irPins[i], INPUT);
    }
    pinMode(buttonPin, INPUT_PULLUP); 
}

void loop() {
    checkButton();  

    for (int i = 0; i < numKeys; i++) {
        bool isPressed = digitalRead(irPins[i]) == LOW; 

        if (isPressed && !lastState[i]) {
            sendMIDI(0x90, instruments[instrumentIndex][i], 127); 
            lastState[i] = true;
        } 
        else if (!isPressed && lastState[i]) {
            sendMIDI(0x80, instruments[instrumentIndex][i], 0);
            lastState[i] = false;
        }
    }
}

void checkButton() {
    bool currentButtonState = digitalRead(buttonPin);

    if (currentButtonState == LOW && lastButtonState == HIGH && (millis() - lastDebounceTime) > debounceDelay) {
        instrumentIndex = (instrumentIndex + 1) % totalInstruments; 
        Serial.print("Switched to Instrument: ");
        Serial.println(instrumentIndex);
        lastDebounceTime = millis();
    }

    lastButtonState = currentButtonState;
}

void sendMIDI(byte command, byte data1, byte data2) {
    Serial.write(command);
    Serial.write(data1);
    Serial.write(data2);
}
