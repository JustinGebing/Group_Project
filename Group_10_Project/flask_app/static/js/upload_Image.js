var billImage = document.getElementById('file');
billImage.onsubmit = function(e){
        e.preventDefault();
        var form = new FormData(billImage);
        var amt = $("#amount").val();
        fetch("http://localhost:5000/new/bill/image", { method :'POST', body : form}, function(result){
                amt.innerHtml(result)})
            .then( response => response.json() )
            .then( data => console.log(data) )
    }