======
TODOs
======

  * remove OpenMeta dependency, and make it optional (currently that restricts us to OS X unnecessarily)  
  * test (ha!)
  * document (ha!)
  * parse success of edit and login operations
  * CUL doesn't like more than one request every 5 seconds. Currently i use a
    wait_for_api_limit() method to throttle connections, but this is error
    prone
    
     * it might be cleaner to subclass mechanize and enforce it there, plus
       include a backoff (see next)
    
  * The server is patchily available, at least from my ISP, so we should also
    override the fetch methods to do retry with automatic backoff, e.g.
    
    * https://gist.github.com/728327
    * http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    
  * downloaded PDFs should link back to their CUL page
  * cache cookies to save a page load
