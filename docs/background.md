# Background and Philosophy 

## Background
This project was originally written to run on a beefy Linux server without containerization.  Everything was hard-coded, since it was designed to run in my house (meters don't change very often :-). I used MongoDB as the backing-store, since I could feed the JSON output of rtlamr into it without any transformations.  

Then last year I got a new water meter.  And had an unused Raspberry Pi . . . and wanted to play with Docker.  And now this project is now ready for its first release.  Hopefully someone else will find it useful.

## Philosophy

Keep it simple.  For this first release, I wanted no external Python libraries, no external database engines, etc.  Just a simple as it could be, yet still provide a robust, easy-to-access data store that facilitated graphing and data analysis.  

The python app that takes the JSON output of rtlamr is very simple:  no classes, only a couple of very simple functions, and utilizes the native SQLite module.  At some point in the future I may re-write it to be more "modern" with a database abstraction layer to allow easy use of SQLite or a "real" data base. 