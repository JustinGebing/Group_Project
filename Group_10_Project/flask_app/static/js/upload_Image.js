var billImage = document.getElementById('file');
billImage.onsubmit = function(e){
        e.preventDefault();
        var form = new FormData(billImage);
        fetch("http://localhost:5000/new/bill", { method :'POST', body : form})
            .then( response => response.json() )
            .then( data => console.log(data) )
    }