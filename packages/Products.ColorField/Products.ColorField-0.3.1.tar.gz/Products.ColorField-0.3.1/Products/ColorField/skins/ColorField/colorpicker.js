function setBg() {
   var c = document.getElementById("cp2_bgcolor").style.backgroundColor;
   document.body.style.backgroundColor = c;
   var tds = document.getElementsByTagName("td");
   for (var i in tds) {
      if (tds[i].style)
         tds[i].style.backgroundColor = c;
   }
   return;
}

function setColorPreview(name, color) {
   color = parseColor(color);
   if (color)
      document.getElementById(name).style.backgroundColor = color;
   else
      color = parseColor(document.getElementById(name).style.backgroundColor);
   if (color.indexOf("#") == 0)
      color = color.substr(1,color.length-1);
   document.getElementById(name).value = color;
}

function parseColor(color) {
   c = color.toLowerCase();
   var colorNames = new Object();
   colorNames["aliceblue"] = true;
   colorNames["antiquewhite"]= true
   colorNames["aqua"] = true;
   colorNames["aquamarine"] = true;
   colorNames["azure"] = true;
   colorNames["beige"] = true;
   colorNames["bisque"] = true;
   colorNames["black"] = true;
   colorNames["blanchedalmond"] = true;
   colorNames["blue"] = true;
   colorNames["blueviolet"] = true;
   colorNames["brown"] = true;
   colorNames["burlywood"] = true;
   colorNames["cadetblue"] = true;
   colorNames["chartreuse"] = true;
   colorNames["chocolate"] = true;
   colorNames["coral"] = true;
   colorNames["cornflowerblue"] = true;
   colorNames["cornsilk"] = true;
   colorNames["crimson"] = true;
   colorNames["cyan"] = true;
   colorNames["darkblue"] = true;
   colorNames["darkcyan"] = true;
   colorNames["darkgoldenrod"] = true;
   colorNames["darkgray"] = true;
   colorNames["darkgreen"] = true;
   colorNames["darkkhaki"] = true;
   colorNames["darkmagenta"] = true;
   colorNames["darkolivegreen"] = true;
   colorNames["darkorange"] = true;
   colorNames["darkorchid"] = true;
   colorNames["darkred"] = true;
   colorNames["darksalmon"] = true;
   colorNames["darkseagreen"] = true;
   colorNames["darkslateblue"] = true;
   colorNames["darkslategray"] = true;
   colorNames["darkturquoise"] = true;
   colorNames["darkviolet"] = true;
   colorNames["deeppink"] = true;
   colorNames["deepskyblue"] = true;
   colorNames["dimgray"] = true;
   colorNames["dodgerblue"] = true;
   colorNames["firebrick"] = true;
   colorNames["floralwhite"] = true;
   colorNames["forestgreen"] = true;
   colorNames["fuchsia"] = true;
   colorNames["gainsboro"] = true;
   colorNames["ghostwhite"] = true;
   colorNames["gold"] = true;
   colorNames["goldenrod"] = true;
   colorNames["gray"] = true;
   colorNames["green"] = true;
   colorNames["greenyellow"] = true;
   colorNames["honeydew"] = true;
   colorNames["hotpink"] = true;
   colorNames["indianred "] = true;
   colorNames["indigo "] = true;
   colorNames["ivory"] = true;
   colorNames["khaki"] = true;
   colorNames["lavender"] = true;
   colorNames["lavenderblush"] = true;
   colorNames["lawngreen"] = true;
   colorNames["lemonchiffon"] = true;
   colorNames["lightblue"] = true;
   colorNames["lightcoral"] = true;
   colorNames["lightcyan"] = true;
   colorNames["lightgoldenrodyellow"] = true;
   colorNames["lightgrey"] = true;
   colorNames["lightgreen"] = true;
   colorNames["lightpink"] = true;
   colorNames["lightsalmon"] = true;
   colorNames["lightseagreen"] = true;
   colorNames["lightskyblue"] = true;
   colorNames["lightslateblue"] = true;
   colorNames["lightslategray"] = true;
   colorNames["lightsteelblue"] = true;
   colorNames["lightyellow"] = true;
   colorNames["lime"] = true;
   colorNames["limegreen"] = true;
   colorNames["linen"] = true;
   colorNames["magenta"] = true;
   colorNames["maroon"] = true;
   colorNames["mediumaquamarine"] = true;
   colorNames["mediumblue"] = true;
   colorNames["mediumorchid"] = true;
   colorNames["mediumpurple"] = true;
   colorNames["mediumseagreen"] = true;
   colorNames["mediumslateblue"] = true;
   colorNames["mediumspringgreen"] = true;
   colorNames["mediumturquoise"] = true;
   colorNames["mediumvioletred"] = true;
   colorNames["midnightblue"] = true;
   colorNames["mintcream"] = true;
   colorNames["mistyrose"] = true;
   colorNames["moccasin"] = true;
   colorNames["navajowhite"] = true;
   colorNames["navy"] = true;
   colorNames["oldlace"] = true;
   colorNames["olive"] = true;
   colorNames["olivedrab"] = true;
   colorNames["orange"] = true;
   colorNames["orangered"] = true;
   colorNames["orchid"] = true;
   colorNames["palegoldenrod"] = true;
   colorNames["palegreen"] = true;
   colorNames["paleturquoise"] = true;
   colorNames["palevioletred"] = true;
   colorNames["papayawhip"] = true;
   colorNames["peachpuff"] = true;
   colorNames["peru"] = true;
   colorNames["pink"] = true;
   colorNames["plum"] = true;
   colorNames["powderblue"] = true;
   colorNames["purple"] = true;
   colorNames["red"] = true;
   colorNames["rosybrown"] = true;
   colorNames["royalblue"] = true;
   colorNames["saddlebrown"] = true;
   colorNames["salmon"] = true;
   colorNames["sandybrown"] = true;
   colorNames["seagreen"] = true;
   colorNames["seashell"] = true;
   colorNames["sienna"] = true;
   colorNames["silver"] = true;
   colorNames["skyblue"] = true;
   colorNames["slateblue"] = true;
   colorNames["slategray"] = true;
   colorNames["snow"] = true;
   colorNames["springgreen"] = true;
   colorNames["steelblue"] = true;
   colorNames["tan"] = true;
   colorNames["teal"] = true;
   colorNames["thistle"] = true;
   colorNames["tomato"] = true;
   colorNames["turquoise"] = true;
   colorNames["violet"] = true;
   colorNames["violetred"] = true;
   colorNames["wheat"] = true;
   colorNames["white"] = true;
   colorNames["whitesmoke"] = true;
   colorNames["yellow"] = true;
   colorNames["yellowgreen"] = true;

   if (colorNames[c])
      return(c);

   var rgb = new RegExp("rgb ?\\( ?([0-9^,]*), ?([0-9^,]*), ?([0-9^ \\)]*) ?\\)");
   var result = color.match(rgb);
   if (result) {
      var R = parseInt(result[1]).toString(16);
      var G = parseInt(result[2]).toString(16);
      var B = parseInt(result[3]).toString(16);
      if (R.length == 1) R="0"+R;
      if (G.length == 1) G="0"+G;
      if (B.length == 1) B="0"+B;
      return("#"+R+G+B);
   }
   if (c.indexOf("#") == 0)
      c = c.substr(1,c.length-1);
   if (c.length == 6) {
      var nonhex = new RegExp("[^0-9,a-f]");
      nonhex.ignoreCase = true;
      var found = c.match(nonhex);
      if (!found)
         return("#" + c);
   }
   return(null);
}

var brightness = new Array();
brightness[0] = new Array("000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000");
brightness[1] = new Array("151515","151313","151212","151010","150e0e","150c0c","150b0b","150909","150707","150505","150404","150202","150000","151515","151413","151312","151310","15120e","15110c","15100b","150f09","150e07","150d05","150c04","150c02","150b00","151515","151513","151512","151510","15150e","15150c","15150b","151509","151507","151505","151504","151502","151500","151515","141513","131512","131510","12150e","11150c","10150b","0f1509","0e1507","0d1505","0c1504","0c1502","0b1500","151515","131513","121512","101510","0e150e","0c150c","0b150b","091509","071507","051505","041504","021502","001500","151515","131514","121513","101513","0e1512","0c1511","0b1510","09150f","07150e","05150d","04150c","02150c","00150b","151515","131515","121515","101515","0e1515","0c1515","0b1515","091515","071515","051515","041515","021515","001515","151515","131415","121315","101315","0e1215","0c1115","0b1015","090f15","070e15","050d15","040c15","020c15","000b15","151515","131315","121215","101015","0e0e15","0c0c15","0b0b15","090915","070715","050515","040415","020215","000015","151515","141315","131215","131015","120e15","110c15","100b15","0f0915","0e0715","0d0515","0c0415","0c0215","0b0015","151515","151315","151215","151015","150e15","150c15","150b15","150915","150715","150515","150415","150215","150015","151515","151314","151213","151013","150e12","150c11","150b10","15090f","15070e","15050d","15040c","15020c","15000b","151515","151313","151212","151010","150e0e","150c0c","150b0b","150909","150707","150505","150404","150202","150000");
brightness[2] = new Array("2b2b2b","2b2727","2b2323","2b2020","2b1c1c","2b1919","2b1515","2b1212","2b0e0e","2b0b0b","2b0707","2b0404","2b0000","2b2b2b","2b2927","2b2723","2b2520","2b231c","2b2219","2b2015","2b1e12","2b1c0e","2b1b0b","2b1907","2b1704","2b1500","2b2b2b","2a2b27","2b2b23","2b2b20","2b2b1c","2a2b19","2b2b15","2b2b12","2a2b0e","2b2b0b","2b2b07","2b2b04","2b2b00","2b2b2b","292b27","272b23","252b20","232b1c","222b19","202b15","1e2b12","1c2b0e","1b2b0b","192b07","172b04","152b00","2b2b2b","272b27","232b23","202b20","1c2b1c","192b19","152b15","122b12","0e2b0e","0b2b0b","072b07","042b04","002b00","2b2b2b","272b29","232b27","202b25","1c2b23","192b22","152b20","122b1e","0e2b1c","0b2b1b","072b19","042b17","002b15","2b2b2b","272b2a","232b2a","202b2b","1c2b2b","192b2a","152b2a","122b2a","0e2b2a","0b2b2a","072b2a","042b2a","002b2a","2b2b2b","27292b","23272b","20252b","1c232b","19222b","15202b","121e2b","0e1c2b","0b1b2b","07192b","04172b","00152b","2b2b2b","27272b","23232b","20202b","1c1c2b","19192b","15152b","12122b","0e0e2b","0b0b2b","07072b","04042b","00002b","2b2b2b","29272b","27232b","25202b","231c2b","22192b","20152b","1e122b","1c0e2b","1b0b2b","19072b","17042b","15002b","2b2b2b","2b272a","2b232b","2b202b","2b1c2b","2b192a","2b152b","2b122b","2b0e2a","2b0b2b","2b072b","2b042b","2b002b","2b2b2b","2b2729","2b2327","2b2025","2b1c23","2b1922","2b1520","2b121e","2b0e1c","2b0b1b","2b0719","2b0417","2b0015","2b2b2b","2b2727","2b2323","2b2020","2b1c1c","2b1919","2b1515","2b1212","2b0e0e","2b0b0b","2b0707","2b0404","2b0000");
brightness[3] = new Array("404040","403a3a","403535","403030","402b2b","402525","402020","401b1b","401515","401010","400b0b","400505","400000","404040","403d3a","403a35","403830","40352b","403225","403020","402d1b","402b15","402810","40250b","402305","402000","404040","40403a","404035","404030","40402b","404025","404020","40401b","404015","404010","40400b","404005","404000","404040","3d403a","3a4035","384030","35402b","324025","304020","2d401b","2b4015","284010","25400b","234005","204000","404040","3a403a","354035","304030","2b402b","254025","204020","1b401b","154015","104010","0b400b","054005","004000","404040","3a403d","35403a","304038","2b4035","254032","204030","1b402d","15402b","104028","0b4025","054023","004020","404040","3a4040","354040","304040","2b4040","254040","204040","1b4040","154040","104040","0b4040","054040","004040","404040","3a3d40","353a40","303840","2b3540","253240","203040","1b2d40","152b40","102840","0b2540","052340","002040","404040","3a3a40","353540","303040","2b2b40","252540","202040","1b1b40","151540","101040","0b0b40","050540","000040","404040","3d3a40","3a3540","383040","352b40","322540","302040","2d1b40","2b1540","281040","250b40","230540","200040","404040","403a40","403540","403040","402b40","402540","402040","401b40","401540","401040","400b40","400540","400040","404040","403a3d","40353a","403038","402b35","402532","402030","401b2d","40152a","401028","400b25","400523","400020","404040","403a3a","403535","403030","402b2b","402525","402020","401b1b","401515","401010","400b0b","400505","400000");
brightness[4] = new Array("555555","554e4e","554747","554040","553939","553232","552b2b","552323","551c1c","551515","550e0e","550707","550000","555555","55514e","554e47","554a40","554739","554332","55402b","553c23","55391c","553515","55320e","552e07","552b00","555555","55554e","555547","555540","555539","555532","55552b","555523","55551c","555515","55550e","555507","555500","555555","51554e","4e5547","4a5540","475539","435532","40552b","3c5523","39551c","355515","32550e","2e5507","2b5500","555555","4e554e","475547","405540","395539","325532","2b552b","235523","1c551c","155515","0e550e","075507","005500","555555","4e5551","47554e","40554a","395547","325543","2b5540","23553c","1c5539","155535","0e5532","07552e","00552b","555555","4e5555","475555","405555","395555","325555","2b5555","235555","1c5555","155555","0e5555","075555","005555","555555","4e5155","474e55","404a55","394755","324355","2b4055","233c55","1c3955","153555","0e3255","072e55","002b55","555555","4e4e55","474755","404055","393955","323255","2b2b55","232355","1c1c55","151555","0e0e55","070755","000055","555555","514e55","4e4755","4a4055","473955","433255","402b55","3c2355","391c55","351555","320e55","2e0755","2b0055","555555","554e55","554755","554055","553955","553255","552b55","552355","551c55","551555","550e55","550755","550055","555555","554e51","55474e","55404a","553947","553243","552b40","55233c","551c39","551535","550e32","55072e","55002a","555555","554e4e","554747","554040","553939","553232","552b2b","552323","551c1c","551515","550e0e","550707","550000");
brightness[5] = new Array("6a6a6a","6a6161","6a5959","6a5050","6a4747","6a3e3e","6a3535","6a2c2c","6a2323","6a1b1b","6a1212","6a0909","6a0000","6a6a6a","6a6661","6a6159","6a5d50","6a5947","6a543e","6a5035","6a4b2c","6a4723","6a421b","6a3e12","6a3a09","6a3500","6a6a6a","6a6a61","6a6a59","6a6a50","6a6a47","6a6a3e","6a6a35","6a6a2c","6a6a23","6a6a1b","6a6a12","6a6a09","6a6a00","6a6a6a","666a61","616a59","5d6a50","596a47","546a3e","506a35","4b6a2c","476a23","426a1b","3e6a12","3a6a09","356a00","6a6a6a","616a61","596a59","506a50","476a47","3e6a3e","356a35","2c6a2c","236a23","1b6a1b","126a12","096a09","006a00","6a6a6a","616a66","596a61","506a5d","476a59","3e6a54","356a50","2c6a4b","236a47","1b6a42","126a3e","096a3a","006a35","6a6a6a","616a6a","596a6a","506a6a","476a6a","3e6a6a","356a6a","2c6a6a","236a6a","1b6a6a","126a6a","096a6a","006a6a","6a6a6a","61666a","59616a","505d6a","47596a","3e546a","35506a","2c4b6a","23476a","1b426a","123e6a","093a6a","00356a","6a6a6a","61616a","59596a","50506a","47476a","3e3e6a","35356a","2c2c6a","23236a","1b1b6a","12126a","09096a","00006a","6a6a6a","66616a","61596a","5d506a","59476a","543e6a","50356a","4b2c6a","47236a","421b6a","3e126a","3a096a","35006a","6a6a6a","6a616a","6a596a","6a506a","6a476a","6a3e6a","6a356a","6a2c6a","6a236a","6a1b6a","6a126a","6a096a","6a006a","6a6a6a","6a6166","6a5961","6a505d","6a4759","6a3e54","6a3550","6a2c4b","6a2347","6a1b42","6a123e","6a093a","6a0035","6a6a6a","6a6161","6a5959","6a5050","6a4747","6a3e3e","6a3535","6a2c2c","6a2323","6a1b1b","6a1212","6a0909","6a0000");
brightness[6] = new Array("7f7f7f","7f7575","7f6a6a","7f6060","7f5555","7f4a4a","7f4040","7f3535","7f2b2b","7f2020","7f1515","7f0b0b","7f0000","7f7f7f","7f7a75","7f756a","7f7060","7f6a55","7f654a","7f6040","7f5a35","7f552b","7f5020","7f4a15","7f450b","7f4000","7f7f7f","7f7f75","7f7f6a","7f7f60","7f7f55","7f7f4a","7f7f40","7f7f35","7f7f2b","7f7f20","7f7f15","7f7f0b","7f7f00","7f7f7f","7a7f75","757f6a","707f60","6a7f55","657f4a","607f40","5a7f35","557f2b","507f20","4a7f15","457f0b","407f00","7f7f7f","757f75","6a7f6a","607f60","557f55","4a7f4a","407f40","357f35","2b7f2b","207f20","157f15","0b7f0b","007f00","7f7f7f","757f7a","6a7f75","607f70","557f6a","4a7f65","407f60","357f5a","2b7f55","207f50","157f4a","0b7f45","007f40","7f7f7f","757f7f","6a7f7f","607f7f","557f7f","4a7f7f","407f7f","357f7f","2b7f7f","207f7f","157f7f","0b7f7f","007f7f","7f7f7f","757a7f","6a757f","60707f","556a7f","4a657f","40607f","355a7f","2b557f","20507f","154a7f","0b457f","00407f","7f7f7f","75757f","6a6a7f","60607f","55557f","4a4a7f","40407f","35357f","2b2b7f","20207f","15157f","0b0b7f","00007f","7f7f7f","7a757f","756a7f","70607f","6a557f","654a7f","60407f","5a357f","552b7f","50207f","4a157f","450b7f","40007f","7f7f7f","7f757f","7f6a7f","7f607f","7f557f","7f4a7f","7f407f","7f357f","7f2b7f","7f207f","7f157f","7f0b7f","7f007f","7f7f7f","7f757a","7f6a75","7f6070","7f556a","7f4a65","7f4060","7f355a","7f2b55","7f2050","7f154a","7f0b45","7f0040","7f7f7f","7f7575","7f6a6a","7f6060","7f5555","7f4a4a","7f4040","7f3535","7f2b2b","7f2020","7f1515","7f0b0b","7f0000");
brightness[7] = new Array("959595","958888","957c7c","957070","956363","955757","954a4a","953e3e","953232","952525","951919","950c0c","950000","959595","958f88","95887c","958270","957c63","957657","95704a","95693e","956332","955d25","955719","95510c","954a00","959595","959588","95957c","959570","959563","959557","95954a","95953e","959532","959525","959519","95950c","959500","959595","8f9588","88957c","829570","7c9563","769557","70954a","69953e","639532","5d9525","579519","51950c","4a9500","959595","889588","7c957c","709570","639563","579557","4a954a","3e953e","329532","259525","199519","0c950c","009500","959595","88958f","7c9588","709582","63957c","579576","4a9570","3e9569","329563","25955d","199557","0c9551","00954a","959595","889595","7c9595","709595","639595","579595","4a9595","3e9595","329595","259595","199595","0c9595","009595","959595","888f95","7c8895","708295","637c95","577695","4a7095","3e6995","326395","255d95","195795","0c5195","004a95","959595","888895","7c7c95","707095","636395","575795","4a4a95","3e3e95","323295","252595","191995","0c0c95","000095","959595","8f8895","887c95","827095","7c6395","765795","704a95","693e95","633295","5d2595","571995","510c95","4a0095","959595","958895","957c95","957095","956395","955795","954a95","953e95","953295","952595","951995","950c95","950095","959595","95888f","957c88","957082","95637c","955776","954a70","953e69","953263","95255d","951957","950c51","95004a","959595","958888","957c7c","957070","956363","955757","954a4a","953e3e","953232","952525","951919","950c0c","950000");
brightness[8] = new Array("aaaaaa","aa9c9c","aa8e8e","aa8080","aa7171","aa6363","aa5555","aa4747","aa3939","aa2b2b","aa1c1c","aa0e0e","aa0000","aaaaaa","aaa39c","aa9c8e","aa9580","aa8e71","aa8763","aa8055","aa7847","aa7139","aa6a2b","aa631c","aa5c0e","aa5500","aaaaaa","aaaa9c","aaaa8e","aaaa80","aaaa71","aaaa63","aaaa55","aaaa47","aaaa39","aaaa2b","aaaa1c","aaaa0e","aaaa00","aaaaaa","a3aa9c","9caa8e","95aa80","8eaa71","87aa63","80aa55","78aa47","71aa39","6aaa2b","63aa1c","5caa0e","55aa00","aaaaaa","9caa9c","8eaa8e","80aa80","71aa71","63aa63","55aa55","47aa47","39aa39","2baa2b","1caa1c","0eaa0e","00aa00","aaaaaa","9caaa3","8eaa9c","80aa95","71aa8e","63aa87","55aa80","47aa78","39aa71","2baa6a","1caa63","0eaa5c","00aa55","aaaaaa","9caaaa","8eaaaa","80aaaa","71aaaa","63aaaa","55aaaa","47aaaa","39aaaa","2baaaa","1caaaa","0eaaaa","00aaaa","aaaaaa","9ca3aa","8e9caa","8095aa","718eaa","6387aa","5580aa","4778aa","3971aa","2b6aaa","1c63aa","0e5caa","0055aa","aaaaaa","9c9caa","8e8eaa","8080aa","7171aa","6363aa","5555aa","4747aa","3939aa","2b2baa","1c1caa","0e0eaa","0000aa","aaaaaa","a39caa","9c8eaa","9580aa","8e71aa","8763aa","8055aa","7847aa","7139aa","6a2baa","631caa","5c0eaa","5500aa","aaaaaa","aa9caa","aa8eaa","aa80aa","aa71aa","aa63aa","aa55aa","aa47aa","aa39aa","aa2baa","aa1caa","aa0eaa","aa00aa","aaaaaa","aa9ca3","aa8e9c","aa8095","aa718e","aa6387","aa557f","aa4778","aa3971","aa2b6a","aa1c63","aa0e5c","aa0055","aaaaaa","aa9c9c","aa8e8e","aa8080","aa7171","aa6363","aa5555","aa4747","aa3939","aa2b2b","aa1c1c","aa0e0e","aa0000");
brightness[9] = new Array("bfbfbf","bfafaf","bf9f9f","bf8f8f","bf8080","bf7070","bf6060","bf5050","bf4040","bf3030","bf2020","bf1010","bf0000","bfbfbf","bfb7af","bfaf9f","bfa78f","bf9f80","bf9770","bf8f60","bf8750","bf8040","bf7830","bf7020","bf6810","bf6000","bfbfbf","bfbfaf","bfbf9f","bfbf8f","bfbf80","bfbf70","bfbf60","bfbf50","bfbf40","bfbf30","bfbf20","bfbf10","bfbf00","bfbfbf","b7bfaf","afbf9f","a7bf8f","9fbf80","97bf70","8fbf60","87bf50","80bf40","78bf30","70bf20","68bf10","60bf00","bfbfbf","afbfaf","9fbf9f","8fbf8f","80bf80","70bf70","60bf60","50bf50","40bf40","30bf30","20bf20","10bf10","00bf00","bfbfbf","afbfb7","9fbfaf","8fbfa7","80bf9f","70bf97","60bf8f","50bf87","40bf80","30bf78","20bf70","10bf68","00bf60","bfbfbf","afbfbf","9fbfbf","8fbfbf","80bfbf","70bfbf","60bfbf","50bfbf","40bfbf","30bfbf","20bfbf","10bfbf","00bfbf","bfbfbf","afb7bf","9fafbf","8fa7bf","809fbf","7097bf","608fbf","5087bf","4080bf","3078bf","2070bf","1068bf","0060bf","bfbfbf","afafbf","9f9fbf","8f8fbf","8080bf","7070bf","6060bf","5050bf","4040bf","3030bf","2020bf","1010bf","0000bf","bfbfbf","b7afbf","af9fbf","a78fbf","9f80bf","9770bf","8f60bf","8750bf","8040bf","7830bf","7020bf","6810bf","6000bf","bfbfbf","bfafbf","bf9fbf","bf8fbf","bf80bf","bf70bf","bf60bf","bf50bf","bf40bf","bf30bf","bf20bf","bf10bf","bf00bf","bfbfbf","bfafb7","bf9faf","bf8fa7","bf809f","bf7097","bf608f","bf5087","bf407f","bf3078","bf2070","bf1068","bf0060","bfbfbf","bfafaf","bf9f9f","bf8f8f","bf8080","bf7070","bf6060","bf5050","bf4040","bf3030","bf2020","bf1010","bf0000");
brightness[10] = new Array("d5d5d5","d5c3c3","d5b1b1","d59f9f","d58e8e","d57c7c","d56a6a","d55959","d54747","d53535","d52323","d51212","d50000","d5d5d5","d5ccc3","d5c3b1","d5ba9f","d5b18e","d5a87c","d59f6a","d59759","d58e47","d58535","d57c23","d57312","d56a00","d5d5d5","d4d5c3","d5d5b1","d5d59f","d5d58e","d4d57c","d5d56a","d5d559","d4d547","d5d535","d5d523","d5d512","d5d500","d5d5d5","ccd5c3","c3d5b1","bad59f","b1d58e","a8d57c","9fd56a","97d559","8ed547","85d535","7cd523","73d512","6ad500","d5d5d5","c3d5c3","b1d5b1","9fd59f","8ed58e","7cd57c","6ad56a","59d559","47d547","35d535","23d523","12d512","00d500","d5d5d5","c3d5cc","b1d5c3","9fd5ba","8ed5b1","7cd5a8","6ad59f","59d597","47d58e","35d585","23d57c","12d573","00d56a","d5d5d5","c3d5d4","b1d5d4","9fd5d5","8ed5d5","7cd5d4","6ad5d4","59d5d4","47d5d4","35d5d4","23d5d4","12d5d4","00d5d4","d5d5d5","c3ccd5","b1c3d5","9fbad5","8eb1d5","7ca8d5","6a9fd5","5997d5","478ed5","3585d5","237cd5","1273d5","006ad5","d5d5d5","c3c3d5","b1b1d5","9f9fd5","8e8ed5","7c7cd5","6a6ad5","5959d5","4747d5","3535d5","2323d5","1212d5","0000d5","d5d5d5","ccc3d5","c3b1d5","ba9fd5","b18ed5","a87cd5","9f6ad5","9759d5","8e47d5","8535d5","7c23d5","7312d5","6a00d5","d5d5d5","d5c3d4","d5b1d5","d59fd5","d58ed5","d57cd4","d56ad5","d559d5","d547d4","d535d5","d523d5","d512d5","d500d5","d5d5d5","d5c3cc","d5b1c3","d59fba","d58eb1","d57ca8","d56a9f","d55997","d5478e","d53585","d5237c","d51273","d5006a","d5d5d5","d5c3c3","d5b1b1","d59f9f","d58e8e","d57c7c","d56a6a","d55959","d54747","d53535","d52323","d51212","d50000");
brightness[11] = new Array("eaeaea","ead6d6","eac3c3","eaafaf","ea9c9c","ea8888","ea7575","ea6161","ea4e4e","ea3a3a","ea2727","ea1313","ea0000","eaeaea","eae0d6","ead6c3","eacdaf","eac39c","eab988","eaaf75","eaa661","ea9c4e","ea923a","ea8827","ea7f13","ea7500","eaeaea","eaead6","eaeac3","eaeaaf","eaea9c","eaea88","eaea75","eaea61","eaea4e","eaea3a","eaea27","eaea13","eaea00","eaeaea","e0ead6","d6eac3","cdeaaf","c3ea9c","b9ea88","afea75","a6ea61","9cea4e","92ea3a","88ea27","7fea13","75ea00","eaeaea","d6ead6","c3eac3","afeaaf","9cea9c","88ea88","75ea75","61ea61","4eea4e","3aea3a","27ea27","13ea13","00ea00","eaeaea","d6eae0","c3ead6","afeacd","9ceac3","88eab9","75eaaf","61eaa6","4eea9c","3aea92","27ea88","13ea7f","00ea75","eaeaea","d6eaea","c3eaea","afeaea","9ceaea","88eaea","75eaea","61eaea","4eeaea","3aeaea","27eaea","13eaea","00eaea","eaeaea","d6e0ea","c3d6ea","afcdea","9cc3ea","88b9ea","75afea","61a6ea","4e9cea","3a92ea","2788ea","137fea","0075ea","eaeaea","d6d6ea","c3c3ea","afafea","9c9cea","8888ea","7575ea","6161ea","4e4eea","3a3aea","2727ea","1313ea","0000ea","eaeaea","e0d6ea","d6c3ea","cdafea","c39cea","b988ea","af75ea","a661ea","9c4eea","923aea","8827ea","7f13ea","7500ea","eaeaea","ead6ea","eac3ea","eaafea","ea9cea","ea88ea","ea75ea","ea61ea","ea4eea","ea3aea","ea27ea","ea13ea","ea00ea","eaeaea","ead6e0","eac3d6","eaafcd","ea9cc3","ea88b9","ea75af","ea61a6","ea4e9c","ea3a92","ea2788","ea137f","ea0075","eaeaea","ead6d6","eac3c3","eaafaf","ea9c9c","ea8888","ea7575","ea6161","ea4e4e","ea3a3a","ea2727","ea1313","ea0000");
brightness[12] = new Array("ffffff","ffeaea","ffd5d5","ffbfbf","ffaaaa","ff9595","ff8080","ff6a6a","ff5555","ff4040","ff2a2a","ff1515","ff0000","ffffff","fff4ea","ffead5","ffdfbf","ffd5aa","ffca95","ffbf80","ffb56a","ffaa55","ff9f40","ff952a","ff8a15","ff8000","ffffff","ffffea","ffffd5","ffffbf","ffffaa","ffff95","ffff80","ffff6a","ffff55","ffff40","ffff2a","ffff15","ffff00","ffffff","f4ffea","eaffd5","dfffbf","d5ffaa","caff95","bfff80","b5ff6a","aaff55","9fff40","95ff2a","8aff15","80ff00","ffffff","eaffea","d5ffd5","bfffbf","aaffaa","95ff95","80ff80","6aff6a","55ff55","40ff40","2aff2a","15ff15","00ff00","ffffff","eafff4","d5ffea","bfffdf","aaffd4","95ffca","80ffbf","6affb5","55ffaa","40ff9f","2aff95","15ff8a","00ff80","ffffff","eaffff","d5ffff","bfffff","aaffff","95ffff","80ffff","6affff","55ffff","40ffff","2affff","15ffff","00ffff","ffffff","eaf4ff","d5eaff","bfdfff","aad5ff","95caff","80bfff","6ab5ff","55aaff","409fff","2a95ff","158aff","0080ff","ffffff","eaeaff","d5d5ff","bfbfff","aaaaff","9595ff","8080ff","6a6aff","5555ff","4040ff","2a2aff","1515ff","0000ff","ffffff","f4eaff","ead5ff","dfbfff","d5aaff","ca95ff","bf80ff","b56aff","aa55ff","9f40ff","952aff","8a15ff","8000ff","ffffff","ffeaff","ffd5ff","ffbfff","ffaaff","ff95ff","ff80ff","ff6aff","ff55ff","ff40ff","ff2aff","ff15ff","ff00ff","ffffff","ffeaf4","ffd5ea","ffbfdf","ffaad4","ff95ca","ff80bf","ff6ab5","ff55aa","ff409f","ff2a95","ff158a","ff007f","ffffff","ffeaea","ffd5d5","ffbfbf","ffaaaa","ff9595","ff8080","ff6a6a","ff5555","ff4040","ff2a2b","ff1515","ff0000");

var squareSize = 15;
var defaultPalette = brightness[brightness.length-1];
var colorPalette, selectedColor;
var lastMarquee, lastMarquee2;

var pixel = new Image();
pixel.src = "pixel.gif";

var marquee = new Image();
marquee.src = "marquee.gif";

function setMarquee(obj) {
   if (lastMarquee)
      lastMarquee.src = pixel.src;
   obj.src = marquee.src;
   lastMarquee = obj;
   return;
}

function setMarquee2(obj) {
   if (lastMarquee2)
      lastMarquee2.src = pixel.src;
   obj.src = marquee.src;
   lastMarquee2 = obj;
   return;
}

function displayColorValue(obj) {
   var col = obj.style.backgroundColor;
   var rgb = new RegExp("rgb ?\\( ?([0-9^,]*), ?([0-9^,]*), ?([0-9^ \\)]*) ?\\)");
   var result = col.match(rgb);
   if (result) {
      var R = parseInt(result[1]).toString(16);
      var G = parseInt(result[2]).toString(16);
      var B = parseInt(result[3]).toString(16);
      if (R.length == 1) R="0"+R;
      if (G.length == 1) G="0"+G;
      if (B.length == 1) B="0"+B;
      col = R+G+B;
   }
   else if (col.indexOf("#") == 0)
      col = col.substring(1, col.length);
   document.getElementById("display").value = col.toUpperCase();
   return;
}

function displayColorset(obj, idx) {
   if (obj)
      setMarquee(obj);
   for (var i=0; i < brightness.length; i++)
      document.getElementById("bright"+i).style.backgroundColor = "#"+brightness[i][idx];
   return;
}

function displayColor(obj) {
   displayColorValue(obj);
   var col = obj.style.backgroundColor;
   document.getElementById("result").value = col;
   document.getElementsByTagName("body")[0].style.backgroundColor = col.toUpperCase();
   return;
}

function updatePalette(obj, p) {
   displayColor(obj);
   var palette = brightness[p];
   if (!colorPalette) {
      colorPalette = new Array();
      for (var i=0; i < palette.length; i++)
         colorPalette[i] = document.getElementById("color"+i);
   }
   for (var i=0; i < palette.length; i++)
      colorPalette[i].style.backgroundColor = "#"+palette[i];
   selectedColor = obj;
   return;
}

function cp_submit(name) {
   var col = document.getElementById("result").value;
   if (self.opener && col) {
      col = parseColor(col);
      var cValue = col
      var element=window.opener.document.getElementsByName(name);
      element[0].value = cValue.toUpperCase();
      var element=window.opener.document.getElementsByName('preview'+name);	
      element[0].style.backgroundColor = cValue.toUpperCase();     
   }
   self.close();
   cp_cancel();
   return;
}

function cp_cancel() {
   self.close();
   return;
}

