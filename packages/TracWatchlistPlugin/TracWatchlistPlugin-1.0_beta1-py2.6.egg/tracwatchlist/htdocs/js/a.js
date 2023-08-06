function format ( fmt, date )
    {
        var d = new Date(date.getTime());
        var t;
        var str = '';
        for ( var f = 0 ; f < fmt.length ; f++ )
        {
          if ( fmt.charAt(f) != '%' )
            str += fmt.charAt(f);
          else
          {
            var ch = fmt.charAt(f+1)
            switch ( ch )
            {
              case 'a': // Abbreviated weekday name (Sun..Sat)
                str += this.dAbbr[ d.getDay() ];
                break;
              case 'B': // BCE string (eAbbr[0], usually BCE or BC, only if appropriate) (NON-MYSQL)
                if ( d.getFullYear() < 0 )
                  str += this.eAbbr[0];
                break;
              case 'b': // Abbreviated month name (Jan..Dec)
                str += this.mAbbr[ d.getMonth() ];
                break;
              case 'C': // CE string (eAbbr[1], usually CE or AD, only if appropriate) (NON-MYSQL)
                if ( d.getFullYear() > 0 )
                  str += this.eAbbr[1];
                break;
              case 'c': // Month, numeric (0..12)
                str += d.getMonth()+1;
                break;
              case 'd': // Day of the month, numeric (00..31)
                t = d.getDate();
                if ( t < 10 ) str += '0';
                str += String(t);
                break;
              case 'D': // Day of the month with English suffix (0th, 1st,...)
                t = String(d.getDate());
                str += t;
                if ( ( t.length == 2 ) && ( t.charAt(0) == '1' ) )
                  str += 'th';
                else
                {
                  switch ( t.charAt( t.length-1 ) )
                  {
                    case '1': str += 'st'; break;
                    case '2': str += 'nd'; break;
                    case '3': str += 'rd'; break;
                    default: str += 'th'; break;
                  }
                }
                break;
              case 'E': // era string (from eAbbr[], BCE, CE, BC or AD) (NON-MYSQL)
                str += this.eAbbr[ (d.getFullYear()<0) ? 0 : 1 ];
                break;
              case 'e': // Day of the month, numeric (0..31)
                str += d.getDate();
                break;
              case 'H': // Hour (00..23)
                t = d.getHours();
                if ( t < 10 ) str += '0';
                str += String(t);
                break;
              case 'h': // Hour (01..12)
              case 'I': // Hour (01..12)
                t = d.getHours() % 12;
                if ( t == 0 )
                  str += '12';
                else
                {
                  if ( t < 10 ) str += '0';
                  str += String(t);
                }
                break;
              case 'i': // Minutes, numeric (00..59)
                t = d.getMinutes();
                if ( t < 10 ) str += '0';
                str += String(t);
                break;
              case 'k': // Hour (0..23)
                str += d.getHours();
                break;
              case 'l': // Hour (1..12)
                t = d.getHours() % 12;
                if ( t == 0 )
                  str += '12';
                else
                  str += String(t);
                break;
              case 'M': // Month name (January..December)
                str += this.mNames[ d.getMonth() ];
                break;
              case 'm': // Month, numeric (00..12)
                t = d.getMonth() + 1;
                if ( t < 10 ) str += '0';
                str += String(t);
                break;
              case 'p': // AM or PM
                str += ( ( d.getHours() < 12 ) ? 'AM' : 'PM' );
                break;
              case 'r': // Time, 12-hour (hh:mm:ss followed by AM or PM)
                t = d.getHours() % 12;
                if ( t == 0 )
                  str += '12:';
                else
                {
                  if ( t < 10 ) str += '0';
                  str += String(t) + ':';
                }
                t = d.getMinutes();
                if ( t < 10 ) str += '0';
                str += String(t) + ':';
                t = d.getSeconds();
                if ( t < 10 ) str += '0';
                str += String(t);
                str += ( ( d.getHours() < 12 ) ? 'AM' : 'PM' );
                break;
              case 'S': // Seconds (00..59)
              case 's': // Seconds (00..59)
                t = d.getSeconds();
                if ( t < 10 ) str += '0';
                str += String(t);
                break;
              case 'T': // Time, 24-hour (hh:mm:ss)
                t = d.getHours();
                if ( t < 10 ) str += '0';
                str += String(t) + ':';
                t = d.getMinutes();
                if ( t < 10 ) str += '0';
                str += String(t) + ':';
                t = d.getSeconds();
                if ( t < 10 ) str += '0';
                str += String(t);
                break;
              case 'W': // Weekday name (Sunday..Saturday)
                str += this.dNames[ d.getDay() ];
                break;
              case 'w': // Day of the week (0=Sunday..6=Saturday)
                str += d.getDay();
                break;
              case 'Y': // Year, numeric, four digits (negative if before 0001)
                str += AnyTime.pad(d.getFullYear(),4);
                break;
              case 'y': // Year, numeric (two digits, negative if before 0001)
                t = d.getFullYear() % 100;
                str += AnyTime.pad(t,2);
                break;
              case 'Z': // Year, numeric, four digits, unsigned (NON-MYSQL)
                str += AnyTime.pad(Math.abs(d.getFullYear()),4);
                break;
              case 'z': // Year, numeric, variable length, unsigned (NON-MYSQL)
                str += Math.abs(d.getFullYear());
                break;
              case '%': // A literal '%' character
                str += '%';
                break;
              case '#': // signed timezone offset in minutes
                t = ( _offAl != Number.MIN_VALUE ) ? _offAl :
                    ( _offF == Number.MIN_VALUE ) ? (0-d.getTimezoneOffset()) : _offF;
                if ( t >= 0 )
                    str += '+';
                str += t;
                break;
              case '@': // timezone offset label
                t = ( _offAl != Number.MIN_VALUE ) ? _offAl :
                    ( _offF == Number.MIN_VALUE ) ? (0-d.getTimezoneOffset()) : _offF;
                if ( AnyTime.utcLabel && AnyTime.utcLabel[t] )
                {
                  if ( ( _offFSI > 0 ) && ( _offFSI < AnyTime.utcLabel[t].length ) )
                    str += AnyTime.utcLabel[t][_offFSI];
                  else
                    str += AnyTime.utcLabel[t][0];
                  break;
                }
                str += 'UTC';
                ch = ':'; // drop through for offset formatting
              case '+': // signed, 4-digit timezone offset in hours and minutes
              case '-': // signed, 3-or-4-digit timezone offset in hours and minutes
              case ':': // signed 4-digit timezone offset with colon delimiter
              case ';': // signed 3-or-4-digit timezone offset with colon delimiter
                t = ( _offAl != Number.MIN_VALUE ) ? _offAl :
                        ( _offF == Number.MIN_VALUE ) ? (0-d.getTimezoneOffset()) : _offF;
                if ( t < 0 )
                  str += '-';
                else
                  str += '+';
                t = Math.abs(t);
                str += ((ch=='+')||(ch==':')) ? AnyTime.pad(Math.floor(t/60),2) : Math.floor(t/60);
                if ( (ch==':') || (ch==';') )
                  str += ':';
                str += AnyTime.pad(t%60,2);
                break;
              case 'f': // Microseconds (000000..999999)
              case 'j': // Day of year (001..366)
              case 'U': // Week (00..53), where Sunday is the first day of the week
              case 'u': // Week (00..53), where Monday is the first day of the week
              case 'V': // Week (01..53), where Sunday is the first day of the week; used with %X
              case 'v': // Week (01..53), where Monday is the first day of the week; used with %x
              case 'X': // Year for the week where Sunday is the first day of the week, numeric, four digits; used with %V
              case 'x': // Year for the week, where Monday is the first day of the week, numeric, four digits; used with %v
                throw '%'+ch+' not implemented by AnyTime.Converter';
              default: // for any character not listed above
                str += this.fmt.substr(f,2);
            } // switch ( this.fmt.charAt(f+1) )
            f++;
          } // else
        } // for ( var f = 0 ; f < _flen ; f++ )
        return str;
        
    };
        
        
var d = new Date();

format('%l', d);


