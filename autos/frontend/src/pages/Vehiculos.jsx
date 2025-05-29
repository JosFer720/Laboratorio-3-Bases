import React, { useEffect, useState } from 'react';
import VehiculoForm from '../components/VehiculoForm';
import VehiculoList from '../components/VehiculoList';

const API = 'http://localhost:8000/api/vehiculos';

const VehiculosPage = () => {
  const [vehiculos, setVehiculos] = useState([]);
  const [vehiculoEdit, setVehiculoEdit] = useState(null);

  const cargarVehiculos = async () => {
    try {
      const res = await fetch(API);
      const data = await res.json();
      setVehiculos(data);
    } catch (error) {
      alert('Error al cargar vehículos');
    }
  };

  const crearVehiculo = async (data) => {
    try {
      await fetch(API + '/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      alert('Vehículo creado');
      cargarVehiculos();
    } catch (error) {
      alert('Error al crear vehículo');
    }
  };

  const actualizarVehiculo = async (id, data) => {
    try {
      await fetch(`${API}/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      alert('Vehículo actualizado');
      cargarVehiculos();
    } catch (error) {
      alert('Error al actualizar vehículo');
    }
  };

  const eliminarVehiculo = async (id) => {
    const confirm = window.confirm('¿Estás seguro de eliminar este vehículo?');
    if (!confirm) return;

    try {
      await fetch(`${API}/${id}`, {
        method: 'DELETE'
      });
      alert('Vehículo eliminado');
      cargarVehiculos();
    } catch (error) {
      alert('Error al eliminar vehículo');
    }
  };

  useEffect(() => {
    cargarVehiculos();
  }, []);

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <VehiculoForm
        onSubmit={vehiculoEdit ? actualizarVehiculo : crearVehiculo}
        vehiculoEdit={vehiculoEdit}
        clearEdit={() => setVehiculoEdit(null)}
      />
      <VehiculoList
        vehiculos={vehiculos}
        onDelete={eliminarVehiculo}
        onEdit={(vehiculo) => setVehiculoEdit(vehiculo)}
      />
    </div>
  );
};

export default VehiculosPage;
