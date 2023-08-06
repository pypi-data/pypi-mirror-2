function getElementsByClassName(className, node, tagName) {
    var
    node = node || document,
    tagName=tagName || '*',
    list = node.getElementsByTagName(tagName),
    length = list.length,
    result = [],
    i;
    
    for(i = 0; i < length; i++) {
        if(list[i].className.search(className) != -1) {
	        result.push(list[i]);
	}
    }
    
    return result;
}