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
      var opciones_radio_lab = document.querySelector("#lab_opciones_radio")
      opciones_radio_lab.setAttribute("style", "display:none;");
      var modo_reserva_unico_grupal = document.querySelector("#modo_unico_grupal");
      modo_reserva_unico_grupal.style.display = "flex";
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

  var formReserva = document.getElementById('form_reserva'); // Obtener el formulario por su ID

  function eliminarBotones() {
    var computadoraButtons = formReserva.getElementsByClassName('computadora-button');
    while (computadoraButtons.length > 0) {
      computadoraButtons[0].remove();
    }
  }

  if (botonesPC) {
    eliminarBotones();
  }

  if (modo_selecionado == "grupal") {
    var selectedPC = null;
    var pcButton = document.createElement('button'); // Crear un elemento de botón
    pcButton.textContent = "Reservar"; // Establecer el texto del botón
    pcButton.value = 1; // Asignar el valor del ID de la computadora al botón

    pcButton.addEventListener('click', function () {
      selectedPC = this.value; // Almacenar el valor del botón en la variable selectedPC
      console.log('Computadora seleccionada:', selectedPC);

      // Realizar la reserva con la computadora seleccionada

      var xhr = new XMLHttpRequest();
      xhr.open("POST", "/reservas/crear", true);
      xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

      xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
          if (xhr.status === 200) {
            var response = xhr.responseText;
            console.log('Reserva realizada:', response);
          } else {
            console.error("Error en la solicitud: " + xhr.status);
          }
        }
      };

      var data = "responsable=" + encodeURIComponent(document.getElementById('responsablejsjs').textContent) +
        "&fecha=" + encodeURIComponent(dia_seleccionado) +
        "&hora=" + encodeURIComponent(horaReserva1) +
        "&tipo=" + encodeURIComponent(document.querySelector('input[name=tipo_reserva]:checked').value) +
        "&laboratorio=" + encodeURIComponent(lab_seleccionado) +
        "&computadora=" + encodeURIComponent(selectedPC);

      xhr.send(data);
    });

    pcButton.classList.add('computadora-button');
    formReserva.appendChild(pcButton); // Agregar el botón al formulario
    botonesPC = true;
  } else {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/horarios/PC_disponible", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          var response = JSON.parse(xhr.responseText);
          console.log('Respuesta de la base de datos:', response);
          var formReserva = document.getElementById('form_reserva'); // Obtener el formulario por su ID
          var selectedPC = null; // Variable para almacenar la computadora seleccionada

          response.forEach(function (pc) {
            var pcButton = document.createElement('button'); // Crear un elemento de botón
            pcButton.textContent = 'Computadora ' + pc.computadora; // Establecer el texto del botón
            pcButton.value = pc.computadora; // Asignar el valor del ID de la computadora al botón

            if (pc.disponible === 'Disponible') {
              pcButton.disabled = false; // Habilitar el botón si está disponible
            } else {
              pcButton.disabled = true; // Deshabilitar el botón si no está disponible
            }

            pcButton.addEventListener('click', function () {
              selectedPC = this.value; // Almacenar el valor del botón en la variable selectedPC
              console.log('Computadora seleccionada:', selectedPC);

              // Realizar la reserva con la computadora seleccionada
              var xhr = new XMLHttpRequest();
              xhr.open("POST", "/reservas/crear", true);
              xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

              xhr.onreadystatechange = function () {
                if (xhr.readyState === XMLHttpRequest.DONE) {
                  if (xhr.status === 200) {
                    var response = xhr.responseText;
                    console.log('Reserva realizada:', response);
                  } else {
                    console.error("Error en la solicitud: " + xhr.status);
                  }
                }
              };

              var data = "responsable=" + encodeURIComponent(document.getElementById('responsablejsjs').textContent) +
                "&fecha=" + encodeURIComponent(dia_seleccionado) +
                "&hora=" + encodeURIComponent(horaReserva1) +
                "&tipo=" + encodeURIComponent(document.querySelector('input[name=tipo_reserva]:checked').value) +
                "&laboratorio=" + encodeURIComponent(lab_seleccionado) +
                "&computadora=" + encodeURIComponent(selectedPC);

              xhr.send(data);
            });

            pcButton.classList.add('computadora-button');
            formReserva.appendChild(pcButton); // Agregar el botón al formulario
          });
          botonesPC = true;
        } else {
          console.error("Error en la solicitud: " + xhr.status);
        }
      }
    };

    var data = "fecha=" + encodeURIComponent(dia_seleccionado) +
      "&hora=" + encodeURIComponent(horaReserva1) +
      "&laboratorio=" + encodeURIComponent(lab_seleccionado);

    xhr.send(data);
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

        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/horarios/mostrar", true);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        xhr.onreadystatechange = function () {
          if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
              var data = JSON.parse(xhr.responseText);
              var select = document.querySelector('#menu_solicitud select');
              select.innerHTML = '';

              var defaultOption = document.createElement('option');
              defaultOption.disabled = true;
              defaultOption.selected = true;
              defaultOption.value = '';
              defaultOption.text = 'Selecciona una opción';
              select.appendChild(defaultOption);

              data.forEach(function (opcion) {
                var option = document.createElement('option');
                option.value = opcion.valor;
                option.text = opcion.texto;
                select.appendChild(option);
              });
            } else {
              console.error("Error en la solicitud: " + xhr.status);
            }
          }
        };

        var data = "fecha=" + encodeURIComponent(dia_seleccionado) +
          "&modo=" + encodeURIComponent(opcion.value) +
          "&laboratorio=" + encodeURIComponent(lab_seleccionado);

        xhr.send(data);
      }
    });
  });

  //////
  var formReserva = document.querySelector('#form_reserva'); // Obtener el formulario por su ID

  function eliminarBotones() {
    var computadoraButtons = formReserva.querySelectorAll('.computadora-button');
    computadoraButtons.forEach(function (button) {
      button.remove();
    });
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

