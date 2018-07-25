$( document ).ready(function() {
    change_tab_to_current_user_stats()
});

function change_tab_to_new_friends() {
        $.ajax({
            url: suggestFriends ,
            dataType : 'html',
            timeout : 30000,
            success: function(data){
                $('#statistics').html(data);
            }
        });
    }

function change_tab_to_find_owner() {
        $.ajax({
            url: findOwner,
            dataType : 'html',
            timeout : 30000,
            success: function(data){
                $('#statistics').html(data);
            }
        });
    }

function change_tab_to_current_user_stats() {
        $.ajax({
            url: currentUser ,
            dataType : 'html',
            timeout : 30000,
            success: function(data){
                $('#statistics').html(data);
            }
        });
    }

function w3_open() {
    document.getElementById("mySidebar").style.display = "block";
}
function w3_close() {
    document.getElementById("mySidebar").style.display = "none";
}
