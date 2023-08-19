function redirect() {
    console.log("Redirect function called");
    var text = document.getElementById('text').value;
    var url = "/search/" + text;
    window.location.assign(url);
    console.log("clicked");
}