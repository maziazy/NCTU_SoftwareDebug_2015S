var current_page;

function ChangePage(page) {
	if(typeof current_page != "undefined") {
		document.getElementById('page-' + current_page).style.display = 'none'
		
		if(document.getElementById('li-' + current_page) != null)
			document.getElementById('li-' + current_page).className = ''
	}
	
	current_page = page;
	document.getElementById('page-' + current_page).style.display = 'block'
	if(document.getElementById('li-' + current_page) != null)
		document.getElementById('li-' + current_page).className = 'selected'
}

function Rand(a, b)	{
	return Math.floor(Math.random()*(b-a+1))+a
}

function RandRGB()	{
	var R = Rand(50,225);
	var G = Rand(50,225);
	var B = Rand(50,225);
	
	return {ori: 'rgb('+R+','+G+','+B+')', 
			hover: 'rgb('+(R+30)+','+(G+30)+','+(B+30)+')'};
}

function initial() {
	sorttable.init()
	
	ChangePage('index')
	process()	
}

function log(t) {
	console.log(t)
}

function Halt() {
	document.getElementById('Processing').style.display = 'block'
}

function Resume() {
	document.getElementById('Processing').style.display = 'none'
}

window.onload = initial;

/*-----------*/

function process() {
	//document.getElementsByTagName('table')
}