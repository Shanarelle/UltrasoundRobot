#include "usarray.h"

#include "xparameters.h"

#include "pulsegen.h"
#include "us_receiver.h"


#define USVoltageToTriggerLevel(x) (unsigned short) ((((unsigned int) x) * ((1 << USADCPrecision) - 1)) / USADCReference) // Voltage expressed in hundredths
#define USSampleIndexToTime(x) (unsigned short) ((((1000000 * 10) / US_SAMPLE_RATE) * (((unsigned int) x) + 1)) / 10) // Time expressed in uS
#define USTimeToSampleIndex(x) (unsigned short) ((((unsigned int) x) * 10) / ((1000000 * 10) / US_SAMPLE_RATE) - 1) // Time in uS
#define N 5		//order of sequence
#define M 31 	//length of sequence (2^order - 1)

const unsigned char usSensorMap[] = US_SENSOR_MAP; // Sensor position to address map

unsigned char usSensorIndex = 0; // Next sensor to scan
unsigned short usSampleIndex = 0; // Sample index, incremented once per ADC conversion, representative of ToF
unsigned short usWaveformData[US_SENSOR_COUNT][US_RX_COUNT]; // Current raw waveform data - stored as ADC results
signed short usRangeReadings[US_SENSOR_COUNT]; // Latest range readings - stored as sample indexes
signed short signalDifference; // The amount consecutive range readings are allowed to differ by

unsigned short usTriggerChangeIndex = USTimeToSampleIndex(TRIGGER_NEAR_FAR_CHANGE); // Trigger changeover time
unsigned short usTriggerNearUpper = USVoltageToTriggerLevel(TRIGGER_BASE + TRIGGER_OFFSET_NEAR); // Upper trigger level
unsigned short usTriggerNearLower = USVoltageToTriggerLevel(TRIGGER_BASE - TRIGGER_OFFSET_NEAR); // Lower trigger level
unsigned short usTriggerFarUpper = USVoltageToTriggerLevel(TRIGGER_BASE + TRIGGER_OFFSET_FAR); // Upper trigger level
unsigned short usTriggerFarLower = USVoltageToTriggerLevel(TRIGGER_BASE - TRIGGER_OFFSET_FAR); // Lower trigger level

signed short usTemperature = 210; // Temperature in degrees C, expressed in tenths

//where the id sequences for pulse transmission will be stored
unsigned char usIdSequences[US_SENSOR_COUNT][M];


int init_usarray() {
	// Reset all ranges
	int i;
	for(i = 0; i < US_SENSOR_COUNT; i++) usRangeReadings[i] = -1;

	// Setup ADC by writing to setup register (0x64)
	// Set to use internal clock for sampling and conversions, use external single ended reference
	sendUSInit();

	u8 status;
	u8 type;
	u32 data;
	readUSData(&status, &type, &data);

	if (status == US_STATUS_OK && type == US_RESP_NONE)
		return XST_SUCCESS;
	else
		return XST_FAILURE;
}

void usarray_set_sensor(unsigned char newSensor) {
	// Select new sensor
	usSensorIndex = newSensor;
}

unsigned char usarray_get_sensor() {
	// Return sensor
	return usSensorIndex;
}

void usarray_set_triggers(unsigned short changover, unsigned short nearLower, unsigned short nearUpper, unsigned short farLower, unsigned short farUpper) {
	// Update trigger levels
	usTriggerChangeIndex = USTimeToSampleIndex(changover);
	usTriggerNearLower = USVoltageToTriggerLevel(nearLower);
	usTriggerNearUpper = USVoltageToTriggerLevel(nearUpper);
	usTriggerFarUpper = USVoltageToTriggerLevel(farLower);
	usTriggerFarLower = USVoltageToTriggerLevel(farUpper);
}

short usarray_get_temperature() {
	// Return temperature
	return usTemperature;
}

void usarray_measure_temp() {
	// Compute conversion byte, request temperature conversion and ignore single channel conversion (0xf9)
	sendUSTempRequest();

	// Read temperature back (blocking)
	u8 status;
	u8 type;
	u32 adcTempResult;
	readUSData(&status, &type, &adcTempResult);

	// This might not be right? Doing (temp*1.25) seems too high, but might just be warm chip.
	usTemperature = (((int) adcTempResult) * 125 * 10) / 1000;
}

/* generates an M-sequence of 1s and 0s for each of the sensors
*/
void usarray_generate_sequence(u8 numSensors)	{
	u8 taps[N] = {0,0,1,0,1}; //set those indices where primitive polynomial has that power to 1
	u8 m[N] = {[0 ... N-1] = 1}; //initialise array to all ones
	
	u8 i, j;
	u8 buf = 0;
	for(i=0; i<M; i++) {
		for(j=0; j<M; j++) {
			buf += taps[j] * m[j];	//replace this with a bitwise operator later
		}
		buf = buf % 2;
		//shift left
		for(j=N-1; j>0; j--) {
			m[j] = m[j-1];
		}
		
		m[0] = buf;
		usIdSequences[0][i] = m[N-1];
	}
}

void usarray_send_pulse(u8 sensorNum) {
	u8 i;
	for(i=0; i<M; i++) {
		if(usIdSequences[sensorNum][i] != 0) { //if the sequence is a 1, send pulse
			pulseGen_GeneratePulse(XPAR_AXI_PULSEGEN_US_BASEADDR, 1, usSensorMap[sensorNum], US_TX_COUNT);
		} else {	//otherwise, send silence
			pulseGen_GeneratePulse(XPAR_AXI_PULSEGEN_US_BASEADDR, 0, usSensorMap[sensorNum], US_TX_COUNT);
		}
	}
}

void usarray_scan(u8 sensors[], u8 numSensors) {
	if (numSensors == 0 || numSensors > US_SENSOR_COUNT)
		return;

	// Reset sample index
	usSampleIndex = 0;

	int sensor;
	int sample;
	u8 sensorNum;

	// Iterate through sensors
	for (sensor = 0; sensor < numSensors; sensor++) {
		sensorNum = sensors[sensor];

		// Generate ultrasound pulse
		usarray_send_pulse(sensorNum);

		// Start sampling at 80kHz
		sendUSSampleRequest(usSensorMap[sensorNum], US_RX_COUNT, 1250);

		// Read all sample data
		for (sample = 0; sample < US_RX_COUNT; sample++) {
			u8 status;
			u8 type;
			u32 adcResult;
			readUSData(&status, &type, &adcResult);

			usWaveformData[sensorNum][sample] = adcResult;
		}
	}
}

void usarray_update_ranges(u8 sensors[], u8 numSensors) {
	if (numSensors == 0 || numSensors > US_SENSOR_COUNT)
		return;

	// Compute speed of sound based on temperature
	unsigned int speedOfSound = (3313000 + 606 * usTemperature) / 10000; //mm/uS expressed in thousandths

	// Update range readings for each sensor
	u8 sensorNum;
	int iSensor;
	int iSample;
	unsigned short triggerUpper;
	unsigned short triggerLower;
	for(iSensor = 0; iSensor < numSensors; iSensor++) {
		sensorNum = sensors[iSensor];

		// Assume nothing will be found
		//usRangeReadings[sensorNum] = -1;

		// Example each sample
		for(iSample = 0; iSample < US_RX_COUNT; iSample++) {
			// Work out trigger levels for sample
			if(iSample <= usTriggerChangeIndex) {
				triggerUpper = usTriggerNearUpper;
				triggerLower = usTriggerNearLower;
			} else {
				triggerUpper = usTriggerFarUpper;
				triggerLower = usTriggerFarLower;
			}

			signed short newRange;
			// Check sample against trigger levels
			if(usWaveformData[sensorNum][iSample] <= triggerLower || usWaveformData[sensorNum][iSample] >= triggerUpper) {
				// Update range reading - converting distance from thousandths of mm to mm and halving to retrieve one way distance
				newRange = ((((unsigned int) USSampleIndexToTime(iSample)) * speedOfSound) / (1000 * 2)) - 20;
				// Only save range reading if similar enough to previous one
				if(newRange - usRangeReadings[sensorNum] <= signalDifference || usRangeReadings[sensorNum] - newRange <= signalDifference) {
					usRangeReadings[sensorNum] = newRange;
				}

				// Done
				break;
			}
		}
	}
}

u16 usarray_distance(u8 sensor) {
	return usRangeReadings[sensor];
}

u8 usarray_detect_obstacle(u8 sensor, u16 distance) {
	return (usRangeReadings[sensor] > 0 && usRangeReadings[sensor] < distance);
}

