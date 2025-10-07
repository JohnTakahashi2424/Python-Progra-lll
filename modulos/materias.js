async function guardarMaterias() {
    const datos = {
        codigo: document.getElementById("txtCodigoMateria").value,
        nombre: document.getElementById("txtNombreMateria").value,
        descripcion: document.getElementById("txtDescripcionMateria").value
    };
    const respuesta = await fetch("/guardar_materia", {
        method: "POST",
        body: JSON.stringify(datos)
    });
    const resultado = await respuesta.json();
    alert(resultado.msg === "ok" ? "Materia guardada" : "Error al guardar");
    limpiarFormularioMateria();
    obtenerMaterias();
}

function limpiarFormularioMateria(){
    document.getElementById("txtCodigoMateria").value = "";
    document.getElementById("txtNombreMateria").value = "";
    document.getElementById("txtDescripcionMateria").value = "";
}

async function obtenerMaterias() {
    const respuesta = await fetch("/materias");
    const materias = await respuesta.json();
    const tbody = document.querySelector("#tablaMaterias tbody");
    tbody.innerHTML = "";
    materias.forEach(materia => {
        const fila = `<tr>
            <td>${materia.codigo}</td>
            <td>${materia.nombre}</td>
            <td>${materia.descripcion}</td>
            <td><button onclick='eliminarMateria(${materia.idMateria})' class='btn btn-danger btn-sm'>Eliminar</button></td>
        </tr>`;
        tbody.innerHTML += fila;
    });
}

document.getElementById("frmMaterias").addEventListener("submit", async function(e) {
    e.preventDefault();
    await guardarMaterias();
});

document.addEventListener("DOMContentLoaded", obtenerMaterias);

async function eliminarMateria(idMateria) {
    if(confirm("¿Seguro que deseas eliminar esta materia?")){
        const respuesta = await fetch(`/eliminar_materia?id=${idMateria}`, { method: "DELETE" });
        const resultado = await respuesta.json();
        alert(resultado.msg === "ok" ? "Materia eliminada" : "Error al eliminar");
        obtenerMaterias();
    }
}
