RsTeX
=====

RsTeX provides additional functionality over ``rst2latex``, which is a 
ReStructuedText to latex translator. It is based on ideas found in ``sphinx``
and provides a math role (``:math:``), reference role (``:ref:``), a math 
directive and a pure LaTeX "environment" with ``uspackage`` injection.

  - a math role ``:math:`` e.g. ``:math:`\frac{\log 23}{\pi}```
  - a ref role ``:ref:`` e.g. ``:ref:`my_label```
  - a math directive ``.. math::`` e.g.::
  
      .. math::
        :label: my_label
      
        \pi \neq \sigma
        
  - a raw latex directive ``.. latex::`` e.g.::
  
      .. latex::
        :usepackage: url
        
        
        \emph{a link} \url{http://muralab.org/rstex}
        



