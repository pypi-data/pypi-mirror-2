## coding: utf-8
##<%inherit file="${context['mako_layout']}"/>
<%inherit file="static_base.mako"/>

<%def name="headers()">
    <link rel="stylesheet" href="${pathto('_static/pygments.css', 1)}" type="text/css" />
    <link rel="stylesheet" href="${pathto('_static/docs.css', 1)}" type="text/css" />
    <link rel="stylesheet" href="${pathto('_static/sqlkit.css', 1)}" type="text/css" />
##    <link rel="stylesheet" href="${pathto('_static/menu-css.css', 1)}" type="text/css" />
    <link rel="stylesheet" href="${pathto('_static/jqueryslidemenu.css', 1)}" type="text/css" />

    <script type="text/javascript">
      var DOCUMENTATION_OPTIONS = {
          URL_ROOT:    '${pathto("", 1)}',
          VERSION:     '${release|h}',
          COLLAPSE_MODINDEX: false,
          FILE_SUFFIX: '${file_suffix}'
      };
    </script>
    % for scriptfile in script_files + self.attr.local_script_files:
        <script type="text/javascript" src="${pathto(scriptfile, 1)}"></script>
    % endfor
    <script type="text/javascript" src="${pathto('_static/jqueryslidemenu.js', 1)}"/>

    <script type="text/javascript" src="${pathto('_static/init.js', 1)}"></script>
    % if hasdoc('about'):
        <link rel="author" title="${_('About these documents')}" href="${pathto('about')}" />
    % endif
    <link rel="index" title="${_('Index')}" href="${pathto('genindex')}" />
    <link rel="search" title="${_('Search')}" href="${pathto('search')}" />
##    % if hasdoc('copyright'):
##        <link rel="copyright" title="${_('Copyright')}" href="${pathto('copyright')}" />
##    % endif
    <link rel="top" title="${docstitle|h}" href="${pathto('index')}" />
    % if parents:
        <link rel="up" title="${parents[-1]['title']|util.striptags}" href="${parents[-1]['link']|h}" />
    % endif
    % if nexttopic:
        <link rel="next" title="${nexttopic['title']|util.striptags}" href="${nexttopic['link']|h}" />
    % endif
    % if prevtopic:
        <link rel="prev" title="${prevtopic['title']|util.striptags}" href="${prevtopic['link']|h}" />
    % endif
    ${self.extrahead()}
</%def>
<%def name="extrahead()"></%def>
<!--[if !IE 7]>
	<style type="text/css">
		#wrap {display:table;height:100%}
	</style>
<![endif]-->


<div id="wrap">
    ${self.testata()}
    ${self.related()}
    ${self.sidebar()}
    <div class="document">
      <div class="documentwrapper">
        <div class="bodywrapper">

            <div class="body">
                ${next.body()}
            </div>
        </div>
     </div>
   </div>

        <%def name="footer()">
            <div class="bottomnav footer">
                <div class="doc_copyright">
                Alessandro Dentella -- Copyright 2006-2007-2008-2009-2010
		  Sqlkit release ${release}
<!--                 % if hasdoc('copyright'): -->
<!--                     &copy; <a href="${pathto('copyright')}">Copyright</a> ${copyright|h}. -->
<!--                 % else: -->
<!--                     &copy; Copyright ${copyright|h}. -->
<!--                 % endif -->
                % if show_sphinx:
                    creato usando  <a href="http://sphinx.pocoo.org/">Sphinx</a> ${sphinx_version|h}.
                % endif
                </div>
            </div>
        </%def>
</div> <!-- wrap -->
${self.footer()}

<%def name="prevnext()">
<div class="prevnext">
    % if prevtopic:
        Previous:
        <a href="${prevtopic['link']|h}" title="${_('previous chapter')}">${prevtopic['title']}</a>
    % endif
    % if nexttopic:
        Next:
        <a href="${nexttopic['link']|h}" title="${_('next chapter')}">${nexttopic['title']}</a>
    % endif
</div>
</%def>

<%def name="prevnextheader()">
<!-- <div class="prevnext"> -->
<!--    <li class="right"  style="margin-right: 10px">Indice -->
<!--      <a href="${pathto('genindex')}" title="Indice generale" -->
<!--                accesskey="I">indice</a></li> -->

    % if prevtopic:
        <li class="right">Prev:
        <a href="${prevtopic['link']|h}" title="${_('previous chapter')}">${prevtopic['title']}</a></li>
    % endif
    % if nexttopic:
        <li class="right">Next:
        <a href="${nexttopic['link']|h}" title="${_('next chapter')}">${nexttopic['title']}</a></li>
    % endif
<!-- </div> -->
</%def>

<%def name="show_title()">
% if title:
    ${title}
% endif
</%def>

<%def name="sidebar()">
  <div class="sphinxsidebar">
     <div class="sphinxsidebarwrapper">
##	<%include file="sidebar.mako"/>


	    <div class="topnav">
		% if display_toc and not current_page_name.startswith('index'):
    <h3>Table of contents</h3>
		    ${toc}
		% endif
		<div class="clearboth"></div>
	    </div>



    <h3>Questions?</h3>

    <p>Subscribe to out mailing list <a href="http://groups.google.com/group/sqlkit">
       Google group</a>:</p>

    <form action="http://groups.google.com/group/sqlkit/boxsubscribe" style="padding-left: 1em">
      <input type="text" name="email" value="your@email"/>
      <input type="submit" name="sub" value="Subscribe" />
    </form>
    <div id="searchbox" style="display: none">

    <h3>Quick search</h3>
	<form class="search" action="${pathto('search.html', 1)}" method="get">
	  <input type="text" name="q" size="18" />
	  <input type="submit" value="Search" />
	  <input type="hidden" name="check_keywords" value="yes" />

	  <input type="hidden" name="area" value="default" />
	</form>
	<p class="searchtip" style="font-size: 90%">
        Enter search terms or a module, class or function name.
	</p>
    <h3>License</h3>
	<img src="${pathto('_static/gplv3.png', 1)}" alt="logo GPLv3">

    </div>
    <script type="text/javascript">$('#searchbox').show(0);</script>

     </div>
  </div>
</%def>

<%def name="related()">
    <div class="related">
      <ul>
##        <li><a href="${pathto('index.html', 1)}">ReteIsi </a> |&nbsp;</li>
##       <li><a href="${pathto('contents.html', 1)}">Documentazione </a> &raquo;</li>

	${self.prevnextheader()}

      </ul>

    </div>
</%def>

<%def name="testata()">
<div id="header">

	<div class="logo"><a href="${pathto('sqlkit/tour')}">
       <img src="${pathto('_static/sqlkit.png', 1)}" align="left"  alt="Logo" border="0"/></a>
        </div>
	<div id="description">Acces to db made easy</div>
</div>


   <div style="clear:left;"></div>


<div id="main_menu" class="jqueryslidemenu">
	<ul>
            <li ><a href="${pathto('sqlkit/tour')}" title="Home" 
                  ><span>Home</span></a></li>

            <li ><a href="${pathto('sqlkit/contents')}"
                  title="Sqlkit - the python package" 
                  ><span>Sqlkit</span></a>

	       <ul>
		 <li ><a href="${pathto('sqlkit/contents')}"
		       title="Sqlkit - the python package" 
		       ><span>Sqlkit</span></a></li>

		 <li ><a href="${pathto('sqlkit/sqlwidget')}" title="Widgets" 
		       ><span>Widgets</span></a>
		       <ul> 
			 <li ><a href="${pathto('sqlkit/mask')}" title="Mask" 
			       ><span>Mask view</span></a></li>
			 <li ><a href="${pathto('sqlkit/table')}" title="Table" 
			       ><span>Table view</span></a></li>
		       </ul>
                 </li>
		 <li ><a href="${pathto('sqlkit/browsing')}" title="Browsing Data" 
		       ><span>Browsing data</span></a>
		    <ul> 
		      <li ><a href="${pathto('sqlkit/constraints')}" title="Constraints" 
			    ><span>Constraints</span></a></li>
		      <li ><a href="${pathto('sqlkit/filters')}" title="Filters" 
			    ><span>Filters</span></a></li>
		      <li ><a href="${pathto('sqlkit/totals')}" title="Totals" 
			    ><span>Totals</span></a></li>
		    </ul>
                 </li>
		 <li ><a href="${pathto('sqlkit/editing')}" title="Editing Data" 
		       ><span>Editing data</span></a>
			 <ul> 
			   <li ><a href="${pathto('sqlkit/completion')}" title="Completion" 
				 ><span>Completion</span></a></li>
			   <li ><a href="${pathto('sqlkit/validation')}" title="Validation" 
				 ><span>Validation</span></a></li>
			   <li ><a href="${pathto('sqlkit/relationship')}" title="Relationships" 
				 ><span>Relationships</span></a></li>
			 </ul>
		       </li>
		 <li ><a href="${pathto('sqlkit/advanced/contents')}" title="Advanced configuration" 
		       ><span>Advanced configuration</span></a>
			 <ul> 
			   <li ><a href="${pathto('sqlkit/advanced/fields')}" title="Fields" 
				 ><span>Fields</span></a></li>
			   <li ><a href="${pathto('sqlkit/advanced/views')}" title="Views" 
				 ><span>Views</span></a></li>
			 </ul>
		       </li>

	       </ul>
            </li>

            <li ><a href="${pathto('misc/sqledit')}"
                  title="Sqledit GUI" 
                  ><span>Sqledit GUI</span></a></li>

            <li ><a href="${pathto('sqlkit/tutorial',)}" title="Tutorial" 
                  ><span>Tutorial</span></a></li>

            <li ><a href="${pathto('layout/contents')}" title="Layout"
                  ><span>Layout</span></a></li>

            <li ><a href="${pathto('misc/contents')}" title="Download" 
                  ><span>Download</span></a>

	       <ul>
		 <li ><a href="${pathto('misc/contents')}"
		       title="Download"
		       ><span>Download</span></a></li>
		 <li ><a href="http://sqlkit.argolinux.org/download/Changelog"  title="Changelog"
		       title="Changelog"
		       ><span>Changelog</span></a></li>
		 <li ><a href="${pathto('misc/backward_incompatibilities')}"
		       title="Backward incompatibilities"
		       ><span>Backward incompatibilities</span></a></li>
	       </ul>
            </li>



        </ul>
</div>
   <div style="clear:left;"></div>
  
</%def>
<br style="clear: left" />
