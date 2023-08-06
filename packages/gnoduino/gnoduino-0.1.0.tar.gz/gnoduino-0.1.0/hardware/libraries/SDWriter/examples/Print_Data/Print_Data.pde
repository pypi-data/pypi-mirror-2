#include <wprogram.h>
#include <avr/pgmspace.h>
#include <microfat2.h>
#include <mmc.h>
#include "SDWriter.h"

SDWriter sd; // create an SDWriter
//We can wrtie with sd.print() and sd.println();

void setup(void){
  Serial.begin(9600);
  sd.init(PSTR("DATA    BIN"));  //open file data.bin, 15KB should be plenty for this

  for(int s=0;s<500;s++){ //take 500 readings, will span several sectors and take about 20 seconds
    sd.print(millis());  // write millis as ASCII string
    sd.print(",");
    sd.print(analogRead(0)); // write analog 0 reading as ASCII string
    sd.print(",");
    sd.println(analogRead(1)); // write analog 1 reading as ASCII string
    delay(50);
  }
  
  sd.println("END"); // mark end of data, by writing "END"
  //this will help us when we read in the data so we know not to continue into the junk data at the end of the file
  
  sd.flush(); // write the final sector to disk
  
  Serial.println("Done");
}

void loop(){
  ;
}
