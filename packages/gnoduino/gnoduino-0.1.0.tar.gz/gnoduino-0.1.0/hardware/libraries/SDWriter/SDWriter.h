#ifndef SD_Writer
#define SD_Writer

#include "WConstants.h"

class SDWriter: public Print{
	public:
	  boolean init(char *fname);
	  void write(unsigned long,int);
	  void flush();
	  //void flush(byte b);
	  virtual void write(uint8_t theByte);
	private:
	  byte sector_buffer[512];
	  int buffer_pos;
	  unsigned long sector_pos;
	  unsigned long start_sector;
	  unsigned long file_size;
	  unsigned long sectors;
};

#endif
