import React from 'react'

const VehiculoList = ({ vehiculos, onDelete, onEdit }) => {
    return (
        <ul>
        {vehiculos.map(v => (
            <li key={v.id}>
            {v.placa} - {v.modelo} - Marca: {v.marca_nombre}
            <button onClick={() => onEdit(v)}>Editar</button>
            <button onClick={() => onDelete(v.id)}>Eliminar</button>
            </li>
        ))}
        </ul>
    )
}

export default VehiculoList
