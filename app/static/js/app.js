let listaCompleta = [];

async function cargarMeses() {
    const res = await fetch('/api/meses');
    const meses = await res.json();
    const select = document.getElementById('filtroMes');
    select.innerHTML = '';
    meses.forEach(m => {
        const option = document.createElement('option');
        option.value = m;
        option.textContent = m === "Todas" ? "Todos los meses" : m;
        select.appendChild(option);
    });
}

async function cargarGastos() {
    const categoria = document.getElementById('filtroCategoria').value;
    const mes = document.getElementById('filtroMes').value;

    const params = new URLSearchParams({ categoria, mes });
    const res = await fetch('/api/gastos?' + params.toString());
    const data = await res.json();
    listaCompleta = data;

    const lista = document.getElementById('listaGastos');
    lista.innerHTML = '';
    let total = 0;

    if (data.length === 0) {
        lista.innerHTML = "<em>No se encontraron gastos con los filtros seleccionados.</em>";
        return;
    }

    data.forEach((gasto, index) => {
        total += gasto.monto;
        const div = document.createElement('div');
        div.innerHTML = `
            <strong>${gasto.fecha}</strong> | <em>${gasto.categoria}</em> > ${gasto.subcategoria}: 
            <strong>$${gasto.monto.toFixed(2)}</strong>
            <button onclick="eliminarGasto(${index})" style="margin-left:10px; background:#dc3545;">❌</button>
        `;
        lista.appendChild(div);
    });

    const totalDiv = document.createElement('div');
    totalDiv.className = 'total';
    totalDiv.textContent = `🔸 Total gastado: $${total.toFixed(2)}`;
    lista.appendChild(totalDiv);
}

async function registrarGasto() {
    const categoria = document.getElementById('categoria').value;
    const subcategoria = document.getElementById('subcategoria').value.trim();
    const monto = document.getElementById('monto').value.trim();

    if (!subcategoria || !monto) {
        alert("Completa todos los campos.");
        return;
    }

    const res = await fetch('/api/gastos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ categoria, subcategoria, monto })
    });

    if (res.ok) {
        cargarMeses();
        cargarGastos();
        document.getElementById('subcategoria').value = '';
        document.getElementById('monto').value = '';
    }
}

async function eliminarGasto(index) {
    const gasto = listaCompleta[index];
    if (!gasto) return;

    const confirmacion = confirm(`¿Eliminar gasto de ${gasto.subcategoria} por $${gasto.monto.toFixed(2)}?`);
    if (!confirmacion) return;

    const resTodos = await fetch('/api/gastos');
    const listaTotal = await resTodos.json();

    const idxReal = listaTotal.findIndex(g =>
        g.categoria === gasto.categoria &&
        g.subcategoria === gasto.subcategoria &&
        g.monto === gasto.monto &&
        g.fecha === gasto.fecha
    );

    if (idxReal >= 0) {
        await fetch(`/api/gastos/${idxReal}`, { method: 'DELETE' });
        cargarMeses();
        cargarGastos();
    }
}

window.onload = async () => {
    await cargarMeses(); 
    document.getElementById('filtroCategoria').value = "Todas";
    document.getElementById('filtroMes').value = "Todas";
    cargarGastos();
};

