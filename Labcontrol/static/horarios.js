var reservas = document.querySelectorAll(".reserva");
console.log(reservas)

for (let i of reservas) {
    if (i.textContent != "") {
        i.addEventListener('click', () => {
            console.log("Dia")
            console.log(i.textContent)
        })

    }
}
document.addEventListener('DOMContentLoaded', function () {
    var solicitar_open = document.querySelectorAll('.solicitar');
    var menu_solicitud = document.getElementById('menu_solicitud');
    var closeBtn = document.getElementById('close-btn');
    var overlay = document.querySelector('.overlay');

    // Función para abrir la ventana emergente
    function openPopup() {
        menu_solicitud.classList.add('open');
        overlay.style.display = 'block';
    }

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
