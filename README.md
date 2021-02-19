### Modelling a Chatroom to demonstrate Asynchronous Non-Blocking threads using Python 
---
* ### [+] Chatroom(1):
  ![](https://github.com/tuhinnn-py/Python-Chatroom-EventLoop/blob/main/(1).png)
  ---
* ### [+] Chatroom(2):  
  ![](https://github.com/tuhinnn-py/Python-Chatroom-EventLoop/blob/main/(2).png)
* #### Synchronous vs Asynchronous vs Blocking vs Non-blocking 
  ---
  Synchronous execution usually refers to code executing in sequence. Asynchronous execution refers to execution that doesn't run in the sequence it appears in the code.

  Blocking refers to operations that block further execution until that operation finishes. Non-blocking refers to code that doesn't block execution. In the given example, localStorage is a blocking operation as it stalls execution to read.

  An example of synchronous, blocking operations is how some web servers like ones in Java or PHP handle IO or network requests. If your code reads from a file or the database, your code "blocks" everything after it from executing. In that period, your machine is holding onto memory and processing time for a thread that isn't doing anything. 
  In order to cater other requests while that thread has stalled depends on your software. What most server software do is spawn more threads to cater the additional requests. This requires more memory consumed and more processing.

  Asynchronous, non-blocking servers - like ones made in Node - only use one thread to service all requests. This means an instance of Node makes the most out of a single thread. The creators designed it with the premise that the I/O and network operations are the bottleneck.

  When requests arrive at the server, they are serviced one at a time. However, when the code serviced needs to query the DB for example, it sends the callback to a second queue and the main thread will continue running (it doesn't wait). Now when the DB operation completes and returns, the corresponding callback pulled out of the second queue and queued in a third queue where they are pending execution. When the engine gets a chance to execute something else (like when the execution stack is emptied), it picks up a callback from the third queue and executes it.

* #### Eventloop 
  ---
  JavaScript has a concurrency model based on an event loop, which is responsible for executing the code, collecting and processing events, and executing queued sub-tasks. This model is quite different from models in other languages like C and Java.
  The event loop is what allows Node.js to perform non-blocking I/O operations — despite the fact that JavaScript is single-threaded — by offloading operations to the system kernel whenever possible.
  Since most modern kernels are multi-threaded, they can handle multiple operations executing in the background. When one of these operations completes, the kernel tells Node.js so that the appropriate callback may be added to the poll queue to eventually be executed.
  
  ![](https://github.com/tuhinnn-py/Python-Chatroom-EventLoop/blob/main/Node%20js%20el.png)
