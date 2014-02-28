#include <stdio.h>

#define US_SAMPLE_RATE 80000 // Hz
#define USSampleIndexToTime(x) (unsigned short) ((((1000000 * 10) / US_SAMPLE_RATE) * (((unsigned int) x) + 1)) / 10) // Time expressed in uS

#define N 5
#define M 31
#define sensor_separation 12 //expressed in mm

signed short usTemperature = 210; // Temperature in degrees C, expressed in tenths


/* 
*  generates an M-sequence of 1s and 0s for each of the sensors
*/
void usarray_set_m_sequence(int numSensors)	{
	int taps[N] = {0,0,1,0,1}; //set those indices where primitive polynomial has that power to 1
	int m[N] = {[0 ... N-1] = 1}; //initialise array to all ones
	
	int regout[M] = {[0 ... M-1] = 0};
	int i, j;
	int buf = 0;
	for(i=0; i<M; i++) {
		for(j=0; j<M; j++) {
			buf += taps[j] * m[j];	//replace this with a bitwise operator later
		}
		buf = buf % 2;
		//shift left  - Array.Copy(m, 1, m, 0, M-1);
		for(j=N-1; j>0; j--) {
			m[j] = m[j-1];
		}
		
		m[0] = buf;
		regout[i] = m[N-1];
	}
	
	//print regout
	for(i=0; i<M; i++) {
		printf("%i, ", regout[i]);
	}
}


/********Post sensor processing of ranges************************************************************************************************/
/* Assumes that robot gives set of tuples of the form (transmittingSensor, receivingSensor, timeOfFlight) */
void process_us_readings() {
	int array_length = 3;
	signed short readings[array_length][3];
	signed short ranges[3];
	//populate readings
	readings[0][0] = 1;
	readings[0][1] = 1;
	readings[0][2] = 150;
	readings[1][0] = 2;
	readings[1][1] = 2;
	readings[1][2] = 172;
	readings[2][0] = 1;
	readings[2][1] = 2;
	readings[2][2] = 298;
	// Compute speed of sound based on temperature
	unsigned int speedOfSound = (3313000 + 606 * usTemperature) / 10000; //mm/uS expressed in thousandths
	//figure out ranges
	int i;
	for (i=0; i<array_length; i++) {
		signed short distance = ((readings[i][2] * speedOfSound) / (1000 * 2)) - 20;
		if (readings[i][0] == readings[i][1]) { //simple case, same transmitter and receiver
			ranges[i] = distance;
			printf("%i: distance: %d, angle: 0\n", i, distance);
		} else { //in the first instance, assume hit object and came straight to receiver
			//find distance between transmitter and receiver
			signed short diff;
			if (readings[i][0] > readings[i][1]) {
				diff = readings[i][0] - readings[i][1];
			} else {
				diff = readings[i][1] - readings[i][0];
			}
			diff = sensor_separation * diff;
			diff = diff / 2;
			printf("%i: distance: %d, angle: %d\n", i, distance, diff);

			//calculate distance to obstacle
			ranges[i] = sqrt((distance + diff)*(distance - diff));	//rounds to nearest mm
		}
		printf("%i: final range: %d\n", i, ranges[i]);
	}
}




/******* Main Function - to check outputs ***********************************************************************************************/
int main(void){
	printf("Hello World!\n");
	//usarray_set_m_sequence(1);
	process_us_readings();
	return 0;
}