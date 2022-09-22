var billImage = document.getElementById('file');
billImage.onsubmit = function(e){
        e.preventDefault();
        var form = new FormData(billImage);
        fetch("http://localhost:5000/new/bill", { method :'POST', body : form})
            .then( response => response.json() )
            .then( data => console.log(data) )
    }
    $(document).ready(function(){
        $("input").keyup(function(){
                var img = $("#file").val();
                var amount = $("input").val();
                $.post("http://localhost:5000/new/bill/img",img,function(result){
                        $("#amount").val(result);})
                })
        })