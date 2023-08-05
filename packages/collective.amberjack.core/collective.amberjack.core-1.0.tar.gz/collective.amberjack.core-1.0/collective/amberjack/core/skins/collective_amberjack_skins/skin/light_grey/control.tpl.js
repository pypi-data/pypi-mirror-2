AmberjackControl.open(
  '<div id="ajControl">'+
    '<div id="ajControlNavi">' +
		      '<div id="ajPlayerCell">' +
/*	  
*        '<a id="ajPrev" class="{prevClass}" href="javascript:;" onclick="this.blur();{prevClick}"><span>{textPrev}</span></a>' + 
*/
        '<span id="ajCount">{currPage} {textOf} {pageCount}</span>' +
		'<a id="ajNext" class="{nextClass}" href="javascript:;" onclick="this.blur();{nextClick}"><span>{textNext}</span></a>' +
		      '</div>' +
		      '<div id="ajCloseCell">' +
		        '<a id="ajClose" href="javascript:;" onclick="Amberjack.close();return false"><span>{textClose}</span></a>' +
		      '</div>' +
          '</div>' +
	'<div class="lightgrey_tl">' +
    '<div class="lightgrey_tr">' +
	  '<div class="lightgrey_bl">' +
	    '<div class="lightgrey_br">' +
    	  '<div id="ajControlBody">{body}</div>' + 
        '</div>' +
	  '</div>' +
	'</div></div>' +
	'<div id="ajControlInfo">Tour powered by <a class="ajFooterLink" href="http://amberjack.org">Amberjack</a> &amp; {skinId} skin</div>' +
  '</div>'
);