/********************************************************
 * Bibliographica Wikipedia Gadget
 * meant for interaction and information exchange between 
 * Bibliographica.org and Wikipedia 
 *
 *
 * - to install you need to be a registered user of the wikipedia project.
 *  
 * - go to http://en.wikipedia.org/wiki/Special:MyPage/vector.js and write:
 *
 *	  importScriptURI('https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.9/jquery-ui.js')
 *	  importScript('User:Acracia/wp-bibliographica.js');
 *
 *   
 *   - if you are a member of another language wikipedia, 
 *   		you can still link to this file: 
 *   	
 *	  importScriptURI('https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.9/jquery-ui.js')
 *   	importScriptURI('http://en.wikipedia.org/wiki/User:Acracia/wp-bibliographica.js');
 *
 *   	(notice the URI!!)
 *
 * - You need to reload the cache of the page for the changes to take effect: 
 * 	usually Ctrl+Shift+R will do.
 * - For an example, visit http://en.wikipedia.org/wiki/Charles_Dickens
 *   In the left sidebar there should be a box with links to the 
 *   bibliographica.org records present in both Bibliographica and 
 *   the article.
 *
 *
 *   OKFN - http://okfn.org http://bibliographica.org
 *
 ******************************************************/


function getdata (ISBN, parentnode) {
  // gets data about ISBNs metioned in references from Bibliographica 

  var parentself = parentnode 

  $.getJSON('http://bibliographica.org/isbn/'+ISBN, function(data) {
    if ((data[0] != undefined) && (data[0]['title'] != '' ) && (data != null )) {
      // if we have the record in bibliographica, 
      // create a tooltip with information about the book
      parentself.css('border', 'dotted 1px blue');        
      var contributors = [];
      $.each(data[0].contributors, function(key, val) {
        contributors.push(val.name);
      });
      var tooltiptext = 'by <em>'+ contributors.join(', ')+
          '</em><br> Publisher: '+ data[0].publisher.name +
          '<br>';
      if (data[0].description != undefined ){
        tooltiptext = tooltiptext + data[0].description;
      }
        tooltiptext = tooltiptext +'\n<p><small>information retrieved from '+
        '\n<a href="'+ data[0].uri +'">bibliographica.org</a></small></p>';

      var $dialog = $('<div></div>').html(tooltiptext).dialog({
          autoOpen: false,
          modal: false,
          hide: "fold",
          position: ['bottom','left'],
          width: 400,
          title: data[0].title +' ('+ data[0].issued.split("-")[0] +')',

        });
      $dialog.hover(function() {
        $dialog.dialog('open');
      },  function() {
        // no need of closing 
      });

    parentself.hover(function() {
        //this is the function to call the tooltip on hover
        $dialog.dialog('open');
      }, function() {
      //  also possible to make it close 
      //  automatically after 4 seconds 
      //  uncommenting the next 3 lines:
      //setTimeout(function() {
        //$dialog.dialog('close'); 
        //}, 4000 );

      });

    }  else {
      // here we should send info about the book, new for bibliographica
    };
  
  });
};

  

function scrapingisbn () {
  
  // to find all the ISBNs in the page once it has loaded 
  // (there are two different kinds of links:

  $('a.mw-magiclink-isbn').each(function () {
    var ISBN = $(this).text().split(' ')[1] ; //scraping the ISBN number
    // gets the info from http://bibliographica.org/isbn	
    getdata (ISBN, $(this));

  });
  $('a[title*="Special\\:BookSources"]').each(function () {
    // another type of ISBN link (cite format)
    var ISBN = $(this).text() ; //scraping the ISBN number
    // gets the info from http://bibliographica.org/isbn/<number>
    getdata (ISBN, $(this));
    
  });
  

};

$(document).ready(function($) {
  scrapingisbn();

 });

