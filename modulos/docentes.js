async function guardarDocentes() {
    const datos = {
        codigo: document.getElementById("txtCodigoDocente").value,
        nombre: document.getElementById("txtNombreDocente").value,
        direccion: document.getElementById("txtDireccionDocente").value,
        telefono: document.getElementById("txtTelefonoDocente").value,
        email: document.getElementById("txtEmailDocente").value,
        dui: document.getElementById("txtDuiDocente").value,
        escalafon: document.getElementById("txtEscalafonDocente").value
    };
    const respuesta = await fetch("/guardar_docente", {
        method: "POST",
        body: JSON.stringify(datos)
    });
    const resultado = await respuesta.json();
    alert(resultado.msg === "ok" ? "Docente guardado" : "Error al guardar");
}

async function obtenerDocentes() {
    const respuesta = await fetch("/docentes");
    const docentes = await respuesta.json();
    const tbody = document.querySelector("#tablaDocentes tbody");
    tbody.innerHTML = "";
    docentes.forEach(docente => {
        const fila = `<tr>
            <td>${docente.codigo}</td>
            <td>${docente.nombre}</td>
            <td>${docente.direccion}</td>
            <td>${docente.telefono}</td>
            <td>${docente.email}</td>
            <td>${docente.dui}</td>
            <td>${docente.escalafon}</td>
        </tr>`;
        tbody.innerHTML += fila;
    });
}

document.getElementById("frmDocentes").addEventListener("submit", async function(e) {
    e.preventDefault();
    await guardarDocentes();
    await obtenerDocentes();
});

document.addEventListener("DOMContentLoaded", obtenerDocentes);

frmDocentes.addEventListener("submit", async function(e) {
    e.preventDefault();
    await guardarDocentes();
});

btnNuevoDocente.addEventListener("click", function() {
    limpiarFormularioDocente();
});

btnBuscarDocente.addEventListener("click", function() {
    abrirVentanaBusquedaDocentes();
});

function abrirVentanaBusquedaDocentes() {
    // Si usas el mismo sistema que alumnos, deberías tener una función para mostrar la búsqueda
    // Por ejemplo, si tienes un div con id="busqueda_docentes":
    fetch("/vistas?form=busqueda_docentes")
        .then(response => response.text())
        .then(html => {
            document.getElementById("busqueda_docentes").innerHTML = html;
        });
}      