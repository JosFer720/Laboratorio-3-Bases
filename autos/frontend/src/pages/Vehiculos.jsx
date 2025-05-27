import { useEffect, useState } from 'react'

function Vehiculos() {
  const [vehiculos, setVehiculos] = useState([])

  useEffect(() => {
    fetch('http://localhost:8000/api/vehiculos')
      .then(res => res.json())
      .then(data => setVehiculos(data))
      .catch(err => console.error('Error:', err))
  }, [])

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Vehículos disponibles</h1>
      <table className="w-full border">
        <thead>
          <tr className="bg-gray-200">
            <th>ID</th>
            <th>Modelo</th>
            <th>Año</th>
            <th>Precio</th>
            <th>Disponible</th>
          </tr>
        </thead>
        <tbody>
          {vehiculos.map(v => (
            <tr key={v.id} className="border-t">
              <td>{v.id}</td>
              <td>{v.modelo}</td>
              <td>{v.anio}</td>
              <td>${v.precio}</td>
              <td>{v.disponible ? 'Sí' : 'No'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default Vehiculos
