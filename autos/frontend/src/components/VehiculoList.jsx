import React from 'react';

const VehiculoList = ({ vehiculos, onDelete, onEdit }) => {
    const formatFecha = (fecha) => {
        return new Date(fecha).toLocaleDateString('es-ES', {
        year: 'numeric', month: 'long', day: 'numeric'
        });
    };

    return (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 p-4">
        {vehiculos.map((v) => (
            <div
            key={v.id}
            className="bg-white text-gray-900 rounded-xl shadow-lg p-5 border border-gray-200 hover:shadow-xl transition-shadow"
            >
            <h2 className="text-2xl font-semibold mb-1">{v.modelo} ({v.anio})</h2>
            <p className="text-sm text-gray-600 mb-2">{v.descripcion}</p>

            <ul className="text-sm space-y-1">
                <li><strong>Placa:</strong> {v.placa}</li>
                <li><strong>Marca:</strong> {v.marca}</li>
                <li><strong>Tipo:</strong> {v.tipo}</li>
                <li><strong>Categoría:</strong> {v.categorias}</li>
                <li><strong>Precio:</strong> ${parseFloat(v.precio).toLocaleString()}</li>
                <li><strong>Vendedor:</strong> {v.vendedor}</li>
                <li>
                <strong>Disponible:</strong>{' '}
                <span className={v.disponible ? 'text-green-600' : 'text-red-600'}>
                    {v.disponible ? 'Sí' : 'No'}
                </span>
                </li>
                <li><strong>Publicado:</strong> {formatFecha(v.fecha_publicacion)}</li>
            </ul>

            <div className="mt-4 flex gap-3">
                <button
                onClick={() => onEdit(v)}
                className="bg-blue-600 hover:bg-blue-700 text-white py-1 px-4 rounded-md"
                >
                Editar
                </button>
                <button
                onClick={() => onDelete(v.id)}
                className="bg-red-600 hover:bg-red-700 text-white py-1 px-4 rounded-md"
                >
                Eliminar
                </button>
            </div>
            </div>
        ))}
        </div>
    );
};

export default VehiculoList;
