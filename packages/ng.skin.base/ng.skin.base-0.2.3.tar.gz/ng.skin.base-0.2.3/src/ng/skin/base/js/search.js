function clear_field(obj, value) {
    if(obj.value == value) {
        obj.value = '';
    }
}

function restore_field(obj, value) {
   if(obj.value == '') {
       obj.value = value;
   }
}
