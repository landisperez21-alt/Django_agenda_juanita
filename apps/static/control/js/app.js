// Navegación lateral en móviles + confirmación de eliminación + avisos.
document.addEventListener("DOMContentLoaded", function () {

    // ---------------------------------------------------------
    // Navegación lateral (móvil)
    // ---------------------------------------------------------

    var body = document.body;
    var toggle = document.querySelector("[data-toggle-nav]");
    var closers = document.querySelectorAll("[data-close-nav]");

    function setNav(open) {
        body.classList.toggle("nav-open", open);
        if (toggle) {
            toggle.setAttribute("aria-expanded", open ? "true" : "false");
        }
    }

    if (toggle) {
        toggle.addEventListener("click", function () {
            setNav(!body.classList.contains("nav-open"));
        });
    }

    closers.forEach(function (el) {
        el.addEventListener("click", function () {
            setNav(false);
        });
    });

    document.querySelectorAll(".side-nav a").forEach(function (link) {
        link.addEventListener("click", function () {
            setNav(false);
        });
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            setNav(false);
        }
    });

    // ---------------------------------------------------------
    // Confirmar antes de eliminar
    // ---------------------------------------------------------

    document.querySelectorAll(".form-eliminar").forEach(function (formulario) {
        formulario.addEventListener("submit", function (evento) {
            if (!confirm("¿Seguro que deseas eliminar este registro?")) {
                evento.preventDefault();
            }
        });
    });

    // ---------------------------------------------------------
    // Mostrar campos según el tipo de reunión
    // ---------------------------------------------------------

    var tipo = document.getElementById("id_tipo_reunion");

    if (tipo) {
        var campos = document.querySelectorAll("[data-campo]");

        function mostrarCampos() {
            var virtual = tipo.value === "Virtual";
            var presencial = tipo.value === "Presencial";

            campos.forEach(function (campo) {
                var nombre = campo.getAttribute("data-campo");
                var visible = (nombre === "virtual" && virtual) ||
                              (nombre === "presencial" && presencial);
                campo.hidden = !visible;
            });
        }

        tipo.addEventListener("change", mostrarCampos);
        mostrarCampos();
    }

    // ---------------------------------------------------------
    // Los avisos desaparecen solos después de unos segundos
    // ---------------------------------------------------------

    document.querySelectorAll(".aviso").forEach(function (aviso) {
        setTimeout(function () {
            aviso.classList.add("is-hiding");
            setTimeout(function () {
                aviso.remove();
            }, 400);
        }, 5000);
    });
});
