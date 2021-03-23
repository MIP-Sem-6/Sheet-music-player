
function setDeleteId(id){
    document.getElementById("songid_delete").value = id;
    console.log(id);
}

  let c = 1;
  
  function sendCount(id) {
  $.ajax({
      url: "{% url 'index' %}",
      type: "POST",
      data: {
        'count': c,
        'id':id,
        csrfmiddlewaretoken: '{{ csrf_token }}'
      },
      dataType: 'json'
    });

  }

  function favButton(id,flag)
  {
    let sid = "#heart"+String(id);

    if (flag=="True")
    {
      console.log('unliked');

      $.ajax({
      url: "{% url 'index' %}",
      type: "POST",
      data: {
        'remove_fav':id,
        csrfmiddlewaretoken: '{{ csrf_token }}'
      },
      dataType: 'json'
    });
    $(sid).removeClass("fa-heart");
    $(sid).addClass("fa-heart-o");
    }
    else{
      $.ajax({
      url: "{% url 'index' %}",
      type: "POST",
      data: {
        'add_fav':id,
        csrfmiddlewaretoken: '{{ csrf_token }}'
      },
      dataType: 'json'
    });

    }
    $(sid).removeClass("fa-heart-o");
    $(sid).addClass("fa-heart");
    console.log('liked');
  
    console.log("Step 1");
 $(document).ready(function(){
              
             $('#upload-file').change(function() {
                var filename = $(this).val();
                console.log("Step 1");
                $('#file-upload-name').html(filename);
                if(filename!=""){
                    setTimeout(function(){
                        $('.upload-wrapper').addClass("uploaded");
                    }, 600);
                    setTimeout(function(){
                        $('.upload-wrapper').removeClass("uploaded");
                        $('.upload-wrapper').addClass("success");
                    }, 1600);
                }
            });
        });
  }  
