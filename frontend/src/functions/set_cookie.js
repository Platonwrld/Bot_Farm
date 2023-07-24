function setCookie(name,value,days) {
    var expires = "";
    if (days) {
        expires = "; max-age=" + 24*60*60*1000;
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
    console.log(document.cookie)
}
export default setCookie