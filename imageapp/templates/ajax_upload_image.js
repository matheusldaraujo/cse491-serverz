$has_image = $("#has_image");
$delete_option = $("#delete_option");
$msg = $("#msg");
$msg_text = $("#msg_text");
name_input = $("#name_input");
save_name = $("#save");
file_input = $("#file");
form = $("#form1");


$(document).ready(function (e) {
    // //Set default cookie
    //Check already upload
    if (getCookie("cname") != ""){
        $msg_text.html("<div id='p1'>Hello, " + getCookie("cname") + ". </div>")         
        $msg.show()
        if($has_image.val() == "True"){
            $delete_option.show()    
        }

    } else {
        setCookie("cname","")
        setCookie("img_id","")
    }


    save_name.click(function(e){
        e.preventDefault()
        setCookie("cname",name_input.val())
        setCookie("img_id","")
        $msg_text.html("Name saved!")
        $msg_text.addClass("success")
        $msg.show()
        })

    file_input.click(function(e){
        //Check saved name
        if (getCookie("cname") == ""){
            $msg.show()
            $msg_text.html("Please save your name.")
            $msg_text.addClass("error")
            e.preventDefault()
        } 
        else {
            $msg.hide()
        }
    })

    form.on('submit',(function(e) {
        

        e.preventDefault();
        var formData = new FormData(this);

        $.ajax({
            type:'POST',
            url: $(this).attr('action'),
            data:formData,
            cache:false,
            contentType: false,
            processData: false,
            success:function(id){
                console.log("success");
                $("#success").fadeIn()
                $("#image").attr("src","/image_raw/" + getCookie("img_id"))
                $("#image").attr("style","max-height:200px")
                setCookie("img_id",id)
            },
            error: function(data){
                console.log("error");
                
            }
        });
    }));

    file_input.on("change", function() {
        form.submit();
    });
});

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i].trim();
        if (c.indexOf(name) == 0)
            return c.substring(name.length, c.length);
    }
    return "";
}

function setCookie(cname,cval){
    document.cookie = cname + "=" + cval
}

function deleteMyImage(img_id){
    $.post("/delete",{"img_id" : img_id}, function(){
        $msg_text.html("Delete Succes!")
        $msg_text.addClass("success")
        $msg.show()
        $delete_option.hide()

    })
}