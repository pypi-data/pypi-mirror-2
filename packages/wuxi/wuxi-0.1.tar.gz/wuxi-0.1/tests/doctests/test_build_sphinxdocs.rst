
A basic document::

    >>> from util import TEST_DOCUMENTS
    >>> docroot = TEST_DOCUMENTS['sphinxdoc']

Output utilities::

    >>> from cStringIO import StringIO
    >>> from util import logfilter
    >>> status = StringIO()
    >>> warn = StringIO()
    >>> info = lambda : logfilter(status.getvalue())
    >>> warnings = lambda : logfilter(warn.getvalue())

Create a Sphinx application::

    >>> from sphinx.application import Sphinx
    >>> from util import setup_sources
    >>> builder = 'html'
    >>> args = setup_sources(docroot, builder)
    >>> kwargs = {'status': status, 'warning': warn}
    >>> application = Sphinx(*args, **kwargs)
    >>> info() #doctest: +ELLIPSIS
    Running Sphinx ...
    loading pickled environment... not yet created
    >>> warnings()

Check config values::

    >>> application.config.html_title
    'Sphinx v1.0.3 documentation'
    >>> application.config.template_bridge
    'wuxi.bridge.DjangoTemplateBridge'
    >>> for ext in sorted(application.config.extensions):
    ...     print ext
    ...
    sphinx.ext.autodoc
    sphinx.ext.autosummary
    sphinx.ext.doctest
    sphinx.ext.extlinks
    sphinx.ext.todo
    wuxi

Template loader is from Wuxi::

    >>> application.builder.templates #doctest: +ELLIPSIS
    <wuxi.bridge.DjangoTemplateBridge object at ...>

Create the document::

    >>> application.build(force_all=True)
    >>> info() #doctest: +ELLIPSIS
    Running Sphinx v1.0.3
    loading pickled environment... not yet created
    building [html]: all source files
    updating environment: 40 added, 0 changed, 0 removed
    reading sources... [  2%] builders                                                                                          
    reading sources... [  5%] changes                                                                                           
    reading sources... [  7%] config                                                                                            
    reading sources... [ 10%] contents                                                                                          
    reading sources... [ 12%] domains                                                                                           
    reading sources... [ 15%] examples                                                                                          
    reading sources... [ 17%] ext/appapi                                                                                        
    reading sources... [ 20%] ext/autodoc                                                                                       
    reading sources... [ 22%] ext/autosummary                                                                                   
    reading sources... [ 25%] ext/builderapi                                                                                    
    reading sources... [ 27%] ext/coverage                                                                                      
    reading sources... [ 30%] ext/doctest                                                                                       
    reading sources... [ 32%] ext/extlinks                                                                                      
    reading sources... [ 35%] ext/graphviz                                                                                      
    reading sources... [ 37%] ext/ifconfig                                                                                      
    reading sources... [ 40%] ext/inheritance                                                                                   
    reading sources... [ 42%] ext/intersphinx                                                                                   
    reading sources... [ 45%] ext/math                                                                                          
    reading sources... [ 47%] ext/oldcmarkup                                                                                    
    reading sources... [ 50%] ext/refcounting                                                                                   
    reading sources... [ 52%] ext/todo                                                                                          
    reading sources... [ 55%] ext/tutorial                                                                                      
    reading sources... [ 57%] ext/viewcode                                                                                      
    reading sources... [ 60%] extensions                                                                                        
    reading sources... [ 62%] faq                                                                                               
    reading sources... [ 65%] glossary                                                                                          
    reading sources... [ 67%] intro                                                                                             
    reading sources... [ 70%] invocation                                                                                        
    reading sources... [ 72%] man/sphinx-build                                                                                  
    reading sources... [ 75%] man/sphinx-quickstart                                                                             
    reading sources... [ 77%] markup/code                                                                                       
    reading sources... [ 80%] markup/index                                                                                      
    reading sources... [ 82%] markup/inline                                                                                     
    reading sources... [ 85%] markup/misc                                                                                       
    reading sources... [ 87%] markup/para                                                                                       
    reading sources... [ 90%] markup/toctree                                                                                    
    reading sources... [ 92%] rest                                                                                              
    reading sources... [ 95%] templating                                                                                        
    reading sources... [ 97%] theming                                                                                           
    reading sources... [100%] tutorial                                                                                          
    looking for now-outdated files... none found
    pickling environment... done
    checking consistency... done
    preparing documents... done
    writing output... [  2%] builders                                                                                           
    writing output... [  5%] changes                                                                                            
    writing output... [  7%] config                                                                                             
    writing output... [ 10%] contents                                                                                           
    writing output... [ 12%] domains                                                                                            
    writing output... [ 15%] examples                                                                                           
    writing output... [ 17%] ext/appapi                                                                                         
    writing output... [ 20%] ext/autodoc                                                                                        
    writing output... [ 22%] ext/autosummary                                                                                    
    writing output... [ 25%] ext/builderapi                                                                                     
    writing output... [ 27%] ext/coverage                                                                                       
    writing output... [ 30%] ext/doctest                                                                                        
    writing output... [ 32%] ext/extlinks                                                                                       
    writing output... [ 35%] ext/graphviz                                                                                       
    writing output... [ 37%] ext/ifconfig                                                                                       
    writing output... [ 40%] ext/inheritance                                                                                    
    writing output... [ 42%] ext/intersphinx                                                                                    
    writing output... [ 45%] ext/math                                                                                           
    writing output... [ 47%] ext/oldcmarkup                                                                                     
    writing output... [ 50%] ext/refcounting                                                                                    
    writing output... [ 52%] ext/todo                                                                                           
    writing output... [ 55%] ext/tutorial                                                                                       
    writing output... [ 57%] ext/viewcode                                                                                       
    writing output... [ 60%] extensions                                                                                         
    writing output... [ 62%] faq                                                                                                
    writing output... [ 65%] glossary                                                                                           
    writing output... [ 67%] intro                                                                                              
    writing output... [ 70%] invocation                                                                                         
    writing output... [ 72%] man/sphinx-build                                                                                   
    writing output... [ 75%] man/sphinx-quickstart                                                                              
    writing output... [ 77%] markup/code                                                                                        
    writing output... [ 80%] markup/index                                                                                       
    writing output... [ 82%] markup/inline                                                                                      
    writing output... [ 85%] markup/misc                                                                                        
    writing output... [ 87%] markup/para                                                                                        
    writing output... [ 90%] markup/toctree                                                                                     
    writing output... [ 92%] rest                                                                                               
    writing output... [ 95%] templating                                                                                         
    writing output... [ 97%] theming                                                                                            
    writing output... [100%] tutorial                                                                                           
    writing additional files... genindex py-modindex search index opensearch
    copying images... [ 12%] themes/default.png                                                                                 
    copying images... [ 25%] themes/haiku.png                                                                                   
    copying images... [ 37%] themes/sphinxdoc.png                                                                               
    copying images... [ 50%] themes/traditional.png                                                                             
    copying images... [ 62%] themes/scrolls.png                                                                                 
    copying images... [ 75%] more.png                                                                                           
    copying images... [ 87%] themes/nature.png                                                                                  
    copying images... [100%] themes/agogo.png                                                                                   
    copying static files... done
    dumping search index... done
    dumping object inventory... done
    build succeeded.
    >>> warnings()


