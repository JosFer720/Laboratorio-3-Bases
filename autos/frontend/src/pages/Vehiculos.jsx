import React, { useEffect, useState } from 'react'
import VehiculoForm from '../components/VehiculoForm'
import VehiculoList from '../components/VehiculoList'

const API = 'http://localhost:8000/api/vehiculos'

const VehiculosPage = () => {
  const [vehiculos, setVehiculos] = useState([])
  const [vehiculoEdit, setVehiculoEdit] = useState(null)

  const cargarVehiculos = async () => {
    const res = await fetch(API)
    const data = await res.json()
    setVehiculos(data)
  }

  const crearVehiculo = async (data) => {
    await fetch(API + '/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    cargarVehiculos()
  }

  const actualizarVehiculo = async (id, data) => {
    await fetch(`${API}/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    cargarVehiculos()
  }

  const eliminarVehiculo = async (id) => {
    await fetch(`${API}/${id}`, {
      method: 'DELETE'
    })
    cargarVehiculos()
  }

  useEffect(() => {
    cargarVehiculos()
  }, [])

  return (
    <div>
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
  )
}

export default VehiculosPage
