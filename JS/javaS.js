//Carrito de compras

document.addEventListener('DOMContentLoaded', () => {
    const botonesAgregar = document.querySelectorAll('.boton-agregar-carrito');
    const contadorCarrito = document.getElementById('contador-carrito');
    const carritoContenedor = document.querySelector('.carrito-contenedor');
    const modalCarrito = document.getElementById('modal-carrito');
    const cerrarModal = document.querySelector('.cerrar-modal');
    const listaCarrito = document.getElementById('lista-carrito');
    const totalCarrito = document.getElementById('total-carrito');
    const botonComprar = document.getElementById('boton-comprar');
  
    let carrito = [];
  
    // Función para actualizar la visualización del carrito (contador y modal)
    function actualizarCarritoUI() {
      contadorCarrito.textContent = carrito.length;
      listaCarrito.innerHTML = '';
      let total = 0;
  
      carrito.forEach(item => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `
          ${item.nombre} - $${item.precio.toLocaleString('es-AR')}
          <button class="eliminar-item" data-id="${item.id}">Eliminar</button>
        `;
        listaCarrito.appendChild(listItem);
        total += item.precio;
      });
  
      totalCarrito.textContent = `Total: $${total.toLocaleString('es-AR')}`;
  
      if (carrito.length > 0) {
        botonComprar.disabled = false;
      } else {
        botonComprar.disabled = true;
      }
    }
  
    // Función para agregar un producto al carrito
    function agregarAlCarrito(event) {
      const boton = event.target;
      const tarjetaProducto = boton.closest('.tarjeta-producto');
      const id = parseInt(tarjetaProducto.dataset.id);
      const nombre = tarjetaProducto.dataset.nombre;
      const precio = parseInt(tarjetaProducto.dataset.precio);
  
      const productoExistente = carrito.find(item => item.id === id);
  
      if (productoExistente) {
        // Aquí podrías aumentar la cantidad si quisieras permitir múltiples unidades
        alert('Este producto ya está en el carrito.');
      } else {
        carrito.push({ id, nombre, precio });
        actualizarCarritoUI();
      }
    }
  
    // Event listeners
    botonesAgregar.forEach(boton => {
      boton.addEventListener('click', agregarAlCarrito);
    });
  
    carritoContenedor.addEventListener('click', () => {
      modalCarrito.style.display = 'block';
    });
  
    cerrarModal.addEventListener('click', () => {
      modalCarrito.style.display = 'none';
    });
  
    window.addEventListener('click', (event) => {
      if (event.target === modalCarrito) {
        modalCarrito.style.display = 'none';
      }
    });
  
    listaCarrito.addEventListener('click', (event) => {
      if (event.target.classList.contains('eliminar-item')) {
        const idAEliminar = parseInt(event.target.dataset.id);
        carrito = carrito.filter(item => item.id !== idAEliminar);
        actualizarCarritoUI();
      }
    });
  
    botonComprar.addEventListener('click', () => {
      if (carrito.length > 0) {
        alert('¡Gracias por tu compra!');
        carrito = []; // Vaciar el carrito después de la compra (simulada)
        actualizarCarritoUI();
      }
    });
  
    // Cargar el carrito desde localStorage si existe (opcional)
    const carritoGuardado = localStorage.getItem('carrito');
    if (carritoGuardado) {
      carrito = JSON.parse(carritoGuardado);
      actualizarCarritoUI();
    }
  
    // Guardar el carrito en localStorage antes de que la página se cierre (opcional)
    window.addEventListener('beforeunload', () => {
      localStorage.setItem('carrito', JSON.stringify(carrito));
    });
  });