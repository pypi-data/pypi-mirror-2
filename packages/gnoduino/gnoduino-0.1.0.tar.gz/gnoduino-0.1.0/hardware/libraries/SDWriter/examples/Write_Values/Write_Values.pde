#include <wprogram.h>
#include <avr/pgmspace.h>
#include <microfat2.h>
#include <mmc.h>
#include "SDWriter.h"

SDWriter sd; // create an SDWriter

//we write with sd.write(value,bytes);
//value: value to write
//bytes: number for bytes to use
//we don't have to worry about sectors, when the current sector buffer is full it is written to disk and writing continues in
//the next sectors buffer, splitting the value across sectors if necessary.
//don't forget to sd.flush(); at the very end of writing to write the final buffer to disk or your last sector will be lost.

void setup(void){
  Serial.begin(9600);
  sd.init(PSTR("DATA    BIN"));  //open file data.bin, 5KB should be plenty for this

  for(int s=0;s<500;s++){ //take 500 readings, will span several sectors and take about 20 seconds
    sd.write(millis(),3);  // write millis as 3 bytes
    sd.write(analogRead(0),2); // write analog 0 reading as 2 bytes
    sd.write(analogRead(1),2); // write analog 1 reading as 2 bytes
    delay(50);
  }
  
  sd.write(0,7); // mark end of data, by writing 7 bytes (millis, analog 0 and analog 1) all as value 0
  //this will help us when we read in the data so we know not to continue into the junk data at the end of the file
  
  sd.flush(); // write the final sector to disk
  
  Serial.println("Done");
}

void loop(){
  ;
}
