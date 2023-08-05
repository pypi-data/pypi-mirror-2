 jq(document).ready(function(){
     jq(".mouseaction").mouseenter(function () {
        jq(".mouseaction img").slideUp();
         });

     jq(".mouseaction").mouseleave(function () {
        jq(".mouseaction img").slideDown("fast");
         });
     jq(".mouseactionII").mouseenter(function () {
        jq(".mouseactionII img").fadeOut("1000");
         });

     jq(".mouseactionII").mouseleave(function () {
        jq(".mouseactionII img").fadeIn("slow");
         });

     });