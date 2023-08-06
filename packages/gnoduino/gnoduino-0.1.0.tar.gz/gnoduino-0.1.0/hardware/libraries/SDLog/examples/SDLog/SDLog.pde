/* Code starts here - call it GPSLogger_v2.1 :) */

// this is a generic logger that does checksum testing so the data written should be always good
// Assumes a sirf III chipset logger attached to pin 0 and 1

#include "AF_SDLog.h"
#include "util.h"
#include <avr/pgmspace.h>


AF_SDLog card;
File f;

#define BUFFSIZE 75
char buffer[BUFFSIZE];
uint8_t bufferidx = 0;


void setup()
{
  Serial.begin(9600);
  Serial.println("Startup");


  if (card.init_card()) 
  {
    Serial.println("Card init. failed!");
  }
  if (!card.open_partition()) 
  {
    Serial.println("No partition!");
  }
  if (!card.open_filesys()) 
  {
    Serial.println("Can't open filesys");
  }
  if (!card.open_dir("/")) 
  {
    Serial.println("Can't open /");
  }

  strcpy(buffer, "LOG00000.TXT");
  
  for (;;)
  {
    Serial.print("trying to open ");Serial.print(buffer);
    f = card.open_file(buffer);
    if (!f)
      break;
    Serial.println("...exists");
    card.close_file(f);
    
    
    for (byte pos=7;pos>=3;pos--)
    {
      if(buffer[pos]=='9')
      {
        buffer[pos]='0';
        continue;
      }
      buffer[pos]++;
      break; 
    }
    
  }

  Serial.print("\ncreating ");
  Serial.println(buffer);
  if(!card.create_file(buffer)) 
  {
    Serial.print("couldnt create ");
    Serial.println(buffer);
  }
  Serial.print("opening ");
  Serial.println(buffer);
  f = card.open_file(buffer);
  if (!f) 
  {
    Serial.print("error opening ");
    Serial.println(buffer);
    card.close_file(f);
  }

 
  Serial.print("writing to ");
  Serial.println(buffer);
  Serial.println("ready!");


}

void loop()
{
  // rad. lets log it!
  strcpy(buffer,"Hello");
  bufferidx = strlen(buffer);
  Serial.println(buffer);
  Serial.print("Length: "); Serial.println(bufferidx,DEC);
  
  if(card.write_file(f, (uint8_t *) buffer, bufferidx) != bufferidx) 
  {
    Serial.println("can't write!");
  }
      
  delay(3000);
}

