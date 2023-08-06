function getMouseX(e) {
   return e.pageX
                  || ( e.clientX + ( document.documentElement.scrollLeft
                  || document.body.scrollLeft ) );
}

function getMouseY(e) {
    return e.pageY
                  || ( e.clientY + ( document.documentElement.scrollTop
                  || document.body.scrollTop ) );
}
