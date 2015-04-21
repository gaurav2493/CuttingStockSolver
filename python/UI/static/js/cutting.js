var counter =1;
function checkWasteSize()
{
	var stockSize =document.getElementById("stockSize").value;
	var wasteSize =document.getElementById("wasteThreshold").value;
	//document.write(stockSize+blockSize);
	if(wasteSize>stockSize)
	{
		alert("Please enter waste size less than or equal to "+ stockSize);
	}
}

function checkBlockSize()
{
	var stockSize =document.getElementById("stockSize").value;
	var blockSize =document.getElementsByName("bsize")[0].value;
	//document.write(stockSize+blockSize);
	if(blockSize>stockSize)
	{
		alert("Please enter block size less than or equal to "+ stockSize);
	}
}

function addMore() {
    var table = document.getElementById("blockTable");
    var row = table.insertRow(table.rows.length);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    cell1.innerHTML = "<input type='number' class='form-control' id='bSize"+counter+ "' width='200' required>";
    cell2.innerHTML = "<input type='number' class='form-control' id='bqty"+counter+" ' width='200' required>";
	counter++;
}

function selectAlgo()
{
	if (document.getElementById('genetic').checked) {
        document.getElementById('stockinput').style.visibility = 'visible';
		document.getElementById('algo').value='genetic';
		//document.write(document.getElementById('algo').value);
    } 
	if (document.getElementById('greedy').checked) {
        document.getElementById('stockinput').style.visibility = 'visible';
		document.getElementById('algo').value='greedy';
		
    }
}

var algo;
var stockSize;
var wasteThreshold;
var data;

function getBlockSizeNumber()
{
	//alert("hello");
	algo = document.querySelector('input[name="algoSelect"]:checked').value;
	stockSize=document.getElementById("stockSize").value;
	wasteThreshold=document.getElementById("wasteThreshold").value;
	var x = document.getElementById("form1");
    data = "{";
    var i;
	//alert("ankit");
	//alert(x);
    for (i = 5; i < x.length-2 ;i++) {
        
		
		if(i%2 !=00)
		{
			if(x.elements[i].value=="")
				break;
			data += x.elements[i].value +":" ;
		}
		else
		{
			data += x.elements[i].value +"," ;
		}
    }
	var json = data.substring(0, data.length-1) + "}";
	alert(json);
	loadXMLDoc();
	return false;
	
}
function loadXMLDoc()
{
var xmlhttp;
if (window.XMLHttpRequest)
  {// code for IE7+, Firefox, Chrome, Opera, Safari
  xmlhttp=new XMLHttpRequest();
  }
else
  {// code for IE6, IE5
  xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
xmlhttp.onreadystatechange=function()
  {
  if (xmlhttp.readyState==4 && xmlhttp.status==200)
    {
    dalert(xmlhttp.responseText);
    }
  }
xmlhttp.open("GET","solution?stocksize="+stockSize+"&waste="+wasteThreshold+"&algo="+algo+"&data="+encodeURI(data),true);
xmlhttp.send();
}



