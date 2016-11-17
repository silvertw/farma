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

//EVENTO POR DEFECTO PARA QUE EL MENU APAREZCA Y SE VALLA
$("#sidebar-wrapper").trigger("mouseleave", function(){
   e.preventDefault();
   $("#wrapper").toggleClass("toggled");
});