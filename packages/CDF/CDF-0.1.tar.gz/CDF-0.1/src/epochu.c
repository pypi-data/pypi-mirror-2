/******************************************************************************
*
*  NSSDC/CDF                       EPOCH utility routines for C applications.
*
*  Version 2.4b, 7-Dec-95, Hughes STX.
*
*  Modification history:
*
*   V1.0  24-Jan-91, D Grogan   Original version (for CDF V2.0).
*   V1.1  25-Mar-91, J Love     Added support for Silicon Graphics (MIPSEB
*                               encoding, IRIX - UNIX).
*   V1.2  26-Mar-91, J Love     Added "types.h" include for SunOS 4.0.3
*                               systems (UNIX).  Added "ctypes.h" include and
*                               removed definitions of toupper & tolower.  Use
*                               toupper the safe way.  Added definition for
*                               toupper if SunOS 4.0.3.
*   V1.3  19-Jun-91, J Love     Changed epochParse to return FALSE if illegal
*                               date/time string (and added more error
*                               checking) and to set 'tSince0'.
*   V1.4  29-Jul-91, J Love     TRUE/FALSE.  Don't display error messages (the
*                               caller will do that).
*   V1.5  23-Sep-91, J Love     Modified for IBM-PC port.
*   V2.0   1-Apr-92, J Love     Added to CDF library.  Added additional ways
*                    A Warnock  to display an EPOCH date/time.
*   V2.1  30-Jun-92, J Love     CDF V2.3 (shareable/NeXT/zVar).
*   V2.2  24-Jan-94, J Love     CDF V2.4.  Handle negative EPOCHs.
*   V2.3  13-Dec-94, J Love     CDF V2.5.
*   V2.3a 18-Jan-95, J Love	Made `computeEPOCH' more flexible.
*   V2.3b 24-Jan-95, J Love	Changed `parseEPOCH' for Salford C.  Consider
*				milliseconds in `encodeEPOCH1'.
*   V2.3c 24-Feb-95, J Love	Solaris 2.3 IDL i/f.
*   V2.4   9-May-95, J Love	Added parseEPOCH1, parseEPOCH2, & parseEPOCH3.
*   V2.4a 13-Jun-95, J Love	EPOCH custom format.
*   V2.4b  7-Dec-95, J Love	OSF/1 bug in `sprintf'.
*
******************************************************************************/

#include "cdflib.h"

/******************************************************************************
* Local macro definitions.
******************************************************************************/

#define MAX_PART_LEN		10
#define MAX_MOD_LEN		10
#define MAX_ePART_LEN		25

/******************************************************************************
* Local function prototypes.
******************************************************************************/

static long JulianDay PROTOARGs((long, long, long));
static char *MonthToken PROTOARGs((long));
static char *FullDayToken PROTOARGs((char *));
static Logical AppendFractionPart PROTOARGs((
  char *encoded, double fraction, int defaultWidth, char *modifier
));
static Logical AppendIntegerPart PROTOARGs((
  char *encoded, long integer, int defaultWidth, Logical defaultLeading0,
  char *modifier
));
static Logical AppendPart PROTOARGs((
  char *encoded, char *ePart, int width, Logical leading0
));

/******************************************************************************
* parseEPOCH.
*   This function parses an input date/time string and returns an EPOCH
* value.  The format must be exactly as shown below.  Month abbreviations may
* be in any case and are always the first three letters of the month.
*
* Format:	dd-mmm-yyyy hh:mm:ss.mmm
* Examples:	 1-Apr-1990 03:05:02.000
*		10-Oct-1993 23:45:49.999
*
* The expected format is the same as that produced by encodeEPOCH.
******************************************************************************/

STATICforIDL double parseEPOCH (inString)
char *inString;
{
  char moString[4];
  long year, month, day, hour, minute, second, msec;
  int monthX;
  if (sscanf(inString,"%ld-%c%c%c-%ld %ld:%ld:%ld.%ld",
	     &day, &(moString[0]), &(moString[1]), &(moString[2]), &year,
	     &hour, &minute, &second, &msec) != 9) return ILLEGAL_EPOCH_VALUE;
  moString[0] = ToUpperChr(moString[0]);   /* J */
  moString[1] = ToLowerChr(moString[1]);   /* a */
  moString[2] = ToLowerChr(moString[2]);   /* n */
  moString[3] = NUL;
  for (monthX = 1, month = 0; monthX <= 12; monthX++) {
    if (!strcmp(moString,MonthToken(monthX))) {
      month = monthX;
      break;
    }
  }
  if (month == 0) return ILLEGAL_EPOCH_VALUE;
  return computeEPOCH (year, month, day, hour, minute, second, msec);
}

/******************************************************************************
* parseEPOCH1.
*   This function parses an input date/time string and returns an EPOCH
* value.  The format must be exactly as shown below.  Note that if there are
* less than 7 digits after the decimal point, zeros (0's) are assumed for the
* missing digits.
*
* Format:	yyyymmdd.ttttttt
* Examples:	19950508.0000000
*		19671231.58      (== 19671213.5800000)
*
* The expected format is the same as that produced by encodeEPOCH1.
******************************************************************************/

STATICforIDL double parseEPOCH1 (inString)
char *inString;
{
  char temp[EPOCH1_STRING_LEN+1]; double fraction; int i;
  long year, month, day, hour, minute, second, msec, fractionL;
  strcpyX (temp, inString, EPOCH1_STRING_LEN);
  for (i = strlen(temp); i < EPOCH1_STRING_LEN; i++) temp[i] = '0';
  temp[i] = NUL;
  if (sscanf(temp,"%4ld%2ld%2ld.%ld",
	     &year, &month, &day, &fractionL) != 4) return ILLEGAL_EPOCH_VALUE;
  fraction = ((double) fractionL) / 10000000.0;
  hour = (long) (fraction * 24.0);
  fraction -= (double) (hour / 24.0);
  minute = (long) (fraction * 1440.0);
  fraction -= (double) (minute / 1440.0);
  second = (long) (fraction * 86400.0);
  fraction -= (double) (second / 86400.0);
  msec = (long) (fraction * 86400000.0);
  return computeEPOCH (year, month, day, hour, minute, second, msec);
}

/******************************************************************************
* parseEPOCH2.
*   This function parses an input date/time string and returns an EPOCH
* value.  The format must be exactly as shown below.
*
* Format:	yyyymmddhhmmss
* Examples:	19950508000000
*		19671231235959
*
* The expected format is the same as that produced by encodeEPOCH2.
******************************************************************************/

STATICforIDL double parseEPOCH2 (inString)
char *inString;
{
  long year, month, day, hour, minute, second;
  if (sscanf(inString,"%4ld%2ld%2ld%2ld%2ld%2ld",
	     &year,&month,&day,&hour,&minute,&second) != 6) {
    return ILLEGAL_EPOCH_VALUE;
  }
  return computeEPOCH (year, month, day, hour, minute, second, 0L);
}

/******************************************************************************
* parseEPOCH3.
*   This function parses an input date/time string and returns an EPOCH
* value.  The format must be exactly as shown below.
*
* Format:	yyyy-mm-ddThh:mm:ss.cccZ
* Examples:	1990-04-01T03:05:02.000Z
*		1993-10-10T23:45:49.999Z
*
* The expected format is the same as that produced by encodeEPOCH3.
******************************************************************************/

STATICforIDL double parseEPOCH3 (inString)
char *inString;
{
  long year, month, day, hour, minute, second, msec;
  if (sscanf(inString,"%ld-%ld-%ldT%ld:%ld:%ld.%ldZ",
	     &year,&month,&day,&hour,&minute,&second,&msec) != 7) {
    return ILLEGAL_EPOCH_VALUE;
  }
  return computeEPOCH (year, month, day, hour, minute, second, msec);
}

/******************************************************************************
* encodeEPOCH.
*   Converts an EPOCH value into a readable date/time string.
*
* Format:	dd-mmm-yyyy hh:mm:ss.ccc
* Examples:	01-Apr-1990 03:05:02.000
*		10-Oct-1993 23:45:49.999
*
* This format is the same as that expected by parseEPOCH.
******************************************************************************/

STATICforIDL void encodeEPOCH (epoch, epString)
double epoch;
char epString[EPOCH_STRING_LEN+1];
{
  encodeEPOCHx (epoch, "<dom.02>-<month>-<year> <hour>:<min>:<sec>.<fos>",
		epString);
  return;
}

/******************************************************************************
* encodeEPOCH1.
*   Converts an EPOCH value into a readable date/time string.
*
* Format:	yyyymmdd.ttttttt
* Examples:	19900401.3658893
*		19611231.0000000
*
* This format is the same as that expected by parseEPOCH1.
******************************************************************************/

STATICforIDL void encodeEPOCH1 (epoch, epString)
double epoch;
char epString[EPOCH1_STRING_LEN+1];
{
  encodeEPOCHx (epoch, "<year><mm.02><dom.02>.<fod.7>",
		epString);
  return;
}

/******************************************************************************
* encodeEPOCH2.
*   Converts an EPOCH value into a readable date/time string.
*
* Format:	yyyymmddhhmmss
* Examples:	19900401235959
*		19611231000000
*
* This format is the same as that expected by parseEPOCH2.
******************************************************************************/

STATICforIDL void encodeEPOCH2 (epoch, epString)
double epoch;
char epString[EPOCH2_STRING_LEN+1];
{
  encodeEPOCHx (epoch, "<year><mm.02><dom.02><hour><min><sec>",
		epString);
  return;
}

/******************************************************************************
* encodeEPOCH3.
*   Converts an EPOCH value into a readable date/time string.
*
* Format:	yyyy-mm-ddThh:mm:ss.cccZ
* Examples:	1990-04-01T03:05:02.000Z
*		1993-10-10T23:45:49.999Z
*
* This format is the same as that expected by parseEPOCH3.
******************************************************************************/

STATICforIDL void encodeEPOCH3 (epoch, epString)
double epoch;
char epString[EPOCH3_STRING_LEN+1];
{
  encodeEPOCHx (epoch, "<year>-<mm.02>-<dom.02>T<hour>:<min>:<sec>.<fos>Z",
		epString);
  return;
}

/******************************************************************************
* encodeEPOCHx.
******************************************************************************/

STATICforIDL void encodeEPOCHx (epoch, format, encoded)
double epoch;
char *format;
char *encoded;
{
  char *ptr = format;		/* Current position in format string. */
  char *ptrD;			/* Pointer to decimal point. */
  char *ptrE;			/* Pointer to ending right angle bracket. */
  char *p;			/* Temporary pointer. */
  char part[MAX_PART_LEN+1];	/* Part being encoded. */
  char mod[MAX_MOD_LEN+1];	/* Part modifier. */
  long year, month, day, hour,
       minute, second, msec;	/* EPOCH components. */
  /****************************************************************************
  * Break EPOCH down into its components, validate the format specification,
  * and initialize the encoded string.
  ****************************************************************************/
  if (format == NULL || NULstring(format)) {
    encodeEPOCH (epoch, encoded);
    return;
  }
  EPOCHbreakdown (epoch, &year, &month, &day, &hour, &minute, &second, &msec);
  MakeNUL (encoded);
  /****************************************************************************
  * Scan format string.
  ****************************************************************************/
  for (;;) {
     switch (*ptr) {
       /***********************************************************************
       * End of format string.
       ***********************************************************************/
       case NUL:
	 return;
       /***********************************************************************
       * Start of part to be encoded.
       ***********************************************************************/
       case '<':
	 /*********************************************************************
	 * If next character is also a `<' (character stuffing), then append
	 * a `<' and move on.
	 *********************************************************************/
	 if (*(ptr+1) == '<') {
	   strcatX (encoded, "<", 0);
	   ptr += 2;
	   break;
	 }
	 /*********************************************************************
	 * Find ending right angle bracket.
	 *********************************************************************/
	 ptrE = strchr (ptr + 1, '>');
	 if (ptrE == NULL) {
	   strcatX (encoded, "?", 0);
	   return;
	 }
	 /*********************************************************************
	 * Check for a part modifier.
	 *********************************************************************/
	 ptrD = strchr (ptr + 1, '.');
	 if (ptrD != NULL && ptrD < ptrE) {
	   MakeNUL (part);
	   for (p = ptr+1; p != ptrD; p++) catchrX (part, (int) *p,
						    MAX_PART_LEN);
	   MakeNUL (mod);
	   for (p = ptrD+1; p != ptrE; p++) catchrX (mod, (int) *p,
						     MAX_MOD_LEN);
	 }
	 else {
	   MakeNUL (part);
	   for (p = ptr+1; p != ptrE; p++) catchrX (part, (int) *p,
						    MAX_PART_LEN);
	   MakeNUL (mod);
	 }
	 ptr = ptrE + 1;
	 /*********************************************************************
	 * Day (of month), <dom>.
	 *********************************************************************/
	 if (!strcmp(part,"dom")) {
	   if (!AppendIntegerPart(encoded,day,0,FALSE,mod)) return;
	   break;
	 }
	 /*********************************************************************
	 * Day of year, <doy>.
	 *********************************************************************/
	 if (!strcmp(part,"doy")) {
	   long doy = JulianDay(year,month,day) - JulianDay(year,1L,1L) + 1;
	   if (!AppendIntegerPart(encoded,doy,3,TRUE,mod)) return;
	   break;
	 }
	 /*********************************************************************
	 * Month (3-character), <month>.
	 *********************************************************************/
	 if (!strcmp(part,"month")) {
	   strcatX (encoded, MonthToken(month), 0);
	   break;
	 }
	 /*********************************************************************
	 * Month (digits), <mm>.
	 *********************************************************************/
	 if (!strcmp(part,"mm")) {
	   if (!AppendIntegerPart(encoded,month,0,FALSE,mod)) return;
	   break;
	 }
	 /*********************************************************************
	 * Year (full), <year>.
	 *********************************************************************/
	 if (!strcmp(part,"year")) {
	   if (!AppendIntegerPart(encoded,year,4,TRUE,mod)) return;
	   break;
	 }
	 /*********************************************************************
	 * Year (2-digit), <yr>.
	 *********************************************************************/
	 if (!strcmp(part,"yr")) {
	   long yr = year % 100L;
	   if (!AppendIntegerPart(encoded,yr,2,TRUE,mod)) return;
	   break;
	 }
	 /*********************************************************************
	 * Hour, <hour>.
	 *********************************************************************/
	 if (!strcmp(part,"hour")) {
	   if (!AppendIntegerPart(encoded,hour,2,TRUE,mod)) return;
	   break;
	 }
	 /*********************************************************************
	 * Minute, <min>.
	 *********************************************************************/
	 if (!strcmp(part,"min")) {
	   if (!AppendIntegerPart(encoded,minute,2,TRUE,mod)) return;
	   break;
	 }
	 /*********************************************************************
	 * Second, <sec>.
	 *********************************************************************/
	 if (!strcmp(part,"sec")) {
	   if (!AppendIntegerPart(encoded,second,2,TRUE,mod)) return;
	   break;
	 }
	 /*********************************************************************
	 * Fraction of second, <fos>.
	 *********************************************************************/
	 if (!strcmp(part,"fos")) {
	   double fos = ((double) msec) / 1000.0;
	   if (!AppendFractionPart(encoded,fos,3,mod)) return;
	   break;
	 }
	 /*********************************************************************
	 * Fraction of day, <fod>.
	 *********************************************************************/
	 if (!strcmp(part,"fod")) {
	   double fod = ((double) hour / 24.0) +
			((double) minute / 1440.0) +
			((double) second / 86400.0) +
			((double) msec / 86400000.0);
	   if (!AppendFractionPart(encoded,fod,8,mod)) return;
	   break;
	 }
	 /*********************************************************************
	 * Unknown/unsupported part.
	 *********************************************************************/
	 strcatX (encoded, "?", 0);
	 return;
       /***********************************************************************
       * Character to be copied.
       ***********************************************************************/
       default:
	 catchrX (encoded, (int) *ptr, 0);
	 ptr++;
	 break;
     }
  }
}

static Logical AppendFractionPart (encoded, fraction, defaultWidth, modifier)
char *encoded;
double fraction;
int defaultWidth;
char *modifier;
{
  char ePart[MAX_ePART_LEN+1]; int width, i;
  if (!NULstring(modifier)) {
    if (sscanf(modifier,"%d",&width) != 1) {
      strcatX (encoded, "?", 0);
      return FALSE;
    }
    if (width < 1) {
      strcatX (encoded, "?", 0);
      return FALSE;
    }
  }
  else
    width = defaultWidth;
  sprintf (ePart, "%*.*f", width + 2, width, fraction);
#if defined(alphaosf)
  /****************************************************************************
  * V3.2 of OSF/1 apparently has a bug involving `sprintf'.  The preceeding
  * call to `sprintf' produces a string containing one too many digits after
  * the decimal.  Eg., if width=7 the encoded string might be 0.12345678
  * rather than 0.1234567 as it should be.  So we'll fix it...
  ****************************************************************************/
  ePart[width+2] = NUL;
#endif
  if (ePart[0] == '1') for (i = 0; i < width; i++) ePart[i+2] = '9';
  return AppendPart (encoded, strchr(ePart,'.') + 1, width, FALSE);
}

static Logical AppendIntegerPart (encoded, integer, defaultWidth,
				  defaultLeading0, modifier)
char *encoded;
long integer;
int defaultWidth;
Logical defaultLeading0;
char *modifier;
{
  char ePart[MAX_ePART_LEN+1]; int width; Logical leading0;
  if (!NULstring(modifier)) {
    if (sscanf(modifier,"%d",&width) != 1) {
      strcatX (encoded, "?", 0);
      return FALSE;
    }
    if (width < 0) {
      strcatX (encoded, "?", 0);
      return FALSE;
    }
    leading0 = (modifier[0] == '0');
  }
  else {
    width = defaultWidth;
    leading0 = defaultLeading0;
  }
  sprintf (ePart, "%ld", integer);
  return AppendPart (encoded, ePart, width, leading0);
}

static Logical AppendPart (encoded, ePart, width, leading0)
char *encoded;
char *ePart;
int width;
Logical leading0;
{
  int i;
  if (width == 0) {
    strcatX (encoded, ePart, 0);
  }
  else {
    size_t length = strlen(ePart);
    if (length > width) {
      for (i = 0; i < width; i++) strcatX (encoded, "*", 0);
    }
    else {
      int pad = width - length;
      if (pad > 0) {
        for (i = 0; i < pad; i++) strcatX (encoded, BOO(leading0,"0"," "), 0);
      }
      strcatX (encoded, ePart, 0);
    }
  }
  return TRUE;
}

/******************************************************************************
* computeEPOCH.
*   Computes (and returns) an EPOCH value based on its component parts.
* ILLEGAL_EPOCH_VALUE is returned if an illegal component part is detected.
******************************************************************************/

STATICforIDL double computeEPOCH (year, month, day, hour, minute, second, msec)
long year, month, day, hour, minute, second, msec;
{
  long daysSince0AD, msecInDay;
  /****************************************************************************
  * Calculate the days since 0 A.D (1-Jan-0000).  If a value of zero is passed
  * in for `month', assume that `day' is the day-of-year (DOY) with January 1st
  * being day 1.
  ****************************************************************************/
  if (month == 0) {
    if (year < 0 || year > 9999) return ILLEGAL_EPOCH_VALUE;
    if (day < 0 || day > 366) return ILLEGAL_EPOCH_VALUE;
    daysSince0AD = (JulianDay(year,1L,1L) + (day-1)) - 1721060L;
  }
  else {
    if (year < 0 || year > 9999) return ILLEGAL_EPOCH_VALUE;
    if (month < 1 || month > 12) return ILLEGAL_EPOCH_VALUE;
    if (day < 0 || day > 31) return ILLEGAL_EPOCH_VALUE;
    daysSince0AD = JulianDay(year,month,day) - 1721060L;
  }
  /****************************************************************************
  * Calculate the millisecond in the day (with the first millisecond being 0).
  * If values of zero are passed in for `hour', `minute', and `second', assume
  * that `msec' is the millisecond in the day.
  ****************************************************************************/
  if (hour == 0 && minute == 0 && second == 0) {
    if (msec < 0 || msec > 86399999L) return ILLEGAL_EPOCH_VALUE;
    msecInDay = msec;
  }
  else {
    if (hour < 0 || hour > 23) return ILLEGAL_EPOCH_VALUE;
    if (minute < 0 || minute > 59) return ILLEGAL_EPOCH_VALUE;
    if (second < 0 || second > 59) return ILLEGAL_EPOCH_VALUE;
    if (msec < 0 || msec > 999) return ILLEGAL_EPOCH_VALUE;
    msecInDay = (3600000L * hour) + (60000L * minute) + (1000 * second) + msec;
  }
  /****************************************************************************
  * Return the milliseconds since 0 A.D.
  ****************************************************************************/
  return ((86400000L * ((double) daysSince0AD)) + ((double) msecInDay));
}

/******************************************************************************
* EPOCHbreakdown.
*   Breaks an EPOCH value down into its component parts.
******************************************************************************/

STATICforIDL void EPOCHbreakdown (epoch, year, month, day, hour, minute,
				  second, msec)
double epoch;
long *year, *month, *day, *hour, *minute, *second, *msec;
{
  long jd,i,j,k,l,n;
  double msec_AD, second_AD, minute_AD, hour_AD, day_AD;

  if (NegativeZeroReal8(&epoch)) {
    *year = 0;
    *month = 0;
    *day = 0;
    *hour = 0;
    *minute = 0;
    *second = 0;
    *msec = 0;
    return;
  }

  if (epoch < 0.0) epoch = -epoch;
  epoch = MINIMUM (MAX_EPOCH_BINARY, epoch);

  msec_AD = epoch;
  second_AD = msec_AD / 1000.0;
  minute_AD = second_AD / 60.0;
  hour_AD = minute_AD / 60.0;
  day_AD = hour_AD / 24.0;

  jd = (long) (1721060 + day_AD);
  l=jd+68569;
  n=4*l/146097;
  l=l-(146097*n+3)/4;
  i=4000*(l+1)/1461001;
  l=l-1461*i/4+31;
  j=80*l/2447;
  k=l-2447*j/80;
  l=j/11;
  j=j+2-12*l;
  i=100*(n-49)+i+l;

  *year = i;
  *month = j;
  *day = k;

  *hour   = fmod (hour_AD, (double) 24.0);
  *minute = fmod (minute_AD, (double) 60.0);
  *second = fmod (second_AD, (double) 60.0);
  *msec   = fmod (msec_AD, (double) 1000.0);

  return;
}

/******************************************************************************
* JulianDay.
*    The year, month, and day are assumed to have already been validated.  This
* is the day since 0 AD/1 BC.  (Julian day may not be the proper term.)
******************************************************************************/

static long JulianDay (y,m,d)
long y, m, d;
{
  return (367*y-7*(y+(m+9)/12)/4-3*((y+(m-9)/7)/100+1)/4+275*m/9+d+1721029);
}

/******************************************************************************
* MonthToken.
******************************************************************************/

static char *MonthToken (month)
long month;
{
  switch (month) {
    case 1: return "Jan";
    case 2: return "Feb";
    case 3: return "Mar";
    case 4: return "Apr";
    case 5: return "May";
    case 6: return "Jun";
    case 7: return "Jul";
    case 8: return "Aug";
    case 9: return "Sep";
    case 10: return "Oct";
    case 11: return "Nov";
    case 12: return "Dec";
  }
  return "???";
}

/******************************************************************************
* FullDayToken.
******************************************************************************/

static char *FullDayToken (day3)
char *day3;
{
  if (!strcmp(day3,"Sun")) return "Sunday";
  if (!strcmp(day3,"Mon")) return "Monday";
  if (!strcmp(day3,"Tue")) return "Tuesday";
  if (!strcmp(day3,"Wed")) return "Wednesday";
  if (!strcmp(day3,"Thu")) return "Thursday";
  if (!strcmp(day3,"Fri")) return "Friday";
  if (!strcmp(day3,"Sat")) return "Saturday";
  return "Someday";
}

/******************************************************************************
* TimeStamp.
*   Gets the date & time from the system and encodes a string in the following
* form:
*
*     ddddddddd, dd-mmm-yyyy hh:mm:ss
*
* Examples:
*
*     Saturday, 23-Oct-1993 09:37:34
*     Sunday, 2-Jan-1994 10:00:00
*     Wednesday, 27-Oct-1993 23:59:59
*
* Trailing blanks are not appended if the string is shorter than its maximum
* possible length.
******************************************************************************/

STATICforIDL void TimeStamp (stampStr)
char *stampStr;
{
  time_t bintim;
  char ctimeStr[CTIME_STRING_LEN+1], dayOfWeek3[3+1], dayOfMonth[2+1],
       year[4+1], month[3+1], hourMinuteSecond[8+1];
  time (&bintim);
  strcpyX (ctimeStr, ctime(&bintim), CTIME_STRING_LEN);
  strcpyX (dayOfWeek3, ctimeStr, 3);
  strcpyX (dayOfMonth, &ctimeStr[8], 2);
  if (dayOfMonth[0] == ' ') memmove (dayOfMonth, &dayOfMonth[1], 2);
  strcpyX (year, &ctimeStr[20], 4);
  strcpyX (month, &ctimeStr[4], 3);
  strcpyX (hourMinuteSecond, &ctimeStr[11], 8);
  sprintf (stampStr, "%s, %s-%s-%s %s", FullDayToken(dayOfWeek3), dayOfMonth,
	   month, year, hourMinuteSecond);
  return;
}
