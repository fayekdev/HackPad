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
    FIELD_HARDWARE,
    FIELD_TASKS
};

GxEPD2_BW<GxEPD2_290_T94, GxEPD2_290_T94::HEIGHT> display(
    GxEPD2_290_T94(EPD_CS, EPD_DC, EPD_RST, EPD_BUSY)
);

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

String lastTimeText;
String lastAppText;
String lastMusicText;
String lastDateText;
String lastTempText;
String lastWeatherText;
String lastSoundText;
String lastMicText;
String lastTask1Text;
String lastTask2Text;
String lastTask3Text;
String lastTask4Text;

bool buttons[16] = {false};

int last_enc_CLK = LOW;
long encoder_pos = 0;

unsigned long lastUpdateTime = 0;
unsigned long last_pc_packet_time = 0;

const unsigned long updateInterval = 1000;
const unsigned long pcTimeout = 3500;

bool is_pc_connected = false;

int partialRefreshCounter = 0;
const int maxPartialRefreshes = 60;

void drawScreen_Full();
void drawStaticLayout();
void drawAllFields();
void updateDynamicField(DynamicField field);

String extractField(const String &src, const char *tag)
{
    int start = src.indexOf(tag);

    if (start < 0)
        return "";

    start += strlen(tag);

    int end = src.indexOf('|', start);

    if (end < 0)
        end = src.length();

    return src.substring(start, end);
}

void setup()
{
    Serial.begin(115200);
    Serial.setTimeout(50);

    pinMode(SR_PL_LATCH, OUTPUT);
    pinMode(SR_CLK, OUTPUT);
    pinMode(SR_DATA_IN, INPUT);

    digitalWrite(SR_PL_LATCH, HIGH);
    digitalWrite(SR_CLK, LOW);

    pinMode(ENC_CLK, INPUT_PULLUP);
    pinMode(ENC_DT, INPUT_PULLUP);

    last_enc_CLK = digitalRead(ENC_CLK);

    SPI.begin(EPD_SCK, -1, EPD_MOSI, EPD_CS);

    display.init(115200, true, 2, false);
    display.setRotation(3);

    drawScreen_Full();
}

void loop()
{
    unsigned long currentMillis = millis();

    bool button_changed = false;
    bool encoder_changed = false;

    digitalWrite(SR_PL_LATCH, LOW);
    delayMicroseconds(5);
    digitalWrite(SR_PL_LATCH, HIGH);

    for (int i = 0; i < 16; i++)
    {
        bool raw_val = !digitalRead(SR_DATA_IN);

        digitalWrite(SR_CLK, HIGH);
        delayMicroseconds(2);
        digitalWrite(SR_CLK, LOW);

        if (buttons[i] != raw_val)
        {
            buttons[i] = raw_val;
            button_changed = true;
        }
    }

    int current_enc_CLK = digitalRead(ENC_CLK);

    if (current_enc_CLK != last_enc_CLK &&
        current_enc_CLK == LOW)
    {
        if (digitalRead(ENC_DT) != current_enc_CLK)
            encoder_pos++;
        else
            encoder_pos--;

        encoder_changed = true;
    }

    last_enc_CLK = current_enc_CLK;

    int joyX = analogRead(JOY_X);
    int joyY = analogRead(JOY_Y);

    if (Serial.available())
    {
        String input = Serial.readStringUntil('\n');
        input.trim();

        if (input.startsWith("HELLO"))
        {
            last_pc_packet_time = currentMillis;

            if (!is_pc_connected)
            {
                is_pc_connected = true;
                drawScreen_Full();
            }
        }
        else if (input.startsWith("DATA:"))
        {
            last_pc_packet_time = currentMillis;
            is_pc_connected = true;

            String value;

            value = extractField(input, "|APP:");
            if (value.length())
                string_3_text = value;

            value = extractField(input, "|WEA:");
            if (value.length())
                state_weather = value;

            value = extractField(input, "|TMP:");
            if (value.length())
                string_17_text = value;

            value = extractField(input, "|SND:");
            if (value.length())
                state_sound = value;

            value = extractField(input, "|MIC:");
            if (value.length())
                state_mic = value;

            value = extractField(input, "|SNG:");
            if (value.length())
                string_4_text = value;

            value = extractField(input, "|DAT:");
            if (value.length())
                string_9_text = value;

            value = extractField(input, "|TIM:");
            if (value.length())
                string_1_text = value;

            value = extractField(input, "|T1:");
            if (value.length())
                string_11_text = value;

            value = extractField(input, "|T2:");
            if (value.length())
                string_11_copy_1_text = value;

            value = extractField(input, "|T3:");
            if (value.length())
                state_task3 = value;

            value = extractField(input, "|T4:");
            if (value.length())
                state_task4 = value;
        }
    }

    if (currentMillis - lastUpdateTime >= updateInterval)
    {
        lastUpdateTime = currentMillis;

        bool timeChanged =
            string_1_text != lastTimeText;

        bool appChanged =
            string_3_text != lastAppText;

        bool musicChanged =
            string_4_text != lastMusicText;

        bool dateChanged =
            string_9_text != lastDateText;

        bool tempChanged =
            string_17_text != lastTempText;

        bool weatherChanged =
            state_weather != lastWeatherText;

        bool soundChanged =
            state_sound != lastSoundText;

        bool micChanged =
            state_mic != lastMicText;

        bool tasksChanged =
            string_11_text != lastTask1Text ||
            string_11_copy_1_text != lastTask2Text ||
            state_task3 != lastTask3Text ||
            state_task4 != lastTask4Text;

        bool anythingChanged =
            timeChanged ||
            appChanged ||
            musicChanged ||
            dateChanged ||
            tempChanged ||
            weatherChanged ||
            soundChanged ||
            micChanged ||
            tasksChanged;

        if (anythingChanged)
        {
            if (partialRefreshCounter >= maxPartialRefreshes)
            {
                drawScreen_Full();
                partialRefreshCounter = 0;
            }
            else
            {
                if (timeChanged)
                    updateDynamicField(FIELD_TIME);

                if (appChanged)
                    updateDynamicField(FIELD_APP);

                if (musicChanged)
                    updateDynamicField(FIELD_MUSIC);

                if (dateChanged)
                    updateDynamicField(FIELD_WEATHER);

                if (tempChanged)
                    updateDynamicField(FIELD_WEATHER);

                if (weatherChanged)
                    updateDynamicField(FIELD_WEATHER);

                if (soundChanged || micChanged)
                    updateDynamicField(FIELD_HARDWARE);

                if (tasksChanged)
                    updateDynamicField(FIELD_TASKS);

                partialRefreshCounter++;
            }

            lastTimeText = string_1_text;
            lastAppText = string_3_text;
            lastMusicText = string_4_text;
            lastDateText = string_9_text;
            lastTempText = string_17_text;
            lastWeatherText = state_weather;
            lastSoundText = state_sound;
            lastMicText = state_mic;
            lastTask1Text = string_11_text;
            lastTask2Text = string_11_copy_1_text;
            lastTask3Text = state_task3;
            lastTask4Text = state_task4;
        }
    }

    if (is_pc_connected &&
        currentMillis - last_pc_packet_time > pcTimeout)
    {
        is_pc_connected = false;

        string_1_text = "--:--";
        string_3_text = "OFFLINE";
        string_4_text = "None";
        string_9_text = "--- --";
        string_17_text = "--C";

        string_11_text = "-";
        string_11_copy_1_text = "-";
        state_task3 = "-";
        state_task4 = "-";

        state_weather = "Sunny";
        state_sound = "low";
        state_mic = "off";

        drawScreen_Full();
        partialRefreshCounter = 0;
    }

    if (is_pc_connected)
    {
        static unsigned long last_tx = 0;

        if (currentMillis - last_tx > 40 ||
            button_changed ||
            encoder_changed)
        {
            last_tx = currentMillis;

            Serial.print("{\"joyX\":");
            Serial.print(joyX);

            Serial.print(",\"joyY\":");
            Serial.print(joyY);

            Serial.print(",\"encoder\":");
            Serial.print(encoder_pos);

            Serial.print(",\"buttons\":[");

            for (int i = 0; i < 16; i++)
            {
                Serial.print(buttons[i] ? "1" : "0");

                if (i < 15)
                    Serial.print(",");
            }

            Serial.println("]}");
        }
    }

    delay(5);
}

void drawScreen_Full()
{
    display.setFullWindow();
    display.firstPage();

    do
    {
        display.fillScreen(GxEPD_WHITE);

        drawStaticLayout();
        drawAllFields();

    } while (display.nextPage());
}

void drawStaticLayout()
{
    display.setTextSize(1);
    display.setTextColor(GxEPD_BLACK);
    display.setTextWrap(false);

    display.setCursor(107, 12);
    display.print("KEEP WORKIN'!");

    display.drawRect(
        123,
        51,
        41,
        38,
        GxEPD_BLACK
    );

    display.drawCircle(197, 43, 4, GxEPD_BLACK);
    display.drawCircle(197, 60, 4, GxEPD_BLACK);
    display.drawCircle(197, 77, 4, GxEPD_BLACK);
    display.drawCircle(197, 95, 4, GxEPD_BLACK);
}

void drawAllFields()
{
    display.setTextSize(1);
    display.setTextColor(GxEPD_BLACK);
    display.setTextWrap(false);

    display.setCursor(10, 11);
    display.print(string_9_text);

    display.setCursor(254, 11);
    display.print(string_1_text);

    display.setCursor(134, 37);
    display.print(string_3_text);

    display.drawBitmap(
        135,
        62,
        image_music_bits,
        14,
        16,
        GxEPD_BLACK
    );

    display.setCursor(132, 102);
    display.print(string_4_text);

    display.setCursor(207, 39);
    display.print(string_11_text);

    display.setCursor(207, 57);
    display.print(string_11_copy_1_text);

    display.setCursor(207, 74);
    display.print(state_task3);

    display.setCursor(207, 92);
    display.print(state_task4);

    drawHardwareIcons();
    drawWeather();
}

void drawHardwareIcons()
{
    if (state_sound.equalsIgnoreCase("loud"))
    {
        display.drawBitmap(
            240,
            109,
            image_volume_loud_bits,
            20,
            16,
            GxEPD_BLACK
        );
    }
    else
    {
        display.drawBitmap(
            240,
            109,
            image_volume_low_bits,
            18,
            16,
            GxEPD_BLACK
        );
    }

    if (state_mic.equalsIgnoreCase("on"))
    {
        display.drawBitmap(
            267,
            109,
            image_microphone_1_bits,
            15,
            16,
            GxEPD_BLACK
        );
    }
    else
    {
        display.drawBitmap(
            268,
            109,
            image_microphone_muted_bits,
            15,
            16,
            GxEPD_BLACK
        );
    }
}

void drawWeather()
{
    if (state_weather.equalsIgnoreCase("Sunny"))
    {
        display.drawBitmap(
            34,
            43,
            image_weather_sun_bits,
            30,
            32,
            GxEPD_BLACK
        );
    }
    else
    {
        display.drawBitmap(
            34,
            43,
            image_weather_sun_bits,
            30,
            32,
            GxEPD_BLACK
        );
    }

    display.setCursor(37, 77);
    display.print(string_17_text);
}

void updateDynamicField(DynamicField field)
{
    uint16_t x = 0;
    uint16_t y = 0;
    uint16_t w = 0;
    uint16_t h = 0;

    switch (field)
    {
        case FIELD_TIME:
            x = 248;
            y = 3;
            w = 48;
            h = 14;
            break;

        case FIELD_APP:
            x = 130;
            y = 30;
            w = 166;
            h = 15;
            break;

        case FIELD_MUSIC:
            x = 128;
            y = 98;
            w = 168;
            h = 16;
            break;

        case FIELD_WEATHER:
            x = 30;
            y = 39;
            w = 38;
            h = 42;
            break;

        case FIELD_HARDWARE:
            x = 237;
            y = 106;
            w = 59;
            h = 21;
            break;

        case FIELD_TASKS:
            x = 204;
            y = 34;
            w = 91;
            h = 65;
            break;
    }

    display.setPartialWindow(x, y, w, h);

    display.firstPage();

    do
    {
        display.fillRect(
            x,
            y,
            w,
            h,
            GxEPD_WHITE
        );

        display.setTextSize(1);
        display.setTextColor(GxEPD_BLACK);
        display.setTextWrap(false);

        switch (field)
        {
            case FIELD_TIME:
                display.setCursor(254, 11);
                display.print(string_1_text);
                break;

            case FIELD_APP:
                display.setCursor(134, 37);
                display.print(string_3_text);
                break;

            case FIELD_MUSIC:
                display.setCursor(132, 102);
                display.print(string_4_text);
                break;

            case FIELD_WEATHER:
                drawWeather();
                break;

            case FIELD_HARDWARE:
                drawHardwareIcons();
                break;

            case FIELD_TASKS:
                display.setCursor(207, 39);
                display.print(string_11_text);

                display.setCursor(207, 57);
                display.print(string_11_copy_1_text);

                display.setCursor(207, 74);
                display.print(state_task3);

                display.setCursor(207, 92);
                display.print(state_task4);
                break;
        }

    } while (display.nextPage());
}