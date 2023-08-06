/*- coding: utf-8
 *
 * Copyright (C) 2010 Roberto Longobardi - seccanj@gmail.com, Marco Cipriani
 */

var selectData = [];
var deselectData = [];
var selectHide = true;
var selectBold = true;
var htimer = null;

function toggleAll(isexpand) {
    var nodes=document.getElementById("ticketContainer").getElementsByTagName("span");
    for(var i=0;i<nodes.length;i++) {
        if (nodes.item(i).getAttribute("name") === "toggable") {
            if (isexpand) {
                expand(nodes.item(i).id);
            } else {
                collapse(nodes.item(i).id);
            }
        }
    }
};

function collapse(id) {
    var el = document.getElementById(id);
    el.firstChild.innerHTML = "+";
    document.getElementById(el.id+"_list").style.display = "none";
};

function expand(id) {
    var el = document.getElementById(id);
    el.firstChild.innerHTML = "-";
    document.getElementById(el.id+"_list").style.display = "";
};

function toggle(id) {
    var el=document.getElementById(id);
    if (el.firstChild.innerHTML == "+") {
        expand(id);
    } else {
        collapse(id);
    }
}

function highlight(string) {
    clearSelection();
    if (string && string !== "") {
        var res=[];
        var tks=string.split(" ");
        for (var i=0;i<tks.length;i++) {
            res[res.length]=new RegExp(regexpescape(tks[i].toLowerCase()), "g");
        }
        var nodes=document.getElementById("ticketContainer").getElementsByTagName("a");
        for(var i=0;i<nodes.length;i++) {
            var n=nodes.item(i);
            if (filterMatch(n,res)) {
                select(n);
            }else{
                deselect(n);
            }
        }
    }
}

function regexpescape(text) {
    return text.replace(/[-[\]{}()+?.,\\\\^$|#\s]/g, "\\\\$&").replace(/\*/g,".*");
}

function filterMatch(node,res) {
    var name=node.innerHTML.toLowerCase();
    var match=true;
    for (var i=0;i<res.length;i++) {
        match=match && name.match(res[i]);
    } 
    return match;
}

function clearSelection() {
    toggleAll(false);
    for (var i=0;i<selectData.length;i++) {
        selectData[i].style.fontWeight="normal";
        selectData[i].style.display="";
    }
    selectData=[];
    for (var i=0;i<deselectData.length;i++) {
        if (selectHide) {
            deselectData[i].style.display="";
        }
    }
    deselectData=[];
}

function select(node) {
    do {
        if (node.tagName ==="UL" && node.id.indexOf("b_") === 0) {
            expand(node.id.substr(0,node.id.indexOf("_list")));
        }
        if(node.tagName === "LI") {
            if (selectBold) {
                node.style.fontWeight = "bold";
            }
            if (selectHide) {
                node.style.display = "block";
            }
            selectData[selectData.length]=node;
        }
        node=node.parentNode;
    } while(node.id!=="ticketContainer");
}

function deselect(node) {
    do {
        if(node.tagName === "LI") {
            if (selectHide && node.style.display==="") {
                node.style.display = "none";
                deselectData[deselectData.length]=node;
            }
        }
        node=node.parentNode;
    } while(node.id!=="ticketContainer");
}

function starthighlight(string,now) {
    if (htimer) {
        clearTimeout(htimer);
    } 
    if (now) {
        highlight(string);
    } else {
        htimer = setTimeout(function() {
                                highlight(string)
                            },500);
    }
}

function checkFilter(now) {
    var f=document.getElementById("filter");
    if (f) {
        starthighlight(f.value,now);
    }
    document.getElementById("ticketContainer").style.display = "";
}

window.onload = function() {
                    checkFilter(true);
                };

