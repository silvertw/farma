// EVENTOS DEL BOTON (TOCAR)
$("#menu-toggle").click(function(e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
  });

// EVENTOS DE EL MENU
$( "#sidebar-wrapper" )
  .on( "mouseleave", function(){
   $("#wrapper").toggleClass("toggled");
});

//EVENTO POR DEFECTO
