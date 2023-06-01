var reservas = document.querySelectorAll(".solicitar");

var dia_seleccionado = ""

for (let i of reservas) {
  if (i.textContent != "") {
    i.addEventListener('click', () => {
      dia_seleccionado = i.querySelector('div').textContent;
    });
  }
}


document.addEventListener('DOMContentLoaded', function () {
  var solicitar_open = document.querySelectorAll('.solicitar');
  var menu_solicitud = document.getElementById('menu_solicitud');
  var closeBtn = document.getElementById('close-btn');
  var overlay = document.querySelector('.overlay');

  // ...

  // Función para abrir la ventana emergente
  function openPopup() {
    menu_solicitud.classList.add('open');
    overlay.style.display = 'block';
    var miDiv = document.getElementById('diajsjs');
    miDiv.textContent = "Has seleccionado el día: " + dia_seleccionado.toString();

    // Hacer la solicitud AJAX para obtener las opciones del select
    $.post("/horarios/mostrar", { fecha: dia_seleccionado }, function (data) {
      var select = $('#menu_solicitud select'); // Obtén el elemento select dentro del modal
      select.empty(); // Limpia las opciones existentes

      // Agrega las nuevas opciones obtenidas desde el servidor
      $.each(data, function (index, opcion) {
        select.append($('<option>', {
          value: opcion.valor,
          text: opcion.texto
        }));
      });
    });


  // Agregar evento de escucha al botón de enviar del formulario
  $('#menu_solicitud form').submit(function (event) {
    event.preventDefault(); // Evitar que se envíe el formulario de forma convencional

    // Obtener los valores ingresados por el usuario
    var responsable = $('#responsablejsjs').text();
    var tipoReserva = $('input[name=tipo_reserva]:checked').val();
    var horaReserva = $('#menu_solicitud select').val();

    // Realizar la solicitud AJAX para enviar los datos al servidor
    $.post("/reservas/crear", {
      responsable: responsable,
      fecha: dia_seleccionado,
      hora: horaReserva,
      tipo: tipoReserva
    }, function (response) {
      // Realizar cualquier acción adicional después de enviar los datos
      console.log('Respuesta del servidor:', response);
    });

    // Cerrar la ventana emergente
    closePopup();
  });


  }

  // ...



  //selecccion de modo
  var opciones = document.getElementsByName('tipo_reserva');

  // Agregar un controlador de eventos para cada opción
  opciones.forEach(function (opcion) {
    opcion.addEventListener('change', function () {
      // Verificar cuál opción ha sido seleccionada
      if (opcion.checked) {
        console.log('Opción seleccionada:', opcion.value);
      }
    });
  });

  // Función para cerrar la ventana emergente
  function closePopup() {
    menu_solicitud.classList.remove('open');
    overlay.style.display = 'none';
  }

  // Agregar eventos de clic a todas las casillas popup-trigger
  solicitar_open.forEach(function (trigger) {
    trigger.addEventListener('click', openPopup);
  });

  // Cerrar la ventana emergente al hacer clic en el botón de cerrar
  closeBtn.addEventListener('click', closePopup);

  // Cerrar la ventana emergente al hacer clic fuera de ella
  overlay.addEventListener('click', closePopup);
});



/////


