## coding: utf-8
<%inherit file="layout.mako"/>

<%def name="extrahead()">
    <link rel="stylesheet" href="${pathto('_static/tour.css', 1)}" type="text/css" media="screen" />
    <script type="text/javascript" src="${pathto('_static/preview.js', 1)}"></script>
</%def>

<%def name="prevnextheader()"></%def>


<%def name="sidebar()">

  <div class="sphinxsidebar">
     <div class="sphinxsidebarwrapper">
      <div class="news">

      <h2>Release 0.9 is out</h2>
      
      I'm happy to announce that on September, 8 2010 I released 
      <a href="${pathto('misc/download', )}#download">version 0.9</a> of
	sqlkit that adds a huge quantity of new features and bug fixes (see 
	<a href="/download/Changelog">changelog</a>). This release works
      with sqlalchemy 0.5 and 0.6 that is now a fully supported release.
	
     </div>
     </div>

   </div>
</%def>

${next.body()}
