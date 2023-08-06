#include "WProgram.h"
#include <wprogram.h>
#include <avr/pgmspace.h>
#include <microfat2.h>
#include <mmc.h>
#include "SDWriter.h"

boolean SDWriter::init(char *fname){
  while(mmc::initialize() != RES_OK){
    Serial.println("init failed... retry");
    delay(500);
  }

  if (!microfat2::initialize(sector_buffer, &mmc::readSectors)){
    Serial.println("uFat init failed.");
	return false;
  }

  if(!microfat2::locateFileStart(fname, start_sector, file_size)){
    Serial.println("Cant find file");
	return false;
  }
  sectors=file_size/512;

  sector_pos=buffer_pos=0;

  Serial.print("data file is: ");
  Serial.print(file_size);
  Serial.print("bytes = ");
  Serial.print(sectors);
  Serial.println("sectors");
  
  return true;
}

void SDWriter::write(uint8_t theByte)
{
  sector_buffer[buffer_pos]= theByte;
  ++buffer_pos;
  if(buffer_pos==512)
  {
    flush();
  }
}

void SDWriter::write(unsigned long val,int bytes)
{
  for(int b=bytes-1;b>=0;--b)
  {
    write((val>>(8*b)) & 0xff);
  }
}

void SDWriter::flush(){
    if(RES_OK != mmc::writeSectors(sector_buffer, start_sector+sector_pos, 1)){
      Serial.println("Error Writing");
    }
    sector_pos++;
    buffer_pos=0;
    Serial.print("Written sector: ");
    Serial.print(sector_pos);
    Serial.print(" of ");
	Serial.println(sectors);
}

