Django SSI
==========

See http://wiki.nginx.org/HttpSsiModule

::
    
    {% load nginxssi_tags %}
    {% nginxssi %}
        <b> okidoki </b> {%now "jS F Y H:i"%} Hello {{foo}}
    {% nginxssi %}
    
Renders as:

::
    
    <!--# include virtual="/nginxssi/a3e5fa678243e0bab620fbca75f6601d/" -->
    
A request to `/nginxssi/a3e5fa678243e0bab620fbca75f6601d/` renders:

::
    
    <b> okidoki </b> 25th January 2011 13:26 Hello bar

How it works
------------

    1. The template is cached in its raw unrendered form
    2. The template string's md5 hash is used as a cache key
    3. The template's context is stored with the cache key as a prefix
    4. A request to the SSI url looks up the template and the context 
       in the cache, renders it and returns the HttpResponse
    