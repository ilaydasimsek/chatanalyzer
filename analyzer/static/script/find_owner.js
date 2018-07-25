function create_form(){
    var f = document.createElement("form");
    f.setAttribute('method',"post");
    f.setAttribute('id',"message");
    f.setAttribute('name',"message" );
    f.onclick = function onclick(event){
        var message_text = String(document.getElementById("message_text").value);
        Cookies.set('message_text',message_text, {path:'/'});
        if(message_text !== ""){
          $.ajax({
            url: findOwnerResult ,
            dataType : 'html',
            timeout : 30000,
            success: function(data){
                $("#result").html("<h3 class = 'w3-lobster' style = 'color:#074954;font-size:35px;'>This message is most probably written by " + data + ".</h3>");
                Cookies.remove('message_text', { path: '/' })
            }

        }
        );}
    };

    var k = document.createElement("input");
    k.setAttribute('type', 'text');
    k.setAttribute('name', "message_");
    k.setAttribute('id', "message_text");
    k.style = "width: 95%;height: 35px;border: 2px solid #064752; border-radius: 4px;background-color:  #ddd;color: black;resize: both;overflow: auto;top:20%;"

    var s = document.createElement("input");
    s.type = "button";
    s.value = "Submit";
    s.className = "btn w3-buttonColor w3-lobster";
    s.setAttribute('id', "button");



    f.appendChild(k);
    f.appendChild(s);

    var inputElem = document.createElement('input');
    inputElem.type = 'hidden';
    inputElem.name = 'csrfmiddlewaretoken';
    inputElem.value = Cookies.get('csrftoken');
    f.appendChild(inputElem);

    $("#form").append(f);
};

