jQuery.fn.exists = function(){return jQuery(this).length>0;}

// =============== ANFANG ================================
$(document).ready(
    function () { 
                        
        // ANFANG ------
                                
        if ( $("#edit-bar").exists() ) {        
            var bc = $("#edit-bar").html();
            if (bc != "") {
                $("#edit-bar").show()                
            } else {$("#edit-bar").hide() }
        };        

        
        // ENDE ---
    }
); 



