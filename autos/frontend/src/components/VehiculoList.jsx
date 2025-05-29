import React from 'react';
import './VehiculoStyle.css';

const VehiculoList = ({ vehiculos, onDelete, onEdit }) => {
    const formatFecha = (fecha) => {
        return new Date(fecha).toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        });
    };

    return (
        <div className="p-4 overflow-x-auto">
        <table className="vehiculo-table w-full border-collapse border border-gray-300">
            <thead className="bg-gray-100 text-gray-800 text-sm">
            <tr>
                <th className="px-4 py-2 border">Modelo</th>
                <th className="px-4 py-2 border">Año</th>
                <th className="px-4 py-2 border">Marca</th>
                <th className="px-4 py-2 border">Tipo</th>
                <th className="px-4 py-2 border">Categoría</th>
                <th className="px-4 py-2 border">Descripción</th>
                <th className="px-4 py-2 border">Precio</th>
                <th className="px-4 py-2 border">Vendedor</th>
                <th className="px-4 py-2 border">Disponible</th>
                <th className="px-4 py-2 border">Publicado</th>
                <th className="px-4 py-2 border">Acciones</th>
            </tr>
            </thead>
            <tbody className="text-sm text-gray-700">
            {vehiculos.map((v) => (
                <tr key={v.id} className="hover:bg-gray-50">
                <td className="px-4 py-2 border">{v.modelo}</td>
                <td className="px-4 py-2 border">{v.anio}</td>
                <td className="px-4 py-2 border">{v.marca}</td>
                <td className="px-4 py-2 border">{v.tipo}</td>
                <td className="px-4 py-2 border">{v.categorias}</td>
                <td className="px-4 py-2 border">{v.descripcion}</td>
                <td className="px-4 py-2 border">${parseFloat(v.precio).toLocaleString()}</td>
                <td className="px-4 py-2 border">{v.vendedor}</td>
                <td className={`px-4 py-2 border ${v.disponible ? 'text-green-600' : 'text-red-600'}`}>
                    {v.disponible ? 'Sí' : 'No'}
                </td>
                <td className="px-4 py-2 border">{formatFecha(v.fecha_publicacion)}</td>
                <td className="px-4 py-2 border">
                    <div className="flex gap-2">
                    <button onClick={() => onEdit(v)} className="btn-editar text-blue-600 hover:underline">
                        Editar
                    </button>
                    <button onClick={() => onDelete(v.id)} className="btn-eliminar text-red-600 hover:underline">
                        Eliminar
                    </button>
                    </div>
                </td>
                </tr>
            ))}
            </tbody>
        </table>
    </div>
    );
};

export default VehiculoList;
