var reservas = document.querySelectorAll(".solicitar");

var dia_seleccionado = ""

for (let i of reservas) {
  if (i.textContent != "") {
    i.addEventListener('click', () => {
      dia_seleccionado = i.querySelector('div').textContent;
    });
  }
}

var horaReserva1 = "";


function guardarHoraSeleccionada() {
  var select = document.getElementById("hora_reserva");
  horaReserva1 = select.value;
  console.log(horaReserva1)


  $.post("/horarios/PC_disponible", { fecha: dia_seleccionado, hora: horaReserva1 }, function (response) {

    console.log($('#menu_solicitud select').val())
    console.log('Respuesta de la base de datos:', response);
  });
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
    var form = document.getElementById("form_reserva");
    form.reset();
  }

  // ...

  $('#menu_solicitud form').submit(function (event) {
    event.preventDefault();

    var responsable = $('#responsablejsjs').text();
    var tipoReserva = $('input[name=tipo_reserva]:checked').val();
    var horaReserva = $('#menu_solicitud select').val();

    

    $.post("/reservas/crear", {
      responsable: responsable,
      fecha: dia_seleccionado,
      hora: horaReserva,
      tipo: tipoReserva,
      laboratorio: lab_seleccionado
    }, function (response) {
 

    });

    // Cerrar la ventana emergente
    closePopup();

    var selectHoraReserva = document.getElementById("hora_reserva");
    selectHoraReserva.addEventListener("change", guardarHoraSeleccionada);
  });


  //selecccion de modo
  var opciones = document.getElementsByName('tipo_reserva');


  opciones.forEach(function (opcion) {
    opcion.addEventListener('click', function () {
      
      if (opcion.checked) {
        console.log('Opción seleccionada:', opcion.value);

        if (opcion.value == "grupal") {
          $.post("/horarios/mostrar", { fecha: dia_seleccionado, modo: opcion.value, laboratorio: lab_seleccionado}, function (data) {
            var select = $('#menu_solicitud select');
            select.empty();
            select.append($('<option>', {
              disabled: true,
              selected: true,
              value: '',
              text: 'Selecciona una opción'
            }));

            $.each(data, function (index, opcion) {
              select.append($('<option>', {
                value: opcion.valor,
                text: opcion.texto
              }));
            });
          });
        }
        if (opcion.value == "unico") {
          $.post("/horarios/mostrar", { fecha: dia_seleccionado, modo : opcion.value, laboratorio: lab_seleccionado}, function (data) {
            var select = $('#menu_solicitud select');
            select.empty();
            select.append($('<option>', {
              disabled: true,
              selected: true,
              value: '',
              text: 'Selecciona una opción'
            }));

            $.each(data, function (index, opcion) {
              select.append($('<option>', {
                value: opcion.valor,
                text: opcion.texto
              }));
            });
          });
        }
      }
    });
  });

//////


  //selecccion de modo
  var opciones_lab = document.getElementsByName('tipo_laboratorio');
  var lab_seleccionado = "";

  opciones_lab.forEach(function (opcion) {
    opcion.addEventListener('click', function () {
      
      if (opcion.checked) {
        console.log('Opción seleccionada:', opcion.value);
        lab_seleccionado = opcion.value[opcion.value.length - 1];
        console.log(lab_seleccionado)
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

  var selectHoraReserva = document.getElementById("hora_reserva");
  selectHoraReserva.addEventListener("change", guardarHoraSeleccionada);

});

