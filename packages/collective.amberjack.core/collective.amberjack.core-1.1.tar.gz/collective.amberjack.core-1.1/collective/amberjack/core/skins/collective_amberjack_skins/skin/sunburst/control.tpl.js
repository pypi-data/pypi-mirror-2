AmberjackControl.open(
  '<div id="ajControl">' +  
      '<div id="ajCloseCell" class="close">' +
        '<a id="ajClose" href="javascript:;" onclick="Amberjack.close();return false"><span>{textClose}</span></a>' +
      '</div>' +
      '<div class="pb-ajax">' +
	    '<div id="ajControlNavi">' +
	      '<div id="ajPlayerCell">' +
	/*	  
	*        '<a id="ajPrev" class="{prevClass}" href="javascript:;" onclick="this.blur();{prevClick}"><span>{textPrev}</span></a>' + 
	*/
	        '<span id="ajCount">{currPage} {textOf} {pageCount}</span>' +
			'<a id="ajNext" title="{nextTitle}" class="{nextClass}" href="javascript:;" onclick="this.blur();{nextClick}"><span>{textNext}</span></a>' +
	      '</div>' +
	    '</div>' +
	    '<div id="ajControlBody">{body}</div>' +
	    '<div id="ajControlInfo">Tour powered by <a href="http://amberjack.org">Amberjack</a> &amp; {skinId} skin</div>' +
	'</div>'+
  '</div>'
);