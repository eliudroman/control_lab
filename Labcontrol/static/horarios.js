var reservas = document.querySelectorAll(".solicitar");

var dia_seleccionado = ""

for (let i of reservas) {
  if (i.textContent != "") {
    i.addEventListener('click', () => {
      dia_seleccionado = i.querySelector('div').textContent;
    });
  }
}

//////////

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


/////////



var horaReserva1 = "";
var botonesPC = false
var modo_selecionado;

function guardarHoraSeleccionada() {
  var select = document.getElementById("hora_reserva");
  horaReserva1 = select.value;
  console.log(horaReserva1);

  var formReserva = $('#form_reserva'); // Obtener el formulario por su ID

  function eliminarBotones() {
    formReserva.find('.computadora-button').remove(); // Eliminar los botones de las computadoras del formulario
  }

  if (botonesPC) {
    eliminarBotones();
  }

  if(modo_selecionado == "grupal") {
    var selectedPC = null;
    var formReserva = $('#form_reserva');
    var pcButton = $('<button></button>'); // Crear un elemento de botón
    pcButton.text("Reservar"); // Establecer el texto del botón
    pcButton.val(1); // Asignar el valor del ID de la computadora al botón

    pcButton.on('click', function () {
      selectedPC = $(this).val(); // Almacenar el valor del botón en la variable selectedPC
      console.log('Computadora seleccionada:', selectedPC);

      // Realizar la reserva con la computadora seleccionada
      

      
      $.post("/reservas/crear", {
        responsable: $('#responsablejsjs').text(),
        fecha: dia_seleccionado,
        hora: horaReserva1,
        tipo: $('input[name=tipo_reserva]:checked').val(),
        laboratorio: lab_seleccionado,
        computadora: selectedPC // Añadir la computadora seleccionada a los datos de reserva
      }, function (response) {
        console.log('Reserva realizada:', response);
      });
      

    });

    pcButton.addClass('computadora-button');
    pcButton.appendTo(formReserva); // Agregar el botón al formulario
    botonesPC = true;


  }

  else {
    $.post("/horarios/PC_disponible", { fecha: dia_seleccionado, hora: horaReserva1, laboratorio: lab_seleccionado }, function (response) {
      console.log('Respuesta de la base de datos:', response);
      var formReserva = $('#form_reserva'); // Obtener el formulario por su ID
      var selectedPC = null; // Variable para almacenar la computadora seleccionada
  
      $.each(response, function (index, pc) {
        var pcButton = $('<button></button>'); // Crear un elemento de botón
        pcButton.text('Computadora ' + pc.computadora); // Establecer el texto del botón
        pcButton.val(pc.computadora); // Asignar el valor del ID de la computadora al botón
  
        if (pc.disponible === 'Disponible') {
          pcButton.prop('disabled', false); // Habilitar el botón si está disponible
        } else {
          pcButton.prop('disabled', true); // Deshabilitar el botón si no está disponible
        }
  
        pcButton.on('click', function () {
          selectedPC = $(this).val(); // Almacenar el valor del botón en la variable selectedPC
          console.log('Computadora seleccionada:', selectedPC);
  
          // Realizar la reserva con la computadora seleccionada
          $.post("/reservas/crear", {
            responsable: $('#responsablejsjs').text(),
            fecha: dia_seleccionado,
            hora: horaReserva1,
            tipo: $('input[name=tipo_reserva]:checked').val(),
            laboratorio: lab_seleccionado,
            computadora: selectedPC // Añadir la computadora seleccionada a los datos de reserva
          }, function (response) {
            console.log('Reserva realizada:', response);
          });
        });
  
        pcButton.addClass('computadora-button');
        pcButton.appendTo(formReserva); // Agregar el botón al formulario
      });
      botonesPC = true;
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
    var form = document.getElementById("form_reserva");
    form.reset();
  }

  
  //selecccion de modo
  var opciones = document.getElementsByName('tipo_reserva');


  opciones.forEach(function (opcion) {
    opcion.addEventListener('click', function () {
      
      if (opcion.checked) {
        console.log('Opción seleccionada:', opcion.value);
        modo_selecionado = opcion.value;
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
var formReserva = $('#form_reserva'); // Obtener el formulario por su ID

  function eliminarBotones() {
    formReserva.find('.computadora-button').remove(); // Eliminar los botones de las computadoras del formulario
  }

  // Función para cerrar la ventana emergente
  function closePopup() {
    menu_solicitud.classList.remove('open');
    overlay.style.display = 'none';
    eliminarBotones();
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

