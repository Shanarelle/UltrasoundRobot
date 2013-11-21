#include <stdio.h>

#define N 5
#define M 31


/* generates an M-sequence of 1s and 0s for each of the sensors
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





//entry point for testing, just prints things
int main(void){
	printf("Hello World!\n");
	usarray_set_m_sequence(1);
	return 0;
}