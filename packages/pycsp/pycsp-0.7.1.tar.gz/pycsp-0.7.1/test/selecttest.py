"""
Copyright (c) 2009 John Markus Bjoerndalen <jmb@cs.uit.no>,
      Brian Vinter <vinter@diku.dk>, Rune M. Friborg <runef@diku.dk>
Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:
  
The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.  THE
SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from pycsp_import import *
import time
import random

@io
def sleep_random():
    time.sleep(random.random()/10)

@process
def writer(cout, id, cnt, sleeper):
    for i in range(cnt):
        if sleeper: sleeper()
        cout((id, i))
    
@process
def par_reader(cin1,cin2,cin3,cin4, cnt, sleeper):
    for i in range(cnt*4):
        if sleeper: sleeper()
        
        c, msg = AltSelect(
            InputGuard(cin1),
            InputGuard(cin2),
            InputGuard(cin3),
            InputGuard(cin4)
            )
            
        print 'From ',c ,'got',msg

@process
def par_reader_fair(cin1,cin2,cin3,cin4, cnt, sleeper):
    for i in range(cnt*4):
        if sleeper: sleeper()
        
        c, msg = FairSelect(
            InputGuard(cin1),
            InputGuard(cin2),
            InputGuard(cin3),
            InputGuard(cin4)
            )
            
        print 'From ',c ,'got',msg


def Any2One_Alting_Test(par_reader, read_sleeper, write_sleeper):
    c1=Channel('C1')
    c2=Channel('C2')
    c3=Channel('C3')
    c4=Channel('C4')

    cnt = 10
    
    Parallel(par_reader(+c1,+c2,+c3,+c4,cnt, read_sleeper),
             writer(-c1,0,cnt, write_sleeper),
             writer(-c2,1,cnt, write_sleeper),
             writer(-c3,2,cnt, write_sleeper),
             writer(-c4,3,cnt, write_sleeper))

if __name__ == '__main__':
    print "Any2One_Alting_Test - AltSelect"
    Any2One_Alting_Test(par_reader, sleep_random, sleep_random)
    print "Any2One_Alting_Test - FairSelect"
    Any2One_Alting_Test(par_reader_fair, sleep_random, sleep_random)
        
