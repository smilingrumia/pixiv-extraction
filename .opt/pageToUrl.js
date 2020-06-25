/*
	How to download all art from artist page, in old order.
	OS: Linux
	Browser: Firefox

	Open artist page in old order
		example:
		https://www.pixiv.net/users/12345678/artworks?p=3
		https://www.pixiv.net/users/12345678/artworks?p=2
		https://www.pixiv.net/users/12345678/artworks

	Create dllist(a new text file)

	F12 -> Console -> copy all this java script -> execute  -> Copy all url and paste in dllist
		example:
		do this on https://www.pixiv.net/users/12345678/artworks?p=3
		this will yield all art url of page3, in old order.
		Select all and copy&paste to dllist(new text file).
		next, do the same thing on page2, page1.

		dllist will look like:
		https://www.pixiv.net/en/artworks/12345678
		https://www.pixiv.net/en/artworks/23456781
		https://www.pixiv.net/en/artworks/34567812
		...

	cat dllist | xargs ./extraction

*/
var arts = new Array();
var artsRaw = document.getElementsByTagName("a");
var cnt = 0
for(var i in artsRaw){
   var url = artsRaw[i].href;
  
   if(url != null)
   if(url.match('artworks\/[0-9]{1,10}$') != null){

    if(cnt > 0){
    	if( arts[cnt-1] != url ){
           arts.push(url);
       	   cnt++;
     	}
    }
     else {
       arts.push(url);
       cnt++;
      }
   }
}

console.log(arts.length + 'arts')
document.body.innerHTML = "";
for(var i = arts.length-1 ; i >= 0 ; i--){
  document.body.innerHTML += arts[i] + '<br>';
}
