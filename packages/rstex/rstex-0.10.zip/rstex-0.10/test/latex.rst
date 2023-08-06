Without a mu (no latex in titles sorry)
#######################################

ReStructuredText can be translated into LaTeX. All the standard semantics of
ReStructuredText are supported via the ``rst2latex`` or ``rst2newlatex`` 
commands. The difference between them is subtle one is bad at providing "nice"
LaTeX markup, but the output is good, the other generates nice code, but the
quality if the rendering is sub-optimal. RsTeX is based on rst2latex. It enhaces
ReStructuredText by providing roles and directives for LaTeX inlined and 
displayed math and a raw latex directive.

math directive code ::

  .. math::

    \pi = \sigma 

math directive output:

.. math::

  \pi = \sigma
  
  
math inline code: ``:math:`\pi```

math inline output: :math:`\pi`


math directive with label code::

  .. math::
    :label: my_label
  
    \pi \new \Pi


math directive with label output:

.. math::
  :label: my_label
  
   \pi \neq \Pi
   
reference to a labeled equation code: ``:ref:`my_label```

reference to a labeled equation otuput: :ref:`my_label`

For speedy RsTeXing it is possible to gather multiple equations in one 
"``.. math::``" directive, the equations are still separate::

  .. math::
    :type: gather
  
    1 + 1 = 1 \\
    2 = 2 \\
    3 -2 = 3
   
output:
    
.. math::
  :type: gather
  
  1 + 1 = 1 \\
  2 = 2 \\
  3 -2 = 3
  
Or to group multiple lines as the same equation::

  .. math::
    :type: gathered
    :label: gthr
  
    1 + 1 = 1 \\
    2 = 2 \\
    3 -2 = 3  

output:

.. math::
  :type: gathered
  :label: gthr
  
  1 + 1 = 1 \\
  2 = 2 \\
  3 -2 = 3  

And refer to it :ref:`gthr` end.


Finally any LaTeX code can be injected into the out::

  .. latex::
    :usepackage: url, array

    \begin{tabular}{ l c r }
      1 & 2 & 3 \\
      4 & \url{http://muralab.org} & 6 \\
      7 & 8 & 9 \\
    \end{tabular}
  
  this is good \emph{North East West South}!

output:

.. latex::
  :usepackage: url, array

  \begin{tabular}{ l c r }
    1 & 2 & 3 \\
    4 & \url{http://muralab.org} & 6 \\
    7 & 8 & 9 \\
  \end{tabular}
  
  this is good \emph{North East West South}!
  

  

  
  
